#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get custom_defined_behaviors
behaviors = data.get('custom_defined_behaviors', '')

print("Searching for devicetree overlay syntax in custom_defined_behaviors:")
print()

# Devicetree overlays use "&" syntax and braces
# Look for patterns like: &label { ... }

# Find all lines with devicetree-like syntax
dt_pattern = re.compile(r'^\s*&\w+\s*{', re.MULTILINE)
matches = dt_pattern.finditer(behaviors)

dt_sections = []
for match in matches:
    start = match.start()
    # Find the line number
    line_num = behaviors[:start].count('\n') + 1
    line_content = behaviors[start:start+100].split('\n')[0]
    dt_sections.append((line_num, line_content))

print(f"Found {len(dt_sections)} devicetree overlay sections:")
for line_num, content in dt_sections[:20]:  # Show first 20
    print(f"  Line {line_num}: {content}")

if len(dt_sections) > 20:
    print(f"  ... and {len(dt_sections) - 20} more")

# Also check for layer definitions in devicetree format
print("\n" + "="*80)
print("Looking for layer definitions in devicetree format:")
print("="*80)

layer_dt_pattern = re.compile(r'^\s*\w+_layer\s*{', re.MULTILINE)
layer_matches = layer_dt_pattern.finditer(behaviors)

for match in layer_matches:
    start = match.start()
    line_num = behaviors[:start].count('\n') + 1
    # Get surrounding context
    context_start = max(0, start - 200)
    context_end = min(len(behaviors), start + 500)
    context = behaviors[context_start:context_end]

    print(f"\nFound at line {line_num}:")
    print(context)
    print("\n" + "-"*80)

# Check for RGB underglow definitions
print("\n" + "="*80)
print("Looking for RGB underglow layer definitions:")
print("="*80)

rgb_pattern = re.compile(r'#ifdef\s+LAYER_\w+.*?#endif', re.DOTALL)
rgb_matches = list(rgb_pattern.finditer(behaviors))

print(f"Found {len(rgb_matches)} #ifdef LAYER blocks")

# Check if any of these blocks contain devicetree syntax at column 121
for i, match in enumerate(rgb_matches):
    block_start = match.start()
    block_end = match.end()
    block = match.group()
    lines = block.splitlines()

    # Check if any line in this block is >= 121 chars
    for j, line in enumerate(lines):
        if len(line) >= 121:
            line_num = behaviors[:block_start].count('\n') + j + 1
            char_121 = line[120]
            print(f"\n  Block {i+1}, line {line_num} has length {len(line)}, char at 121: '{char_121}'")
            print(f"    Context: ...{line[100:140]}...")
