/* Lightweight JS tokenizer / structure checker.
 * Reports brace depth per line and flags where an IIFE closes early.
 * Handles line comments, block comments, strings, template literals
 * and regex literals.
 */
const fs = require('fs');

function tokenize(src) {
  const kinds = [];   // {type, line}
  let i = 0, line = 1, n = src.length;
  let lastSig = null; // last significant token (for regex detection)

  const isIdStart = c => /[A-Za-z_$]/.test(c);
  const isIdPart = c => /[A-Za-z0-9_$]/.test(c);

  const regexAllowed = () => {
    if (lastSig === null) return true;
    if (lastSig.type === 'punct') {
      return !([')', ']', '}'].includes(lastSig.value));
    }
    if (lastSig.type === 'keyword') {
      return ['return', 'typeof', 'instanceof', 'in', 'of', 'new', 'delete',
              'void', 'case', 'do', 'else', 'yield', 'await'].includes(lastSig.value);
    }
    return false;
  };

  while (i < n) {
    const c = src[i];

    if (c === '\n') { line++; i++; continue; }
    if (c === ' ' || c === '\t' || c === '\r') { i++; continue; }

    // comments
    if (c === '/' && src[i + 1] === '/') {
      while (i < n && src[i] !== '\n') i++;
      continue;
    }
    if (c === '/' && src[i + 1] === '*') {
      const end = src.indexOf('*/', i + 2);
      if (end === -1) throw new Error(`unterminated block comment at line ${line}`);
      for (let k = i; k < end; k++) if (src[k] === '\n') line++;
      i = end + 2;
      continue;
    }

    // strings
    if (c === '"' || c === "'") {
      const quote = c;
      const startLine = line;
      i++;
      while (i < n) {
        if (src[i] === '\\') { if (src[i + 1] === '\n') line++; i += 2; continue; }
        if (src[i] === quote) { i++; break; }
        if (src[i] === '\n') line++;
        i++;
      }
      lastSig = { type: 'string', value: quote, line: startLine };
      kinds.push(lastSig);
      continue;
    }

    // template literals (with nested ${})
    if (c === '`') {
      const startLine = line;
      i++;
      let tdepth = 0;
      while (i < n) {
        if (src[i] === '\\') { i += 2; continue; }
        if (tdepth === 0 && src[i] === '`') { i++; break; }
        if (tdepth === 0 && src[i] === '$' && src[i + 1] === '{') { tdepth = 1; i += 2; continue; }
        if (tdepth > 0) {
          if (src[i] === '{') tdepth++;
          else if (src[i] === '}') tdepth--;
          else if (src[i] === '"' || src[i] === "'" || src[i] === '`') {
            const q = src[i]; i++;
            while (i < n) {
              if (src[i] === '\\') { i += 2; continue; }
              if (src[i] === q) { i++; break; }
              i++;
            }
            continue;
          }
        }
        if (src[i] === '\n') line++;
        i++;
      }
      lastSig = { type: 'template', value: '`', line: startLine };
      kinds.push(lastSig);
      continue;
    }

    // regex literal
    if (c === '/' && regexAllowed()) {
      const startLine = line;
      let j = i + 1, inClass = false, ok = false;
      while (j < n) {
        const d = src[j];
        if (d === '\\') { j += 2; continue; }
        if (d === '\n') break;
        if (d === '[') inClass = true;
        else if (d === ']') inClass = false;
        else if (d === '/' && !inClass) { ok = true; j++; break; }
        j++;
      }
      if (ok) {
        while (j < n && /[a-z]/.test(src[j])) j++;
        lastSig = { type: 'regex', value: '/', line: startLine };
        kinds.push(lastSig);
        i = j;
        continue;
      }
    }

    // identifier / keyword
    if (isIdStart(c)) {
      let j = i;
      while (j < n && isIdPart(src[j])) j++;
      const word = src.slice(i, j);
      const isKw = ['function','return','if','else','for','while','var','let','const',
                    'new','typeof','instanceof','in','of','delete','void','case','do',
                    'yield','await','true','false','null','undefined','this'].includes(word);
      lastSig = { type: isKw ? 'keyword' : 'ident', value: word, line };
      kinds.push(lastSig);
      i = j;
      continue;
    }

    // numbers
    if (/[0-9]/.test(c)) {
      let j = i;
      while (j < n && /[0-9a-fA-FxXoObB._]/.test(src[j])) j++;
      lastSig = { type: 'num', value: src.slice(i, j), line };
      kinds.push(lastSig);
      i = j;
      continue;
    }

    // punctuation
    lastSig = { type: 'punct', value: c, line };
    kinds.push(lastSig);
    i++;
  }
  return kinds;
}

const path = process.argv[2];
const src = fs.readFileSync(path, 'utf8');
const srcLines = src.split('\n');

let kinds;
try {
  kinds = tokenize(src);
} catch (e) {
  console.log('ERROR:', e.message);
  process.exit(1);
}

let depth = 0;
const depthAtLine = [];
let lastLine = 1;
for (const k of kinds) {
  if (k.type === 'punct') {
    if (k.value === '{') depth++;
    else if (k.value === '}') depth--;
  }
  for (let l = lastLine; l < k.line; l++) depthAtLine[l] = depth;
  lastLine = k.line;
  depthAtLine[k.line] = depth;
}
for (let l = lastLine; l <= srcLines.length; l++) depthAtLine[l] = depth;

console.log(`=== ${path} ===`);
console.log(`final brace depth: ${depth}`);

// find where depth first returns to 0 (excluding the very end)
const zeroLines = [];
for (let l = 1; l <= srcLines.length; l++) {
  if (depthAtLine[l] === 0 && l < srcLines.length) zeroLines.push(l);
}
if (zeroLines.length) {
  console.log('depth returns to 0 at line(s):', zeroLines.join(', '));
  for (const l of zeroLines.slice(0, 5)) {
    console.log(`  line ${l}: ${srcLines[l - 1].trim().slice(0, 90)}`);
  }
} else {
  console.log('depth never returns to 0 before EOF -> OK');
}
