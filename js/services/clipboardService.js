/**
 * Executive Clipboard & Slide Export Engine
 * AI-Powered Discovery Engine for Google Photos
 * Phase 6: Slide Export, Clipboard Engine & Micro-Interactions
 * 
 * Provides robust 1-click export of synthesized PM deliverables
 * into Google Slides, Google Docs, and PRD specifications with rich
 * HTML and optimized plaintext fallbacks.
 */

import { MarkdownRenderer } from './markdownRenderer.js';

export class ClipboardService {
  /**
   * Copy plain text to the system clipboard with modern API & fallback
   * @param {string} text - Raw text to copy
   * @returns {Promise<{success: boolean, error?: string}>}
   */
  static async copyText(text) {
    if (!text || typeof text !== 'string') {
      return { success: false, error: 'No text content provided to copy.' };
    }

    // Modern Clipboard API
    if (navigator?.clipboard?.writeText) {
      try {
        await navigator.clipboard.writeText(text);
        return { success: true };
      } catch (err) {
        console.warn('[ClipboardService] navigator.clipboard.writeText failed, attempting execCommand fallback:', err);
      }
    }

    // Fallback for older browsers or restricted iframe contexts
    return this.fallbackCopyText(text);
  }

  /**
   * Fallback copy using hidden DOM textarea and document.execCommand('copy')
   * @param {string} text
   * @returns {{success: boolean, error?: string}}
   */
  static fallbackCopyText(text) {
    try {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.setAttribute('readonly', '');
      textArea.style.position = 'fixed';
      textArea.style.top = '-9999px';
      textArea.style.left = '-9999px';
      textArea.style.opacity = '0';
      document.body.appendChild(textArea);

      textArea.focus();
      textArea.select();

      const successful = document.execCommand('copy');
      document.body.removeChild(textArea);

      if (successful) {
        return { success: true };
      }
      return { success: false, error: 'execCommand copy returned false.' };
    } catch (err) {
      console.error('[ClipboardService] execCommand fallback failed:', err);
      return { success: false, error: err.message };
    }
  }

  /**
   * Copy formatted report with multi-MIME rich text (text/html + text/plain)
   * Ensures Google Docs, Google Slides, and email clients receive rich tables,
   * colors, and styled quotes while plaintext receives clean markdown.
   * @param {string} markdown - Raw LLM Markdown
   * @param {string} [htmlOverride] - Optional pre-rendered HTML
   * @returns {Promise<{success: boolean, error?: string}>}
   */
  static async copyFormattedReport(markdown, htmlOverride = null) {
    if (!markdown) {
      return { success: false, error: 'Empty markdown content.' };
    }

    const plainText = this.optimizeForSlides(markdown);
    const htmlContent = htmlOverride || MarkdownRenderer.render(markdown);

    // Check if ClipboardItem is supported (Chrome, Edge, Safari, Firefox 127+)
    if (typeof ClipboardItem !== 'undefined' && navigator?.clipboard?.write) {
      try {
        const textBlob = new Blob([plainText], { type: 'text/plain' });
        const htmlBlob = new Blob([
          `<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>${htmlContent}</body></html>`,
        ], { type: 'text/html' });

        const item = new ClipboardItem({
          'text/plain': textBlob,
          'text/html': htmlBlob,
        });

        await navigator.clipboard.write([item]);
        return { success: true, format: 'rich' };
      } catch (err) {
        console.warn('[ClipboardService] ClipboardItem multi-MIME write failed, falling back to writeText:', err);
      }
    }

    // Fallback to text copy
    const fallbackRes = await this.copyText(plainText);
    return { ...fallbackRes, format: 'text' };
  }

