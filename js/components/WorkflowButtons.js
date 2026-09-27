/**
 * Standardized Analytical Workflow Buttons Component
 * AI-Powered Discovery Engine for Google Photos
 * Phase 4: Left Control Sidebar & Trigger Subsystem
 */

import { WORKFLOWS } from '../config/constants.js';

export class WorkflowButtons {
  /**
   * @param {Object} options
   * @param {HTMLElement} options.container - DOM element to render into
   * @param {(workflowId: string) => void} [options.onWorkflowSelect] - Trigger callback
   */
  constructor({ container, onWorkflowSelect = null }) {
    this.container = container;
    this.onWorkflowSelect = onWorkflowSelect;
    this.activeWorkflowId = null;
    this.disabled = false;

    this.render();
    this.cacheDom();
    this.bindEvents();
  }

  render() {
    this.container.innerHTML = `
      <div class="sidebar-card-header">
        <h2 class="sidebar-card-title" id="workflows-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <circle cx="12" cy="12" r="10"></circle>
            <polygon points="10 8 16 12 10 16 10 8"></polygon>
          </svg>
          Analytical Workflows
        </h2>
      </div>
      <p class="sidebar-card-subtitle">Deterministic prompts • Beyond review summarization</p>

      <div class="workflows-group" id="workflows-group" role="group" aria-label="Standardized Analytical Workflows">
        <!-- Button 1: Taxonomy of Lost Photos -->
        <button type="button" class="workflow-card-btn" id="btn-workflow-taxonomy" data-workflow="taxonomy" aria-label="Workflow 1: Taxonomy of Lost Photos">
          <div class="workflow-card-top">
            <span class="workflow-number-tag">Workflow 01</span>
            <span class="workflow-pill workflow-pill-edge">Edge Cases</span>
          </div>
          <div class="workflow-card-title">Taxonomy of "Lost" Photos</div>
          <div class="workflow-card-desc">Categorizes high-friction retrieval edge-cases grounded in real user quotes.</div>
        </button>

        <!-- Button 2: Cognitive Gap Matrix -->
        <button type="button" class="workflow-card-btn" id="btn-workflow-cognitive-gap" data-workflow="cognitive_gap" aria-label="Workflow 2: Cognitive Gap Matrix">
          <div class="workflow-card-top">
            <span class="workflow-number-tag">Workflow 02</span>
            <span class="workflow-pill workflow-pill-chart">T-Chart</span>
          </div>
          <div class="workflow-card-title">Cognitive Gap Matrix</div>
          <div class="workflow-card-desc">Deconstructs episodic memory anchors vs. rigid system index demands.</div>
        </button>

        <!-- Button 3: Behavioral Workarounds -->
        <button type="button" class="workflow-card-btn" id="btn-workflow-workarounds" data-workflow="workarounds" aria-label="Workflow 3: Behavioral Workarounds">
          <div class="workflow-card-top">
            <span class="workflow-number-tag">Workflow 03</span>
            <span class="workflow-pill workflow-pill-friction">Friction Scores</span>
          </div>
          <div class="workflow-card-title">Behavioral Workarounds</div>
          <div class="workflow-card-desc">Maps manual compensatory actions with High/Medium/Low friction ratings.</div>
        </button>

        <!-- Button 4: Product Opportunity Synthesis -->
        <button type="button" class="workflow-card-btn" id="btn-workflow-poa" data-workflow="poa" aria-label="Workflow 4: Product Opportunity Synthesis">
          <div class="workflow-card-top">
            <span class="workflow-number-tag">Workflow 04</span>
            <span class="workflow-pill workflow-pill-poa">POAs & Matrix</span>
          </div>
          <div class="workflow-card-title">Product Opportunity Synthesis</div>
          <div class="workflow-card-desc">Synthesizes 2 POAs + mandatory Comparison and Trade-off Matrix.</div>
        </button>
      </div>
    `;
  }

  cacheDom() {
    this.buttons = this.container.querySelectorAll('.workflow-card-btn');
  }

  bindEvents() {
    this.buttons.forEach((btn) => {
      btn.addEventListener('click', () => {
        if (this.disabled) return;
        const workflowId = btn.dataset.workflow;
        this.setActiveWorkflow(workflowId);

        if (this.onWorkflowSelect) {
          this.onWorkflowSelect(workflowId);
        }
      });
    });
  }

  setActiveWorkflow(workflowId) {
    this.activeWorkflowId = workflowId;
    this.buttons.forEach((btn) => {
      if (btn.dataset.workflow === workflowId) {
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
      } else {
        btn.classList.remove('active');
        btn.setAttribute('aria-pressed', 'false');
      }
    });
  }

  getActiveWorkflow() {
    return this.activeWorkflowId;
  }

  /**
   * Disables/Enables all workflow buttons to eliminate rapid-clicking race conditions during active synthesis
   * @param {boolean} disabled
   */
  setDisabled(disabled) {
    this.disabled = disabled;
    this.buttons.forEach((btn) => {
      btn.disabled = disabled;
      if (disabled) {
        btn.setAttribute('aria-disabled', 'true');
      } else {
        btn.removeAttribute('aria-disabled');
      }
    });
  }
}
