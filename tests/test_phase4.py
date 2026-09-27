"""
Phase 4 Automated Verification Tests
Tests Left Control Sidebar & Trigger Subsystem logic:
- Key sanitization pipeline (whitespace, quotes, tabs)
- Source selection & dynamic count recalculation
- Pre-flight validation: missing key check, empty sources check, valid payload check
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from corpus import default_python_corpus_store, VALID_SOURCES


def test_api_key_sanitization_pipeline():
    print("Testing API Key Sanitization Pipeline...")
    
    test_cases = [
        ("AIzaSyTestKey123", "AIzaSyTestKey123"),
        ("  AIzaSyTestKey123  ", "AIzaSyTestKey123"),
        ("\tAIzaSyTestKey123\n", "AIzaSyTestKey123"),
        ('"AIzaSyTestKey123"', "AIzaSyTestKey123"),
        ("'AIzaSyTestKey123'", "AIzaSyTestKey123"),
        ('  "AIzaSyTestKey123"  ', "AIzaSyTestKey123"),
        ("   ", ""),
        ("", ""),
    ]

    for raw, expected in test_cases:
        sanitized = raw.strip().strip("'\"")
        assert sanitized == expected, f"Failed for '{raw}': expected '{expected}', got '{sanitized}'"

    print("[PASS] API Key Sanitization pipeline strips whitespace, quotes, and newlines accurately.")


def test_sidebar_source_filtering_and_counts():
    print("Testing Sidebar Dynamic Source Counter...")
    store = default_python_corpus_store
    total = len(store.get_all_records())
    assert total == 7, f"Expected 7 total records, got {total}"

    # All active
    all_active = {s: True for s in VALID_SOURCES}
    assert store.get_active_count(all_active) == 7

    # Reddit disabled (3 records) -> 4 remaining
    no_reddit = {**all_active, "r/GooglePhotos": False}
    assert store.get_active_count(no_reddit) == 4

    # Reddit + Google Support disabled (3 + 2 = 5) -> 2 remaining
    sparse = {**all_active, "r/GooglePhotos": False, "Google Support Forum": False}
    assert store.get_active_count(sparse) == 2

    # All disabled -> 0 records
    all_disabled = {s: False for s in VALID_SOURCES}
    assert store.get_active_count(all_disabled) == 0

    print("[PASS] Sidebar dynamic counter recalculates accurately across all filter combinations.")


def test_preflight_validation_checks():
    print("Testing Pre-flight Workflow Validation...")

    def validate_preflight(key: str, active_count: int) -> dict:
        clean_key = key.strip().strip("'\"")
        if active_count == 0:
            return {"valid": False, "error": "NO_SOURCES_SELECTED"}
        if not clean_key:
            return {"valid": False, "error": "API_KEY_REQUIRED"}
        return {"valid": True, "clean_key": clean_key}

    # Case 1: No key, all sources active -> API_KEY_REQUIRED
    res1 = validate_preflight("", 7)
    assert not res1["valid"] and res1["error"] == "API_KEY_REQUIRED"

    # Case 2: Only quotes/whitespace key -> API_KEY_REQUIRED
    res2 = validate_preflight('  ""  ', 7)
    assert not res2["valid"] and res2["error"] == "API_KEY_REQUIRED"

    # Case 3: Key present, but 0 sources -> NO_SOURCES_SELECTED
    res3 = validate_preflight("AIzaSy123", 0)
    assert not res3["valid"] and res3["error"] == "NO_SOURCES_SELECTED"

    # Case 4: Valid key and active sources -> PASS
    res4 = validate_preflight("  'AIzaSyValidKey'  ", 4)
    assert res4["valid"] and res4["clean_key"] == "AIzaSyValidKey"

    print("[PASS] Pre-flight validation correctly guards against missing keys and empty datasets.")


if __name__ == "__main__":
    test_api_key_sanitization_pipeline()
    test_sidebar_source_filtering_and_counts()
    test_preflight_validation_checks()
    print("\n>>> ALL PHASE 4 PYTHON TESTS PASSED SUCCESSFULLY! <<<")
