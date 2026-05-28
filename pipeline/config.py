"""Configuration centralisée et validation des variables d'environnement.

Usage:
    python config.py            # valide les clés présentes et sort un rapport
    from config import settings # dans les autres modules
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Localisation
ROOT_DIR = Path(__file__).resolve().parent
REPO_ROOT = ROOT_DIR.parent
ENV_PATH = ROOT_DIR / ".env"

load_dotenv(ENV_PATH)


@dataclass(frozen=True)
class Settings:
    # IA
    gemini_api_key: Optional[str] = field(default_factory=lambda: os.getenv("GEMINI_API_KEY"))
    groq_api_key: Optional[str] = field(default_factory=lambda: os.getenv("GROQ_API_KEY"))

    # Publication (Git + Vercel)
    github_token: Optional[str] = field(default_factory=lambda: os.getenv("GITHUB_TOKEN"))
    github_repo: Optional[str] = field(default_factory=lambda: os.getenv("GITHUB_REPO"))
    github_branch: str = field(default_factory=lambda: os.getenv("GITHUB_BRANCH", "main"))
    repo_local_path: Optional[str] = field(default_factory=lambda: os.getenv("REPO_LOCAL_PATH"))
    vercel_deploy_hook: Optional[str] = field(default_factory=lambda: os.getenv("VERCEL_DEPLOY_HOOK"))

    # Images
    pexels_api_key: Optional[str] = field(default_factory=lambda: os.getenv("PEXELS_API_KEY"))
    unsplash_access_key: Optional[str] = field(default_factory=lambda: os.getenv("UNSPLASH_ACCESS_KEY"))

    # Affiliation
    amazon_partner_tag: Optional[str] = field(default_factory=lambda: os.getenv("AMAZON_PARTNER_TAG"))
    awin_publisher_id: Optional[str] = field(default_factory=lambda: os.getenv("AWIN_PUBLISHER_ID"))

    # Monitoring
    telegram_bot_token: Optional[str] = field(default_factory=lambda: os.getenv("TELEGRAM_BOT_TOKEN"))
    telegram_chat_id: Optional[str] = field(default_factory=lambda: os.getenv("TELEGRAM_CHAT_ID"))

    # Paths
    data_dir: Path = ROOT_DIR / "data"
    outputs_dir: Path = ROOT_DIR / "outputs"
    templates_dir: Path = ROOT_DIR / "data" / "templates"


settings = Settings()


# Clés essentielles : la pipeline ne peut pas tourner sans
ESSENTIAL_KEYS = {
    "GEMINI_API_KEY": settings.gemini_api_key,
    "GITHUB_TOKEN": settings.github_token,
    "GITHUB_REPO": settings.github_repo,
    "REPO_LOCAL_PATH": settings.repo_local_path,
}

# Clés recommandées : nécessaires à terme mais OK absent en Phase 0/1
RECOMMENDED_KEYS = {
    "GROQ_API_KEY": settings.groq_api_key,
    "PEXELS_API_KEY": settings.pexels_api_key,
    "UNSPLASH_ACCESS_KEY": settings.unsplash_access_key,
    "AMAZON_PARTNER_TAG": settings.amazon_partner_tag,
    "AWIN_PUBLISHER_ID": settings.awin_publisher_id,
    "TELEGRAM_BOT_TOKEN": settings.telegram_bot_token,
    "TELEGRAM_CHAT_ID": settings.telegram_chat_id,
}


def validate_env(strict: bool = False) -> bool:
    """Valide la présence des clés .env. Plante en mode strict si essentielles manquent.

    Args:
        strict: Si True, lève SystemExit quand une clé essentielle manque.

    Returns:
        True si toutes les clés essentielles sont présentes.
    """
    missing_essential = [k for k, v in ESSENTIAL_KEYS.items() if not v]
    missing_recommended = [k for k, v in RECOMMENDED_KEYS.items() if not v]

    print("\n=== Validation des variables d'environnement ===\n")
    print(f"Fichier .env : {ENV_PATH}")
    print(f"Existe : {ENV_PATH.exists()}\n")

    if missing_essential:
        print("❌ Clés ESSENTIELLES manquantes (la pipeline ne tournera pas) :")
        for k in missing_essential:
            print(f"   - {k}")
        print()
    else:
        print("✅ Toutes les clés essentielles sont présentes\n")

    if missing_recommended:
        print("⚠️  Clés recommandées manquantes (OK en Phase 0, à remplir avant prod) :")
        for k in missing_recommended:
            print(f"   - {k}")
        print()

    if missing_essential and strict:
        print("Mode strict : sortie avec erreur.\n")
        sys.exit(1)

    return not missing_essential


if __name__ == "__main__":
    ok = validate_env(strict=False)
    sys.exit(0 if ok else 1)
