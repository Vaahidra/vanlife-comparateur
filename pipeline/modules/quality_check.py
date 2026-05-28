"""Validation qualité d'un article avant publication.

Checks bloquants (un seul fail → article passe en pending_review):
    - Longueur min/max selon type (comparatif 3000-4500, test 1800-2500, guide 2500-3500)
    - Densité mot-clé principal entre 0.5% et 2%
    - Minimum 6 H2
    - Au moins 1 tableau, 3 listes, 1 FAQ
    - Meta description < 160 caractères
    - Pas de markers IA en surutilisation
    - Au moins 2 liens externes (sources d'autorité)
    - Au moins 3 liens internes (autres articles du site)
    - 3+ CTA d'affiliation, max 1 par 600 mots
    - Featured image + 2-3 images dans le corps
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Literal

logger = logging.getLogger(__name__)

ArticleType = Literal["comparatif", "test_produit", "guide_achat"]

# Markers IA à éviter (surutilisation = signal Google "contenu IA non retouché")
AI_MARKERS = [
    "il est important de noter",
    "il convient de souligner",
    "en conclusion",
    "néanmoins",
    "cependant",
    "en effet",
    "il est essentiel de",
    "il convient de mentionner",
    "force est de constater",
    "en somme",
    "à noter que",
    "par ailleurs",
]


@dataclass
class CheckResult:
    passed: bool
    failures: list[str]
    warnings: list[str]


LENGTH_RANGES = {
    "comparatif": (3000, 4500),
    "test_produit": (1800, 2500),
    "guide_achat": (2500, 3500),
}


def run_all_checks(article: dict, article_type: ArticleType) -> CheckResult:
    """TODO Phase 4: lance tous les checks qualité et retourne le résultat."""
    raise NotImplementedError("À implémenter en Phase 4")


def check_length(text: str, article_type: ArticleType) -> tuple[bool, str]:
    """Valide la longueur selon le type d'article."""
    word_count = len(text.split())
    min_words, max_words = LENGTH_RANGES[article_type]
    if word_count < min_words:
        return False, f"Trop court: {word_count} mots (min {min_words})"
    if word_count > max_words:
        return False, f"Trop long: {word_count} mots (max {max_words})"
    return True, f"OK: {word_count} mots"


def check_ai_markers(text: str, max_total: int = 4) -> tuple[bool, str]:
    """Détecte la surutilisation de markers IA."""
    text_lower = text.lower()
    total = sum(text_lower.count(marker) for marker in AI_MARKERS)
    if total > max_total:
        return False, f"Trop de markers IA: {total} (max {max_total})"
    return True, f"OK: {total} markers IA"


def check_headings(text: str, min_h2: int = 6) -> tuple[bool, str]:
    """Compte les H2 dans le texte markdown."""
    h2_count = len(re.findall(r"^##\s", text, flags=re.MULTILINE))
    if h2_count < min_h2:
        return False, f"Pas assez de H2: {h2_count} (min {min_h2})"
    return True, f"OK: {h2_count} H2"


def check_meta_description(meta: str, max_chars: int = 160) -> tuple[bool, str]:
    if len(meta) > max_chars:
        return False, f"Meta trop longue: {len(meta)} chars (max {max_chars})"
    return True, f"OK: {len(meta)} chars"
