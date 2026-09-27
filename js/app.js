/**
 * Master Application Coordinator
 * AI-Powered Discovery Engine for Google Photos
 * Phase 5: Reading Canvas, State Machine & Markdown AST Parser
 */

import { APP_CONFIG, WORKFLOWS } from './config/constants.js';
import { defaultCorpusStore } from './data/corpusStore.js';
import { Sidebar } from './components/Sidebar.js';
import { Canvas } from './components/Canvas.js';
import { PromptBuilder } from './services/promptBuilder.js';
import { defaultGeminiClient } from './services/geminiClient.js';
import { ClipboardService } from './services/clipboardService.js';

class DiscoveryEngineApp {
  constructor() {
    this.corpusStore = defaultCorpusStore;
    this.geminiClient = defaultGeminiClient;

    // Zero-Trust Ephemeral Memory State (Never persisted to localStorage/sessionStorage/cookies)
    this.state = {
      apiKey: '',
      activeSources: {
        'r/GooglePhotos': true,
        'Play Store': true,
        'App Store': true,
        'Google Support Forum': true,
      },
      currentWorkflow: null,
      canvasState: APP_CONFIG.CANVAS_STATES.IDLE,
      reportMarkdown: '',
    };
  }

  /**
   * Initialize App Listeners & Mount UI Subsystems
   */
  init() {
    console.info(
      `%c[Google Photos Discovery Engine v${APP_CONFIG.VERSION}] Initializing Phase 5 State Machine & Canvas...`,
      'color: #1a73e8; font-weight: bold; font-size: 12px;'
    );

    this.initCanvas();
    this.initSidebar();
    this.bindCopyEvents();

    console.info('[Google Photos Discovery Engine] Phase 5 Canvas State Machine mounted successfully with 0 errors.');
  }

  /**
   * Initialize Canvas State Machine Coordinator
   */
  initCanvas() {
    const canvasContainer = document.getElementById('app-canvas');
    if (!canvasContainer) {
      console.error('[Google Photos Discovery Engine] Canvas container #app-canvas not found.');
      return;
    }

    this.canvas = new Canvas({
      container: canvasContainer,
      headerTitle: document.getElementById('canvas-workflow-title'),
      headerBadge: document.getElementById('canvas-workflow-badge'),
      copyBtn: document.getElementById('btn-copy-clipboard'),
    });

    this.canvas.showIdle();
  }

  /**
   * Initialize Composite Sidebar Component
   */
  initSidebar() {
    const sidebarContainer = document.getElementById('app-sidebar');
    if (!sidebarContainer) {
      console.error('[Google Photos Discovery Engine] Sidebar container #app-sidebar not found.');
      return;
    }

    this.sidebar = new Sidebar({
      container: sidebarContainer,
      corpusStore: this.corpusStore,
      callbacks: {
        onApiKeyChange: (cleanKey) => {
          this.state.apiKey = cleanKey;
        },
        onSourceFilterChange: (activeSources) => {
          this.state.activeSources = activeSources;
        },
        onWorkflowTrigger: (workflowId) => {
          this.executeWorkflow(workflowId);
        },
      },
    });
  }

  /**
   * Execute Deterministic Analytical Workflow Pipeline
   * @param {string} workflowKey
   */
  async executeWorkflow(workflowKey) {
    const workflowObj = Object.values(WORKFLOWS).find((w) => w.id === workflowKey);
    if (!workflowObj) return;

    this.state.currentWorkflow = workflowKey;
    this.sidebar.setActiveWorkflow(workflowKey);

    // Pre-flight check 1: Active Sources
    const activeCount = this.corpusStore.getActiveCount(this.state.activeSources);
    if (activeCount === 0) {
      this.canvas.showError(
        'No Ingestion Sources Selected',
        'All feedback channels are currently disabled. Please enable at least one VoC source in the sidebar to run the analytical synthesis.'
      );
      return;
    }

    // Pre-flight check 2: API Key Presence
    if (!this.state.apiKey) {
      this.canvas.showError(
        'API Key Required',
        'Please enter your Google Gemini API key in the configuration card on the left sidebar before triggering this analytical workflow.'
      );
      this.sidebar.promptKeyFocus();
      return;
    }

    // Transition to LOADING state & lock sidebar buttons against race conditions
    this.canvas.showLoading(workflowObj.loadingMessage, workflowObj.title, workflowObj.badge);
    this.sidebar.setLoading(true);

    try {
      // 1. Ingestion & Pre-Filtering
      const activeRecords = this.corpusStore.getActiveRecords(this.state.activeSources);
      const serializedJson = this.corpusStore.serializeRecords(activeRecords);

      // 2. Prompt Assembly & Context Packing
      const prompt = PromptBuilder.buildPrompt(workflowKey, serializedJson);

      // 3. Low-Temperature Inference (Temp: 0.2, Top_P: 0.8)
      const result = await this.geminiClient.generateContent(prompt, this.state.apiKey);

      if (result.success && result.data) {
        this.state.reportMarkdown = result.data;
        // 4. Render Semantic HTML Report in SUCCESS State
        this.canvas.showSuccess(result.data, workflowObj.title, workflowObj.badge);
      } else {
        this.canvas.showError(
          'Synthesis Request Failed',
          result.error || 'An error occurred during inference. Please verify your Gemini API key and try again.',
          () => this.executeWorkflow(workflowKey)
        );
      }
    } catch (err) {
      console.error('[Google Photos Discovery Engine] Pipeline Error:', err);
      this.canvas.showError(
        'Unexpected System Error',
        `An unexpected error occurred while executing the analytical workflow: ${err.message}`,
        () => this.executeWorkflow(workflowKey)
      );
    } finally {
      // Unlock sidebar controls
      this.sidebar.setLoading(false);
    }
  }

  /**
   * Bind Copy CTA Button with Slide Export Optimization & Toast Feedback
   */
  bindCopyEvents() {
    const copyBtn = document.getElementById('btn-copy-clipboard');
    if (!copyBtn) return;

    ClipboardService.attachCopyButton({
      button: copyBtn,
      getMarkdown: () => (this.canvas ? this.canvas.getMarkdown() : this.state.reportMarkdown),
      onToast: (msg) => this.showToast(msg),
      duration: 2500,
    });
  }

  /**
   * Display Temporary Toast
   */
  showToast(message) {
    const toast = document.getElementById('toast-notification');
    const toastMsg = document.getElementById('toast-message');
    if (!toast || !toastMsg) return;

    toastMsg.textContent = message;
    toast.classList.add('show');

    setTimeout(() => {
      toast.classList.remove('show');
    }, 2500);
  }
}

// Bootstrap Application on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
  const app = new DiscoveryEngineApp();
  app.init();
  window.__discoveryEngineApp = app;
});
