#!/usr/bin/env python3
import json

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get custom_defined_behaviors
behaviors = data.get('custom_defined_behaviors', '')

lines = behaviors.splitlines()
total_lines = len(lines)

print(f"Total lines in custom_defined_behaviors: {total_lines}")
print(f"Looking for issues around lines that could be at position 10668 in build.keymap")
print()

# The error is at line 10668, column 121
# Let's check lines around that position
# Since behaviors comes first, line 10668 should be behaviors line ~10668

if total_lines < 10668:
    print(f"custom_defined_behaviors only has {total_lines} lines")
    print(f"Line 10668 in build.keymap would be in custom_devicetree")

    # Calculate which line in devicetree
    devicetree_line = 10668 - total_lines
    print(f"Would be line {devicetree_line} of custom_devicetree")

    # Get custom_devicetree
    devicetree = data.get('custom_devicetree', '')
    dt_lines = devicetree.splitlines()

    if devicetree_line <= len(dt_lines):
        actual_line = dt_lines[devicetree_line - 1]
        print(f"\nLine {devicetree_line} of custom_devicetree:")
        print(f"  Length: {len(actual_line)}")
        print(f"  Content: {actual_line}")
        if len(actual_line) >= 121:
            char_121 = actual_line[120]
            context = actual_line[100:140] if len(actual_line) > 100 else actual_line
            print(f"  Character at column 121: '{char_121}' (ASCII {ord(char_121)})")
            print(f"  Context: {context}")
else:
    # Check the actual line 10668
    line_idx = 10668 - 1  # 0-indexed
    if line_idx < len(lines):
        actual_line = lines[line_idx]
        print(f"Line 10668 of custom_defined_behaviors:")
        print(f"  Length: {len(actual_line)}")
        print(f"  Content: {actual_line}")

        if len(actual_line) >= 121:
            char_121 = actual_line[120]
            context = actual_line[100:140] if len(actual_line) > 100 else actual_line
            print(f"  Character at column 121: '{char_121}' (ASCII {ord(char_121)})")
            print(f"  Context [100-140]: {context}")

# Also check for lines with exactly column 121 issues
print("\n" + "="*80)
print("Searching all lines with potential column 121 issues:")
print("="*80)

for i, line in enumerate(lines, 1):
    if len(line) >= 121:
        char_121 = line[120]
        # Check for problematic characters at column 121
        # Devicetree parser might choke on certain characters
        if char_121 in ['&', '<', '>', '(', ')', '{', '}', '[', ']']:
            print(f"\nLine {i} has '{char_121}' at column 121 (length {len(line)}):")
            context_start = max(0, 110)
            context_end = min(len(line), 135)
            context = line[context_start:context_end]
            print(f"  Context: ...{context}...")
