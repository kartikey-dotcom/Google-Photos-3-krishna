/**
 * Main Reading Canvas & UI State Machine Coordinator
 * AI-Powered Discovery Engine for Google Photos
 * Phase 5: Reading Canvas, State Machine & Markdown AST Parser
 */

import { APP_CONFIG, WORKFLOWS } from '../config/constants.js';
import { MarkdownRenderer } from '../services/markdownRenderer.js';
import { LoadingSkeleton } from './LoadingSkeleton.js';

export class Canvas {
  /**
   * @param {Object} options
   * @param {HTMLElement} options.container - Root canvas element (#app-canvas)
   * @param {HTMLElement} [options.headerTitle] - Title element (#canvas-workflow-title)
   * @param {HTMLElement} [options.headerBadge] - Badge element (#canvas-workflow-badge)
   * @param {HTMLButtonElement} [options.copyBtn] - Copy CTA button (#btn-copy-clipboard)
   */
  constructor({ container, headerTitle, headerBadge, copyBtn }) {
    this.container = container;
    this.headerTitle = headerTitle || container.querySelector('#canvas-workflow-title');
    this.headerBadge = headerBadge || container.querySelector('#canvas-workflow-badge');
    this.copyBtn = copyBtn || container.querySelector('#btn-copy-clipboard');

    this.currentState = APP_CONFIG.CANVAS_STATES.IDLE;
    this.reportMarkdown = '';
    this.retryCallback = null;

    this.cacheDom();
    this.loadingSkeleton = new LoadingSkeleton({ container: this.loadingStateEl });
    this.bindEvents();
  }

  cacheDom() {
    this.idleStateEl = this.container.querySelector('#idle-state');
    this.loadingStateEl = this.container.querySelector('#loading-state');
    this.errorStateEl = this.container.querySelector('#error-state');
    this.errorTitleEl = this.container.querySelector('#error-title');
    this.errorBodyEl = this.container.querySelector('#error-body');
    this.btnRetryEl = this.container.querySelector('#btn-retry-workflow');
    this.reportStateEl = this.container.querySelector('#report-state');
  }

  bindEvents() {
    if (this.btnRetryEl) {
      this.btnRetryEl.addEventListener('click', () => {
        if (this.retryCallback) {
          this.retryCallback();
        }
      });
    }
  }

  /**
   * Transition to IDLE State
   */
  showIdle() {
    this.currentState = APP_CONFIG.CANVAS_STATES.IDLE;
    this.reportMarkdown = '';

    if (this.headerBadge) this.headerBadge.textContent = 'IDLE';
    if (this.headerTitle) this.headerTitle.textContent = 'Awaiting Workflow Selection';
    if (this.copyBtn) this.copyBtn.disabled = true;

    this.loadingSkeleton.stop();
    if (this.loadingStateEl) this.loadingStateEl.style.display = 'none';
    if (this.errorStateEl) this.errorStateEl.style.display = 'none';
    if (this.reportStateEl) this.reportStateEl.style.display = 'none';
    if (this.idleStateEl) this.idleStateEl.style.display = 'flex';
  }

  /**
   * Transition to LOADING State
   * @param {string} [loadingMessage]
   * @param {string} [workflowTitle]
   * @param {string} [workflowBadge]
   */
  showLoading(loadingMessage = null, workflowTitle = null, workflowBadge = null) {
    this.currentState = APP_CONFIG.CANVAS_STATES.LOADING;

    if (workflowBadge && this.headerBadge) this.headerBadge.textContent = workflowBadge;
    if (workflowTitle && this.headerTitle) this.headerTitle.textContent = workflowTitle;
    if (this.copyBtn) this.copyBtn.disabled = true;

    if (this.idleStateEl) this.idleStateEl.style.display = 'none';
    if (this.errorStateEl) this.errorStateEl.style.display = 'none';
    if (this.reportStateEl) this.reportStateEl.style.display = 'none';

    this.loadingSkeleton.start(loadingMessage);
  }

  /**
   * Transition to ERROR State with inline remediation guidance
   * @param {string} title - Diagnostic title
   * @param {string} message - Remediation message
   * @param {() => void} [onRetry] - Optional retry callback
   */
  showError(title, message, onRetry = null) {
    this.currentState = APP_CONFIG.CANVAS_STATES.ERROR;
    this.retryCallback = onRetry;

    this.loadingSkeleton.stop();
    if (this.idleStateEl) this.idleStateEl.style.display = 'none';
    if (this.loadingStateEl) this.loadingStateEl.style.display = 'none';
    if (this.reportStateEl) this.reportStateEl.style.display = 'none';

    if (this.errorTitleEl) this.errorTitleEl.textContent = title;
    if (this.errorBodyEl) this.errorBodyEl.textContent = message;

    if (this.btnRetryEl) {
      this.btnRetryEl.style.display = onRetry ? 'inline-block' : 'none';
    }

    if (this.errorStateEl) {
      this.errorStateEl.style.display = 'flex';
      this.errorStateEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    if (this.copyBtn) this.copyBtn.disabled = true;
  }

  /**
   * Transition to SUCCESS State and render executive Markdown report
   * @param {string} markdown - Synthesized LLM Markdown
   * @param {string} [workflowTitle]
   * @param {string} [workflowBadge]
   */
  showSuccess(markdown, workflowTitle = null, workflowBadge = null) {
    this.currentState = APP_CONFIG.CANVAS_STATES.SUCCESS;
    this.reportMarkdown = markdown;

    if (workflowBadge && this.headerBadge) this.headerBadge.textContent = workflowBadge;
    if (workflowTitle && this.headerTitle) this.headerTitle.textContent = workflowTitle;

    this.loadingSkeleton.stop();
    if (this.idleStateEl) this.idleStateEl.style.display = 'none';
    if (this.loadingStateEl) this.loadingStateEl.style.display = 'none';
    if (this.errorStateEl) this.errorStateEl.style.display = 'none';

    // Parse and render semantic HTML via MarkdownRenderer
    const parsedHtml = MarkdownRenderer.render(markdown);
    if (this.reportStateEl) {
      this.reportStateEl.innerHTML = parsedHtml;
      this.reportStateEl.style.display = 'block';
      this.reportStateEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Enable Copy to Clipboard CTA
    if (this.copyBtn) {
      this.copyBtn.disabled = false;
    }
  }

  getState() {
    return this.currentState;
  }

  getMarkdown() {
    return this.reportMarkdown;
  }
}
