import sys, io

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

def parse(path):
    raw = open(path, encoding='utf-8').read()
    stack = []
    errors = []
    i = 0
    n = len(raw)
    line = 1
    while i < n:
        c = raw[i]
        if c == '\n':
            line += 1
            i += 1
            continue
        if c != '<':
            i += 1
            continue
        # comment
        if raw.startswith('<!--', i):
            end = raw.find('-->', i)
            if end == -1:
                errors.append(f'line {line}: unterminated comment')
                break
            line += raw.count('\n', i, end)
            i = end + 3
            continue
        # doctype / declaration
        if raw.startswith('<!', i):
            end = raw.find('>', i)
            line += raw.count('\n', i, end)
            i = end + 1
            continue
        # closing tag
        if raw.startswith('</', i):
            end = raw.find('>', i)
            name = raw[i+2:end].strip().lower()
            line += raw.count('\n', i, end)
            i = end + 1
            if name in VOID:
                continue
            if not stack:
                errors.append(f'line {line}: stray closing </{name}>')
                continue
            if stack[-1][0] != name:
                errors.append(f'line {line}: </{name}> but expected </{stack[-1][0]}> (opened line {stack[-1][1]})')
                # try to recover
                for j in range(len(stack)-1, -1, -1):
                    if stack[j][0] == name:
                        for k in range(len(stack)-1, j-1, -1):
                            errors.append(f'  -> implicitly closing <{stack[k][0]}> opened line {stack[k][1]}')
                        stack = stack[:j]
                        break
                else:
                    stack.pop()
                continue
            stack.pop()
            continue
        # opening tag
        end = raw.find('>', i)
        if end == -1:
            errors.append(f'line {line}: unterminated tag')
            break
        inner = raw[i+1:end]
        selfclose = inner.rstrip().endswith('/')
        m = __import__('re').match(r'([a-zA-Z][\w:-]*)', inner)
        if not m:
            i = end + 1
            continue
        name = m.group(1).lower()
        line += raw.count('\n', i, end)
        i = end + 1
        if name in VOID or selfclose:
            continue
        stack.append((name, line))
    return stack, errors

for path in sys.argv[1:]:
    stack, errors = parse(path)
    print(f'=== {path} ===')
    if errors:
        for e in errors:
            print('  ERROR', e)
    else:
        print('  no mismatches')
    if stack:
        print('  UNCLOSED at EOF:')
        for name, ln in stack:
            print(f'    <{name}> opened line {ln}')
    else:
        print('  all tags balanced')
    print()