  /**
   * Plaintext Slide Paste Optimizer
   * Converts markdown tables into tab-delimited rows for instant Google Slides / Docs
   * table cell paste, indents quotes, and cleans formatting artifacts.
   * @param {string} markdown
   * @returns {string}
   */
  static optimizeForSlides(markdown) {
    if (!markdown) return '';

    const lines = markdown.split(/\r?\n/);
    const output = [];
    let i = 0;

    while (i < lines.length) {
      const line = lines[i];

      // Markdown Table Conversion
      if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
        const tableLines = [];
        while (i < lines.length && lines[i].trim().startsWith('|') && lines[i].trim().endsWith('|')) {
          tableLines.push(lines[i].trim());
          i++;
        }

        const tsvLines = this.convertTableToTsv(tableLines);
        output.push(...tsvLines);
        output.push('');
        continue;
      }

      // Verbatim Blockquote Conversion
      if (line.trim().startsWith('>')) {
        let quoteText = line.trim().replace(/^>\s?/, '').trim();
        if ((quoteText.startsWith('"') && quoteText.endsWith('"')) || (quoteText.startsWith("'") && quoteText.endsWith("'"))) {
          quoteText = quoteText.slice(1, -1).trim();
        }
        output.push(`    "${quoteText}"`);
        i++;
        continue;
      }

      // Header normalization for Slides
      if (/^#{1,3}\s+/.test(line)) {
        const level = line.match(/^(#{1,3})/)[1].length;
        const text = line.replace(/^#{1,3}\s+/, '').trim();
        if (level === 1 || level === 2) {
          output.push(`\n=== ${text.toUpperCase()} ===\n`);
        } else {
          output.push(`\n--- ${text} ---`);
        }
        i++;
        continue;
      }

      // Regular line
      output.push(line);
      i++;
    }

    return output.join('\n').trim();
  }

  /**
   * Converts Markdown table rows into tab-delimited values (TSV)
   * Pasting TSV directly into Google Docs or Google Slides creates structured table cells.
   * @param {string[]} tableLines
   * @returns {string[]}
   */
  static convertTableToTsv(tableLines) {
    if (!tableLines || tableLines.length < 2) return tableLines;

    const parseCells = (row) => {
      const raw = row.split('|');
      const cells = raw.length > 2 ? raw.slice(1, -1) : raw;
      return cells.map((c) => c.trim().replace(/\t/g, ' '));
    };

    const hasSeparator = tableLines.length > 1 && /^[|\s:-]+$/.test(tableLines[1]);
    const bodyStart = hasSeparator ? 2 : 1;

    const header = parseCells(tableLines[0]).join('\t');
    const rows = [header];

    for (let r = bodyStart; r < tableLines.length; r++) {
      const cells = parseCells(tableLines[r]);
      if (cells.length > 0 && cells.some((c) => c.length > 0)) {
        rows.push(cells.join('\t'));
      }
    }

    return rows;
  }

  /**
   * Wire a Copy CTA button with 2.5s feedback transition
   * @param {Object} options
   * @param {HTMLButtonElement} options.button - Button element
   * @param {() => string} options.getMarkdown - Function returning raw markdown
   * @param {(message: string) => void} [options.onToast] - Toast notification callback
   * @param {number} [options.duration=2500] - Duration of feedback state in ms
   */
  static attachCopyButton({ button, getMarkdown, onToast, duration = 2500 }) {
    if (!button) return;

    let resetTimer = null;
    const originalText = button.querySelector('#copy-btn-text')?.textContent || 'Copy to Clipboard';
    const textSpan = button.querySelector('#copy-btn-text');

    button.addEventListener('click', async () => {
      const markdown = getMarkdown ? getMarkdown() : '';
      if (!markdown) {
        if (onToast) onToast('Select and execute a workflow to generate a report first.');
        return;
      }

      // Disable button briefly to prevent double click
      button.disabled = true;

      const result = await this.copyFormattedReport(markdown);

      button.disabled = false;

      if (result.success) {
        button.classList.add('copied');
        if (textSpan) {
          textSpan.textContent = '✓ Copied for Slides!';
        }

        if (onToast) {
          onToast('✓ Copied formatted report to clipboard for Google Slides!');
        }

        if (resetTimer) {
          clearTimeout(resetTimer);
        }

        resetTimer = setTimeout(() => {
          button.classList.remove('copied');
          if (textSpan) {
            textSpan.textContent = originalText;
          }
          resetTimer = null;
        }, duration);
      } else {
        if (onToast) {
          onToast('Failed to copy to clipboard: ' + (result.error || 'Unknown error'));
        }
      }
    });
  }
}
