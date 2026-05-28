"""Génération et injection de liens d'affiliation.

Programmes supportés:
    - Amazon Partenaires France (commission 3-7%)
    - Awin (Cdiscount, ManoMano, Decathlon — commission 5-8%)
    - Programmes directs constructeurs (EcoFlow, Bluetti, Victron — 6-12%)

Règles légales (FR):
    - rel="sponsored nofollow" OBLIGATOIRE sur tous les liens affiliés
    - Mention transparence visible en haut de chaque article comparatif
    - Pas de masking de liens (interdit par Amazon + illégal)
    - Pas plus d'1 CTA par 600 mots dans le corps (anti-spam)
"""

from __future__ import annotations

import logging
from typing import Optional

from config import settings

logger = logging.getLogger(__name__)


TRANSPARENCY_MENTION = """\
*Certains liens de cet article sont affiliés. Si tu achètes via ces liens, je touche une \
petite commission sans surcoût pour toi. Cela m'aide à entretenir ce blog. Merci !*"""


def make_amazon_link(asin: str) -> str:
    """Construit un lien d'affiliation Amazon FR."""
    tag = settings.amazon_partner_tag
    if not tag:
        logger.warning("AMAZON_PARTNER_TAG manquant, lien sans tag d'affiliation")
        return f"https://www.amazon.fr/dp/{asin}"
    return f"https://www.amazon.fr/dp/{asin}?tag={tag}"


def make_awin_link(merchant_id: str, deep_link: str) -> str:
    """TODO Phase 6: construit un lien affilié Awin."""
    raise NotImplementedError("À implémenter en Phase 6")


def make_cta_button(url: str, label: str = "Voir le prix sur Amazon →") -> str:
    """Génère un bouton CTA HTML avec attributs d'affiliation requis."""
    return (
        f'<a href="{url}" rel="sponsored nofollow" target="_blank" class="cta-button">'
        f"{label}</a>"
    )


def inject_links_in_article(article_md: str, products_db: dict) -> str:
    """TODO Phase 6: détecte les noms de produits dans l'article et injecte les bons CTA."""
    raise NotImplementedError("À implémenter en Phase 6")


def count_cta_density(article_md: str) -> tuple[int, int]:
    """Retourne (nb_cta, nb_mots) pour valider la règle 1 CTA / 600 mots."""
    nb_words = len(article_md.split())
    nb_cta = article_md.count('class="cta-button"')
    return nb_cta, nb_words
