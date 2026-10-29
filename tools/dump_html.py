import os
root = r'k:\Newfolder'
html = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
out = os.path.join(root, 'tools', 'html_dump.txt')
with open(out, 'w', encoding='utf-8') as f:
    for i, line in enumerate(html.split('\n'), 1):
        f.write(f'{i:4d}| {line}\n')
print('wrote', out, len(html.split('\n')), 'lines')
