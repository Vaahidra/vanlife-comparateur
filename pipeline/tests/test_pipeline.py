"""Tests smoke du scaffold Phase 0.

Vérifie que:
    - L'arborescence est correcte
    - Les imports modules fonctionnent
    - validate_env() retourne un bool sans planter
    - Les utilitaires de base marchent
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ajoute pipeline/ au PYTHONPATH pour les tests
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PIPELINE_ROOT))


def test_arborescence_exists():
    """Vérifie que les dossiers essentiels existent."""
    assert (PIPELINE_ROOT / "modules").is_dir()
    assert (PIPELINE_ROOT / "data").is_dir()
    assert (PIPELINE_ROOT / "data" / "templates").is_dir()
    assert (PIPELINE_ROOT / "outputs").is_dir()


def test_data_files_exist():
    """Vérifie que les JSON de données existent."""
    assert (PIPELINE_ROOT / "data" / "topics_queue.json").is_file()
    assert (PIPELINE_ROOT / "data" / "topics_done.json").is_file()
    assert (PIPELINE_ROOT / "data" / "products_db.json").is_file()


def test_templates_exist():
    """Vérifie les 3 templates Markdown."""
    templates_dir = PIPELINE_ROOT / "data" / "templates"
    assert (templates_dir / "article_comparatif.md").is_file()
    assert (templates_dir / "article_test_produit.md").is_file()
    assert (templates_dir / "article_guide_achat.md").is_file()


def test_config_imports():
    """validate_env() doit être appelable sans planter."""
    from config import validate_env

    result = validate_env(strict=False)
    assert isinstance(result, bool)


def test_modules_import():
    """Tous les modules doivent s'importer (stubs OK)."""
    from modules import (
        topics,
        product_research,
        content_writer,
        seo_optimizer,
        image_handler,
        affiliate_linker,
        nuxt_publisher,
        quality_check,
        notify,
        utils,
    )

    assert hasattr(topics, "pop_next")
    assert hasattr(content_writer, "generate")
    assert hasattr(affiliate_linker, "make_amazon_link")
    assert hasattr(utils, "make_slug")


def test_utils_slug():
    """make_slug doit produire un slug propre."""
    from modules.utils import make_slug

    assert make_slug("Meilleure batterie lithium 100Ah vanlife") == "meilleure-batterie-lithium-100ah-vanlife"
    # python-slugify retire `&` et translit les accents FR
    assert make_slug("Test  spécial  & accents éàç") == "test-special-accents-eac"


def test_affiliate_link_format():
    """make_amazon_link doit retourner un lien Amazon FR."""
    from modules.affiliate_linker import make_amazon_link

    link = make_amazon_link("B0EXAMPLE123")
    assert "amazon.fr/dp/B0EXAMPLE123" in link


def test_quality_check_length():
    """check_length doit valider les longueurs correctement.

    Range comparatif = (3000, 4500) mots.
    """
    from modules.quality_check import check_length

    short_text = "mot " * 100         # 100 mots → trop court
    too_long_text = "mot " * 5000     # 5000 mots → trop long (> 4500)
    ok_text = "mot " * 3500           # 3500 mots → dans la range

    ok_short, _ = check_length(short_text, "comparatif")
    ok_long, _ = check_length(too_long_text, "comparatif")
    ok_mid, _ = check_length(ok_text, "comparatif")
    assert not ok_short
    assert not ok_long
    assert ok_mid


def test_keyword_density():
    """compute_keyword_density doit retourner un float."""
    from modules.seo_optimizer import compute_keyword_density

    text = "vanlife vanlife test mot fourgon vanlife"
    density = compute_keyword_density(text, "vanlife")
    assert 0 < density < 100
