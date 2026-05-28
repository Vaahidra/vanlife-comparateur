"""Gestion des images: download, génération, compression, upload.

Sources:
    - Pexels API (gratuit, HD, libre de droit)
    - Unsplash API (gratuit, HD, libre de droit)
    - Gemini Imagen 4 (génération IA, gratuit)
    - Constructeurs (avec crédit + lien source)

Pipeline:
    - Featured image 1920x1080 + overlay titre
    - 1 image tous les 600-800 mots dans le corps
    - Compression: max 1200px, WebP qualité 82
    - Alt text généré par Gemini (SEO + accessibilité)

Stockage:
    - Local: pipeline/outputs/images/{article-slug}/
    - Frontend: frontend/public/images/{article-slug}/ (déposé par nuxt_publisher)
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def fetch_pexels(query: str, count: int = 1) -> list[str]:
    """TODO Phase 5: cherche des images sur Pexels API."""
    raise NotImplementedError("À implémenter en Phase 5")


def fetch_unsplash(query: str, count: int = 1) -> list[str]:
    """TODO Phase 5: cherche des images sur Unsplash API."""
    raise NotImplementedError("À implémenter en Phase 5")


def generate_via_imagen(description: str) -> bytes:
    """TODO Phase 5: génère une image via Gemini Imagen 4."""
    raise NotImplementedError("À implémenter en Phase 5")


def add_title_overlay(image_path: Path, title: str, output_path: Path) -> None:
    """TODO Phase 5: ajoute un overlay titre en bas d'image (Pillow)."""
    raise NotImplementedError("À implémenter en Phase 5")


def compress_image(image_path: Path, max_width: int = 1200, quality: int = 82) -> Path:
    """TODO Phase 5: compresse une image en WebP."""
    raise NotImplementedError("À implémenter en Phase 5")


def generate_alt_text(image_context: str) -> str:
    """TODO Phase 5: génère un alt text SEO via Gemini."""
    raise NotImplementedError("À implémenter en Phase 5")
