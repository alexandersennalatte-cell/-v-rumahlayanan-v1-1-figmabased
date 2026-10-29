import re, sys, io, os

root = r'k:\Newfolder'
html = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
css = open(os.path.join(root, 'css', 'style.css'), encoding='utf-8').read() if os.path.exists(os.path.join(root, 'css', 'style.css')) else ''

cls = set()
for m in re.finditer(r'class="([^"]+)"', html):
    for c in m.group(1).split():
        cls.add(c)

used_ids = set(re.findall(r'id="([^"]+)"', html))

# collect css selectors
css_classes = set(re.findall(r'\.([A-Za-z_][A-Za-z0-9_-]*)', css))

print('--- classes in HTML with NO css rule ---')
missing = sorted(c for c in cls if c not in css_classes)
print(len(missing))
for c in missing:
    print('   ', c)

print()
print('--- css classes not used in HTML ---')
unused = sorted(c for c in css_classes if c not in cls)
print(len(unused))
for c in unused:
    print('   ', c)
