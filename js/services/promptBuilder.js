/**
 * Multi-Shot Prompt Assembler & Comparison Engine
 * AI-Powered Discovery Engine for Google Photos
 * Phase 3: Prompt Orchestrator, Gemini 1.5 Client & Comparison Engine
 */

import { WORKFLOWS } from '../config/constants.js';

export class PromptBuilder {
  /**
   * System Prompt Directives for each analytical workflow
   */
  static DIRECTIVES = {
    taxonomy: `SYSTEM INSTRUCTION:
Act as a Principal Product Manager for Google Photos Core Search. Analyze the provided VoC feedback dataset.
Identify exactly 3 distinct categories of personal photos that users struggle to retrieve using conventional keyword search.
EXCLUDE generic categories (e.g., 'vacations', 'birthdays', 'pets').
FOCUS strictly on edge-cases such as 'Incidental Screenshots', 'Situational/Aesthetic Vibe Photos', or 'Relative-Temporal Events'.

OUTPUT CONTRACT:
- Use strictly Markdown formatting.
- For each category, use H3 (###) for the category name.
- Use bullet points (-) for the formal analytical definition.
- Use Blockquotes (>) for the exact verbatim quote from the provided data as empirical evidence.
- Do NOT include conversational opening or closing statements. Output ONLY the structured analysis.`,

    cognitive_gap: `SYSTEM INSTRUCTION:
Act as a Principal Cognitive UX Researcher for Google Photos. Analyze the provided VoC feedback dataset to map the cognitive gap during failed photo searches.
Deconstruct what sensory, relational, emotional, or episodic anchors users consistently retain in working memory (e.g., weather, apparel color, companion, ambient setting) versus what rigid absolute metadata the current system demands (e.g., exact calendar dates, GPS coordinates, literal object labels).

OUTPUT CONTRACT:
- Output strictly a Markdown Table (T-Chart) with exactly 3 columns:
  | Retained Episodic Anchors (Human Recall) | Forgotten System Demands (Current Index Requirements) | Failure Mode / Search Breakdown |
- Ground every row directly in user behaviors demonstrated in the dataset.
- Do NOT include introductory text, conversational chatter, or concluding remarks.`,

    workarounds: `SYSTEM INSTRUCTION:
Act as a Staff Product Manager for Google Photos. Analyze the provided VoC dataset to identify the specific manual compensatory actions and brute-force workarounds users endure when search fails.
Name each distinct behavioral pattern with high-impact product terminology (e.g., 'The Person Pivot', 'Chronological Scrubbing', 'External App Trail', 'Multi-Keyword Permutation Roulette').
Assign an analytical 'Friction Score' (High, Medium, or Low) based on the cognitive tax, time loss, and frustration expressed.

OUTPUT CONTRACT:
- Format as a numbered list (1., 2., 3., 4.).
- Bold the name of each workaround.
- Explicitly state the friction score on the next line: "- **Friction Score**: High / Medium / Low".
- Provide a detailed definition explaining the exact sequence of user actions and cognitive friction.
- Output ONLY the numbered list.`,

    poa: `SYSTEM INSTRUCTION:
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
- Output ONLY the structured POAs and Comparison Matrix. Do NOT include conversational opening or closing chatter.`,
  };

  /**
   * Assemble a complete multi-shot prompt binding the LLM to strict system directives
   * and injecting the active serialized customer feedback corpus.
   * 
   * @param {string} workflowId - 'taxonomy' | 'cognitive_gap' | 'workarounds' | 'poa'
   * @param {string} serializedCorpusJson - Filtered JSON string of active feedback records
   * @returns {string} Assembled prompt string
   */
  static buildPrompt(workflowId, serializedCorpusJson) {
    const directive = this.DIRECTIVES[workflowId];
    if (!directive) {
      throw new Error(`Unknown workflow ID: '${workflowId}'. Must be one of: taxonomy, cognitive_gap, workarounds, poa`);
    }

    if (!serializedCorpusJson || serializedCorpusJson.trim() === '[]') {
      throw new Error('Cannot assemble prompt with an empty VoC corpus payload.');
    }

    return `${directive}

---

INPUT VOICE-OF-CUSTOMER (VoC) FEEDBACK DATASET:
\`\`\`json
${serializedCorpusJson}
\`\`\`

Strictly adhere to the output contract and ground all findings in the provided dataset. Begin your analysis now:`;
  }

  /**
   * Return the raw system directive for a given workflow
   * @param {string} workflowId
   * @returns {string}
   */
  static getDirective(workflowId) {
    return this.DIRECTIVES[workflowId] || '';
  }
}
