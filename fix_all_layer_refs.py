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
devicetree = data.get('custom_devicetree', '')

print("Before replacements:")
print(f"  Total length: {len(devicetree)} characters")

# Replace ALL LAYER_ constants with numeric IDs (not just in layer-id assignments)
for layer_name, layer_id in layer_mapping.items():
    # Count occurrences
    count_before = devicetree.count(layer_name)
    if count_before > 0:
        print(f"  {layer_name}: {count_before} occurrences")

    # Replace all occurrences
    devicetree = devicetree.replace(layer_name, str(layer_id))

# Update the JSON
data['custom_devicetree'] = devicetree

# Write back
with open('keymap.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nAfter replacements:")
print(f"  Total length: {len(devicetree)} characters")

# Check for any remaining LAYER_ references
remaining = re.findall(r'LAYER_\w+', devicetree)
if remaining:
    print(f"\nWarning: Still found {len(remaining)} LAYER_ references:")
    for ref in set(remaining):
        print(f"  {ref}: {remaining.count(ref)} occurrences")
else:
    print("\nSuccess! No LAYER_ references remain.")
