/**
 * Application Constants & Model Configurations
 * AI-Powered Discovery Engine for Google Photos
 */

export const APP_CONFIG = {
  VERSION: '1.0.0',
  MODEL_NAME: 'gemini-flash-latest',
  GENERATION_CONFIG: {
    temperature: 0.2, // Locked for deterministic, reproducible synthesis
    topP: 0.8,
    topK: 40,
    maxOutputTokens: 2048,
  },
  CANVAS_STATES: {
    IDLE: 'IDLE',
    LOADING: 'LOADING',
    ERROR: 'ERROR',
    SUCCESS: 'SUCCESS',
  },
};

export const WORKFLOWS = {
  TAXONOMY: {
    id: 'taxonomy',
    buttonId: 'btn-workflow-taxonomy',
    badge: 'Edge Cases',
    title: 'Taxonomy of "Lost" Photos',
    desc: 'Categorizes high-friction retrieval edge-cases grounded in real user quotes.',
    loadingMessage: 'Analyzing VoC corpus for search failure edge-case taxonomy...',
  },
  COGNITIVE_GAP: {
    id: 'cognitive_gap',
    buttonId: 'btn-workflow-cognitive-gap',
    badge: 'T-Chart',
    title: 'Cognitive Gap Matrix',
    desc: 'Deconstructs episodic memory anchors vs. rigid system index demands.',
    loadingMessage: 'Mapping episodic human memory anchors against computer vision tags...',
  },
  WORKAROUNDS: {
    id: 'workarounds',
    buttonId: 'btn-workflow-workarounds',
    badge: 'Friction Scores',
    title: 'Behavioral Workarounds',
    desc: 'Maps manual compensatory actions with High/Medium/Low friction ratings.',
    loadingMessage: 'Extracting manual compensatory workarounds and friction ratings...',
  },
  POA: {
    id: 'poa',
    buttonId: 'btn-workflow-poa',
    badge: 'POAs & Matrix',
    title: 'Product Opportunity Synthesis',
    desc: 'Synthesizes 2 POAs + mandatory Comparison and Trade-off Matrix.',
    loadingMessage: 'Formulating strategic Product Opportunity Areas & Trade-off Matrix...',
  },
};

export const SOURCES = [
  { id: 'source-reddit', name: 'r/GooglePhotos', countId: 'count-reddit', defaultCount: 3 },
  { id: 'source-playstore', name: 'Google Play Store', countId: 'count-playstore', defaultCount: 1 },
  { id: 'source-appstore', name: 'Apple App Store', countId: 'count-appstore', defaultCount: 1 },
  { id: 'source-support', name: 'Google Support Forum', countId: 'count-support', defaultCount: 2 },
];
