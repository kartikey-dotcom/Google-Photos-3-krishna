/**
 * Resilient Gemini 1.5 Flash REST Client
 * AI-Powered Discovery Engine for Google Photos
 * Phase 3: Prompt Orchestrator, Gemini 1.5 Client & Comparison Engine
 */

import { APP_CONFIG } from '../config/constants.js';

export class GeminiClient {
  /**
   * @param {Object} [options]
   * @param {string} [options.baseUrl]
   * @param {string} [options.modelName]
   */
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || 'https://generativelanguage.googleapis.com/v1beta/models';
    this.modelName = options.modelName || APP_CONFIG.MODEL_NAME || 'gemini-1.5-flash';
  }

  /**
   * Execute structured prompt inference against Google AI Studio REST API
   * bound strictly to Temperature 0.2 and Top_P 0.8.
   * 
   * @param {string} prompt - Fully assembled prompt string
   * @param {string} apiKey - Sanitized Google AI Studio Gemini API key
   * @returns {Promise<{ success: boolean, data?: string, error?: string, status?: number }>}
   */
  async generateContent(prompt, apiKey) {
    // Client-side pre-flight validations
    const cleanKey = (apiKey || '').trim().replace(/^["']|["']$/g, '');
    if (!cleanKey) {
      return {
        success: false,
        error: 'API Key Required: Please enter your Google Gemini API key in the configuration card on the left sidebar before triggering this analytical workflow.',
        status: 401,
      };
    }

    if (!prompt || typeof prompt !== 'string' || prompt.trim() === '') {
      return {
        success: false,
        error: 'Invalid Request: Prompt cannot be empty.',
        status: 400,
      };
    }

    const endpoint = `${this.baseUrl}/${this.modelName}:generateContent?key=${cleanKey}`;

    const payload = {
      contents: [
        {
          parts: [{ text: prompt }],
        },
      ],
      generationConfig: {
        temperature: APP_CONFIG.GENERATION_CONFIG.temperature, // 0.2
        topP: APP_CONFIG.GENERATION_CONFIG.topP, // 0.8
        topK: APP_CONFIG.GENERATION_CONFIG.topK, // 40
        maxOutputTokens: APP_CONFIG.GENERATION_CONFIG.maxOutputTokens, // 2048
      },
    };

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        return this.handleHttpError(response.status);
      }

      const responseJson = await response.json();
      return this.parseResponse(responseJson);

    } catch (networkError) {
      console.error('[GeminiClient] Network or Fetch Error:', networkError);
      return {
        success: false,
        error: 'Network Connection Failed: Unable to reach Google AI Studio. Please verify your internet connection or proxy settings.',
        status: 0,
      };
    }
  }

  /**
   * Diagnostic Error Interceptor Suite
   * @param {number} status - HTTP status code
   * @returns {{ success: false, error: string, status: number }}
   */
  handleHttpError(status) {
    let errorMessage = '';

    switch (status) {
      case 400:
        errorMessage = 'Invalid Request (400): Invalid request payload or parameter format sent to Google AI Studio.';
        break;
      case 401:
      case 403:
        errorMessage = 'Authentication Failed (401/403): Your Gemini API key is invalid or unauthorized. Please verify your Google AI Studio credentials in the sidebar.';
        break;
      case 429:
        errorMessage = 'Rate Limit Exceeded (429): Google AI Studio quota exceeded. Please wait 30 seconds before triggering another analytical workflow.';
        break;
      case 500:
      case 503:
        errorMessage = 'Service Unavailable (500/503): Google AI Studio is experiencing temporary service disruption. Please retry shortly.';
        break;
      default:
        errorMessage = `Inference Failed (HTTP ${status}): An unexpected error occurred while communicating with Google AI Studio.`;
        break;
    }

    return {
      success: false,
      error: errorMessage,
      status,
    };
  }

  /**
   * Parse and validate returned candidates JSON structure
   * @param {any} responseJson
   * @returns {{ success: boolean, data?: string, error?: string }}
   */
  parseResponse(responseJson) {
    try {
      const candidate = responseJson?.candidates?.[0];
      const text = candidate?.content?.parts?.[0]?.text;

      if (!text || text.trim() === '') {
        return {
          success: false,
          error: 'Empty Model Response: Google Gemini returned an empty response string. Please retry the workflow.',
        };
      }

      return {
        success: true,
        data: text.trim(),
      };
    } catch (parseError) {
      console.error('[GeminiClient] Response Parsing Error:', parseError);
      return {
        success: false,
        error: 'Malformed Response: Failed to parse Google AI Studio candidate text.',
      };
    }
  }
}

/**
 * Singleton instance of GeminiClient
 */
export const defaultGeminiClient = new GeminiClient();
