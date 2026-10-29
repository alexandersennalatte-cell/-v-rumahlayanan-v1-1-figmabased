import json
d = json.load(open('shots/report.json'))['desktop']['metrics']
for s in d['sections']:
    print(f"{s['top']:6d} +{s['h']:5d}  {s['tag']}.{s['id']}")
print('docH', d['docH'], 'scrollW', d['scrollW'])
