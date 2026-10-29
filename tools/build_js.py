import os, glob

root = r'k:\Newfolder'
parts_dir = os.path.join(root, 'tools', 'jsparts')
out_path = os.path.join(root, 'js', 'main.js')

files = sorted(glob.glob(os.path.join(parts_dir, '*.js')))
chunks = []
for f in files:
    with open(f, encoding='utf-8') as fh:
        chunks.append(fh.read().rstrip('\n'))

merged = '\n\n'.join(chunks) + '\n'

os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8', newline='\n') as fh:
    fh.write(merged)

print('merged', len(files), 'parts ->', out_path)
print('lines:', merged.count('\n'))
