"""
Phase 3 Automated Verification Tests
Validates prompt contracts, strict parameter envelopes (Temp 0.2, Top_P 0.8),
corpus injection, Workflow 4 Comparison Matrix requirement, and diagnostic error mapping.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from corpus import SEED_CORPUS
from gemini_service import (
    PROMPT_DIRECTIVES,
    GENERATION_CONFIG,
    build_workflow_prompt,
    map_http_error,
)


def test_generation_config_bounds():
    print("Testing Generation Config Bounds (Temperature & Top_P)...")
    assert GENERATION_CONFIG["temperature"] == 0.2, f"Expected temp 0.2, got {GENERATION_CONFIG['temperature']}"
    assert GENERATION_CONFIG["topP"] == 0.8, f"Expected topP 0.8, got {GENERATION_CONFIG['topP']}"
    assert GENERATION_CONFIG["topK"] == 40, f"Expected topK 40, got {GENERATION_CONFIG['topK']}"
    assert GENERATION_CONFIG["maxOutputTokens"] == 2048, f"Expected maxOutputTokens 2048, got {GENERATION_CONFIG['maxOutputTokens']}"
    print("[PASS] Generation config strictly bound to Temp: 0.2, Top_P: 0.8, MaxTokens: 2048.")


def test_workflow_prompt_contracts():
    print("Testing System Directives and Output Contracts for Workflows 1-4...")

    # Workflow 1: Taxonomy
    wf1 = PROMPT_DIRECTIVES["taxonomy"]
    assert "Principal Product Manager" in wf1
    assert "3 distinct categories" in wf1
    assert "EXCLUDE generic categories" in wf1
    assert "###" in wf1
    assert "Blockquotes (>)" in wf1
    assert "Do NOT include conversational opening" in wf1
    print("[PASS] Workflow 1 (Taxonomy of 'Lost' Photos) contract verified.")

    # Workflow 2: Cognitive Gap
    wf2 = PROMPT_DIRECTIVES["cognitive_gap"]
    assert "Principal Cognitive UX Researcher" in wf2
    assert "Markdown Table (T-Chart) with exactly 3 columns" in wf2
    assert "Retained Episodic Anchors" in wf2
    assert "Forgotten System Demands" in wf2
    assert "Failure Mode / Search Breakdown" in wf2
    print("[PASS] Workflow 2 (Cognitive Gap Matrix) contract verified.")

    # Workflow 3: Behavioral Workarounds
    wf3 = PROMPT_DIRECTIVES["workarounds"]
    assert "Staff Product Manager" in wf3
    assert "Friction Score" in wf3
    assert "High / Medium / Low" in wf3
    assert "numbered list" in wf3
    print("[PASS] Workflow 3 (Behavioral Workaround Mapping) contract verified.")

    # Workflow 4: Product Opportunity Synthesis & Comparison Matrix
    wf4 = PROMPT_DIRECTIVES["poa"]
    assert "VP of Product" in wf4
    assert "2 high-impact Product Opportunity Areas" in wf4
    assert "### Problem Space" in wf4
    assert "### Proposed AI Solution" in wf4
    assert "### Hypothesis to Test" in wf4
    assert "## Comparison / Trade-off Matrix" in wf4
    assert "Evaluation Dimension" in wf4
    assert "Specific Retrieval Problems Solved" in wf4
    assert "User Impact" in wf4
    assert "Implementation Effort" in wf4
    print("[PASS] Workflow 4 (POAs & Comparison / Trade-off Matrix) contract verified.")


def test_prompt_assembly_with_corpus():
    print("Testing Prompt Assembly with Injected Corpus JSON...")
    prompt = build_workflow_prompt("taxonomy", SEED_CORPUS)
    assert "INPUT VOICE-OF-CUSTOMER (VoC) FEEDBACK DATASET:" in prompt
    assert "voc-001" in prompt
    assert "voc-007" in prompt
    assert "Rome trip" in prompt

    # Test error handling on empty corpus
    try:
        build_workflow_prompt("taxonomy", [])
        assert False, "Should raise ValueError on empty records"
    except ValueError:
        pass

    print("[PASS] Prompt assembly correctly injects structured VoC corpus.")


def test_error_interceptor_mappings():
    print("Testing HTTP Error Interceptor Mappings...")
    err400 = map_http_error(400)
    assert "Invalid Request (400)" in err400["error"]

    err401 = map_http_error(401)
    assert "Authentication Failed (401/403)" in err401["error"]

    err429 = map_http_error(429)
    assert "Rate Limit Exceeded (429)" in err429["error"]
    assert "30 seconds" in err429["error"]

    err500 = map_http_error(500)
    assert "Service Unavailable (500/503)" in err500["error"]

    print("[PASS] HTTP diagnostic error interceptors correctly mapped.")


if __name__ == "__main__":
    test_generation_config_bounds()
    test_workflow_prompt_contracts()
    test_prompt_assembly_with_corpus()
    test_error_interceptor_mappings()
    print("\n>>> ALL PHASE 3 TESTS PASSED SUCCESSFULLY! <<<")
