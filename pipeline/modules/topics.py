"""Gestion de la queue de topics à traiter.

Responsabilités:
    - Charger/sauvegarder data/topics_queue.json
    - Pop du prochain topic par priorité
    - Marquer un topic comme done → déplace vers topics_done.json
    - Génération de nouveaux topics via Gemini (Phase 2)
"""

from __future__ import annotations

import json
import logging
import uuid
from pathlib import Path
from typing import Optional

from config import settings
from modules.utils import make_slug, now_iso, today_str

logger = logging.getLogger(__name__)

QUEUE_PATH = settings.data_dir / "topics_queue.json"
DONE_PATH = settings.data_dir / "topics_done.json"


def load_queue() -> dict:
    if not QUEUE_PATH.exists():
        return {"topics": []}
    return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))


def save_queue(data: dict) -> None:
    QUEUE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_done() -> dict:
    if not DONE_PATH.exists():
        return {"topics": []}
    return json.loads(DONE_PATH.read_text(encoding="utf-8"))


def save_done(data: dict) -> None:
    DONE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def pop_next() -> Optional[dict]:
    """Récupère le prochain topic à traiter (priorité haute, statut queued)."""
    data = load_queue()
    queued = [t for t in data.get("topics", []) if t.get("status") == "queued"]
    if not queued:
        return None
    queued.sort(key=lambda t: t.get("priority", 99))
    return queued[0]


def mark_status(topic_id: str, new_status: str) -> bool:
    """Met à jour le statut d'un topic dans la queue."""
    data = load_queue()
    for t in data.get("topics", []):
        if t.get("id") == topic_id:
            t["status"] = new_status
            t["updated_at"] = now_iso()
            save_queue(data)
            return True
    logger.warning(f"Topic {topic_id} introuvable pour mark_status({new_status})")
    return False


def mark_done(topic_id: str, article_url: Optional[str] = None) -> bool:
    """Déplace le topic vers topics_done.json."""
    data = load_queue()
    topic = None
    new_topics = []
    for t in data.get("topics", []):
        if t.get("id") == topic_id:
            topic = t
        else:
            new_topics.append(t)
    if not topic:
        logger.warning(f"Topic {topic_id} introuvable pour mark_done")
        return False

    topic["status"] = "published"
    topic["published_at"] = now_iso()
    if article_url:
        topic["article_url"] = article_url

    data["topics"] = new_topics
    save_queue(data)

    done_data = load_done()
    done_data["topics"].append(topic)
    save_done(done_data)
    logger.info(f"Topic {topic_id} marqué publié")
    return True


def seed_default_topics() -> None:
    """Pré-remplit la queue avec une dizaine de topics génériques vanlife.

    À lancer une fois en setup pour avoir de quoi tester immédiatement.
    """
    seeds = [
        # ÉNERGIE
        {
            "keyword": "meilleure batterie lithium 200ah vanlife",
            "type": "comparatif",
            "category": "energie",
            "products_to_compare": ["Renogy 200Ah", "Victron 200Ah", "Battle Born 200Ah"],
            "priority": 1,
        },
        {
            "keyword": "convertisseur 12v 220v pur sinus vanlife",
            "type": "comparatif",
            "category": "energie",
            "products_to_compare": ["Victron Phoenix 1200", "Renogy 2000W", "EcoFlow 1800W"],
            "priority": 2,
        },
        {
            "keyword": "station electrique portable ecoflow delta 2",
            "type": "test_produit",
            "category": "energie",
            "product_tested": "EcoFlow Delta 2",
            "priority": 3,
        },
        # CUISINE
        {
            "keyword": "meilleur frigo 12v compresseur 40 litres",
            "type": "comparatif",
            "category": "cuisine",
            "products_to_compare": ["Dometic CFX3 45", "ARB Classic II 47", "Engel MR040F"],
            "priority": 1,
        },
        {
            "keyword": "plaque cuisson induction camping car",
            "type": "guide_achat",
            "category": "cuisine",
            "priority": 4,
        },
        # CONFORT
        {
            "keyword": "chauffage diesel autoterm air 2d test",
            "type": "test_produit",
            "category": "confort",
            "product_tested": "Autoterm Air 2D",
            "priority": 1,
        },
        {
            "keyword": "douche solaire portable camping van",
            "type": "comparatif",
            "category": "confort",
            "products_to_compare": ["Helio Pressure Shower", "Yakima RoadShower", "Geyser Systems"],
            "priority": 4,
        },
        {
            "keyword": "toilettes seches separation fourgon amenage",
            "type": "guide_achat",
            "category": "confort",
            "priority": 3,
        },
        # SÉCURITÉ
        {
            "keyword": "tracker gps fourgon longue duree batterie",
            "type": "comparatif",
            "category": "securite",
            "products_to_compare": ["Quadtrak Q-Tracker", "Invoxia GPS Tracker", "Trackimo 3G"],
            "priority": 2,
        },
        # AMÉNAGEMENT
        {
            "keyword": "lanterneau fiamma vs maxxair vanlife",
            "type": "comparatif",
            "category": "amenagement",
            "products_to_compare": ["Fiamma Turbo Vent", "MaxxAir MaxxFan", "Heng's RV Vent"],
            "priority": 2,
        },
    ]

    data = load_queue()
    existing_keywords = {t["keyword"] for t in data.get("topics", [])}

    added = 0
    for seed in seeds:
        if seed["keyword"] in existing_keywords:
            continue
        topic = {
            "id": str(uuid.uuid4()),
            "status": "queued",
            "created_at": now_iso(),
            **seed,
        }
        data["topics"].append(topic)
        added += 1

    save_queue(data)
    logger.info(f"Seed: {added} topics ajoutés à la queue (total: {len(data['topics'])})")


def generate_topics_via_gemini(categories: list[str], count: int = 30) -> list[dict]:
    """TODO Phase 2 complète: génère via Gemini.

    Pour l'instant, fallback sur seed statique.
    """
    logger.warning("generate_topics_via_gemini pas encore implémenté, utiliser seed_default_topics()")
    return []


def validate_trend(keyword: str) -> dict:
    """TODO: pytrends — valide tendance Google."""
    raise NotImplementedError("À implémenter quand pytrends config OK")
