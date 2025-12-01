#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get custom_devicetree
devicetree = data.get('custom_devicetree', '')
lines = devicetree.splitlines()

print("Finding ALL conditional directives:\n")

# Track the stack of conditionals
stack = []
issues = []

for i, line in enumerate(lines, 1):
    stripped = line.strip()

    # Match any conditional start
    if re.match(r'#if\s', stripped) or stripped.startswith('#ifdef') or stripped.startswith('#ifndef'):
        # Push onto stack
        stack.append((i, stripped))
        indent = '  ' * len(stack)
        print(f"{indent}Line {i:4d}: {stripped}")

    elif stripped.startswith('#endif'):
        if stack:
            # Pop from stack
            matched_line, matched_directive = stack.pop()
            indent = '  ' * (len(stack) + 1)
            print(f"{indent}Line {i:4d}: #endif (closes line {matched_line})")
        else:
            # No matching #if
            issues.append((i, stripped, "No matching #if/#ifdef"))
            print(f"Line {i:4d}: #endif ⚠ NO MATCHING #if/#ifdef!")

    elif stripped.startswith('#elif') or stripped.startswith('#else'):
        if stack:
            matched_line, matched_directive = stack[-1]
            indent = '  ' * len(stack)
            print(f"{indent}Line {i:4d}: {stripped.split()[0]} (belongs to line {matched_line})")
        else:
            issues.append((i, stripped, "No matching #if/#ifdef"))
            print(f"Line {i:4d}: {stripped} ⚠ NO MATCHING #if/#ifdef!")

# Check if any conditionals remain unmatched
if stack:
    print("\n⚠ Unmatched conditional directives:")
    for line_num, directive in stack:
        print(f"  Line {line_num}: {directive} (no matching #endif)")
        issues.append((line_num, directive, "No matching #endif"))

if issues:
    print(f"\n⚠ Found {len(issues)} issues with conditional directives")
else:
    print("\n✓ All conditional directives are properly matched")

# Count totals
if_count = len(re.findall(r'#if\s', devicetree))
ifdef_count = len(re.findall(r'#ifdef', devicetree))
ifndef_count = len(re.findall(r'#ifndef', devicetree))
endif_count = len(re.findall(r'#endif', devicetree))

print(f"\nTotal counts:")
print(f"  #if: {if_count}")
print(f"  #ifdef: {ifdef_count}")
print(f"  #ifndef: {ifndef_count}")
print(f"  Total conditional starts: {if_count + ifdef_count + ifndef_count}")
print(f"  #endif: {endif_count}")
print(f"  Balance: {endif_count - (if_count + ifdef_count + ifndef_count)}")
