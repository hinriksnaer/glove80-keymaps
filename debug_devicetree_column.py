#!/usr/bin/env python3
import json

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get both devicetree fields
custom_devicetree = data.get('custom_devicetree', '')
custom_defined_behaviors = data.get('custom_defined_behaviors', '')

print("File structure:")
print(f"  custom_defined_behaviors: {len(custom_defined_behaviors)} chars, {len(custom_defined_behaviors.splitlines())} lines")
print(f"  custom_devicetree: {len(custom_devicetree)} chars, {len(custom_devicetree.splitlines())} lines")
print(f"  Total lines: ~{len(custom_defined_behaviors.splitlines()) + len(custom_devicetree.splitlines())}")

# The error is at line 10668 in build.keymap
# custom_defined_behaviors is ~9900 lines, so 10668 is around line 768 of custom_devicetree
# But let's check all lines in custom_devicetree with length > 120

print("\n" + "="*80)
print("Analyzing custom_devicetree for long lines and column 121 issues:")
print("="*80)

dt_lines = custom_devicetree.splitlines()
print(f"\nTotal lines in custom_devicetree: {len(dt_lines)}")

# Look at lines that are long enough to have column 121
long_lines = []
for i, line in enumerate(dt_lines, 1):
    if len(line) >= 121:
        char_at_121 = line[120]
        long_lines.append((i, len(line), char_at_121, line))

print(f"Lines with length >= 121: {len(long_lines)}")

if long_lines:
    print("\nShowing all long lines:")
    for line_num, length, char, full_line in long_lines:
        print(f"\nLine {line_num} (length {length}):")
        print(f"  Full line: {full_line}")
        print(f"  Character at column 121: '{char}' (ASCII {ord(char)})")
        # Show context around column 121
        if length > 130:
            context = full_line[100:140]
            print(f"  Context [100-140]: {context}")

# Also check for any lines with unusual characters or syntax issues
print("\n" + "="*80)
print("Checking for syntax issues in custom_devicetree:")
print("="*80)

# Check for LAYER_ references
if 'LAYER_' in custom_devicetree:
    import re
    refs = re.findall(r'LAYER_\w+', custom_devicetree)
    print(f"\nFound {len(refs)} LAYER_ references:")
    for ref in sorted(set(refs)):
        print(f"  {ref}: {refs.count(ref)} occurrences")
else:
    print("\nNo LAYER_ references found")

# Check for potential devicetree syntax issues
print("\nChecking layer-id assignments:")
import re
layer_ids = re.findall(r'layer-id\s*=\s*<([^>]+)>', custom_devicetree)
for lid in layer_ids:
    print(f"  layer-id = <{lid}>")
