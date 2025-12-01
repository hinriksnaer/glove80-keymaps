#!/usr/bin/env python3
import json
import re

# Current layer mapping after removals
layer_mapping = {
    'LAYER_Enthium': 0,
    'LAYER_Typing': 1,
    'LAYER_Cursor': 2,
    'LAYER_Number': 3,
    'LAYER_Function': 4,
    'LAYER_Symbol': 5,
    'LAYER_System': 6,
    'LAYER_Gaming': 7,
    'LAYER_Factory': 8,
    'LAYER_Lower': 9,
    'LAYER_Magic': 10
}

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get the custom_devicetree field
devicetree = data.get('custom_defined_devicetree', '')

# Replace all LAYER_ constants with numeric IDs in layer-id assignments
for layer_name, layer_id in layer_mapping.items():
    # Match patterns like: layer-id = <LAYER_Something>;
    pattern = rf'layer-id\s*=\s*<{layer_name}>'
    replacement = f'layer-id = <{layer_id}>'
    devicetree = re.sub(pattern, replacement, devicetree)

# Update the JSON
data['custom_defined_devicetree'] = devicetree

# Write back
with open('keymap.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Fixed layer IDs in custom_devicetree")
print(f"Replaced {len(layer_mapping)} layer constants with numeric IDs")
