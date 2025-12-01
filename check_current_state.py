#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get the custom_defined_behaviors field
behaviors = data.get('custom_defined_behaviors', '')

# Find lines with the problematic patterns from the error
lines = behaviors.splitlines()

print("Checking for problematic patterns:\n")

# Check line 767
if len(lines) >= 767:
    print(f"Line 767: {lines[766]}")

# Check around lines 906, 923
if len(lines) >= 923:
    print(f"Line 906: {lines[905]}")
    print(f"Line 923: {lines[922]}")

# Check lines 1004, 1012
if len(lines) >= 1012:
    print(f"Line 1004: {lines[1003]}")
    print(f"Line 1012: {lines[1011]}")

print("\n" + "="*80)
print("Searching for all #ifdef and #if defined with numbers:")
print("="*80)

# Find all #ifdef with numbers
ifdef_nums = re.findall(r'#ifdef\s+(\d+)', behaviors)
if ifdef_nums:
    print(f"\n#ifdef with numbers: {len(ifdef_nums)} occurrences")
    for num in set(ifdef_nums):
        count = ifdef_nums.count(num)
        print(f"  #ifdef {num}: {count} times")

# Find all #if defined() with numbers
defined_nums = re.findall(r'defined\((\d+)\)', behaviors)
if defined_nums:
    print(f"\ndefined() with numbers: {len(defined_nums)} occurrences")
    for num in set(defined_nums):
        count = defined_nums.count(num)
        print(f"  defined({num}): {count} times")

# Find patterns like: #if defined(SOMETHING) && defined(NUMBER)
mixed_defined = re.findall(r'#if defined\([^)]+\) && defined\((\d+)\)', behaviors)
if mixed_defined:
    print(f"\n#if with mixed defined: {len(mixed_defined)} occurrences")

# Check if there are existing LAYER_ definitions
layer_defines = re.findall(r'#define\s+(LAYER_\w+)\s+(\d+)', behaviors)
print(f"\n\nExisting LAYER_ #define statements: {len(layer_defines)}")
for name, value in layer_defines[:20]:  # Show first 20
    print(f"  #define {name} {value}")
if len(layer_defines) > 20:
    print(f"  ... and {len(layer_defines) - 20} more")
