"""Orchestration end-to-end du pipeline de génération d'articles.

Flow:
    1. Pop un topic depuis data/topics_queue.json (ou via --keyword direct)
    2. Génère l'article via Gemini (content_writer)
    3. Lance les checks qualité (quality_check)
    4. Convertit en Markdown avec frontmatter (nuxt_publisher)
    5. Écrit le fichier dans frontend/content/articles/{slug}.md
    6. (Optionnel) git commit + push si --publish
    7. Marque le topic comme done dans la queue
    8. (Optionnel) Notification Telegram

Usage:
    python pipeline.py                          # traite 1 topic en draft
    python pipeline.py --count 3                # traite N topics
    python pipeline.py --keyword "test vanlife" # force un sujet ad-hoc
    python pipeline.py --publish                # publie (draft=false + git push)
    python pipeline.py --seed                   # pré-remplit la queue puis exit
"""

from __future__ import annotations

import argparse
import logging
import sys
import uuid
from typing import Optional

from config import settings, validate_env

# Setup logging (avant les imports modules qui logent)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("pipeline")


def run(
    count: int = 1,
    keyword: Optional[str] = None,
    publish: bool = False,
    article_type: str = "comparatif",
    category: str = "general",
) -> int:
    """Lance le pipeline pour `count` topics.

    Returns:
        Nombre d'articles générés avec succès.
    """
    from modules import content_writer, nuxt_publisher, quality_check, topics, notify, image_handler

    # Validation env (warnings seulement, mode mock OK si pas de clé)
    validate_env(strict=False)

    if not settings.gemini_api_key:
        logger.warning("⚠️  Pas de GEMINI_API_KEY → mode MOCK actif (articles placeholder)")

    success_count = 0

    for i in range(count):
        logger.info(f"\n=== Itération {i + 1}/{count} ===")

        # 1. Sélection du topic
        if keyword:
            topic = {
                "id": str(uuid.uuid4()),
                "keyword": keyword,
                "type": article_type,
                "category": category,
                "status": "queued",
            }
            logger.info(f"Topic ad-hoc: {keyword}")
        else:
            topic = topics.pop_next()
            if not topic:
                logger.warning("Aucun topic en queue. Lancer `python pipeline.py --seed` pour pré-remplir.")
                break
            logger.info(f"Topic depuis queue: {topic['keyword']} ({topic.get('type')})")
            topics.mark_status(topic["id"], "in_progress")

        # 2. Génération article
        try:
            article = content_writer.generate(
                topic=topic,
                article_type=topic.get("type", article_type),
            )
        except Exception as e:
            logger.error(f"Échec génération article: {e}")
            if not keyword:
                topics.mark_status(topic["id"], "error")
            continue

        # 3. Quality check
        check = quality_check.run_all_checks(article, article_type=topic.get("type", article_type))
        logger.info(f"Quality: passed={check.passed} | failures={len(check.failures)} | warnings={len(check.warnings)}")
        for f in check.failures:
            logger.error(f"  ❌ {f}")
        for w in check.warnings:
            logger.warning(f"  ⚠️  {w}")
        logger.info(f"  📊 Metrics: {check.metrics}")

        if not check.passed and publish:
            logger.error("Article failed quality checks → pas de publication auto. Forcé en draft.")
            publish_this = False
        else:
            publish_this = publish

        # 4. Image featured (Pexels) — fallback gracieux si pas de clé
        slug = article["slug"]
        featured_image = image_handler.fetch_for_article(
            slug=slug,
            query=article["title"],
            category=topic.get("category"),
        )
        if featured_image:
            article["featured_image"] = featured_image

        # 5. Markdown + écriture
        markdown = nuxt_publisher.article_to_markdown(
            article=article,
            topic=topic,
            article_type=topic.get("type", article_type),
            draft=not publish_this,
        )

        file_path = nuxt_publisher.write_article_file(slug=slug, markdown=markdown)
        nuxt_publisher.write_article_to_outputs(slug=slug, markdown=markdown)

        logger.info(f"✅ Article écrit: {file_path}")

        # 5. Git push si --publish
        if publish_this and settings.repo_local_path:
            commit_msg = f"add: article {topic.get('type', 'comparatif')} '{article['title']}'"
            pushed = nuxt_publisher.git_commit_and_push(commit_msg)
            if pushed:
                logger.info(f"🚀 Git push OK → Vercel rebuild auto")
            else:
                logger.warning("Git push échoué (article écrit localement quand même)")

        # 6. Marque done si depuis queue
        if not keyword:
            article_url = f"{settings.repo_local_path}/frontend/content/articles/{slug}.md"
            topics.mark_done(topic["id"], article_url=article_url)

        # 7. Notif
        try:
            site_url = f"https://vanlife-comparateur.vercel.app/articles/{slug}"
            if publish_this:
                notify.notify_article_published(article["title"], site_url)
            else:
                notify.notify_article_generated(article["title"], str(file_path))
        except Exception as e:
            logger.debug(f"Notif Telegram skip: {e}")

        success_count += 1

    logger.info(f"\n=== Pipeline terminé: {success_count}/{count} articles générés ===")
    return success_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline de génération d'articles vanlife")
    parser.add_argument("--count", type=int, default=1, help="Nombre de topics à traiter")
    parser.add_argument("--keyword", type=str, help="Force un sujet ad-hoc (skip queue)")
    parser.add_argument("--type", type=str, default="comparatif",
                        choices=["comparatif", "test_produit", "guide_achat"],
                        help="Type d'article (si --keyword)")
    parser.add_argument("--category", type=str, default="general", help="Catégorie (si --keyword)")
    parser.add_argument("--publish", action="store_true",
                        help="Publie (draft=false + git push). Sinon, draft.")
    parser.add_argument("--seed", action="store_true",
                        help="Pré-remplit la queue avec topics par défaut puis exit")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.seed:
        from modules import topics
        topics.seed_default_topics()
        sys.exit(0)

    success = run(
        count=args.count,
        keyword=args.keyword,
        publish=args.publish,
        article_type=args.type,
        category=args.category,
    )

    sys.exit(0 if success > 0 else 1)
