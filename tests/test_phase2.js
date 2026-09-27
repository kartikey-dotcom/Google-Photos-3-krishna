/**
 * Phase 2 Automated Node.js Tests
 * Tests schema validation, seed corpus integrity, defensive sanitization,
 * source filtering, and JSON serialization.
 */

import {
  VALID_SOURCES,
  VALID_FEEDBACK_TYPES,
  validateFeedbackRecord,
  sanitizeFeedbackRecord,
  validateFeedbackCorpus,
} from '../js/data/schema.js';
import { SEED_CORPUS, RAW_SEED_CORPUS } from '../js/data/seedCorpus.js';
import { CorpusStore } from '../js/data/corpusStore.js';

function runTests() {
  console.log('Testing JS Seed Corpus Integrity...');
  if (SEED_CORPUS.length !== 7) {
    throw new Error(`Expected 7 seed records, found ${SEED_CORPUS.length}`);
  }

  const corpusValidation = validateFeedbackCorpus(SEED_CORPUS);
  if (!corpusValidation.valid) {
    throw new Error(`Seed corpus failed validation: ${JSON.stringify(corpusValidation.errors)}`);
  }
  console.log(`✓ All ${corpusValidation.validCount} records passed strict schema validation.`);

  console.log('Testing Defensive Sanitization...');
  const malformed = {
    id: '  voc-test-x  ',
    source: 'Invalid Forum',
    type: 'Unknown',
    content: null,
    metadata: { date: '2024-05-01' },
  };
  const sanitized = sanitizeFeedbackRecord(malformed);
  if (sanitized.id !== 'voc-test-x') throw new Error(`Expected id 'voc-test-x', got '${sanitized.id}'`);
  if (sanitized.source !== 'Google Support Forum') throw new Error(`Expected fallback source, got '${sanitized.source}'`);
  if (sanitized.content !== 'No review text provided') throw new Error(`Expected fallback content, got '${sanitized.content}'`);
  console.log('✓ Defensive sanitization correctly provided fallbacks.');

  console.log('Testing CorpusStore Source Filtering & Live Counts...');
  const store = new CorpusStore(SEED_CORPUS);
  const counts = store.getSourceCounts();
  if (counts['r/GooglePhotos'] !== 3 || counts['Play Store'] !== 1 || counts['App Store'] !== 1 || counts['Google Support Forum'] !== 2) {
    throw new Error(`Incorrect channel counts: ${JSON.stringify(counts)}`);
  }
  if (counts.total !== 7) throw new Error(`Total count mismatch: expected 7, got ${counts.total}`);

  // Filter test
  const activeSubset = store.getActiveRecords({
    'r/GooglePhotos': false,
    'Play Store': true,
    'App Store': true,
    'Google Support Forum': true,
  });
  if (activeSubset.length !== 4) {
    throw new Error(`Expected 4 active records after filtering out Reddit, got ${activeSubset.length}`);
  }

  // Serialization test
  const serialized = store.serializeRecords(activeSubset);
  const parsed = JSON.parse(serialized);
  if (parsed.length !== 4) {
    throw new Error(`Serialization failed, expected 4 parsed records, got ${parsed.length}`);
  }
  console.log('✓ CorpusStore filtering, counts, and serialization verified.');

  console.log('\n🎉 ALL JS PHASE 2 TESTS PASSED SUCCESSFULLY!');
}

runTests();
