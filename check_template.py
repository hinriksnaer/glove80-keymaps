#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get the custom_devicetree field
devicetree = data.get('custom_devicetree', '')

# Find the context around LAYER_Template
template_idx = devicetree.find('LAYER_Template')
if template_idx != -1:
    # Get 200 characters before and after
    start = max(0, template_idx - 200)
    end = min(len(devicetree), template_idx + 200)
    context = devicetree[start:end]

    print("Context around LAYER_Template:")
    print("-" * 80)
    print(context)
    print("-" * 80)

    # Check if it's in a comment
    # Look backwards for /* or forward for */
    before = devicetree[:template_idx]
    after = devicetree[template_idx:]

    # Check if we're in a /* */ style comment
    last_comment_start = before.rfind('/*')
    last_comment_end = before.rfind('*/')
    next_comment_end = after.find('*/')

    if last_comment_start > last_comment_end:
        print("\n✓ LAYER_Template is inside a /* */ comment block (OK to leave)")
    else:
        print("\n✗ LAYER_Template is NOT in a comment - needs to be fixed or removed")
