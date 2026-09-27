"""
Python Ingestion Engine, Schema Validation & Simulated VoC Corpus
AI-Powered Discovery Engine for Google Photos
Phase 2: Ingestion Engine & Data Contracts
"""

from typing import Dict, List, Any, Optional
import json

VALID_SOURCES = [
    "r/GooglePhotos",
    "Play Store",
    "App Store",
    "Google Support Forum",
]

VALID_FEEDBACK_TYPES = [
    "Reddit Post",
    "1-Star Review",
    "2-Star Review",
    "Support Thread",
    "Feature Request",
]

# 7 Rich Multi-Channel Simulated Feedback Records Grounded in Episodic Retrieval Breakdowns
SEED_CORPUS: List[Dict[str, Any]] = [
    {
        "id": "voc-001",
        "source": "r/GooglePhotos",
        "type": "Reddit Post",
        "content": "I'm trying to find a photo of a specific pasta dish from my Rome trip. Searching 'pasta' gives me screenshots of recipes. I can't remember the exact date, I just know it was raining and I was wearing a red jacket. I gave up after scrolling for 10 minutes.",
        "metadata": {
            "upvotes": 45,
            "date": "2023-11-04",
            "tags": ["search_failure", "screenshots", "travel", "episodic_weather"],
        },
    },
    {
        "id": "voc-002",
        "source": "Play Store",
        "type": "1-Star Review",
        "content": "Search is useless now. If I don't know the exact date, I can't find anything. I try searching for my dog, but it shows every dog photo instead of the specific one where he's sleeping on my messy desk.",
        "metadata": {
            "rating": 1,
            "device": "Pixel 7 Pro",
            "date": "2024-01-15",
            "tags": ["pets", "context_clutter", "posture_ambiguity"],
        },
    },
    {
        "id": "voc-003",
        "source": "Google Support Forum",
        "type": "Support Thread",
        "content": "How do I filter OUT screenshots when searching for tickets or receipts? Every time I search 'concert', I get 200 screenshots of Spotify playlists and ticket confirmations rather than the photos of me and my friends at the venue.",
        "metadata": {
            "upvotes": 112,
            "date": "2023-09-28",
            "tags": ["screenshot_pollution", "concert", "social_retrieval"],
        },
    },
    {
        "id": "voc-004",
        "source": "r/GooglePhotos",
        "type": "Reddit Post",
        "content": "Had to find a picture of my car's tire pressure sticker taken last year. Searched 'tire' and 'car' and got 500 pictures of road trips. I ended up opening WhatsApp to find the date I texted it to my mechanic, then scrolled to that date in Google Photos.",
        "metadata": {
            "upvotes": 88,
            "date": "2024-02-10",
            "tags": ["workaround", "external_app_audit", "utilitarian_doc"],
        },
    },
    {
        "id": "voc-005",
        "source": "App Store",
        "type": "2-Star Review",
        "content": "I remember the vibe of a photo—it was a sunset where everything had a purple haze on the beach in Greece. Searching 'sunset beach' returns 1,200 photos from the last 8 years. Why can't I search 'purple sunset with two people'?",
        "metadata": {
            "rating": 2,
            "device": "iPhone 15 Pro",
            "date": "2024-03-02",
            "tags": ["aesthetic_vibe", "sensory_recall", "color_query"],
        },
    },
    {
        "id": "voc-006",
        "source": "r/GooglePhotos",
        "type": "Reddit Post",
        "content": "I wanted to show my friend a meme I saved three weeks ago about cats in coffee cups. Searching 'cat' brings up thousands of actual pictures of my cat. Why does Google Photos mix saved web garbage with my real life memories?",
        "metadata": {
            "upvotes": 142,
            "date": "2024-03-18",
            "tags": ["meme_pollution", "asset_silos", "saved_media"],
        },
    },
    {
        "id": "voc-007",
        "source": "Google Support Forum",
        "type": "Support Thread",
        "content": "I cannot remember what month my nephew was born, but I know my mom was holding him while sitting in her green floral armchair. Searching 'baby' or 'chair' gives endless hits. I spent 20 minutes scrubbing the timeline year by year.",
        "metadata": {
            "upvotes": 67,
            "date": "2024-04-05",
            "tags": ["chronological_scrubbing", "relational_anchor", "furniture_context"],
        },
    },
]


