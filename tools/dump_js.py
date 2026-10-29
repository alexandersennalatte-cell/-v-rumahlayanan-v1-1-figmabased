import os
root = r'k:\Newfolder'
js = open(os.path.join(root, 'js', 'main.js'), encoding='utf-8').read()
out = os.path.join(root, 'tools', 'js_dump.txt')
with open(out, 'w', encoding='utf-8') as f:
    for i, line in enumerate(js.split('\n'), 1):
        f.write(f'{i:4d}| {line}\n')
print('wrote', out, len(js.split('\n')), 'lines')
