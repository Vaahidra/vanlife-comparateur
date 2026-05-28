"""Notifications Telegram pour suivre l'état du pipeline.

Cas d'usage:
    - Article généré (avec lien admin Decap)
    - Article publié (avec URL publique)
    - Pipeline en erreur (avec stack trace résumée)
    - Reporting hebdomadaire (Phase 10)
"""

from __future__ import annotations

import logging
from typing import Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from config import settings

logger = logging.getLogger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def send_telegram(message: str, parse_mode: str = "Markdown") -> Optional[dict]:
    """Envoie un message Telegram via le bot configuré.

    Args:
        message: Texte du message (Markdown supporté)
        parse_mode: 'Markdown' ou 'HTML'

    Returns:
        Réponse JSON de l'API Telegram, ou None si bot non configuré
    """
    token = settings.telegram_bot_token
    chat_id = settings.telegram_chat_id

    if not token or not chat_id:
        logger.warning("Telegram non configuré, message ignoré")
        return None

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": parse_mode}

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()


def notify_article_generated(title: str, admin_url: str) -> None:
    """Notifie qu'un article a été généré et attend relecture."""
    send_telegram(
        f"📝 *Article généré*\n\n{title}\n\nRelecture: {admin_url}"
    )


def notify_article_published(title: str, public_url: str) -> None:
    """Notifie qu'un article a été publié."""
    send_telegram(
        f"✅ *Article publié*\n\n{title}\n\nLien: {public_url}"
    )


def notify_pipeline_error(context: str, error: str) -> None:
    """Notifie une erreur pipeline."""
    send_telegram(
        f"❌ *Erreur pipeline*\n\nContext: {context}\nErreur: `{error[:500]}`"
    )
