"""Orchestration end-to-end du pipeline de génération d'articles.

Flow:
    1. Pop un topic depuis data/topics_queue.json
    2. Recherche produits + specs (product_research)
    3. Génération article via Gemini (content_writer)
    4. Optimisation SEO (seo_optimizer)
    5. Téléchargement/génération images (image_handler)
    6. Injection liens affiliés (affiliate_linker)
    7. Quality check (quality_check)
    8. Publication : push .md vers git (nuxt_publisher)
    9. Notification Telegram (notify)

Usage:
    python pipeline.py                  # traite 1 topic
    python pipeline.py --count 3        # traite N topics
    python pipeline.py --dry-run        # génère mais ne publie pas
"""

from __future__ import annotations

import argparse
import logging
import sys

from config import settings, validate_env


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("pipeline")


def run(count: int = 1, dry_run: bool = False) -> None:
    """Lance le pipeline pour `count` topics."""
    if not validate_env(strict=False):
        logger.error("Clés .env essentielles manquantes. Stop.")
        sys.exit(1)

    logger.info(f"Pipeline démarré. count={count} dry_run={dry_run}")

    # TODO Phase 2+ : implémenter le flow complet
    # from modules import topics, product_research, content_writer, ...
    # for _ in range(count):
    #     topic = topics.pop_next()
    #     products = product_research.fetch(topic)
    #     article = content_writer.generate(topic, products)
    #     ...

    logger.warning("Pipeline en stub (Phase 0). Implémentation Phases 2-7.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pipeline de génération d'articles vanlife")
    parser.add_argument("--count", type=int, default=1, help="Nombre de topics à traiter")
    parser.add_argument("--dry-run", action="store_true", help="Génère sans publier")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(count=args.count, dry_run=args.dry_run)
