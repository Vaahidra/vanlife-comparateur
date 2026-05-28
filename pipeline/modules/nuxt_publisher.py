"""Publication d'articles vers le frontend Nuxt (écriture fichier `.md`).

Flow:
    1. Convertit l'article (dict structuré) → Markdown avec frontmatter YAML
    2. Écrit dans frontend/content/articles/{slug}.md
    3. (Optionnel) git add + commit + push → rebuild Vercel auto

Le git push n'est PAS automatique par défaut en MVP : le user relit le fichier
généré avant de commit. Activable via `auto_commit=True`.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import Literal, Optional

import yaml

from config import settings
from modules.utils import ensure_dir, now_iso, today_str

logger = logging.getLogger(__name__)

ArticleType = Literal["comparatif", "test_produit", "guide_achat"]


def article_to_markdown(
    article: dict,
    topic: dict,
    article_type: ArticleType,
    draft: bool = True,
    author: str = "Wahid",
) -> str:
    """Convertit le dict article généré + topic → fichier .md avec frontmatter YAML.

    Args:
        article: dict structuré renvoyé par content_writer.generate()
        topic: dict du topic original (pour récupérer category, keyword, products)
        article_type: comparatif | test_produit | guide_achat
        draft: True → frontmatter `draft: true` (page non publique)
        author: nom auteur

    Returns:
        Markdown complet prêt à écrire.
    """
    frontmatter = {
        "title": article["title"],
        "description": article["meta_description"],
        "slug": article["slug"],
        "type": article_type,
        "category": topic.get("category", "general"),
        "keyword_focus": topic.get("keyword", ""),
        "draft": draft,
        "author": author,
        "published_at": now_iso(),
        "updated_at": now_iso(),
        "tags": article.get("tags", []),
    }

    # Featured image (chemin web local si fetché par image_handler)
    if article.get("featured_image"):
        frontmatter["featured_image"] = article["featured_image"]

    # Add comparatif/test fields conditionally
    if article_type == "comparatif" and topic.get("products_to_compare"):
        frontmatter["products_compared"] = topic["products_to_compare"]
    if article_type == "test_produit" and topic.get("product_tested"):
        frontmatter["product_tested"] = topic["product_tested"]

    yaml_block = yaml.safe_dump(
        frontmatter,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )

    body_parts = [
        "---",
        yaml_block.strip(),
        "---",
        "",
        ":affiliate-banner",
        "",
        article["intro"],
        "",
    ]

    for section in article["sections"]:
        body_parts.append(f"## {section['h2']}")
        body_parts.append("")
        body_parts.append(section["content_markdown"])
        body_parts.append("")

    body_parts.append("## Notre verdict")
    body_parts.append("")
    body_parts.append(article["verdict"])
    body_parts.append("")

    if article.get("faq"):
        body_parts.append("## FAQ")
        body_parts.append("")
        for qa in article["faq"]:
            body_parts.append(f"### {qa['question']}")
            body_parts.append("")
            body_parts.append(qa["reponse"])
            body_parts.append("")

    if article.get("conclusion"):
        body_parts.append("## Conclusion")
        body_parts.append("")
        body_parts.append(article["conclusion"])
        body_parts.append("")

    return "\n".join(body_parts)


def write_article_file(slug: str, markdown: str, target_dir: Optional[Path] = None) -> Path:
    """Écrit le markdown dans le dossier content/articles/ du frontend.

    Returns:
        Path absolu du fichier écrit.
    """
    target_dir = target_dir or settings.frontend_content_dir
    ensure_dir(target_dir)

    file_path = target_dir / f"{slug}.md"
    file_path.write_text(markdown, encoding="utf-8")

    logger.info(f"Article écrit: {file_path} ({len(markdown)} chars)")
    return file_path


def write_article_to_outputs(slug: str, markdown: str) -> Path:
    """Écrit aussi une copie dans pipeline/outputs/ (backup + debug)."""
    outputs_dir = ensure_dir(settings.outputs_dir)
    file_path = outputs_dir / f"{today_str()}_{slug}.md"
    file_path.write_text(markdown, encoding="utf-8")
    return file_path


def git_commit_and_push(message: str, repo_path: Optional[str] = None) -> bool:
    """Commit + push les changements via subprocess (plus simple que GitPython pour ce besoin).

    Returns:
        True si succès, False sinon.
    """
    repo_path = repo_path or settings.repo_local_path
    if not repo_path:
        logger.warning("REPO_LOCAL_PATH non configuré, skip git push")
        return False

    repo = Path(repo_path)
    if not (repo / ".git").is_dir():
        logger.error(f"Pas de repo git à {repo_path}")
        return False

    try:
        subprocess.run(["git", "-C", str(repo), "add", "frontend/content/articles/"], check=True, capture_output=True)
        subprocess.run(
            ["git", "-C", str(repo), "commit", "-m", message],
            check=True,
            capture_output=True,
        )
        subprocess.run(["git", "-C", str(repo), "push"], check=True, capture_output=True)
        logger.info(f"Git push réussi: '{message}'")
        return True
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode("utf-8", errors="ignore") if e.stderr else ""
        logger.error(f"Git push échoué: {e}\nstderr: {stderr}")
        return False


def trigger_vercel_rebuild() -> Optional[dict]:
    """Ping le Vercel Deploy Hook (déclenche rebuild sans attendre git push)."""
    if not settings.vercel_deploy_hook:
        return None

    import requests
    try:
        response = requests.post(settings.vercel_deploy_hook, timeout=10)
        response.raise_for_status()
        result = response.json() if response.headers.get("content-type", "").startswith("application/json") else {}
        logger.info(f"Vercel rebuild déclenché: {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur déclenchement Vercel: {e}")
        return None
