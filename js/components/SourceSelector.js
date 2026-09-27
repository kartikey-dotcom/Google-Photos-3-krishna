/**
 * Data Source Selector Component
 * AI-Powered Discovery Engine for Google Photos
 * Phase 4: Left Control Sidebar & Trigger Subsystem
 */

import { SOURCES } from '../config/constants.js';
import { defaultCorpusStore } from '../data/corpusStore.js';

export class SourceSelector {
  /**
   * @param {Object} options
   * @param {HTMLElement} options.container - DOM element to render into
   * @param {import('../data/corpusStore.js').CorpusStore} [options.corpusStore]
   * @param {(activeSources: Record<string, boolean>) => void} [options.onSourcesChange]
   */
  constructor({ container, corpusStore = defaultCorpusStore, onSourcesChange = null }) {
    this.container = container;
    this.corpusStore = corpusStore;
    this.onSourcesChange = onSourcesChange;

    this.activeSources = {
      'r/GooglePhotos': true,
      'Play Store': true,
      'App Store': true,
      'Google Support Forum': true,
    };

    this.render();
    this.cacheDom();
    this.bindEvents();
    this.updateCounterBadge();
  }

  render() {
    const counts = this.corpusStore.getSourceCounts();

    this.container.innerHTML = `
      <div class="sidebar-card-header">
        <h2 class="sidebar-card-title" id="sources-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon>
          </svg>
          Corpus Source Filter
        </h2>
        <span class="badge-chip badge-chip-blue" id="corpus-count-badge">
          7 of 7 Records
        </span>
      </div>
      <p class="sidebar-card-subtitle">Active multi-channel customer conversations</p>

      <div class="source-selector-list" id="source-checkbox-list">
        <label class="source-checkbox-item" for="source-reddit">
          <div class="source-checkbox-left">
            <input type="checkbox" id="source-reddit" class="source-checkbox-input" data-source="r/GooglePhotos" checked />
            <div class="source-label">
              <span>r/GooglePhotos</span>
              <span class="source-meta-tag">Reddit</span>
            </div>
          </div>
          <span class="source-count-pill" id="count-reddit">${counts['r/GooglePhotos'] || 3}</span>
        </label>

        <label class="source-checkbox-item" for="source-playstore">
          <div class="source-checkbox-left">
            <input type="checkbox" id="source-playstore" class="source-checkbox-input" data-source="Play Store" checked />
            <div class="source-label">
              <span>Google Play Store</span>
              <span class="source-meta-tag">Reviews</span>
            </div>
          </div>
          <span class="source-count-pill" id="count-playstore">${counts['Play Store'] || 1}</span>
        </label>

        <label class="source-checkbox-item" for="source-appstore">
          <div class="source-checkbox-left">
            <input type="checkbox" id="source-appstore" class="source-checkbox-input" data-source="App Store" checked />
            <div class="source-label">
              <span>Apple App Store</span>
              <span class="source-meta-tag">Reviews</span>
            </div>
          </div>
          <span class="source-count-pill" id="count-appstore">${counts['App Store'] || 1}</span>
        </label>

        <label class="source-checkbox-item" for="source-support">
          <div class="source-checkbox-left">
            <input type="checkbox" id="source-support" class="source-checkbox-input" data-source="Google Support Forum" checked />
            <div class="source-label">
              <span>Google Support Community</span>
              <span class="source-meta-tag">Forums</span>
            </div>
          </div>
          <span class="source-count-pill" id="count-support">${counts['Google Support Forum'] || 2}</span>
        </label>
      </div>
    `;
  }

  cacheDom() {
    this.badge = this.container.querySelector('#corpus-count-badge');
    this.checkboxes = this.container.querySelectorAll('.source-checkbox-input');
  }

  bindEvents() {
    this.checkboxes.forEach((checkbox) => {
      checkbox.addEventListener('change', (e) => {
        const source = e.target.dataset.source;
        if (source) {
          this.activeSources[source] = e.target.checked;
        }
        this.updateCounterBadge();

        if (this.onSourcesChange) {
          this.onSourcesChange({ ...this.activeSources });
        }
      });
    });
  }

  updateCounterBadge() {
    const activeCount = this.corpusStore.getActiveCount(this.activeSources);
    const totalCount = this.corpusStore.getAllRecords().length;

    this.badge.textContent = `${activeCount} of ${totalCount} Records`;

    if (activeCount === 0) {
      this.badge.className = 'badge-chip';
      this.badge.style.backgroundColor = '#fce8e6';
      this.badge.style.color = '#c5221f';
      this.badge.style.borderColor = '#fad2cf';
      this.badge.setAttribute('title', 'Warning: 0 sources selected. Select at least 1 source.');
    } else {
      this.badge.className = 'badge-chip badge-chip-blue';
      this.badge.style.backgroundColor = '';
      this.badge.style.color = '';
      this.badge.style.borderColor = '';
      this.badge.setAttribute('title', `${activeCount} customer feedback records active`);
    }
  }

  getActiveSources() {
    return { ...this.activeSources };
  }

  getActiveCount() {
    return this.corpusStore.getActiveCount(this.activeSources);
  }

  setDisabled(disabled) {
    this.checkboxes.forEach((cb) => {
      cb.disabled = disabled;
    });
  }
}