def validate_feedback_record(record: Any) -> Dict[str, Any]:
    """Validate a single feedback record against schema rules."""
    errors = []
    if not isinstance(record, dict):
        return {"valid": False, "errors": ["Record must be a dictionary"]}

    if not record.get("id") or not isinstance(record["id"], str):
        errors.append("Record 'id' must be a non-empty string")

    if record.get("source") not in VALID_SOURCES:
        errors.append(f"Record 'source' must be one of: {', '.join(VALID_SOURCES)}")

    if record.get("type") not in VALID_FEEDBACK_TYPES:
        errors.append(f"Record 'type' must be one of: {', '.join(VALID_FEEDBACK_TYPES)}")

    if not record.get("content") or not isinstance(record["content"], str):
        errors.append("Record 'content' must be a non-empty string")

    metadata = record.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("Record 'metadata' must be a valid dictionary")
    else:
        if not metadata.get("date") or not isinstance(metadata["date"], str):
            errors.append("Record 'metadata.date' must be a valid date string")
        if not isinstance(metadata.get("tags"), list):
            errors.append("Record 'metadata.tags' must be a list of strings")

    return {"valid": len(errors) == 0, "errors": errors}


def sanitize_feedback_record(record: Any) -> Dict[str, Any]:
    """Defensive sanitizer providing robust defaults for malformed or missing fields."""
    if not isinstance(record, dict):
        return {
            "id": "voc-fallback",
            "source": "Google Support Forum",
            "type": "Support Thread",
            "content": "No review text provided",
            "metadata": {"date": "Unknown", "tags": []},
        }

    raw_id = str(record.get("id", "")).strip() or "voc-auto"
    source = record.get("source") if record.get("source") in VALID_SOURCES else "Google Support Forum"
    btype = record.get("type") if record.get("type") in VALID_FEEDBACK_TYPES else "Support Thread"
    content = str(record.get("content", "")).strip() or "No review text provided"

    raw_meta = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    metadata = {
        "date": str(raw_meta.get("date", "Unknown")).strip(),
        "tags": [str(t).strip().lower() for t in raw_meta.get("tags", []) if str(t).strip()],
    }

    if "upvotes" in raw_meta and isinstance(raw_meta["upvotes"], (int, float)):
        metadata["upvotes"] = max(0, int(raw_meta["upvotes"]))
    if "rating" in raw_meta and isinstance(raw_meta["rating"], (int, float)):
        metadata["rating"] = min(5, max(1, int(raw_meta["rating"])))
    if "device" in raw_meta and str(raw_meta["device"]).strip():
        metadata["device"] = str(raw_meta["device"]).strip()

    return {
        "id": raw_id,
        "source": source,
        "type": btype,
        "content": content,
        "metadata": metadata,
    }


class PythonCorpusStore:
    """In-memory corpus store managing filtering and serialization for Streamlit."""

    def __init__(self, initial_records: Optional[List[Dict[str, Any]]] = None):
        if initial_records is None:
            self.records = [sanitize_feedback_record(r) for r in SEED_CORPUS]
        else:
            self.records = [sanitize_feedback_record(r) for r in initial_records]

    def get_all_records(self) -> List[Dict[str, Any]]:
        return list(self.records)

    def get_record_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        for r in self.records:
            if r["id"] == record_id:
                return r
        return None

    def get_active_records(self, source_filters: Optional[Dict[str, bool]] = None) -> List[Dict[str, Any]]:
        if not source_filters:
            return list(self.records)
        return [r for r in self.records if source_filters.get(r["source"], True)]

    def get_active_count(self, source_filters: Optional[Dict[str, bool]] = None) -> int:
        return len(self.get_active_records(source_filters))

    def get_source_counts(self) -> Dict[str, int]:
        counts = {s: 0 for s in VALID_SOURCES}
        counts["total"] = len(self.records)
        for r in self.records:
            if r["source"] in counts:
                counts[r["source"]] += 1
        return counts

    def serialize_records(self, records: List[Dict[str, Any]]) -> str:
        """Formats active records into compact JSON string for prompt injection."""
        return json.dumps(records, indent=2)


# Default singleton instance
default_python_corpus_store = PythonCorpusStore()
