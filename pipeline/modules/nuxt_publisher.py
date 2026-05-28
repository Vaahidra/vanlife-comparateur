"""Publication d'articles vers le frontend Nuxt via git push.

Flow:
    1. Convertit l'article (dict structuré) → fichier Markdown avec frontmatter YAML
    2. Écrit dans frontend/content/articles/{slug}.md
    3. Copie les images dans frontend/public/images/{slug}/
    4. git add + commit + push (branche configurée)
    5. Vercel détecte le push → rebuild automatique
    6. Optionnel: ping le Vercel Deploy Hook pour forcer rebuild immédiat

Statut publication:
    - draft: frontmatter `draft: true` → page non générée par Nuxt content
    - ready: frontmatter `draft: false` ou absent → page publique
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from config import settings

logger = logging.getLogger(__name__)


def article_to_markdown(article: dict) -> str:
    """TODO Phase 7: convertit le dict article en .md avec frontmatter YAML."""
    raise NotImplementedError("À implémenter en Phase 7")


def write_article_file(slug: str, markdown: str, draft: bool = True) -> Path:
    """TODO Phase 7: écrit le fichier dans frontend/content/articles/."""
    raise NotImplementedError("À implémenter en Phase 7")


def copy_images_to_public(slug: str, local_images_dir: Path) -> list[Path]:
    """TODO Phase 7: copie les images vers frontend/public/images/{slug}/."""
    raise NotImplementedError("À implémenter en Phase 7")


def git_commit_and_push(message: str) -> None:
    """TODO Phase 7: stage les changements et push via GitPython."""
    raise NotImplementedError("À implémenter en Phase 7")


def trigger_vercel_rebuild() -> Optional[dict]:
    """TODO Phase 7: ping le Vercel Deploy Hook (optionnel)."""
    if not settings.vercel_deploy_hook:
        return None
    raise NotImplementedError("À implémenter en Phase 7")
