"""
Phase 2 Automated Verification Tests
Tests schema validation, seed corpus integrity, defensive sanitization,
source filtering, and JSON serialization.
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from corpus import (
    SEED_CORPUS,
    VALID_SOURCES,
    VALID_FEEDBACK_TYPES,
    validate_feedback_record,
    sanitize_feedback_record,
    PythonCorpusStore,
    default_python_corpus_store,
)


def test_seed_corpus_integrity():
    print("Testing Seed Corpus Integrity...")
    assert len(SEED_CORPUS) == 7, f"Expected 7 records, got {len(SEED_CORPUS)}"

    for record in SEED_CORPUS:
        validation = validate_feedback_record(record)
        assert validation["valid"], f"Record {record.get('id')} failed validation: {validation['errors']}"
        assert record["source"] in VALID_SOURCES
        assert record["type"] in VALID_FEEDBACK_TYPES
        assert len(record["content"]) > 10
        assert "date" in record["metadata"]
        assert len(record["metadata"]["tags"]) > 0

    print("[PASS] All 7 Seed Corpus records passed strict schema validation.")


def test_defensive_sanitization():
    print("Testing Defensive Sanitization on Malformed Records...")
    malformed_record = {
        "id": "   voc-malformed-999  ",
        "source": "Invalid Channel",
        "type": "Unknown Type",
        "content": "",
        "metadata": None,
    }

    sanitized = sanitize_feedback_record(malformed_record)
    assert sanitized["id"] == "voc-malformed-999"
    assert sanitized["source"] == "Google Support Forum"  # default fallback
    assert sanitized["type"] == "Support Thread"  # default fallback
    assert sanitized["content"] == "No review text provided"  # fallback
    assert sanitized["metadata"]["date"] == "Unknown"
    assert sanitized["metadata"]["tags"] == []

    print("[PASS] Defensive sanitization correctly provided all required fallbacks.")


def test_corpus_store_filtering_and_counts():
    print("Testing CorpusStore Source Filtering & Live Counts...")
    store = PythonCorpusStore()

    counts = store.get_source_counts()
    assert counts["r/GooglePhotos"] == 3
    assert counts["Play Store"] == 1
    assert counts["App Store"] == 1
    assert counts["Google Support Forum"] == 2
    assert counts["total"] == 7

    # Test filtering
    filters = {
        "r/GooglePhotos": True,
        "Play Store": False,
        "App Store": False,
        "Google Support Forum": False,
    }
    active_records = store.get_active_records(filters)
    assert len(active_records) == 3
    for r in active_records:
        assert r["source"] == "r/GooglePhotos"

    # Test JSON serialization for prompt injection
    serialized_json = store.serialize_records(active_records)
    parsed = json.loads(serialized_json)
    assert len(parsed) == 3
    assert parsed[0]["id"] == "voc-001"

    # Test empty filter
    empty_filters = {s: False for s in VALID_SOURCES}
    assert store.get_active_count(empty_filters) == 0

    print("[PASS] CorpusStore filtering, counts, and serialization passed with 100% precision.")


if __name__ == "__main__":
    test_seed_corpus_integrity()
    test_defensive_sanitization()
    test_corpus_store_filtering_and_counts()
    print("\n>>> ALL PHASE 2 PYTHON TESTS PASSED SUCCESSFULLY! <<<")
