"""Gestion des images : recherche, download, sauvegarde locale.

Sources actuellement supportées :
    - Pexels API (free tier : 200 req/h, 20 000/mois)
    - Unsplash API (optionnel, fallback)

Pipeline images :
    1. fetch_for_article(slug, query, category) cherche une photo pertinente
    2. Télécharge en local : frontend/public/images/articles/{slug}.jpg
    3. Retourne le chemin web `/images/articles/{slug}.jpg` à mettre dans frontmatter

Fallback gracieux : si pas de PEXELS_API_KEY → log warning + retourne None
(le composant Vue `<PlaceholderImage>` prend le relais côté frontend).

Resize/optimisation : 1200x675 (16/9), JPEG qualité 82 via Pillow.
"""

from __future__ import annotations

import logging
from io import BytesIO
from pathlib import Path
from typing import Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from config import settings

logger = logging.getLogger(__name__)

PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"
ARTICLES_IMG_SUBDIR = "articles"
TARGET_WIDTH = 1200
TARGET_HEIGHT = 675  # 16:9
JPEG_QUALITY = 82


# Mots-clés enrichis par catégorie pour Pexels (français + anglais)
CATEGORY_KEYWORDS = {
    "energie": ["solar panel rv", "campervan battery", "off-grid power"],
    "cuisine": ["camper van kitchen", "campervan cooking", "outdoor kitchen camping"],
    "confort": ["van life cozy", "camper van interior", "rv heating"],
    "securite": ["camper van security", "van travel", "rv lock"],
    "amenagement": ["van conversion", "camper van interior", "campervan diy"],
}


def fetch_for_article(
    slug: str,
    query: str,
    category: Optional[str] = None,
    output_root: Optional[Path] = None,
) -> Optional[str]:
    """Cherche + télécharge une image pour l'article.

    Args:
        slug: slug de l'article (= nom du fichier image)
        query: mot-clé principal (titre / keyword_focus)
        category: catégorie vanlife (energie, cuisine, etc.)
        output_root: dossier racine où écrire (default: frontend/public/images/)

    Returns:
        Chemin web utilisable par le frontmatter (ex: "/images/articles/foo.jpg")
        ou None si aucune image trouvée / clé manquante.
    """
    if not settings.pexels_api_key:
        logger.warning("PEXELS_API_KEY absent → pas de photo téléchargée (fallback PlaceholderImage)")
        return None

    # Compose la query enrichie avec mots-clés catégorie
    enriched_query = _build_query(query, category)
    logger.info(f"Pexels search: '{enriched_query}'")

    photo_url = _search_pexels(enriched_query)
    if not photo_url:
        logger.warning(f"Pexels: aucun résultat pour '{enriched_query}'")
        return None

    if output_root is None:
        output_root = Path(settings.repo_local_path or ".") / "frontend" / "public" / "images"
    target_dir = output_root / ARTICLES_IMG_SUBDIR
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / f"{slug}.jpg"

    try:
        _download_and_save(photo_url, target_file)
    except Exception as e:
        logger.error(f"Échec téléchargement photo: {e}")
        return None

    web_path = f"/images/{ARTICLES_IMG_SUBDIR}/{slug}.jpg"
    logger.info(f"Photo enregistrée: {target_file} → {web_path}")
    return web_path


def _build_query(query: str, category: Optional[str]) -> str:
    """Compose une requête Pexels efficace.

    Pexels favorise les requêtes en anglais et courtes (2-4 mots).
    On combine le mot-clé catégorie + termes vanlife génériques.
    """
    extras = CATEGORY_KEYWORDS.get(category or "", ["van life"])
    # Pexels prend mieux les requêtes anglaises → on remplace quelques mots FR
    cleaned = (
        query.lower()
        .replace("fourgon", "van")
        .replace("amenagement", "interior")
        .replace("vanlife", "van life")
    )
    # Limite à ~6 mots
    words = cleaned.split()[:4]
    base = " ".join(words)
    return f"{base} {extras[0]}".strip()


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=8))
def _search_pexels(query: str) -> Optional[str]:
    """Appelle Pexels search API et retourne l'URL de la 1re photo pertinente."""
    headers = {"Authorization": settings.pexels_api_key}
    params = {
        "query": query,
        "per_page": 5,
        "orientation": "landscape",
        "size": "large",
    }
    r = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params, timeout=15)
    if r.status_code == 401:
        logger.error("PEXELS_API_KEY invalide (401). Vérifier la clé.")
        return None
    r.raise_for_status()
    data = r.json()
    photos = data.get("photos", [])
    if not photos:
        return None

    # Pick la première qui a une "large" source dispo
    for photo in photos:
        src = photo.get("src", {})
        if "large" in src:
            return src["large"]
        if "original" in src:
            return src["original"]
    return None


def _download_and_save(url: str, target: Path) -> None:
    """Télécharge l'image, resize 1200x675, save JPEG qualité 82."""
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    try:
        from PIL import Image, ImageOps
    except ImportError:
        # Pas de Pillow → save raw
        target.write_bytes(response.content)
        return

    img = Image.open(BytesIO(response.content)).convert("RGB")
    # Crop + resize en gardant aspect ratio 16:9
    img = ImageOps.fit(img, (TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
    img.save(target, "JPEG", quality=JPEG_QUALITY, optimize=True)


# ============================================
# Stubs anciens (compat retro avec doc projet)
# ============================================

def fetch_pexels(query: str, count: int = 1) -> list[str]:
    """Compat : retourne une liste d'URLs Pexels (sans download)."""
    if not settings.pexels_api_key:
        return []
    headers = {"Authorization": settings.pexels_api_key}
    params = {"query": query, "per_page": count, "orientation": "landscape"}
    r = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params, timeout=15)
    r.raise_for_status()
    return [p["src"].get("large", p["src"]["original"]) for p in r.json().get("photos", [])]


def fetch_unsplash(query: str, count: int = 1) -> list[str]:
    """TODO Phase 5 : si l'on veut ajouter Unsplash en fallback."""
    raise NotImplementedError("Unsplash pas encore implémenté (Pexels couvre déjà bien)")


def generate_alt_text(image_context: str) -> str:
    """Alt text simple (Gemini override possible en Phase 5+)."""
    return image_context[:120]
