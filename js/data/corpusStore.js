/**
 * In-Memory Corpus Store & Filtering Engine
 * AI-Powered Discovery Engine for Google Photos
 * Phase 2: Ingestion Engine & Simulated VoC Corpus
 */

import { SEED_CORPUS } from './seedCorpus.js';
import { sanitizeFeedbackRecord, validateFeedbackRecord } from './schema.js';

/**
 * CorpusStore manages the active collection of user feedback records,
 * supporting multi-channel source filtering, dynamic count calculation,
 * and deterministic JSON serialization for LLM prompt injection.
 */
export class CorpusStore {
  /**
   * @param {import('./schema.js').UserFeedbackRecord[]} [initialCorpus]
   */
  constructor(initialCorpus = SEED_CORPUS) {
    /** @type {import('./schema.js').UserFeedbackRecord[]} */
    this.records = [...initialCorpus];
  }

  /**
   * Return all currently loaded records
   * @returns {import('./schema.js').UserFeedbackRecord[]}
   */
  getAllRecords() {
    return [...this.records];
  }

  /**
   * Retrieve a record by its unique ID
   * @param {string} id
   * @returns {import('./schema.js').UserFeedbackRecord | undefined}
   */
  getRecordById(id) {
    return this.records.find((r) => r.id === id);
  }

  /**
   * Filter active records based on selected source channels
   * @param {Record<string, boolean>} [sourceFilters] - Object mapping source names to boolean flags
   * @returns {import('./schema.js').UserFeedbackRecord[]}
   */
  getActiveRecords(sourceFilters) {
    if (!sourceFilters || Object.keys(sourceFilters).length === 0) {
      return [...this.records];
    }

    return this.records.filter((record) => {
      // If the source key is explicitly present in filters, return its boolean value; otherwise default to true
      return sourceFilters[record.source] !== false;
    });
  }

  /**
   * Get live record counts grouped by channel source
   * @returns {{ 'r/GooglePhotos': number, 'Play Store': number, 'App Store': number, 'Google Support Forum': number, total: number }}
   */
  getSourceCounts() {
    const counts = {
      'r/GooglePhotos': 0,
      'Play Store': 0,
      'App Store': 0,
      'Google Support Forum': 0,
      total: this.records.length,
    };

    this.records.forEach((record) => {
      if (counts[record.source] !== undefined) {
        counts[record.source]++;
      }
    });

    return counts;
  }

  /**
   * Calculate count of active records given active filters
   * @param {Record<string, boolean>} sourceFilters
   * @returns {number}
   */
  getActiveCount(sourceFilters) {
    return this.getActiveRecords(sourceFilters).length;
  }

  /**
   * Deterministically serialize records into a clean, compact JSON string for LLM prompt injection.
   * Strips out unnecessary spaces while preserving complete verbatim text and episodic metadata.
   * @param {import('./schema.js').UserFeedbackRecord[]} records
   * @returns {string} Clean JSON formatted string
   */
  serializeRecords(records) {
    if (!records || records.length === 0) {
      return '[]';
    }

    const sanitizedRecords = records.map((r) => ({
      id: r.id,
      source: r.source,
      type: r.type,
      content: r.content,
      metadata: {
        ...(r.metadata.rating ? { rating: r.metadata.rating } : {}),
        ...(r.metadata.device ? { device: r.metadata.device } : {}),
        ...(r.metadata.upvotes !== undefined ? { upvotes: r.metadata.upvotes } : {}),
        date: r.metadata.date,
        tags: r.metadata.tags || [],
      },
    }));

    return JSON.stringify(sanitizedRecords, null, 2);
  }

  /**
   * Add a new feedback record defensively
   * @param {any} rawRecord
   * @returns {{ success: boolean, record?: import('./schema.js').UserFeedbackRecord, errors?: string[] }}
   */
  addRecord(rawRecord) {
    const validation = validateFeedbackRecord(rawRecord);
    if (!validation.valid) {
      return { success: false, errors: validation.errors };
    }

    const sanitized = sanitizeFeedbackRecord(rawRecord);
    this.records.push(sanitized);
    return { success: true, record: sanitized };
  }

  /**
   * Reset the store to the default 7-record simulated seed corpus
   */
  resetToSeed() {
    this.records = [...SEED_CORPUS];
  }
}

/**
 * Singleton instance of CorpusStore pre-loaded with SEED_CORPUS
 */
export const defaultCorpusStore = new CorpusStore(SEED_CORPUS);
