/**
 * Master Composite Sidebar Controller
 * AI-Powered Discovery Engine for Google Photos
 * Phase 4: Left Control Sidebar & Trigger Subsystem
 */

import { ApiKeyCard } from './ApiKeyCard.js';
import { SourceSelector } from './SourceSelector.js';
import { WorkflowButtons } from './WorkflowButtons.js';
import { defaultCorpusStore } from '../data/corpusStore.js';

export class Sidebar {
  /**
   * @param {Object} options
   * @param {HTMLElement} options.container - Root aside element (#app-sidebar)
   * @param {import('../data/corpusStore.js').CorpusStore} [options.corpusStore]
   * @param {Object} [options.callbacks]
   * @param {(key: string) => void} [options.callbacks.onApiKeyChange]
   * @param {(activeSources: Record<string, boolean>) => void} [options.callbacks.onSourceFilterChange]
   * @param {(workflowId: string) => void} [options.callbacks.onWorkflowTrigger]
   */
  constructor({ container, corpusStore = defaultCorpusStore, callbacks = {} }) {
    this.container = container;
    this.corpusStore = corpusStore;
    this.callbacks = callbacks;

    this.initChildContainers();
    this.initComponents();
  }

  initChildContainers() {
    // If sections already exist in DOM, reuse them; otherwise create them
    let apiKeySection = this.container.querySelector('#api-key-section');
    if (!apiKeySection) {
      apiKeySection = document.createElement('section');
      apiKeySection.id = 'api-key-section';
      apiKeySection.className = 'sidebar-card';
      apiKeySection.setAttribute('aria-labelledby', 'api-key-title');
      this.container.appendChild(apiKeySection);
    }
    this.apiKeySection = apiKeySection;

    let sourceSection = this.container.querySelector('#source-selector-section');
    if (!sourceSection) {
      sourceSection = document.createElement('section');
      sourceSection.id = 'source-selector-section';
      sourceSection.className = 'sidebar-card';
      sourceSection.setAttribute('aria-labelledby', 'sources-title');
      this.container.appendChild(sourceSection);
    }
    this.sourceSection = sourceSection;

    let workflowSection = this.container.querySelector('#workflow-buttons-section');
    if (!workflowSection) {
      workflowSection = document.createElement('section');
      workflowSection.id = 'workflow-buttons-section';
      workflowSection.className = 'sidebar-card';
      workflowSection.setAttribute('aria-labelledby', 'workflows-title');
      this.container.appendChild(workflowSection);
    }
    this.workflowSection = workflowSection;
  }

  initComponents() {
    // 1. ApiKeyCard Component
    this.apiKeyCard = new ApiKeyCard({
      container: this.apiKeySection,
      onKeyChange: (key) => {
        if (this.callbacks.onApiKeyChange) {
          this.callbacks.onApiKeyChange(key);
        }
      },
    });

    // 2. SourceSelector Component
    this.sourceSelector = new SourceSelector({
      container: this.sourceSection,
      corpusStore: this.corpusStore,
      onSourcesChange: (sources) => {
        if (this.callbacks.onSourceFilterChange) {
          this.callbacks.onSourceFilterChange(sources);
        }
      },
    });

    // 3. WorkflowButtons Component
    this.workflowButtons = new WorkflowButtons({
      container: this.workflowSection,
      onWorkflowSelect: (workflowId) => {
        if (this.callbacks.onWorkflowTrigger) {
          this.callbacks.onWorkflowTrigger(workflowId);
        }
      },
    });
  }

  getKey() {
    return this.apiKeyCard.getKey();
  }

  setKey(key) {
    this.apiKeyCard.setKey(key);
  }

  promptKeyFocus() {
    this.apiKeyCard.focus();
  }

  getActiveSources() {
    return this.sourceSelector.getActiveSources();
  }

  getActiveCount() {
    return this.sourceSelector.getActiveCount();
  }

  getActiveWorkflow() {
    return this.workflowButtons.getActiveWorkflow();
  }

  setActiveWorkflow(workflowId) {
    this.workflowButtons.setActiveWorkflow(workflowId);
  }

  /**
   * Lock/Unlock sidebar controls during active inference to eliminate race conditions
   * @param {boolean} loading
   */
  setLoading(loading) {
    this.workflowButtons.setDisabled(loading);
    this.sourceSelector.setDisabled(loading);
  }
}
