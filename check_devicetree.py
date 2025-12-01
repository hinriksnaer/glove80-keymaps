#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get the custom_devicetree field (not custom_defined_devicetree!)
devicetree = data.get('custom_devicetree', '')

# Find all LAYER_ references
layer_refs = re.findall(r'LAYER_\w+', devicetree)

if layer_refs:
    print(f"Found {len(layer_refs)} LAYER_ references in devicetree:")
    for ref in set(layer_refs):
        count = layer_refs.count(ref)
        print(f"  {ref}: {count} occurrences")
else:
    print("No LAYER_ references found in devicetree")

# Also check for layer-id assignments
layer_id_lines = re.findall(r'layer-id\s*=\s*<[^>]+>', devicetree)
print(f"\nFound {len(layer_id_lines)} layer-id assignments:")
for line in layer_id_lines[:20]:  # Show first 20
    print(f"  {line}")
if len(layer_id_lines) > 20:
    print(f"  ... and {len(layer_id_lines) - 20} more")
