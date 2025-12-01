#!/usr/bin/env python3
import json
import re

# Current layer mapping after removals
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

# Deleted layers - should be replaced with 0 (base layer)
deleted_layers = [
    'LAYER_Engrammer',
    'LAYER_Engram',
    'LAYER_Dvorak',
    'LAYER_Colemak',
    'LAYER_QWERTY',
    'LAYER_ColemakDH',
    'LAYER_LeftPinky',
    'LAYER_LeftRingy',
    'LAYER_LeftMiddy',
    'LAYER_LeftIndex',
    'LAYER_RightPinky',
    'LAYER_RightRingy',
    'LAYER_RightMiddy',
    'LAYER_RightIndex',
    'LAYER_Mouse',
    'LAYER_MouseFine',
    'LAYER_MouseSlow',
    'LAYER_MouseFast',
    'LAYER_MouseWarp',
    'LAYER_Emoji',
    'LAYER_World'
]

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get the custom_defined_behaviors field
behaviors = data.get('custom_defined_behaviors', '')

print("Before replacements:")
print(f"  Total length: {len(behaviors)} characters")

# Find all LAYER_ references
all_refs = re.findall(r'LAYER_\w+', behaviors)
print(f"  Total LAYER_ references: {len(all_refs)}")
for ref in sorted(set(all_refs)):
    count = all_refs.count(ref)
    print(f"    {ref}: {count} occurrences")

# Replace existing layers with numeric IDs
for layer_name, layer_id in layer_mapping.items():
    behaviors = behaviors.replace(layer_name, layer_id)

# Replace deleted layers with 0 (base layer)
for layer_name in deleted_layers:
    behaviors = behaviors.replace(layer_name, '0')

# Update the JSON
data['custom_defined_behaviors'] = behaviors

# Write back
with open('keymap.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\nAfter replacements:")
print(f"  Total length: {len(behaviors)} characters")

# Check for any remaining LAYER_ references
remaining = re.findall(r'LAYER_\w+', behaviors)
if remaining:
    print(f"\n⚠ Warning: Still found {len(remaining)} LAYER_ references:")
    for ref in sorted(set(remaining)):
        count = remaining.count(ref)
        print(f"    {ref}: {count} occurrences")
else:
    print("\n✓ Success! No LAYER_ references remain in custom_defined_behaviors.")
