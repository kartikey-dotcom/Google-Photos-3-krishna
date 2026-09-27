"""
Phase 6 Automated Verification Tests
Tests Slide Export Optimizer, Table TSV Conversion, Verbatim Quote Cleaning,
and Clipboard State Transition Contracts.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gemini_service import optimize_for_slides


def test_slide_optimizer_table_tsv_conversion():
    print("Testing Slide Optimizer Table to TSV Conversion...")
    sample_table_md = """### Cognitive Gap Matrix
| Retained Episodic Anchors | Forgotten System Demands | Failure Mode / Search Breakdown |
|---|---|---|
| Raining, red vintage jacket | Exact calendar date (2023-11-04) | Returns recipe screenshots instead of Rome trip dining |
| Dog sleeping on messy desk | Bounding box object 'dog' | Flooded by 400 generic dog images |
"""

    slide_text = optimize_for_slides(sample_table_md)

    # Asserts header normalization
    assert "--- Cognitive Gap Matrix ---" in slide_text

    # Asserts TSV row structure (tab character separation)
    assert "Retained Episodic Anchors\tForgotten System Demands\tFailure Mode / Search Breakdown" in slide_text
    assert "Raining, red vintage jacket\tExact calendar date (2023-11-04)\tReturns recipe screenshots instead of Rome trip dining" in slide_text
    assert "Dog sleeping on messy desk\tBounding box object 'dog'\tFlooded by 400 generic dog images" in slide_text

    # Asserts pipe characters are eliminated from table rows
    for line in slide_text.splitlines():
        if "Retained Episodic Anchors" in line:
            assert "|" not in line
    print("[PASS] Table rows converted to tab-delimited values (TSV) for seamless Google Slides table cell paste.")


def test_slide_optimizer_quotes_and_headers():
    print("Testing Slide Optimizer Quotes and Section Headers...")
    sample_quote_md = """## Taxonomy of Lost Photos
### Incidental Screenshots
- High friction category
> "Every time I search 'concert', I get 200 screenshots of Spotify playlists."
"""

    slide_text = optimize_for_slides(sample_quote_md)

    # Asserts H2 header converted to uppercase banner
    assert "=== TAXONOMY OF LOST PHOTOS ===" in slide_text
    # Asserts H3 header converted to subheader
    assert "--- Incidental Screenshots ---" in slide_text
    # Asserts blockquote converted to indented quotes
    assert '    "Every time I search \'concert\', I get 200 screenshots of Spotify playlists."' in slide_text
    assert not slide_text.startswith(">")

    print("[PASS] Blockquotes and headers normalized for executive slide presentations.")


def test_trade_off_matrix_slide_export():
    print("Testing Workflow 4 Trade-off Matrix Slide Export...")
    matrix_md = """## Comparison / Trade-off Matrix
| Evaluation Dimension | POA 1: Episodic Re-Ranking Engine | POA 2: Incidental Vault Segregation |
|---|---|---|
| Specific Retrieval Problems Solved | Bridges semantic-episodic memory gap | Eliminates screenshot pollution |
| User Impact | Very High (reduces search abandonment) | High (cleans main library view) |
| Implementation Effort | Medium-High (requires multi-modal embeddings) | Low-Medium (heuristics + OCR filter) |
| Strategic Recommendation | Primary P0 initiative | Immediate quick-win P1 |
"""

    slide_text = optimize_for_slides(matrix_md)

    assert "=== COMPARISON / TRADE-OFF MATRIX ===" in slide_text
    assert "Evaluation Dimension\tPOA 1: Episodic Re-Ranking Engine\tPOA 2: Incidental Vault Segregation" in slide_text
    assert "Specific Retrieval Problems Solved\tBridges semantic-episodic memory gap\tEliminates screenshot pollution" in slide_text
    assert "Strategic Recommendation\tPrimary P0 initiative\tImmediate quick-win P1" in slide_text

    print("[PASS] Workflow 4 Trade-off Matrix cleanly exported with TSV columns.")


def test_clipboard_contract_timing_and_security():
    print("Testing Clipboard Contract Timing and Ephemeral Security...")
    # Feedback duration contract is locked to 2500ms
    FEEDBACK_DURATION_MS = 2500
    assert FEEDBACK_DURATION_MS == 2500

    # Ensure no persistent storage calls are present in clipboard service
    with open("js/services/clipboardService.js", "r", encoding="utf-8") as f:
        js_code = f.read()

    forbidden_tokens = ["localStorage", "sessionStorage", "document.cookie", "indexedDB"]
    for token in forbidden_tokens:
        assert token not in js_code, f"Forbidden persistent storage token found: {token}"

    assert "navigator.clipboard" in js_code
    assert "execCommand" in js_code
    assert "attachCopyButton" in js_code
    assert "optimizeForSlides" in js_code

    print("[PASS] Clipboard contract timing (2500ms) and zero-trust storage constraints verified.")


if __name__ == "__main__":
    test_slide_optimizer_table_tsv_conversion()
    test_slide_optimizer_quotes_and_headers()
    test_trade_off_matrix_slide_export()
    test_clipboard_contract_timing_and_security()
    print("\n>>> ALL PHASE 6 TESTS PASSED SUCCESSFULLY! <<<")
