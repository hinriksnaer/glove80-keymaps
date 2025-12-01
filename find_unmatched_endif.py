#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get custom_devicetree
devicetree = data.get('custom_devicetree', '')
lines = devicetree.splitlines()

print("Finding unmatched #ifdef/#endif directives:\n")

# Track the stack of #ifdef directives
ifdef_stack = []
issues = []

for i, line in enumerate(lines, 1):
    stripped = line.strip()

    if stripped.startswith('#ifdef') or stripped.startswith('#ifndef'):
        # Push onto stack
        ifdef_stack.append((i, stripped))
        print(f"Line {i:4d}: {stripped}")

    elif stripped.startswith('#endif'):
        print(f"Line {i:4d}: {stripped}")
        if ifdef_stack:
            # Pop from stack
            matched_line, matched_directive = ifdef_stack.pop()
            print(f"           └─ matches line {matched_line}: {matched_directive}")
        else:
            # No matching #ifdef
            issues.append((i, stripped, "No matching #ifdef"))
            print(f"           └─ ⚠ NO MATCHING #ifdef!")

    elif stripped.startswith('#elif') or stripped.startswith('#else'):
        print(f"Line {i:4d}: {stripped}")
        if ifdef_stack:
            matched_line, matched_directive = ifdef_stack[-1]
            print(f"           └─ belongs to line {matched_line}: {matched_directive}")
        else:
            issues.append((i, stripped, "No matching #ifdef"))
            print(f"           └─ ⚠ NO MATCHING #ifdef!")

# Check if any #ifdef remain unmatched
if ifdef_stack:
    print("\n⚠ Unmatched #ifdef directives:")
    for line_num, directive in ifdef_stack:
        print(f"  Line {line_num}: {directive} (no matching #endif)")
        issues.append((line_num, directive, "No matching #endif"))

if issues:
    print(f"\n⚠ Found {len(issues)} issues:")
    for line_num, directive, issue in issues:
        print(f"  Line {line_num}: {directive}")
        print(f"    └─ {issue}")
else:
    print("\n✓ All #ifdef/#endif directives are properly matched")
