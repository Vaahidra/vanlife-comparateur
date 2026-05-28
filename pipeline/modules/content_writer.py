"""Génération d'articles via Gemini 2.5 Flash (avec fallback Groq + mock mode).

3 formats supportés:
    - comparatif: article Top X (3000-4500 mots)
    - test_produit: review individuelle (1800-2500 mots)
    - guide_achat: guide thématique (2500-3500 mots)

Mode mock activé si GEMINI_API_KEY absent → génère un article placeholder
pour tester la machinery sans payer / consommer quota.
"""

from __future__ import annotations

import json
import logging
from typing import Literal, Optional

from config import settings
from modules.utils import make_slug, now_iso, today_str

logger = logging.getLogger(__name__)

ArticleType = Literal["comparatif", "test_produit", "guide_achat"]

SYSTEM_PROMPT = """Tu rédiges pour un blog vanlife français destiné à un public AVERTI \
(propriétaires de fourgon, futurs aménageurs). Ils connaissent MPPT, LiFePO4, dimensionnement \
électrique. Ne leur explique pas l'évidence.

Style:
- Direct, concret, factuel
- Tutoiement du lecteur
- Pas de superlatifs vides ("le meilleur", "incroyable", "révolutionnaire")
- Honnête sur les défauts

══════════════════════════════════════════════════════════════════
🚫 INTERDIT ABSOLU — règle critique EEAT 🚫
══════════════════════════════════════════════════════════════════
Le rédacteur N'A PAS d'expérience personnelle vanlife. Tu DOIS éviter
TOUTE formulation à la 1re personne qui sous-entend une expérience vécue :

INTERDIT (sera détecté et rejeté) :
- "j'ai testé / vu / essayé / acheté / installé / utilisé / monté"
- "j'ai eu l'occasion de"
- "dans mon van / fourgon / aménagement"
- "sur mon installation"
- "mon ami / pote / frère / cousin a"
- "d'expérience"
- "personnellement"
- "à mon avis je pense que"

OBLIGATOIRE — reformulations neutres autorisées :
- "Selon plusieurs retours utilisateurs sur les forums vanlife"
- "Les manuels constructeurs indiquent"
- "Les tests labos rapportés mentionnent"
- "D'après les fiches techniques publiques"
- "Les retours communautaires soulignent"
- "Les forums spécialisés (vanlife.fr, Le Monde du Camping-Car) notent"
- Citer des sources externes vérifiables (normes IEC, sites constructeur)
══════════════════════════════════════════════════════════════════

Contraintes EEAT:
- Cite des sources vérifiables (constructeur, norme IEC, étude labo, forums)
- Donne des chiffres précis (Wh, Ah, kg, dB, °C, cycles)
- Si tu ne sais pas: écris "à vérifier" plutôt que d'inventer
- Évite markers IA: "il est important de noter", "en conclusion", \
"néanmoins" en surutilisation, "en effet"

Sortie: JSON strict respectant le schéma fourni."""


# Schémas Gemini (response_schema, dict-based pour éviter dep Pydantic)
ARTICLE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Titre H1 de l'article (max 70 chars, SEO-friendly)"},
        "slug": {"type": "string", "description": "URL slug en kebab-case"},
        "meta_description": {"type": "string", "description": "Meta description SEO (max 155 chars)"},
        "intro": {"type": "string", "description": "Introduction accrocheuse (150-200 mots)"},
        "sections": {
            "type": "array",
            "description": "Sections H2 du corps",
            "items": {
                "type": "object",
                "properties": {
                    "h2": {"type": "string"},
                    "content_markdown": {"type": "string", "description": "Contenu de la section en markdown"},
                },
                "required": ["h2", "content_markdown"],
            },
        },
        "verdict": {"type": "string", "description": "Verdict final synthétique (150-250 mots)"},
        "faq": {
            "type": "array",
            "description": "5-7 questions/réponses pour le snippet Google",
            "items": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "reponse": {"type": "string"},
                },
                "required": ["question", "reponse"],
            },
        },
        "conclusion": {"type": "string", "description": "Conclusion courte (80-150 mots)"},
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "3-7 tags SEO",
        },
    },
    "required": ["title", "slug", "meta_description", "intro", "sections", "verdict", "faq", "conclusion", "tags"],
}


def generate(
    topic: dict,
    products_data: Optional[list[dict]] = None,
    article_type: Optional[ArticleType] = None,
    model: Optional[str] = None,
) -> dict:
    """Génère un article structuré via Gemini.

    Args:
        topic: dict avec keys keyword, category, products_to_compare, type
        products_data: specs des produits (optionnel)
        article_type: comparatif | test_produit | guide_achat (sinon depuis topic['type'])
        model: override du modèle Gemini

    Returns:
        dict structuré (voir ARTICLE_SCHEMA) prêt à être passé à nuxt_publisher.
    """
    article_type = article_type or topic.get("type", "comparatif")
    products_data = products_data or []

    user_prompt = _build_user_prompt(topic, products_data, article_type)

    if not settings.gemini_api_key:
        logger.warning("GEMINI_API_KEY absent → mode mock (article placeholder)")
        return _mock_article(topic, article_type)

    return _generate_via_gemini(user_prompt, model or settings.gemini_model)


