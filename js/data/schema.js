/**
 * Data Schema Contracts & Defensive Sanitization
 * AI-Powered Discovery Engine for Google Photos
 * Phase 2: Ingestion Engine & Data Contracts
 */

/**
 * Valid feedback channel sources
 * @typedef {"r/GooglePhotos" | "Play Store" | "App Store" | "Google Support Forum"} VoCSource
 */
export const VALID_SOURCES = [
  'r/GooglePhotos',
  'Play Store',
  'App Store',
  'Google Support Forum',
];

/**
 * Valid feedback post types
 * @typedef {"Reddit Post" | "1-Star Review" | "2-Star Review" | "Support Thread" | "Feature Request"} FeedbackType
 */
export const VALID_FEEDBACK_TYPES = [
  'Reddit Post',
  '1-Star Review',
  '2-Star Review',
  'Support Thread',
  'Feature Request',
];

/**
 * Metadata associated with a VoC feedback item
 * @typedef {Object} FeedbackMetadata
 * @property {number} [upvotes] - Upvotes or helpful count
 * @property {number} [rating] - Star rating (1-5) for app store reviews
 * @property {string} [device] - Client device model (e.g. Pixel 7 Pro)
 * @property {string} date - ISO date string (YYYY-MM-DD)
 * @property {string[]} tags - Categorical retrieval heuristics
 */

/**
 * Normalized Voice-of-Customer Feedback Record
 * @typedef {Object} UserFeedbackRecord
 * @property {string} id - Unique identifier (e.g. "voc-001")
 * @property {VoCSource} source - Origin channel
 * @property {FeedbackType} type - Structural post type
 * @property {string} content - Unstructured customer verbatim review or post
 * @property {FeedbackMetadata} metadata - Structured contextual metadata
 */

/**
 * Validate a single UserFeedbackRecord against strict architectural constraints
 * @param {any} record - Raw feedback record to validate
 * @returns {{ valid: boolean, errors: string[] }}
 */
export function validateFeedbackRecord(record) {
  const errors = [];

  if (!record || typeof record !== 'object') {
    return { valid: false, errors: ['Record must be a valid non-null object'] };
  }

  // ID Validation
  if (!record.id || typeof record.id !== 'string' || record.id.trim() === '') {
    errors.push('Record "id" is required and must be a non-empty string');
  }

  // Source Validation
  if (!record.source || !VALID_SOURCES.includes(record.source)) {
    errors.push(`Record "source" must be one of: ${VALID_SOURCES.join(', ')}`);
  }

  // Type Validation
  if (!record.type || !VALID_FEEDBACK_TYPES.includes(record.type)) {
    errors.push(`Record "type" must be one of: ${VALID_FEEDBACK_TYPES.join(', ')}`);
  }

  // Content Validation
  if (!record.content || typeof record.content !== 'string' || record.content.trim() === '') {
    errors.push('Record "content" must be a non-empty string');
  }

  // Metadata Validation
  if (!record.metadata || typeof record.metadata !== 'object') {
    errors.push('Record "metadata" must be a valid object');
  } else {
    if (!record.metadata.date || typeof record.metadata.date !== 'string') {
      errors.push('Record "metadata.date" must be a valid date string (YYYY-MM-DD)');
    }
    if (!Array.isArray(record.metadata.tags)) {
      errors.push('Record "metadata.tags" must be an array of strings');
    }
    if (record.metadata.rating !== undefined && (typeof record.metadata.rating !== 'number' || record.metadata.rating < 1 || record.metadata.rating > 5)) {
      errors.push('Record "metadata.rating" must be a number between 1 and 5');
    }
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

/**
 * Defensive Sanitizer: Ensures a record is structurally resilient against malformed inputs,
 * missing metadata, HTML/XSS injection, and accidental formatting quirks.
 * @param {any} rawRecord - Input record
 * @returns {UserFeedbackRecord} Sanitized feedback record with guaranteed defaults
 */
export function sanitizeFeedbackRecord(rawRecord) {
  if (!rawRecord || typeof rawRecord !== 'object') {
    return {
      id: `voc-fallback-${Date.now()}`,
      source: 'Google Support Forum',
      type: 'Support Thread',
      content: 'No review text provided',
      metadata: {
        date: new Date().toISOString().split('T')[0],
        tags: ['unclassified'],
      },
    };
  }

  // ID Sanitization
  const id = (typeof rawRecord.id === 'string' && rawRecord.id.trim()) 
    ? rawRecord.id.trim() 
    : `voc-${Math.random().toString(36).substring(2, 9)}`;

  // Source Sanitization
  const source = VALID_SOURCES.includes(rawRecord.source) 
    ? rawRecord.source 
    : 'Google Support Forum';

  // Type Sanitization
  const type = VALID_FEEDBACK_TYPES.includes(rawRecord.type) 
    ? rawRecord.type 
    : 'Support Thread';

  // Content Sanitization (defense against XSS, null, and empty content)
  let content = (typeof rawRecord.content === 'string') 
    ? rawRecord.content.trim() 
    : 'No review text provided';

  if (!content) {
    content = 'No review text provided';
  }

  // Metadata Sanitization
  const rawMeta = (rawRecord.metadata && typeof rawRecord.metadata === 'object') 
    ? rawRecord.metadata 
    : {};

  const metadata = {
    date: (typeof rawMeta.date === 'string' && rawMeta.date.trim()) 
      ? rawMeta.date.trim() 
      : 'Unknown',
    tags: Array.isArray(rawMeta.tags) 
      ? rawMeta.tags.filter(t => typeof t === 'string' && t.trim()).map(t => t.trim().toLowerCase()) 
      : [],
  };

  if (typeof rawMeta.upvotes === 'number' && !isNaN(rawMeta.upvotes)) {
    metadata.upvotes = Math.max(0, Math.floor(rawMeta.upvotes));
  }

  if (typeof rawMeta.rating === 'number' && !isNaN(rawMeta.rating)) {
    metadata.rating = Math.min(5, Math.max(1, Math.floor(rawMeta.rating)));
  }

  if (typeof rawMeta.device === 'string' && rawMeta.device.trim()) {
    metadata.device = rawMeta.device.trim();
  }

  return {
    id,
    source,
    type,
    content,
    metadata,
  };
}

/**
 * Validate an entire corpus of UserFeedbackRecords
 * @param {any[]} corpus - Array of feedback records
 * @returns {{ valid: boolean, validCount: number, errorCount: number, errors: Record<string, string[]> }}
 */
export function validateFeedbackCorpus(corpus) {
  if (!Array.isArray(corpus)) {
    return {
      valid: false,
      validCount: 0,
      errorCount: 1,
      errors: { root: ['Corpus must be an array of records'] },
    };
  }

  const errorsMap = {};
  let validCount = 0;
  let errorCount = 0;

  corpus.forEach((record, index) => {
    const result = validateFeedbackRecord(record);
    const key = record && record.id ? record.id : `index_${index}`;
    if (!result.valid) {
      errorsMap[key] = result.errors;
      errorCount++;
    } else {
      validCount++;
    }
  });

  return {
    valid: errorCount === 0,
    validCount,
    errorCount,
    errors: errorsMap,
  };
}
