"""Gestion de la queue de topics à traiter.

Responsabilités:
    - Charger/sauvegarder data/topics_queue.json
    - Pop du prochain topic par priorité
    - Marquer un topic comme done → déplace vers topics_done.json
    - Génération de nouveaux topics via Gemini (Phase 2)
    - Validation Google Trends d'un topic (pytrends)
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from config import settings

logger = logging.getLogger(__name__)

QUEUE_PATH = settings.data_dir / "topics_queue.json"
DONE_PATH = settings.data_dir / "topics_done.json"


def load_queue() -> dict:
    """Charge la queue depuis le JSON."""
    if not QUEUE_PATH.exists():
        return {"topics": []}
    return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))


def save_queue(data: dict) -> None:
    """Sauvegarde la queue."""
    QUEUE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def pop_next() -> Optional[dict]:
    """Récupère le prochain topic à traiter (priorité haute en premier, statut queued)."""
    data = load_queue()
    queued = [t for t in data.get("topics", []) if t.get("status") == "queued"]
    if not queued:
        return None
    queued.sort(key=lambda t: t.get("priority", 99))
    return queued[0]


def mark_in_progress(topic_id: str) -> None:
    """TODO Phase 4: passe le statut à 'in_progress'."""
    raise NotImplementedError("À implémenter en Phase 4")


def mark_done(topic_id: str) -> None:
    """TODO Phase 4: déplace le topic vers topics_done.json."""
    raise NotImplementedError("À implémenter en Phase 4")


def generate_topics_via_gemini(categories: list[str], count: int = 80) -> list[dict]:
    """TODO Phase 2: génère une liste de topics structurée via Gemini."""
    raise NotImplementedError("À implémenter en Phase 2")


def validate_trend(keyword: str) -> dict:
    """TODO Phase 2: valide la tendance Google Trends d'un mot-clé via pytrends."""
    raise NotImplementedError("À implémenter en Phase 2")
