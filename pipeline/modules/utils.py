"""Utilitaires partagés du pipeline."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

from slugify import slugify

logger = logging.getLogger(__name__)


def now_iso() -> str:
    """Retourne l'instant courant en ISO 8601 UTC."""
    return datetime.now(timezone.utc).isoformat()


def today_str() -> str:
    """Retourne la date du jour au format YYYY-MM-DD."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def make_slug(text: str, max_length: int = 80) -> str:
    """Convertit un titre en slug URL-safe (FR-aware)."""
    return slugify(text, max_length=max_length, separator="-", lowercase=True)


def ensure_dir(path: Path) -> Path:
    """Crée un dossier s'il n'existe pas et retourne le path."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def truncate(text: str, max_length: int = 160, suffix: str = "...") -> str:
    """Tronque un texte sans couper au milieu d'un mot."""
    if len(text) <= max_length:
        return text
    truncated = text[: max_length - len(suffix)].rsplit(" ", 1)[0]
    return truncated + suffix
