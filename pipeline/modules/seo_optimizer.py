"""Optimisation SEO on-page d'un article généré.

Responsabilités:
    - Meta title + meta description optimisés (longueurs respectées)
    - Schema markup JSON-LD (FAQPage + Product + Review)
    - Structure H1/H2/H3 validée
    - Densité mot-clé principal (0.5% - 2%)
    - Maillage interne automatique (suggestions de 3-5 articles liés)
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def optimize_meta(article: dict, target_keyword: str) -> dict:
    """TODO Phase 4: optimise meta title/description."""
    raise NotImplementedError("À implémenter en Phase 4")


def generate_schema_markup(article: dict, products: list[dict]) -> str:
    """TODO Phase 4: génère le JSON-LD FAQPage + Product + Review."""
    raise NotImplementedError("À implémenter en Phase 4")


def compute_keyword_density(text: str, keyword: str) -> float:
    """Calcule la densité d'un mot-clé dans un texte (en %)."""
    if not text or not keyword:
        return 0.0
    words = text.lower().split()
    occurrences = sum(1 for w in words if keyword.lower() in w)
    return (occurrences / len(words)) * 100 if words else 0.0


def suggest_internal_links(article_slug: str, all_articles: list[dict], top_n: int = 5) -> list[str]:
    """TODO Phase 9: suggère des liens internes via embedding similarity (Gemini)."""
    raise NotImplementedError("À implémenter en Phase 9")
