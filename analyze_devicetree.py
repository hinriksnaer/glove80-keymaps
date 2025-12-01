#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get the custom_devicetree field
devicetree = data.get('custom_devicetree', '')

print("Custom devicetree analysis:")
print(f"Total length: {len(devicetree)} characters")
print(f"Total lines: {len(devicetree.splitlines())}")
print()

# Split into lines and check for issues
lines = devicetree.splitlines()
for i, line in enumerate(lines, 1):
    if len(line) >= 121:
        # Check what's at column 121
        char_at_121 = line[120] if len(line) > 120 else ''
        context = line[110:130] if len(line) > 110 else line
        print(f"Line {i} (length {len(line)}), column 121: '{char_at_121}'")
        print(f"  Context [110-130]: {context}")
        print()

# Look for potential issues
print("\nLooking for potential syntax issues:")

# Check for unmatched angle brackets in layer-id
for i, line in enumerate(lines, 1):
    if 'layer-id' in line:
        print(f"Line {i}: {line.strip()}")
        # Check if brackets are balanced
        open_count = line.count('<')
        close_count = line.count('>')
        if open_count != close_count:
            print(f"  ⚠ Unbalanced brackets: {open_count} open, {close_count} close")

# Check for any remaining LAYER_ references
remaining = re.findall(r'LAYER_\w+', devicetree)
if remaining:
    print(f"\n⚠ Found {len(remaining)} LAYER_ references:")
    for ref in set(remaining):
        print(f"  {ref}")

# Look for lines with issues around column 121
print("\n\nChecking all lines with length > 120:")
for i, line in enumerate(lines, 1):
    if len(line) > 120:
        # Show context around column 121
        before = line[100:120]
        at = line[120] if len(line) > 120 else ''
        after = line[121:141] if len(line) > 121 else ''
        print(f"Line {i}:")
        print(f"  [100-120]: ...{before}")
        print(f"  [121]:     {at}")
        print(f"  [121-141]: {after}...")
        print()
