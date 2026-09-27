/**
 * Multi-Channel Simulated VoC Seed Corpus
 * AI-Powered Discovery Engine for Google Photos
 * Phase 2: Ingestion Engine & Simulated VoC Corpus
 * 
 * Captures authentic human memory retrieval failures & the Semantic-Episodic Gap
 * across Reddit (r/GooglePhotos), Play Store, App Store, and Google Support Forums.
 */

import { sanitizeFeedbackRecord } from './schema.js';

/**
 * Raw Seed Corpus Records
 * @type {import('./schema.js').UserFeedbackRecord[]}
 */
export const RAW_SEED_CORPUS = [
  {
    id: 'voc-001',
    source: 'r/GooglePhotos',
    type: 'Reddit Post',
    content: "I'm trying to find a photo of a specific pasta dish from my Rome trip. Searching 'pasta' gives me screenshots of recipes. I can't remember the exact date, I just know it was raining and I was wearing a red jacket. I gave up after scrolling for 10 minutes.",
    metadata: {
      upvotes: 45,
      date: '2023-11-04',
      tags: ['search_failure', 'screenshots', 'travel', 'episodic_weather'],
    },
  },
  {
    id: 'voc-002',
    source: 'Play Store',
    type: '1-Star Review',
    content: "Search is useless now. If I don't know the exact date, I can't find anything. I try searching for my dog, but it shows every dog photo instead of the specific one where he's sleeping on my messy desk.",
    metadata: {
      rating: 1,
      device: 'Pixel 7 Pro',
      date: '2024-01-15',
      tags: ['pets', 'context_clutter', 'posture_ambiguity'],
    },
  },
  {
    id: 'voc-003',
    source: 'Google Support Forum',
    type: 'Support Thread',
    content: "How do I filter OUT screenshots when searching for tickets or receipts? Every time I search 'concert', I get 200 screenshots of Spotify playlists and ticket confirmations rather than the photos of me and my friends at the venue.",
    metadata: {
      upvotes: 112,
      date: '2023-09-28',
      tags: ['screenshot_pollution', 'concert', 'social_retrieval'],
    },
  },
  {
    id: 'voc-004',
    source: 'r/GooglePhotos',
    type: 'Reddit Post',
    content: "Had to find a picture of my car's tire pressure sticker taken last year. Searched 'tire' and 'car' and got 500 pictures of road trips. I ended up opening WhatsApp to find the date I texted it to my mechanic, then scrolled to that date in Google Photos.",
    metadata: {
      upvotes: 88,
      date: '2024-02-10',
      tags: ['workaround', 'external_app_audit', 'utilitarian_doc'],
    },
  },
  {
    id: 'voc-005',
    source: 'App Store',
    type: '2-Star Review',
    content: "I remember the vibe of a photo—it was a sunset where everything had a purple haze on the beach in Greece. Searching 'sunset beach' returns 1,200 photos from the last 8 years. Why can't I search 'purple sunset with two people'?",
    metadata: {
      rating: 2,
      device: 'iPhone 15 Pro',
      date: '2024-03-02',
      tags: ['aesthetic_vibe', 'sensory_recall', 'color_query'],
    },
  },
  {
    id: 'voc-006',
    source: 'r/GooglePhotos',
    type: 'Reddit Post',
    content: "I wanted to show my friend a meme I saved three weeks ago about cats in coffee cups. Searching 'cat' brings up thousands of actual pictures of my cat. Why does Google Photos mix saved web garbage with my real life memories?",
    metadata: {
      upvotes: 142,
      date: '2024-03-18',
      tags: ['meme_pollution', 'asset_silos', 'saved_media'],
    },
  },
  {
    id: 'voc-007',
    source: 'Google Support Forum',
    type: 'Support Thread',
    content: "I cannot remember what month my nephew was born, but I know my mom was holding him while sitting in her green floral armchair. Searching 'baby' or 'chair' gives endless hits. I spent 20 minutes scrubbing the timeline year by year.",
    metadata: {
      upvotes: 67,
      date: '2024-04-05',
      tags: ['chronological_scrubbing', 'relational_anchor', 'furniture_context'],
    },
  },
];

/**
 * Sanitized and Verified In-Memory Seed Corpus
 * @type {import('./schema.js').UserFeedbackRecord[]}
 */
export const SEED_CORPUS = Object.freeze(
  RAW_SEED_CORPUS.map((record) => sanitizeFeedbackRecord(record))
);
