#!/usr/bin/env python3
import json
import re

# Layer mapping
layer_mapping = {
    'LAYER_Enthium': '0',
    'LAYER_Typing': '1',
    'LAYER_Cursor': '2',
    'LAYER_Number': '3',
    'LAYER_Function': '4',
    'LAYER_Symbol': '5',
    'LAYER_System': '6',
    'LAYER_Gaming': '7',
    'LAYER_Factory': '8',
    'LAYER_Lower': '9',
    'LAYER_Magic': '10'
}

# Deleted layers map to 0 (base layer)
deleted_layers = {
    'LAYER_Emoji': '0',
    'LAYER_World': '0',
    'LAYER_Mouse': '0',
    'LAYER_MouseFine': '0',
    'LAYER_MouseSlow': '0',
    'LAYER_MouseFast': '0',
    'LAYER_MouseWarp': '0',
}

# Combine mappings
all_mappings = {**layer_mapping, **deleted_layers}

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Convert layers array to JSON string, do replacements, convert back
layers_str = json.dumps(data['layers'])

print("Fixing LAYER_ references in layers array:")
print(f"Original length: {len(layers_str)} characters\n")

# Find all LAYER_ refs before
refs_before = re.findall(r'LAYER_\w+', layers_str)
print(f"Before: {len(refs_before)} LAYER_ references")
for ref in sorted(set(refs_before)):
    count = refs_before.count(ref)
    replacement = all_mappings.get(ref, '???')
    print(f"  {ref}: {count} times → will become {replacement}")

# Replace all LAYER_ references
for layer_name, layer_id in all_mappings.items():
    layers_str = layers_str.replace(layer_name, layer_id)

# Convert back to Python object
data['layers'] = json.loads(layers_str)

# Find all LAYER_ refs after
refs_after = re.findall(r'LAYER_\w+', json.dumps(data['layers']))
print(f"\nAfter: {len(refs_after)} LAYER_ references")
if refs_after:
    for ref in sorted(set(refs_after)):
        print(f"  {ref}: {refs_after.count(ref)} times")

# Write back
with open('keymap.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\n✓ Fixed LAYER_ references in layers array!")
print(f"  Replaced {len(refs_before)} references")
