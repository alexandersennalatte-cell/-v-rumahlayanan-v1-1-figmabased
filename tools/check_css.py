"""Accurate CSS structural validator.

Tracks brace depth while skipping strings and comments.
Reports unbalanced blocks, unterminated comments/strings, and duplicate
top-level selectors.
"""
import sys, re, os


def strip_noise(src):
    """Remove comments and string contents, preserving structure."""
    out = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c == '/' and i + 1 < n and src[i + 1] == '*':
            end = src.find('*/', i + 2)
            if end == -1:
                raise ValueError('unterminated comment at offset %d' % i)
            i = end + 2
            continue
        if c in '"\'':
            quote = c
            i += 1
            closed = False
            while i < n:
                if src[i] == '\\':
                    i += 2
                    continue
                if src[i] == quote:
                    i += 1
                    closed = True
                    break
                i += 1
            if not closed:
                raise ValueError('unterminated string literal')
            out.append('""')
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def check(path):
    src = open(path, encoding='utf-8').read()
    print('=== %s ===' % path)

    try:
        clean = strip_noise(src)
    except ValueError as e:
        print('   ERROR:', e)
        print()
        return False

    stack = []
    errors = []
    line = 1
    buf = []
    top_sels = []
    for ch in clean:
        if ch == '{':
            sel = ''.join(buf).strip()
            if len(stack) == 0:
                top_sels.append(sel)
            stack.append((line, sel))
            buf = []
        elif ch == '}':
            if not stack:
                errors.append('line %d: unmatched "}"' % line)
            else:
                stack.pop()
            buf = []
        elif ch == ';':
            buf = []
        else:
            if ch == '\n':
                line += 1
            buf.append(ch)

    for ln, sel in stack:
        errors.append('unclosed block opened at line %d: %r' % (ln, sel[:80]))

    for e in errors:
        print('   ERROR:', e)
    if not errors:
        print('   braces balanced OK')

    seen = {}
    for t in top_sels:
        for sel in t.split(','):
            sel = sel.strip()
            if not sel:
                continue
            seen[sel] = seen.get(sel, 0) + 1
    dups = {k: v for k, v in seen.items() if v > 1}
    if dups:
        print('   duplicate top-level selectors:')
        for k, v in sorted(dups.items()):
            print('     %-42s x%d' % (k[:42], v))
    else:
        print('   no duplicate top-level selectors')

    print()
    return not errors and not dups


ok = True
for p in sys.argv[1:]:
    ok = check(p) and ok
sys.exit(0 if ok else 1)
