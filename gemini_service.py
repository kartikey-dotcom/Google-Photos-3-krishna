"""
Gemini Service & Multi-Shot Prompt Orchestrator for Streamlit
AI-Powered Discovery Engine for Google Photos
Phase 3: Prompt Orchestrator, Gemini 1.5 Client & Comparison Engine
"""

from typing import Dict, List, Any
import json
import requests

# Strict System Prompt Directives for Workflows 1 to 4
PROMPT_DIRECTIVES = {
    "taxonomy": """SYSTEM INSTRUCTION:
Act as a Principal Product Manager for Google Photos Core Search. Analyze the provided VoC feedback dataset.
Identify exactly 3 distinct categories of personal photos that users struggle to retrieve using conventional keyword search.
EXCLUDE generic categories (e.g., 'vacations', 'birthdays', 'pets').
FOCUS strictly on edge-cases such as 'Incidental Screenshots', 'Situational/Aesthetic Vibe Photos', or 'Relative-Temporal Events'.

OUTPUT CONTRACT:
- Use strictly Markdown formatting.
- For each category, use H3 (###) for the category name.
- Use bullet points (-) for the formal analytical definition.
- Use Blockquotes (>) for the exact verbatim quote from the provided data as empirical evidence.
- Do NOT include conversational opening or closing statements. Output ONLY the structured analysis.""",

    "cognitive_gap": """SYSTEM INSTRUCTION:
Act as a Principal Cognitive UX Researcher for Google Photos. Analyze the provided VoC feedback dataset to map the cognitive gap during failed photo searches.
Deconstruct what sensory, relational, emotional, or episodic anchors users consistently retain in working memory (e.g., weather, apparel color, companion, ambient setting) versus what rigid absolute metadata the current system demands (e.g., exact calendar dates, GPS coordinates, literal object labels).

OUTPUT CONTRACT:
- Output strictly a Markdown Table (T-Chart) with exactly 3 columns:
  | Retained Episodic Anchors (Human Recall) | Forgotten System Demands (Current Index Requirements) | Failure Mode / Search Breakdown |
- Ground every row directly in user behaviors demonstrated in the dataset.
- Do NOT include introductory text, conversational chatter, or concluding remarks.""",

    "workarounds": """SYSTEM INSTRUCTION:
Act as a Staff Product Manager for Google Photos. Analyze the provided VoC dataset to identify the specific manual compensatory actions and brute-force workarounds users endure when search fails.
Name each distinct behavioral pattern with high-impact product terminology (e.g., 'The Person Pivot', 'Chronological Scrubbing', 'External App Trail', 'Multi-Keyword Permutation Roulette').
Assign an analytical 'Friction Score' (High, Medium, or Low) based on the cognitive tax, time loss, and frustration expressed.

OUTPUT CONTRACT:
- Format as a numbered list (1., 2., 3., 4.).
- Bold the name of each workaround.
- Explicitly state the friction score on the next line: "- **Friction Score**: High / Medium / Low".
- Provide a detailed definition explaining the exact sequence of user actions and cognitive friction.
- Output ONLY the numbered list.""",

    "poa": """SYSTEM INSTRUCTION:
Act as VP of Product for Google Photos. Based strictly on the identified search failure taxonomies, cognitive gaps, and manual workarounds extracted from the VoC dataset, synthesize exactly 2 high-impact Product Opportunity Areas (POAs).

OUTPUT CONTRACT:
- Use Markdown formatting with H2 (##) for each POA title.
- Under each POA, include exactly three sub-headers using H3 (###):
  ### Problem Space
  ### Proposed AI Solution
  ### Hypothesis to Test
- Formulate the hypothesis using a rigorous PM structure: "If [Proposed Action], then [Measurable Behavioral Outcome], resulting in [Quantifiable Impact on Metric]".
- Immediately following the 2 POAs, include an H2 header: '## Comparison / Trade-off Matrix'.
- Render a structured Markdown Table comparing POA 1 vs POA 2 across:
  | Evaluation Dimension | POA 1: [Short Title] | POA 2: [Short Title] |
  covering rows for:
  | Specific Retrieval Problems Solved | ... | ... |
  | User Impact | ... | ... |
  | Implementation Effort | ... | ... |
  | Strategic Recommendation | ... | ... |
- Output ONLY the structured POAs and Comparison Matrix. Do NOT include conversational opening or closing chatter.""",
}

GENERATION_CONFIG = {
    "temperature": 0.2,  # Locked for deterministic, reproducible synthesis
    "topP": 0.8,
    "topK": 40,
    "maxOutputTokens": 2048,
}


def build_workflow_prompt(workflow_id: str, records: List[Dict[str, Any]]) -> str:
    """Assembles the system directive and injected corpus JSON into a complete prompt."""
    directive = PROMPT_DIRECTIVES.get(workflow_id)
    if not directive:
        raise ValueError(f"Unknown workflow ID: '{workflow_id}'")

    if not records:
        raise ValueError("Cannot assemble prompt with empty feedback records.")

    corpus_json = json.dumps(records, indent=2)

    return f"""{directive}

---

INPUT VOICE-OF-CUSTOMER (VoC) FEEDBACK DATASET:
```json
{corpus_json}
```

Strictly adhere to the output contract and ground all findings in the provided dataset. Begin your analysis now:"""


