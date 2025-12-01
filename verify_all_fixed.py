#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

print("Checking all fields for LAYER_ references:\n")

all_clear = True
for field_name, field_value in data.items():
    if isinstance(field_value, str) and 'LAYER_' in field_value:
        refs = re.findall(r'LAYER_\w+', field_value)
        if refs:
            print(f"⚠ {field_name}: {len(refs)} LAYER_ references")
            for ref in sorted(set(refs)):
                count = refs.count(ref)
                print(f"    {ref}: {count} occurrences")
            all_clear = False

if all_clear:
    print("✓ All clear! No LAYER_ references found in any string fields.")
else:
    print("\n⚠ Some LAYER_ references still remain")
