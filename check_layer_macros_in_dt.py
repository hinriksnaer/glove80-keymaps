#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get both fields
behaviors = data.get('custom_defined_behaviors', '')
devicetree = data.get('custom_devicetree', '')

print("Checking for LAYER_ macro usage in devicetree contexts:")
print("="*80)

# In devicetree contexts, LAYER_ macros need to be defined BEFORE they're used
# Check if LAYER_ definitions come before devicetree sections

behaviors_lines = behaviors.splitlines()

# Find where LAYER_ definitions are
layer_define_line = -1
for i, line in enumerate(behaviors_lines, 1):
    if '#define LAYER_Enthium' in line:
        layer_define_line = i
        print(f"LAYER_ definitions start at line: {layer_define_line}")
        break

# Find where devicetree sections start (& syntax)
first_dt_line = -1
for i, line in enumerate(behaviors_lines, 1):
    if re.match(r'^\s*&\w+\s*{', line):
        first_dt_line = i
        print(f"First devicetree overlay at line: {first_dt_line}")
        print(f"  Content: {line}")
        break

if layer_define_line > 0 and first_dt_line > 0:
    if layer_define_line < first_dt_line:
        print("\n✓ LAYER_ definitions come BEFORE devicetree overlays (good)")
    else:
        print("\n✗ LAYER_ definitions come AFTER devicetree overlays (BAD!)")
        print("  This could cause undefined macro errors in devicetree")

# Check for LAYER_ usage in devicetree sections
print("\n" + "="*80)
print("Checking devicetree sections for LAYER_ references:")
print("="*80)

# Find all devicetree overlay blocks
dt_blocks = []
in_dt_block = False
block_start = -1

for i, line in enumerate(behaviors_lines, 1):
    if re.match(r'^\s*&\w+\s*{', line):
        in_dt_block = True
        block_start = i
        block_lines = [line]
    elif in_dt_block:
        block_lines.append(line)
        if '};' in line:
            in_dt_block = False
            dt_blocks.append((block_start, block_lines))

print(f"Found {len(dt_blocks)} devicetree overlay blocks\n")

for block_start_line, block_lines in dt_blocks:
    block_text = '\n'.join(block_lines)
    # Check for LAYER_ references
    layer_refs = re.findall(r'LAYER_\w+', block_text)
    if layer_refs:
        print(f"Block starting at line {block_start_line} has LAYER_ references:")
        for ref in set(layer_refs):
            print(f"  {ref}")
        print(f"  Block preview:")
        for line in block_lines[:10]:
            print(f"    {line}")
        print()

# Also check custom_devicetree
print("="*80)
print("Checking custom_devicetree field:")
print("="*80)

# The custom_devicetree is added AFTER custom_defined_behaviors in build.keymap
# So LAYER_ definitions from behaviors should be available

layer_refs_in_dt = re.findall(r'LAYER_\w+', devicetree)
if layer_refs_in_dt:
    print(f"Found {len(layer_refs_in_dt)} LAYER_ references in custom_devicetree:")
    for ref in sorted(set(layer_refs_in_dt)):
        count = layer_refs_in_dt.count(ref)
        print(f"  {ref}: {count} times")

    # This is OK because custom_devicetree comes AFTER custom_defined_behaviors
    # where LAYER_ macros are defined
    print("\n  Note: These references come AFTER LAYER_ definitions, so should be OK")
else:
    print("No LAYER_ references in custom_devicetree")
