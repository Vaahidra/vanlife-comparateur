"""Génération d'articles via Gemini 2.5 Flash (avec fallback Groq).

3 formats supportés:
    - comparatif: article Top X (3000-4500 mots)
    - test_produit: review individuelle (1800-2500 mots)
    - guide_achat: guide thématique (2500-3500 mots)

Le prompt système est calibré pour:
    - Ton direct, concret, sans bullshit marketing
    - Pas de markers IA (éviter "il est important", "en effet", "néanmoins" en excès)
    - EEAT: chiffres précis, sources vérifiables, cas d'usage concrets
    - Honnêteté sur défauts produits
"""

from __future__ import annotations

import logging
from typing import Literal, Optional

logger = logging.getLogger(__name__)

ArticleType = Literal["comparatif", "test_produit", "guide_achat"]

SYSTEM_PROMPT = """Tu es un expert vanlife français passionné, qui rédige pour un public AVERTI \
(propriétaires de fourgon, futurs aménageurs). Ils connaissent MPPT, LiFePO4, dimensionnement \
électrique. Ne leur explique pas l'évidence.

Style:
- Direct, concret, factuel
- Tutoiement du lecteur
- Pas de superlatifs vides ("le meilleur", "incroyable", "révolutionnaire")
- Honnête sur les défauts
- Anecdotes terrain quand pertinent (mais ne JAMAIS inventer)

Contraintes EEAT:
- Cite des sources vérifiables (constructeur, norme IEC, étude labo)
- Donne des chiffres précis (Wh, Ah, kg, dB, °C, cycles)
- Si tu ne sais pas: écris "à vérifier" plutôt que d'inventer
- Évite les markers IA: "il est important de noter", "en conclusion", \
"néanmoins" en surutilisation, "en effet"

Sortie: JSON strict respectant le schéma fourni."""


def generate(
    topic: dict,
    products_data: list[dict],
    article_type: ArticleType,
    model: str = "gemini-2.5-flash",
) -> dict:
    """TODO Phase 4: génère un article structuré via Gemini.

    Returns:
        dict avec keys: title, slug, meta_description, h1, intro, sections,
        verdict, faq, conclusion, internal_links_suggestions, schema_markup
    """
    raise NotImplementedError("À implémenter en Phase 4")


def fallback_groq(topic: dict, products_data: list[dict], article_type: ArticleType) -> dict:
    """TODO Phase 4: fallback Llama 3.3 70B via Groq si Gemini fail."""
    raise NotImplementedError("À implémenter en Phase 4")
