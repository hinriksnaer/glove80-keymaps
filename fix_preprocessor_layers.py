#!/usr/bin/env python3
import json
import re

# Current layer mapping after removals
layer_mapping = {
    0: 'LAYER_Enthium',
    1: 'LAYER_Typing',
    2: 'LAYER_Cursor',
    3: 'LAYER_Number',
    4: 'LAYER_Function',
    5: 'LAYER_Symbol',
    6: 'LAYER_System',
    7: 'LAYER_Gaming',
    8: 'LAYER_Factory',
    9: 'LAYER_Lower',
    10: 'LAYER_Magic'
}

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get the custom_defined_behaviors field
behaviors = data.get('custom_defined_behaviors', '')

print("Fixing preprocessor directives:")
print(f"Original length: {len(behaviors)} characters\n")

# Count issues before
ifdef_nums = re.findall(r'#ifdef\s+\d+', behaviors)
defined_nums = re.findall(r'defined\(\d+\)', behaviors)
print(f"Before fix:")
print(f"  #ifdef with numbers: {len(ifdef_nums)}")
print(f"  defined() with numbers: {len(defined_nums)}")

# Fix #ifdef NUMBER -> #ifdef LAYER_Name
for layer_id, layer_name in layer_mapping.items():
    # Match #ifdef followed by whitespace and the number
    pattern = rf'#ifdef\s+{layer_id}\b'
    replacement = f'#ifdef {layer_name}'
    behaviors = re.sub(pattern, replacement, behaviors)

    # Match #ifndef followed by whitespace and the number
    pattern = rf'#ifndef\s+{layer_id}\b'
    replacement = f'#ifndef {layer_name}'
    behaviors = re.sub(pattern, replacement, behaviors)

# Fix defined(NUMBER) -> defined(LAYER_Name)
for layer_id, layer_name in layer_mapping.items():
    pattern = rf'defined\({layer_id}\)'
    replacement = f'defined({layer_name})'
    behaviors = re.sub(pattern, replacement, behaviors)

# Count issues after
ifdef_nums = re.findall(r'#ifdef\s+\d+', behaviors)
defined_nums = re.findall(r'defined\(\d+\)', behaviors)
print(f"\nAfter fix:")
print(f"  #ifdef with numbers: {len(ifdef_nums)}")
print(f"  defined() with numbers: {len(defined_nums)}")

# Now add #define statements at the beginning
layer_defines = "// Layer index definitions for preprocessor\n"
for layer_id, layer_name in sorted(layer_mapping.items()):
    layer_defines += f"#define {layer_name} {layer_id}\n"
layer_defines += "\n"

# Find a good place to insert the defines
# Look for the first real code (after any initial comments)
# Let's insert right at the beginning
behaviors = layer_defines + behaviors

# Update the JSON
data['custom_defined_behaviors'] = behaviors

# Write back
with open('keymap.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nAdded {len(layer_mapping)} #define statements")
print(f"New length: {len(behaviors)} characters")
print("\n✓ Preprocessor directives fixed!")
