#!/usr/bin/env python3
import json

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get custom_defined_behaviors
behaviors = data.get('custom_defined_behaviors', '')
lines = behaviors.splitlines()

print(f"Total lines in custom_defined_behaviors: {len(lines)}")
print()

# Find ALL lines with length >= 121
long_lines = []
for i, line in enumerate(lines, 1):
    if len(line) >= 121:
        char_121 = line[120] if len(line) > 120 else ''
        long_lines.append((i, len(line), char_121, line))

print(f"Found {len(long_lines)} lines with length >= 121:")
print()

# Group by character at column 121
from collections import defaultdict
by_char = defaultdict(list)
for line_num, length, char, line in long_lines:
    by_char[char].append((line_num, length, line))

print("Grouped by character at column 121:")
for char in sorted(by_char.keys()):
    lines_with_char = by_char[char]
    print(f"\n  '{char}' (ASCII {ord(char)}): {len(lines_with_char)} lines")

    # Show first few examples
    for line_num, length, line in lines_with_char[:3]:
        context = line[105:135] if len(line) > 105 else line
        print(f"    Line {line_num} (len {length}): ...{context}...")

    if len(lines_with_char) > 3:
        print(f"    ... and {len(lines_with_char) - 3} more")

# Now specifically look for problematic patterns
# Devicetree parser might choke on certain characters at column 121

print("\n" + "="*80)
print("Checking for potentially problematic lines:")
print("="*80)

problematic_chars = ['<', '>', '(', ')', '{', '}', '[', ']', '&', '*', ',']
for line_num, length, char_121, line in long_lines:
    if char_121 in problematic_chars:
        print(f"\nLine {line_num}: char '{char_121}' at column 121")
        print(f"  Full line: {line}")
