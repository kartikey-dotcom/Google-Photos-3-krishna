# Phase-Wise Implementation Plan: AI-Powered Discovery Engine for Google Photos

**Project Title:** AI-Powered Discovery Engine for Google Photos (Internal PM Intelligence Tool)  
**Target Organization:** Google LLC — Personal Search & Google Photos (`com.google.android.apps.photos`)  
**Target Users:** Google Photos Core Experience & Semantic Search Product Managers (PMs)  
**Domain:** Computational Photography, Semantic Image Retrieval & Personal Knowledge Management (PKM)  
**Document Version:** 1.0.0  
**Status:** Approved Engineering Roadmap  
**Reference Documents:**  
* [problemStatement.md](file:///c:/Users/DELL/OneDrive/Desktop/Krishna/Google%20Photos%203/Google%20photos%20AI%20discovery%20engine/problemStatement.md)  
* [architecture.md](file:///c:/Users/DELL/OneDrive/Desktop/Krishna/Google%20Photos%203/Google%20photos%20AI%20discovery%20engine/architecture.md)  

---

## 1. Executive Implementation Overview & Scope Discipline

This document outlines the **7-Phase Engineering Execution Plan** for building, testing, and hardening the **AI-Powered Discovery Engine for Google Photos**.

The system ingests, normalizes, and synthesizes unstructured multi-channel customer feedback and conversations at scale across **Reddit (`r/GooglePhotos`)**, **Google Play Store**, **Apple App Store**, and **Google Support Forums** to deconstruct **human memory retrieval failures** and bridge the **Semantic-Episodic Gap**.

### Core Engineering Directives:
1. **Beyond Summarization & Sentiment Analysis**: The engine explicitly bypasses naive sentiment scores (e.g., *"2.8/5 stars"*) and generic text summaries. It dissects conversations to categorize failure mechanics and compare candidate opportunity areas.
2. **Deterministic Non-Chatbot Pipeline**: No conversational chatbots or free-form chat inputs. 4 standardized analytical workflow triggers execute structured multi-shot prompts against active feedback data.
3. **Real-User Evidence Grounding**: Every failure taxonomy, cognitive gap, and strategic recommendation is anchored by direct verbatim citations from real user feedback.
4. **Zero-Trust Memory Lifecycle**: The user's Gemini API key is maintained strictly in runtime memory, never written to disk, local storage, or telemetry logs.

```mermaid
gantt
    title Google Photos VoC Discovery Engine — Phased Implementation Roadmap
    dateFormat  X
    axisFormat Phase %d
    section Core Infrastructure
    Phase 1: Project Setup, Design Tokens & 30/70 Layout :p1, 0, 1
    Phase 2: Types, Ingestion Engine & Simulated Corpus   :p2, 1, 2
    section LLM & Logic
    Phase 3: Prompt Orchestrator & Gemini 1.5 Client     :p3, 2, 3
    section UI Components
    Phase 4: Left Control Sidebar & Source Toggles       :p4, 3, 4
    Phase 5: Canvas State Machine & Markdown AST Parser  :p5, 4, 5
    section Export & Hardening
    Phase 6: Clipboard Service & Slide Export Utility    :p6, 5, 6
    Phase 7: End-to-End QA, Prompt Verification & Audit  :p7, 6, 7
```

---

## 2. Detailed Phase-by-Phase Implementation Specifications

```
Target File Architecture:
/
├── index.html                           # Semantic HTML5 desktop shell
├── css/
│   ├── tokens.css                       # Google Material 3 design tokens
│   └── main.css                         # Layout rules, states, and typography
└── js/
    ├── app.js                           # Master application coordinator
    ├── components/                      # Modular UI components
    │   ├── Header.js                    # Pinwheel logo & model status badge
    │   ├── Sidebar.js                   # Composite left control pane
    │   ├── ApiKeyCard.js                # Masked key input with eye toggle
    │   ├── SourceSelector.js            # Multi-channel source checkboxes
    │   ├── WorkflowButtons.js           # 4 analytical trigger buttons
    │   ├── Canvas.js                    # Main reading pane & state machine manager
    │   └── LoadingSkeleton.js           # Pulsing shimmer placeholder animation
    ├── config/
    │   └── constants.js                 # Workflows & model parameter contracts
    ├── data/
    │   ├── schema.js                    # JSDoc type contracts & defensive validation
    │   ├── seedCorpus.js                # 7 multi-channel VoC seed records
    │   └── corpusStore.js               # Reactive filtering & serialization store
    └── services/
        ├── geminiClient.js              # Low-temperature Gemini 1.5 REST client
        ├── markdownRenderer.js          # AST parser for tables, blockquotes, headers
        ├── promptBuilder.js             # Multi-shot prompt & comparison assembler
        └── clipboardService.js          # 1-click clipboard copy with toast feedback
```

---

### Phase 1: Project Foundation, Google Material Tokens & 30/70 Layout Shell

**Objective:** Establish the modular project directory structure, configure Google Material 3 design tokens, and build the desktop-first 30/70 layout shell.

#### Detailed Engineering Tasks:
- [ ] **1.1 Directory Scaffolding & Configuration:**
  - Create standard modular directory structure (`css/`, `js/components/`, `js/config/`, `js/data/`, `js/services/`).
  - Create `index.html` with semantic HTML5 containers and descriptive element IDs.
- [ ] **1.2 Google Material 3 Design Tokens (`css/tokens.css`):**
  - **Brand Colors**: `#1a73e8` (Google Blue), `#ea4335` (Google Red), `#fbbc04` (Google Yellow), `#34a853` (Google Green).
  - **Surface Colors**: Pure white `#ffffff` (Canvas), `#f8f9fa` (Sidebar/Cards), `#f1f3f4` (Input background), `#dadce0` (Borders).
  - **Typography Scale**: Google Sans / Inter for headings, Roboto for body copy, Roboto Mono for metadata tags. Line height: `1.65`.
  - **Elevation Shadows**: Level 1 (`0 1px 2px rgba(60,64,67,0.3)`), Level 2 (`0 1px 3px rgba(60,64,67,0.3), 0 4px 8px rgba(60,64,67,0.15)`).
- [ ] **1.3 Master Desktop 30/70 Shell (`css/main.css` & `index.html`):**
  - **Top Navigation Bar (Height: `64px`)**:
    - Authentic Google Photos 4-color pinwheel SVG logo.
    - Application title: *"Google Photos Memory Retrieval Intelligence Engine"*.
    - Badges: `Core PM Tool v1.0` (Slate chip) and `Gemini 1.5 Flash (Temp: 0.2)` (Google Blue chip).
  - **Left Sidebar (Width: `30%`, min `320px`, max `400px`)**:
    - Sticky scrolling container housing API configuration, data source filters, and workflow trigger buttons.
  - **Main Canvas (Width: `70%`, min `680px`, max container `920px`)**:
    - Reading pane container with fixed header bar (workflow title and clipboard CTA) and reactive content viewport.

#### Phase 1 Verification Milestone:
* Clean desktop 30/70 split loads without layout shifts or console errors. Verified via browser test.

---

### Phase 2: Ingestion Engine, Data Schema & Simulated VoC Corpus

**Objective:** Define the feedback schema, curate a 7-record simulated multi-channel feedback dataset capturing real retrieval breakdowns, and build a reactive in-memory corpus store.

#### Detailed Engineering Tasks:
- [ ] **2.1 Type Contracts & Defensive Validation (`js/data/schema.js`):**
  - Define JSDoc / TypeScript contracts for `UserFeedbackRecord`:
    ```typescript
    interface UserFeedbackRecord {
      id: string;
      source: "r/GooglePhotos" | "Play Store" | "App Store" | "Google Support Forum";
      type: "Reddit Post" | "1-Star Review" | "2-Star Review" | "Support Thread" | "Feature Request";
      content: string;
      metadata: {
        upvotes?: number;
        rating?: number;
        device?: string;
        date: string;
        tags: string[];
      };
    }
    ```
  - Implement `validateFeedbackRecord(record)` and `sanitizeFeedbackRecord(record)` to guarantee defensive fallbacks for missing metadata.
- [ ] **2.2 Multi-Channel Seed Corpus (`js/data/seedCorpus.js`):**
  - Curate 7 rich, realistic feedback records reflecting genuine human episodic retrieval breakdowns:
    1. **`voc-001` (Reddit)**: Trip to Rome, searching *"pasta"* returns recipe screenshots; retained cue: raining and wearing red jacket.
    2. **`voc-002` (Play Store)**: Pixel 7 user searching for dog; returns 400 generic dog photos instead of specific posture (*"sleeping on messy desk"*).
    3. **`voc-003` (Google Support)**: Concert tickets/receipts pollution; searching *"concert"* surfaces 200 Spotify screenshots.
    4. **`voc-004` (Reddit)**: Tire pressure sticker photo; user forced to cross-reference WhatsApp chat history before date scrubbing.
    5. **`voc-005` (App Store)**: iPhone 15 user recalling purple haze sunset in Greece; search returns 1,200 generic sunsets.
    6. **`voc-006` (Reddit)**: Web meme vs. real cat photo pollution; mixing saved web media into personal life archive.
    7. **`voc-007` (Google Support)**: Baby in green armchair; mother spends 20 minutes scrubbing timeline year by year.
- [ ] **2.3 In-Memory Corpus Store (`js/data/corpusStore.js`):**
  - `getActiveRecords(filters)`: Dynamically returns filtered subset based on active checkboxes.
  - `serializeRecords(records)`: Formats records into clean JSON payload for LLM prompt injection.
  - `getSourceCounts()`: Provides live counts per channel for UI badges.

#### Phase 2 Verification Milestone:
* Unit test validates 100% schema compliance. Toggling sources updates filtered JSON output accurately.

---

### Phase 3: Prompt Orchestrator, Gemini 1.5 Client & Comparison Engine

**Objective:** Construct the deterministic multi-shot prompt assembly pipeline and create a resilient Google Gemini REST API client bound to strict parameter envelopes.

#### Detailed Engineering Tasks:
- [ ] **3.1 Multi-Shot Prompt Assembler (`js/services/promptBuilder.js`):**
  - Implement system prompt contracts for all 4 workflows:
    - **Workflow 1 (`taxonomy`)**: Act as Principal PM; categorize 3 distinct edge-cases; exclude generic categories; output `###` headers, `-` bullet definitions, `>` blockquotes citing real user evidence.
    - **Workflow 2 (`cognitive_gap`)**: Act as Principal Cognitive UX Researcher; map sensory recall vs. rigid system demands; output strictly a 3-column Markdown T-Chart comparing *Retained Episodic Anchors* vs. *Forgotten System Demands* vs. *Failure Mode*.
    - **Workflow 3 (`workarounds`)**: Act as Staff PM; identify brute-force behaviors (Chronological Scrubbing, Person Pivot, Social Audit, etc.); output numbered list with bold names and `Friction Score: High/Medium/Low`.
    - **Workflow 4 (`poa`)**: Act as VP of Product; generate 2 POAs with `### Problem Space`, `### Proposed AI Solution`, and `### Hypothesis to Test`. Immediately following the 2 POAs, append a **"Comparison / Trade-off Matrix"** Markdown table comparing POA 1 vs POA 2 across: (1) Specific Retrieval Problems Solved, (2) User Impact, and (3) Implementation Effort.
  - Inject active filtered corpus JSON directly into prompt instructions.
- [ ] **3.2 Resilient Gemini REST Client (`js/services/geminiClient.js`):**
  - Direct HTTPS client calling Google AI Studio REST endpoint:
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}`
  - Request configuration strictly bound to:
    ```json
    {
      "contents": [{ "parts": [{ "text": assembledPrompt }] }],
      "generationConfig": {
        "temperature": 0.2,
        "topP": 0.8,
        "topK": 40,
        "maxOutputTokens": 2048
      }
    }
    ```
  - Diagnostic error interceptors:
    - `400`: Invalid request payload or parameter format.
    - `401 / 403`: Unauthorized or revoked API key.
    - `429`: Quota exhaustion warning with 30s backoff cooldown guidance.
    - `500 / 503`: Temporary Google AI Studio service interruption.
    - Offline / Network error: Catch fetch drops and inform of network disconnection.

#### Phase 3 Verification Milestone:
* Automated contract tests assert that all 4 prompts contain exact system instructions and parameter bounds.

---

### Phase 4: Left Control Sidebar & Trigger Subsystem

**Objective:** Implement the 30% control panel providing secure API key entry, reactive source filtering, and deterministic workflow triggers.

#### Detailed Engineering Tasks:
- [ ] **4.1 API Key Configuration Card (`js/components/ApiKeyCard.js`):**
  - Masked input field (`type="password"`) preventing accidental screen-share leakage during PM discovery reviews.
  - Interactive visibility toggle button with responsive SVG icon swapping.
  - Key sanitization pipeline: Strips leading/trailing whitespace, newlines, and single/double quotes resulting from copying keys from Docs/Slack.
  - In-memory status badge: Transitions from gray *"No Key Entered (Memory Only)"* to green *"Key Configured (In-Memory Only)"*.
- [ ] **4.2 Data Source Selector Component (`js/components/SourceSelector.js`):**
  - Checkboxes for the 4 public channels:
    1. `[x] r/GooglePhotos` (Reddit)
    2. `[x] Google Play Store` (1-Star & 2-Star reviews)
    3. `[x] Apple App Store` (User feedback)
    4. `[x] Google Support Forum` (Community threads)
  - Dynamic corpus counter: Displays `"X of 7 Records"` updating on every checkbox change.
  - Empty corpus warning: When 0 checkboxes are selected, turns text red to prevent empty inferences.
- [ ] **4.3 Workflow Action Buttons (`js/components/WorkflowButtons.js`):**
  - 4 distinct trigger cards with titles, subtitle tooltips, and badges:
    - **Button 1**: `Taxonomy of "Lost" Photos` (`Edge Cases`)
    - **Button 2**: `Cognitive Gap Matrix` (`T-Chart`)
    - **Button 3**: `Behavioral Workarounds` (`Friction Scores`)
    - **Button 4**: `Product Opportunity Synthesis` (`POAs & Matrix`)
  - Active visual state: Google Blue outline and subtle tint.
  - Disabled lock: Buttons disable during active synthesis to eliminate rapid-clicking race conditions.
- [ ] **4.4 Composite Sidebar Controller (`js/components/Sidebar.js`):**
  - Coordinates child components and dispatches events to master application coordinator.

#### Phase 4 Verification Milestone:
* Toggling checkboxes recalculates corpus count dynamically. Entering key updates status indicator. Buttons trigger intended workflow payloads.

---

### Phase 5: Reading Canvas, State Machine & Markdown AST Parser

**Objective:** Implement the 70% reading pane with strict UI state transitions and an executive-grade Markdown AST renderer.

#### Detailed Engineering Tasks:
- [ ] **5.1 State Machine Controller (`js/components/Canvas.js`):**
  - Coordinates transitions between 4 explicit states:
    - **IDLE State**: Google Photos pinwheel icon, subtitle, and prompt to select a workflow.
    - **LOADING State**: Shimmering skeleton cards imitating headers, tables, and quotes with cycling micro-copy (*"Synthesizing unstructured user data..."*, *"Extracting cognitive retrieval heuristics..."*).
    - **ERROR State**: High-contrast Google Red alert banner (`#d93025`) with inline remediation guidance and a *"Retry Workflow"* action.
    - **SUCCESS State**: Displays formatted Markdown report with smooth fade-in transition.
- [ ] **5.2 Pulsing Shimmer Animation (`js/components/LoadingSkeleton.js`):**
  - Pure CSS keyframe shimmer wave across simulated header, paragraph, and table rows.
- [ ] **5.3 Markdown AST Renderer (`js/services/markdownRenderer.js`):**
  - Custom parser converting raw LLM Markdown into semantic HTML:
    - `###` headers: Google Sans / Inter with clean section margins.
    - Blockquotes (`>`): `4px solid #1a73e8` left accent border, light gray `#f8f9fa` background, italicized font.
    - Tables: Formatted with clean borders (`#dadce0`), gray header background (`#f1f3f4`), and alternating zebra striping.
    - Lists: Padded bullet points and bold title spans.

#### Phase 5 Verification Milestone:
* Canvas transitions seamlessly across IDLE, LOADING, ERROR, and SUCCESS states. Markdown output renders with executive typography.

---

### Phase 6: Slide Export, Clipboard Engine & Micro-Interactions

**Objective:** Provide 1-click export workflows allowing instant copying of formatted markdown reports into Google Slides, Docs, or PRDs.

#### Detailed Engineering Tasks:
- [ ] **6.1 One-Click Clipboard Service (`js/services/clipboardService.js`):**
  - Implements `navigator.clipboard.writeText()` to copy raw markdown.
  - Graceful fallback for older environments.
- [ ] **6.2 Copy CTA Button & Toast Feedback:**
  - Sticky header button: *"📋 Copy to Clipboard"*.
  - On click: Transitions instantaneously to *"✓ Copied for Slides!"* (Google Green `#188038`) for 2.5 seconds before resetting.
- [ ] **6.3 Plaintext Slide Paste Optimizer:**
  - Ensures tables, quotes, and bullet hierarchies paste cleanly into Google Docs and Google Slides text boxes without garbled characters.

#### Phase 6 Verification Milestone:
* Clicking copy puts full formatted report into system clipboard and displays green checkmark toast.

---

### Phase 7: End-to-End QA, Acceptance Checklist & Hardening

**Objective:** Execute rigorous cross-workflow validation, verify error resilience, and perform a zero-trust security audit.

#### Detailed Engineering Tasks:
- [ ] **7.1 Workflow 1 Validation (Taxonomy of Lost Photos):**
  - Verify 3 distinct non-generic categories generated with `###` headers.
  - Assert presence of `>` blockquote user evidence quotes.
- [ ] **7.2 Workflow 2 Validation (Cognitive Gap Matrix):**
  - Verify strictly a 3-column Markdown T-Chart comparing *Retained Episodic Anchors* vs *Forgotten System Demands* vs *Failure Mode*.
- [ ] **7.3 Workflow 3 Validation (Behavioral Workaround Mapping):**
  - Verify numbered list with bold names and explicit `Friction Score: High/Medium/Low`.
- [ ] **7.4 Workflow 4 Validation (Product Opportunity Synthesis & Trade-off Matrix):**
  - Verify 2 distinct POAs generated with `### Problem Space`, `### Proposed AI Solution`, and `### Hypothesis to Test` sections.
  - Assert the presence of the **Comparison / Trade-off Matrix** table at the bottom comparing POA 1 vs POA 2 across Specific Retrieval Problems Solved, User Impact, and Implementation Effort.
- [ ] **7.5 Real-User Evidence Citation Audit:**
  - Verify all outputs contain grounded references to real user feedback.
- [ ] **7.6 Zero-Trust Storage & Security Audit:**
  - Inspect codebase to confirm 0 occurrences of `localStorage`, `sessionStorage`, `document.cookie`, or `indexedDB`.
  - Confirm API key input is masked and cleared on page reload.

#### Phase 7 Verification Milestone:
* 100% test pass rate across all 4 workflows with zero conversational chatbot leakage and zero persistence vulnerabilities.

---

## 3. Engineering Acceptance Checklist

| Verification Gate | Expected Criteria | Test Method | Status |
|---|---|---|---|
| **Beyond Summarization** | Workflows extract failure mechanics and comparative POAs rather than sentiment scores | Output semantic audit | **Ready** |
| **Real-User Evidence** | Outputs include direct verbatim quotes (`> [Quote]`) citing specific user feedback | Blockquote citation check | **Ready** |
| **Zero-Chatbot Architecture** | No chat inputs, message histories, or conversational greetings | Visual & code inspection | **Ready** |
| **Deterministic Parameter Envelope** | `temperature: 0.2`, `topP: 0.8` hardcoded in API request | Network payload inspection | **Ready** |
| **Workflow 1 Output Syntax** | `###` category, `-` bullet definition, `>` blockquote quote | Markdown AST analysis | **Ready** |
| **Workflow 2 Output Syntax** | 3-column Markdown T-Chart Table | Table DOM element assertion | **Ready** |
| **Workflow 3 Output Syntax** | Numbered list with bold names and `Friction Score: [High/Med/Low]` | Regex pattern match | **Ready** |
| **Workflow 4 Output Syntax** | 2 POAs (Problem, Solution, Hypothesis) + Comparison/Trade-off Matrix table | Header & table structure audit | **Ready** |
| **API Key Ephemerality** | Key never written to `localStorage` or `sessionStorage` | DevTools storage audit | **Ready** |
| **UI State Machine** | Transitions smoothly between IDLE, LOADING, ERROR, SUCCESS | Functional UI test | **Ready** |
| **Export Action** | 1-click clipboard copy with visual feedback toast | Clipboard verification | **Ready** |
