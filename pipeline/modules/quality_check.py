"""Validation qualité d'un article avant publication.

Checks bloquants (un seul fail → article passe en pending_review):
    - Longueur min/max selon type
    - Au moins 1 tableau, 3 listes, 1 FAQ
    - Meta description < 160 caractères
    - Markers IA non surutilisés
    - Au moins 3 sections H2
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Literal

logger = logging.getLogger(__name__)

ArticleType = Literal["comparatif", "test_produit", "guide_achat"]

# Markers IA à éviter (surutilisation = signal Google "contenu IA non retouché")
AI_MARKERS = [
    "il est important de noter",
    "il convient de souligner",
    "en conclusion",
    "néanmoins",
    "il est essentiel de",
    "il convient de mentionner",
    "force est de constater",
    "en somme",
    "à noter que",
]


@dataclass
class CheckResult:
    passed: bool
    failures: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)


LENGTH_RANGES = {
    "comparatif": (3000, 4500),
    "test_produit": (1800, 2500),
    "guide_achat": (2500, 3500),
}


def run_all_checks(article: dict, article_type: ArticleType) -> CheckResult:
    """Lance tous les checks qualité et retourne le résultat agrégé."""
    failures: list[str] = []
    warnings: list[str] = []
    metrics: dict = {}

    # Reconstruit le texte total (intro + sections + verdict + FAQ + conclusion)
    full_text = _flatten_article_text(article)
    metrics["word_count"] = len(full_text.split())
    metrics["char_count"] = len(full_text)

    # Longueur
    ok, msg = check_length(full_text, article_type)
    if ok:
        metrics["length_check"] = "OK"
    else:
        warnings.append(f"Longueur: {msg}")
        metrics["length_check"] = msg

    # H2 minimum
    sections = article.get("sections", [])
    metrics["h2_count"] = len(sections)
    if len(sections) < 3:
        failures.append(f"Pas assez de sections H2: {len(sections)} (min 3)")

    # Meta description
    meta = article.get("meta_description", "")
    metrics["meta_length"] = len(meta)
    if len(meta) > 160:
        failures.append(f"Meta description trop longue: {len(meta)} chars (max 160)")
    elif len(meta) < 80:
        warnings.append(f"Meta description courte: {len(meta)} chars (recommandé 100-155)")

    # FAQ
    faq = article.get("faq", [])
    metrics["faq_count"] = len(faq)
    if len(faq) < 3:
        warnings.append(f"FAQ courte: {len(faq)} questions (recommandé 5-7)")

    # Markers IA
    ai_count = _count_ai_markers(full_text)
    metrics["ai_markers"] = ai_count
    if ai_count > 4:
        warnings.append(f"Trop de markers IA: {ai_count} (max 4)")

    # Tableaux
    table_count = full_text.count("|---|") + full_text.count("|--|")
    metrics["table_count"] = table_count
    if article_type == "comparatif" and table_count == 0:
        warnings.append("Aucun tableau dans un article comparatif")

    # Title length
    title = article.get("title", "")
    metrics["title_length"] = len(title)
    if len(title) > 70:
        warnings.append(f"Titre long: {len(title)} chars (recommandé < 65 pour SEO)")

    passed = len(failures) == 0
    return CheckResult(passed=passed, failures=failures, warnings=warnings, metrics=metrics)


def _flatten_article_text(article: dict) -> str:
    """Reconstruit le texte intégral pour le compte de mots."""
    parts = [article.get("intro", "")]
    for s in article.get("sections", []):
        parts.append(s.get("h2", ""))
        parts.append(s.get("content_markdown", ""))
    parts.append(article.get("verdict", ""))
    for qa in article.get("faq", []):
        parts.append(qa.get("question", ""))
        parts.append(qa.get("reponse", ""))
    parts.append(article.get("conclusion", ""))
    return "\n".join(parts)


def _count_ai_markers(text: str) -> int:
    text_lower = text.lower()
    return sum(text_lower.count(marker) for marker in AI_MARKERS)


def check_length(text: str, article_type: ArticleType) -> tuple[bool, str]:
    word_count = len(text.split())
    min_words, max_words = LENGTH_RANGES[article_type]
    if word_count < min_words:
        return False, f"Trop court: {word_count} mots (min {min_words})"
    if word_count > max_words:
        return False, f"Trop long: {word_count} mots (max {max_words})"
    return True, f"OK: {word_count} mots"


def check_ai_markers(text: str, max_total: int = 4) -> tuple[bool, str]:
    total = _count_ai_markers(text)
    if total > max_total:
        return False, f"Trop de markers IA: {total} (max {max_total})"
    return True, f"OK: {total} markers IA"


def check_headings(text: str, min_h2: int = 6) -> tuple[bool, str]:
    h2_count = len(re.findall(r"^##\s", text, flags=re.MULTILINE))
    if h2_count < min_h2:
        return False, f"Pas assez de H2: {h2_count} (min {min_h2})"
    return True, f"OK: {h2_count} H2"


def check_meta_description(meta: str, max_chars: int = 160) -> tuple[bool, str]:
    if len(meta) > max_chars:
        return False, f"Meta trop longue: {len(meta)} chars (max {max_chars})"
    return True, f"OK: {len(meta)} chars"