def execute_gemini_inference(prompt: str, api_key: str, model_name: str = "gemini-1.5-flash") -> Dict[str, Any]:
    """
    Direct HTTPS REST client for Google AI Studio Generative Language API
    bound strictly to Temperature 0.2 and Top_P 0.8.
    """
    clean_key = (api_key or "").strip().strip("'\"")
    if not clean_key:
        return {
            "success": False,
            "error": "API Key Required: Please add your GEMINI_API_KEY to the Streamlit Cloud secrets.",
            "status": 401,
        }

    if not prompt or not prompt.strip():
        return {
            "success": False,
            "error": "Invalid Request: Prompt cannot be empty.",
            "status": 400,
        }

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={clean_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": GENERATION_CONFIG,
    }

    import time
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=45,
            )

            if response.status_code in (429, 500, 503) and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
                
            if response.status_code != 200:
                return map_http_error(response.status_code, endpoint)

            data = response.json()
            candidates = data.get("candidates", [])
            if not candidates:
                return {
                    "success": False,
                    "error": "Empty Model Response: Google Gemini returned no candidates.",
                    "status": 200,
                }

            text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            if not text or not text.strip():
                return {
                    "success": False,
                    "error": "Empty Model Response: Model returned an empty text string.",
                    "status": 200,
                }

            return {
                "success": True,
                "data": text.strip(),
                "status": 200,
            }

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return {
                "success": False,
                "error": "Request Timeout: Google AI Studio took longer than 45 seconds to respond. Please retry.",
                "status": 408,
            }
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return {
                "success": False,
                "error": "Network Connection Failed: Unable to reach Google AI Studio. Please verify your internet connection or proxy settings.",
                "status": 0,
            }
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            return {
                "success": False,
                "error": f"Unexpected Error: {str(e)}",
                "status": 500,
            }


def map_http_error(status: int, endpoint: str = "") -> Dict[str, Any]:
    """Maps HTTP status codes to executive diagnostic banners."""
    if status == 400:
        msg = "Invalid Request (400): Invalid request payload or parameter format sent to Google AI Studio."
    elif status in (401, 403):
        msg = "Authentication Failed (401/403): Your Gemini API key is invalid or unauthorized. Please verify your Google AI Studio credentials in the sidebar."
    elif status == 404:
        msg = f"Model Not Found (404): The requested Gemini model was not found for this API key. ({endpoint})"
    elif status == 429:
        msg = "Rate Limit Exceeded (429): Google AI Studio quota exceeded. Please wait 30 seconds before triggering another analytical workflow."
    elif status in (500, 503):
        msg = "Service Unavailable (500/503): Google AI Studio is experiencing temporary service disruption. Please retry shortly."
    else:
        msg = f"Inference Failed (HTTP {status}): An unexpected error occurred while communicating with Google AI Studio."

    return {
        "success": False,
        "error": msg,
        "status": status,
    }


def optimize_for_slides(markdown: str) -> str:
    """
    Plaintext Slide Paste Optimizer
    Converts markdown tables into tab-delimited rows for instant Google Slides / Docs
    table cell paste, indents quotes, and cleans formatting artifacts.
    """
    if not markdown:
        return ""

    import re

    lines = markdown.splitlines()
    output = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Markdown Table Conversion
        if line.strip().startswith("|") and line.strip().endswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i].strip())
                i += 1

            if len(table_lines) >= 2:
                header_cells = [c.strip().replace("\t", " ") for c in table_lines[0].split("|")[1:-1]]
                output.append("\t".join(header_cells))

                body_start = 2 if len(table_lines) > 1 and re.match(r"^[|\s:-]+$", table_lines[1]) else 1
                for row_line in table_lines[body_start:]:
                    cells = [c.strip().replace("\t", " ") for c in row_line.split("|")[1:-1]]
                    if cells and any(len(c) > 0 for c in cells):
                        output.append("\t".join(cells))
            output.append("")
            continue

        # Verbatim Blockquote Conversion
        if line.strip().startswith(">"):
            quote_text = re.sub(r"^>\s?", "", line.strip()).strip()
            if (quote_text.startswith('"') and quote_text.endswith('"')) or (quote_text.startswith("'") and quote_text.endswith("'")):
                quote_text = quote_text[1:-1].strip()
            output.append(f'    "{quote_text}"')
            i += 1
            continue

        # Header normalization for Slides
        if re.match(r"^#{1,3}\s+", line):
            level = len(re.match(r"^(#{1,3})", line).group(1))
            text = re.sub(r"^#{1,3}\s+", "", line).strip()
            if level in (1, 2):
                output.append(f"\n=== {text.upper()} ===\n")
            else:
                output.append(f"\n--- {text} ---")
            i += 1
            continue

        output.append(line)
        i += 1

    return "\n".join(output).strip()

def execute_gemini_inference_stream(prompt: str, api_key: str, model_name: str = "gemini-1.5-flash"):
    import time, json, requests
    clean_key = (api_key or "").strip().strip("'\"")
    if not clean_key:
        yield "Error: Missing API Key"
        return
    if not prompt or not prompt.strip():
        yield "Error: Invalid Request"
        return

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:streamGenerateContent?alt=sse&key={clean_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": GENERATION_CONFIG,
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            with requests.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=45,
                stream=True
            ) as response:
                if response.status_code in (429, 500, 503) and attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                
                if response.status_code != 200:
                    yield f"Error {response.status_code}: {response.text}"
                    return
                
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        if decoded_line.startswith('data: '):
                            data_str = decoded_line[6:]
                            try:
                                chunk = json.loads(data_str)
                                candidates = chunk.get("candidates", [])
                                if candidates:
                                    text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                                    if text:
                                        yield text
                            except Exception:
                                pass
                return
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            yield f"Error: {str(e)}"
            return
