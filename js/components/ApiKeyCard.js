/**
 * API Key Configuration Card Component
 * AI-Powered Discovery Engine for Google Photos
 * Phase 4: Left Control Sidebar & Trigger Subsystem
 */

export class ApiKeyCard {
  /**
   * @param {Object} options
   * @param {HTMLElement} options.container - DOM element to render into or bind
   * @param {string} [options.initialKey] - Initial in-memory key if any
   * @param {(key: string) => void} [options.onKeyChange] - Callback invoked when key changes
   */
  constructor({ container, initialKey = '', onKeyChange = null }) {
    this.container = container;
    this.onKeyChange = onKeyChange;
    this.key = '';
    this.isMasked = true;

    this.render();
    this.cacheDom();
    this.bindEvents();

    if (initialKey) {
      this.setKey(initialKey);
    }
  }

  render() {
    this.container.innerHTML = `
      <div class="sidebar-card-header">
        <h2 class="sidebar-card-title" id="api-key-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
          API Key Configuration
        </h2>
      </div>
      <p class="sidebar-card-subtitle">Zero-trust runtime memory lifecycle (never persisted)</p>

      <div class="api-key-input-wrapper">
        <input 
          type="password" 
          id="api-key-input" 
          class="api-key-input" 
          placeholder="Paste Google AI Studio Key (AIzaSy...)" 
          autocomplete="off" 
          spellcheck="false"
          aria-label="Google AI Studio Gemini API Key"
        />
        <button 
          type="button" 
          id="toggle-key-visibility-btn" 
          class="api-key-toggle-btn" 
          title="Toggle API Key Visibility" 
          aria-label="Toggle API Key Visibility"
        >
          <svg id="eye-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
          </svg>
        </button>
      </div>

      <div class="api-key-status-row">
        <div class="key-status-indicator disconnected" id="api-key-status">
          <span class="status-dot" style="background-color: #9aa0a6;"></span>
          <span id="api-key-status-label">No Key Entered (Memory Only)</span>
        </div>
        <span class="zero-trust-note" title="Held in JS memory only, never written to disk or storage">
          🔒 In-Memory Only
        </span>
      </div>
    `;
  }

  cacheDom() {
    this.input = this.container.querySelector('#api-key-input');
    this.toggleBtn = this.container.querySelector('#toggle-key-visibility-btn');
    this.eyeIcon = this.container.querySelector('#eye-icon');
    this.statusContainer = this.container.querySelector('#api-key-status');
    this.statusLabel = this.container.querySelector('#api-key-status-label');
    this.statusDot = this.container.querySelector('.status-dot');
  }

  bindEvents() {
    this.input.addEventListener('input', (e) => {
      this.handleInputChange(e.target.value);
    });

    this.toggleBtn.addEventListener('click', () => {
      this.toggleVisibility();
    });
  }

  /**
   * Sanitizes input key: trims spaces, tabs, newlines, and stray double/single quotes
   * @param {string} rawKey
   * @returns {string} Sanitized key
   */
  sanitizeKey(rawKey) {
    if (typeof rawKey !== 'string') return '';
    return rawKey.trim().replace(/^["']|["']$/g, '');
  }

  handleInputChange(val) {
    const cleanKey = this.sanitizeKey(val);
    this.key = cleanKey;
    this.updateStatus(Boolean(cleanKey));

    if (this.onKeyChange) {
      this.onKeyChange(cleanKey);
    }
  }

  updateStatus(hasKey) {
    if (hasKey) {
      this.statusContainer.className = 'key-status-indicator connected';
      this.statusDot.style.backgroundColor = '#34a853';
      this.statusLabel.textContent = 'Key Configured (In-Memory Only)';
    } else {
      this.statusContainer.className = 'key-status-indicator disconnected';
      this.statusDot.style.backgroundColor = '#9aa0a6';
      this.statusLabel.textContent = 'No Key Entered (Memory Only)';
    }
  }

  toggleVisibility() {
    this.isMasked = !this.isMasked;
    this.input.type = this.isMasked ? 'password' : 'text';

    if (this.isMasked) {
      this.eyeIcon.innerHTML = `
        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
        <circle cx="12" cy="12" r="3"></circle>
      `;
      this.toggleBtn.setAttribute('title', 'Show API Key');
    } else {
      this.eyeIcon.innerHTML = `
        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
        <line x1="1" y1="1" x2="23" y2="23"></line>
      `;
      this.toggleBtn.setAttribute('title', 'Hide API Key');
    }
  }

  getKey() {
    return this.key;
  }

  setKey(key) {
    const cleanKey = this.sanitizeKey(key);
    this.key = cleanKey;
    this.input.value = cleanKey;
    this.updateStatus(Boolean(cleanKey));
    if (this.onKeyChange) {
      this.onKeyChange(cleanKey);
    }
  }

  focus() {
    this.input.focus();
    this.input.classList.add('pulse-focus');
    setTimeout(() => this.input.classList.remove('pulse-focus'), 1000);
  }
}