def _build_user_prompt(topic: dict, products_data: list[dict], article_type: ArticleType) -> str:
    parts = [
        f"Sujet: {topic['keyword']}",
        f"Catégorie: {topic.get('category', 'general')}",
        f"Format: {article_type}",
    ]

    length_target = {
        "comparatif": "3000-4500 mots",
        "test_produit": "1800-2500 mots",
        "guide_achat": "2500-3500 mots",
    }[article_type]
    parts.append(f"Longueur cible: {length_target}")

    if products := topic.get("products_to_compare"):
        parts.append(f"Produits à comparer: {', '.join(products)}")

    if products_data:
        parts.append("\nSpecs produits disponibles:\n" + json.dumps(products_data, indent=2, ensure_ascii=False))

    parts.append("\nRespecte STRICTEMENT le schéma JSON demandé. Pas de Markdown autour du JSON.")
    return "\n".join(parts)


def _generate_via_gemini(prompt: str, model_name: str) -> dict:
    """Appel réel à Gemini avec structured output."""
    try:
        import google.generativeai as genai
    except ImportError as e:
        logger.error("google-generativeai non installé. Run: pip install google-generativeai")
        raise

    genai.configure(api_key=settings.gemini_api_key)

    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=SYSTEM_PROMPT,
    )

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": ARTICLE_SCHEMA,
                "temperature": 0.7,
                "max_output_tokens": 8192,
            },
        )
    except Exception as e:
        logger.error(f"Erreur appel Gemini: {e}")
        if settings.groq_api_key:
            logger.info("Fallback sur Groq...")
            return _generate_via_groq(prompt)
        raise

    article = json.loads(response.text)
    logger.info(f"Article généré via Gemini: '{article['title']}' ({len(article.get('sections', []))} sections)")
    return article


def _generate_via_groq(prompt: str) -> dict:
    """Fallback Groq (Llama 3.3 70B). Pas de structured output natif → parse JSON manuel."""
    try:
        from groq import Groq
    except ImportError:
        logger.error("groq non installé. Run: pip install groq")
        raise

    client = Groq(api_key=settings.groq_api_key)
    full_prompt = (
        SYSTEM_PROMPT
        + "\n\n"
        + prompt
        + "\n\nIMPORTANT: réponds UNIQUEMENT avec du JSON valide respectant le schéma demandé. "
        + f"Schema:\n{json.dumps(ARTICLE_SCHEMA, ensure_ascii=False)}"
    )

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": full_prompt}],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=8000,
    )
    article = json.loads(response.choices[0].message.content)
    logger.info(f"Article généré via Groq fallback: '{article['title']}'")
    return article


def _mock_article(topic: dict, article_type: ArticleType) -> dict:
    """Article mock pour tester la pipeline sans clé API."""
    keyword = topic.get("keyword", "test vanlife")
    category = topic.get("category", "general")
    slug = make_slug(keyword)

    return {
        "title": f"[MOCK] {keyword.capitalize()}",
        "slug": slug,
        "meta_description": f"Article mock généré pour tester la pipeline. Sujet: {keyword}.",
        "intro": (
            f"⚠️ **Article généré en mode MOCK** (pas de clé GEMINI_API_KEY). "
            f"Sujet: {keyword}. Catégorie: {category}. Format: {article_type}.\n\n"
            "Pour générer du vrai contenu, mettre `GEMINI_API_KEY=xxx` dans `pipeline/.env` "
            "et relancer la pipeline."
        ),
        "sections": [
            {
                "h2": "Section mock 1",
                "content_markdown": f"Lorem ipsum vanlife — sujet *{keyword}*. Cette section serait remplie par Gemini en mode réel.",
            },
            {
                "h2": "Section mock 2 — Comparaison",
                "content_markdown": "| Produit A | Produit B |\n|---|---|\n| Mock data | Mock data |",
            },
        ],
        "verdict": f"Verdict mock pour {keyword}. Le vrai verdict sera généré par Gemini.",
        "faq": [
            {"question": "C'est quoi ce mock ?", "reponse": "Une réponse placeholder pour valider la pipeline sans API."},
            {"question": "Comment générer du vrai contenu ?", "reponse": "Mettre GEMINI_API_KEY dans .env."},
        ],
        "conclusion": "Conclusion mock. Configure Gemini pour du vrai contenu vanlife.",
        "tags": ["mock", "test", category, "pipeline"],
    }
