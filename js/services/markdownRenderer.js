/**
 * Executive Markdown AST Renderer
 * AI-Powered Discovery Engine for Google Photos
 * Phase 5: Reading Canvas, State Machine & Markdown AST Parser
 * 
 * Converts raw LLM Markdown into semantic HTML with executive typography,
 * styled 3-column T-Charts, Trade-off comparison matrices, and verbatim quote blockquotes.
 */

export class MarkdownRenderer {
  /**
   * Escape potentially malicious HTML tags
   * @param {string} text
   * @returns {string}
   */
  static escapeHtml(text) {
    if (!text) return '';
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  /**
   * Convert raw Markdown string into structured, semantic HTML
   * @param {string} markdown
   * @returns {string}
   */
  static render(markdown) {
    if (!markdown || typeof markdown !== 'string') return '';

    const lines = markdown.trim().split(/\r?\n/);
    const htmlBlocks = [];
    let i = 0;

    while (i < lines.length) {
      const line = lines[i];

      // 1. Fenced Code Block (```lang ... ```)
      if (line.trim().startsWith('```')) {
        const lang = line.trim().slice(3).trim();
        const codeLines = [];
        i++;
        while (i < lines.length && !lines[i].trim().startsWith('```')) {
          codeLines.push(this.escapeHtml(lines[i]));
          i++;
        }
        i++; // skip closing ```
        htmlBlocks.push(`<pre><code class="language-${lang || 'plaintext'}">${codeLines.join('\n')}</code></pre>`);
        continue;
      }

      // 2. Horizontal Rule (---, ***, ___)
      if (/^(\s*[-*_]\s*){3,}$/.test(line)) {
        htmlBlocks.push('<hr class="report-divider" />');
        i++;
        continue;
      }

      // 3. Headers (H1 to H4)
      if (/^#{1,4}\s+/.test(line)) {
        const match = line.match(/^(#{1,4})\s+(.+)$/);
        if (match) {
          const level = match[1].length;
          const text = this.renderInline(match[2].trim());
          htmlBlocks.push(`<h${level}>${text}</h${level}>`);
          i++;
          continue;
        }
      }

      // 4. Markdown Table
      if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
        const tableLines = [];
        while (i < lines.length && lines[i].trim().startsWith('|') && lines[i].trim().endsWith('|')) {
          tableLines.push(lines[i].trim());
          i++;
        }
        htmlBlocks.push(this.renderTable(tableLines));
        continue;
      }

      // 5. Blockquotes (>)
      if (line.trim().startsWith('>')) {
        const quoteLines = [];
        while (i < lines.length && (lines[i].trim().startsWith('>') || (lines[i].trim() !== '' && !lines[i].trim().startsWith('#') && !lines[i].trim().startsWith('|')))) {
          if (lines[i].trim().startsWith('>')) {
            quoteLines.push(lines[i].trim().replace(/^>\s?/, ''));
          } else {
            quoteLines.push(lines[i].trim());
          }
          i++;
        }
        const quoteContent = this.renderInline(quoteLines.join(' '));
        htmlBlocks.push(`<blockquote><p>${quoteContent}</p></blockquote>`);
        continue;
      }

      // 6. Ordered Lists (1. Item)
      if (/^\s*\d+\.\s+/.test(line)) {
        const listItems = [];
        while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
          const itemText = lines[i].replace(/^\s*\d+\.\s+/, '').trim();
          listItems.push(`<li>${this.renderInline(itemText)}</li>`);
          i++;
        }
        htmlBlocks.push(`<ol>${listItems.join('')}</ol>`);
        continue;
      }

      // 7. Unordered Lists (- Item or * Item)
      if (/^\s*[-*]\s+/.test(line)) {
        const listItems = [];
        while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
          const itemText = lines[i].replace(/^\s*[-*]\s+/, '').trim();
          listItems.push(`<li>${this.renderInline(itemText)}</li>`);
          i++;
        }
        htmlBlocks.push(`<ul>${listItems.join('')}</ul>`);
        continue;
      }

      // 8. Empty lines
      if (line.trim() === '') {
        i++;
        continue;
      }

      // 9. Regular Paragraphs
      const paragraphLines = [];
      while (
        i < lines.length &&
        lines[i].trim() !== '' &&
        !lines[i].trim().startsWith('#') &&
        !lines[i].trim().startsWith('>') &&
        !lines[i].trim().startsWith('|') &&
        !lines[i].trim().startsWith('```') &&
        !/^\s*[-*]\s+/.test(lines[i]) &&
        !/^\s*\d+\.\s+/.test(lines[i]) &&
        !/^(\s*[-*_]\s*){3,}$/.test(lines[i])
      ) {
        paragraphLines.push(lines[i].trim());
        i++;
      }

      if (paragraphLines.length > 0) {
        const pText = this.renderInline(paragraphLines.join(' '));
        htmlBlocks.push(`<p>${pText}</p>`);
      }
    }

    return htmlBlocks.join('\n');
  }

  /**
   * Render inline elements: bold, italics, inline code, links
   * @param {string} text
   * @returns {string}
   */
  static renderInline(text) {
    if (!text) return '';

    let out = text;

    // Inline code: `code`
    out = out.replace(/`([^`]+)`/g, (match, p1) => `<code>${this.escapeHtml(p1)}</code>`);

    // Bold + Italic: ***text***
    out = out.replace(/\*\*\*([^*]+)\*\*\*/g, '<strong><em>$1</em></strong>');

    // Bold: **text**
    out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

    // Italic: *text* or _text_
    out = out.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    out = out.replace(/(^|\s)_([^_]+)_(\s|$)/g, '$1<em>$2</em>$3');

    // Links: [text](url)
    out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');

    return out;
  }

  /**
   * Parse and render Markdown tables (T-Charts, Trade-off Matrices)
   * @param {string[]} tableLines
   * @returns {string}
   */
  static renderTable(tableLines) {
    if (!tableLines || tableLines.length < 2) return '';

    const parseRow = (line) => {
      // Split by pipe and discard outer empty elements
      const cells = line.split('|');
      if (cells.length > 2) {
        return cells.slice(1, -1).map((c) => c.trim());
      }
      return cells.map((c) => c.trim());
    };

    const headerCells = parseRow(tableLines[0]);
    // Line 1 is typically separator: |---|---|
    const hasSeparator = tableLines.length > 1 && /^[|\s:-]+$/.test(tableLines[1]);
    const bodyStartIdx = hasSeparator ? 2 : 1;

    const thead = `<thead><tr>${headerCells.map((c) => `<th>${this.renderInline(c)}</th>`).join('')}</tr></thead>`;

    const bodyRows = [];
    for (let r = bodyStartIdx; r < tableLines.length; r++) {
      const rowCells = parseRow(tableLines[r]);
      if (rowCells.length > 0 && rowCells.some((c) => c.length > 0)) {
        const tds = rowCells.map((c) => `<td>${this.renderInline(c)}</td>`).join('');
        bodyRows.push(`<tr>${tds}</tr>`);
      }
    }

    const tbody = `<tbody>${bodyRows.join('\n')}</tbody>`;

    return `<div class="table-responsive"><table>${thead}${tbody}</table></div>`;
  }
}
