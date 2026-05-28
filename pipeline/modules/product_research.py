"""Recherche produits et collecte de specs.

Responsabilités:
    - Scraping de specs publiques depuis sites constructeurs (BeautifulSoup)
    - Récupération prix Amazon FR (PA-API officielle, pas de scraping agressif)
    - Téléchargement de 2-3 photos HD par produit (sources légales)
    - Stockage dans data/products_db.json

ATTENTION LÉGAL:
    - Pas de scraping massif Amazon (ban du compte affilié garanti)
    - Respect des robots.txt et rate limiting (tenacity backoff)
    - Sources d'images: constructeur officiel + crédit obligatoire
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def fetch_product_specs(product_name: str, manufacturer_url: Optional[str] = None) -> dict:
    """TODO Phase 3: scrape les specs publiques d'un produit."""
    raise NotImplementedError("À implémenter en Phase 3")


def fetch_amazon_price(asin: str) -> Optional[float]:
    """TODO Phase 3: récupère le prix Amazon FR via PA-API (nécessite compte Partenaires validé)."""
    raise NotImplementedError("À implémenter en Phase 3 + après validation Amazon")


def fetch_product_images(product_name: str, count: int = 3) -> list[str]:
    """TODO Phase 3: récupère N images HD d'un produit (sources légales uniquement)."""
    raise NotImplementedError("À implémenter en Phase 3")
