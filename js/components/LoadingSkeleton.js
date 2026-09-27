/**
 * Loading Skeleton & Pulsing Shimmer Component
 * AI-Powered Discovery Engine for Google Photos
 * Phase 5: Reading Canvas, State Machine & Markdown AST Parser
 */

export class LoadingSkeleton {
  /**
   * @param {Object} options
   * @param {HTMLElement} options.container - DOM container (#loading-state)
   */
  constructor({ container }) {
    this.container = container;
    this.rotationTimer = null;
    this.messageIndex = 0;

    this.defaultMessages = [
      'Extracting behavioral retrieval heuristics from VoC feedback...',
      'Synthesizing multi-source customer conversations with Gemini 1.5 Flash...',
      'Deconstructing episodic memory retrieval breakdowns (The Semantic-Episodic Gap)...',
      'Formatting structured PM deliverable, T-Charts, and Trade-off Matrix...',
    ];

    this.render();
    this.cacheDom();
  }

  render() {
    this.container.innerHTML = `
      <div class="loading-header-banner" role="status" aria-live="polite">
        <div class="spinner-icon" aria-hidden="true"></div>
        <span class="loading-message-text" id="loading-status-text">
          Synthesizing multi-source VoC feedback with Gemini 1.5 Flash...
        </span>
      </div>

      <!-- Skeleton Card 1: Header, Text, and Verbatim Blockquote Shimmer -->
      <div class="skeleton-card" aria-hidden="true">
        <div class="skeleton-shimmer skeleton-title"></div>
        <div class="skeleton-shimmer skeleton-line"></div>
        <div class="skeleton-shimmer skeleton-line short"></div>
        <div class="skeleton-shimmer skeleton-quote"></div>
      </div>

      <!-- Skeleton Card 2: 3-Column T-Chart / Matrix Table Shimmer -->
      <div class="skeleton-card" aria-hidden="true">
        <div class="skeleton-shimmer skeleton-title" style="width: 40%;"></div>
        <div class="skeleton-shimmer skeleton-table"></div>
      </div>
    `;
  }

  cacheDom() {
    this.statusText = this.container.querySelector('#loading-status-text');
  }

  /**
   * Start skeleton shimmer animation and cycle dynamic status micro-copy
   * @param {string} [initialMessage]
   */
  start(initialMessage = null) {
    this.container.style.display = 'flex';
    this.messageIndex = 0;

    const firstMsg = initialMessage || this.defaultMessages[0];
    this.setMessage(firstMsg);

    if (this.rotationTimer) {
      clearInterval(this.rotationTimer);
    }

    this.rotationTimer = setInterval(() => {
      this.messageIndex = (this.messageIndex + 1) % this.defaultMessages.length;
      this.setMessage(this.defaultMessages[this.messageIndex]);
    }, 2500);
  }

  /**
   * Stop skeleton animation and clear rotation timer
   */
  stop() {
    if (this.rotationTimer) {
      clearInterval(this.rotationTimer);
      this.rotationTimer = null;
    }
    this.container.style.display = 'none';
  }

  /**
   * Update the displayed status message
   * @param {string} text
   */
  setMessage(text) {
    if (this.statusText) {
      this.statusText.textContent = text;
    }
  }
}
