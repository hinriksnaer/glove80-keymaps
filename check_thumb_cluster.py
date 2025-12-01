#!/usr/bin/env python3
import json

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get layer 0 (Enthium base layer)
layer0 = data['layers'][0]

# Thumb cluster positions for Glove80
# Left thumb: 52, 53, 54, 55, 56, 57
# Right thumb: 64, 65, 66, 67, 68, 69

left_thumb_positions = [52, 53, 54, 55, 56, 57]
right_thumb_positions = [64, 65, 66, 67, 68, 69]

print("Current thumb cluster configuration on base layer:\n")

print("Left thumb cluster (positions 52-57):")
for pos in left_thumb_positions:
    binding = layer0[pos]
    value = binding.get('value', '')
    params = binding.get('params', [])
    if params:
        param_str = ' '.join([str(p.get('value', '')) if isinstance(p, dict) else str(p) for p in params])
        print(f"  Position {pos}: {value} {param_str}")
    else:
        print(f"  Position {pos}: {value}")

print("\nRight thumb cluster (positions 64-69):")
for pos in right_thumb_positions:
    binding = layer0[pos]
    value = binding.get('value', '')
    params = binding.get('params', [])
    if params:
        param_str = ' '.join([str(p.get('value', '')) if isinstance(p, dict) else str(p) for p in params])
        print(f"  Position {pos}: {value} {param_str}")
    else:
        print(f"  Position {pos}: {value}")

# Also check position 57 specifically since I may have modified it
print(f"\n\nSpecial check - Position 57 (left inner thumb):")
binding = layer0[57]
print(f"  Full binding: {json.dumps(binding, indent=2)}")
