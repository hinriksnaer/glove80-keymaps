#!/usr/bin/env python3
import json
import re

# Layer mapping
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

# Get custom_devicetree
devicetree = data.get('custom_devicetree', '')

print("Fixing #ifdef directives in custom_devicetree:")
print(f"Original length: {len(devicetree)} characters\n")

# Count before
ifdef_nums = re.findall(r'#ifdef\s+\d+', devicetree)
print(f"Before fix: {len(ifdef_nums)} #ifdef with numbers")
for match in set(ifdef_nums):
    print(f"  {match}")

# Fix #ifdef NUMBER -> #ifdef LAYER_Name
for layer_id, layer_name in layer_mapping.items():
    # Match #ifdef followed by whitespace and the number
    pattern = rf'#ifdef\s+{layer_id}\b'
    replacement = f'#ifdef {layer_name}'
    devicetree = re.sub(pattern, replacement, devicetree)

    # Match #ifndef followed by whitespace and the number
    pattern = rf'#ifndef\s+{layer_id}\b'
    replacement = f'#ifndef {layer_name}'
    devicetree = re.sub(pattern, replacement, devicetree)

# Count after
ifdef_nums = re.findall(r'#ifdef\s+\d+', devicetree)
print(f"\nAfter fix: {len(ifdef_nums)} #ifdef with numbers")

# Update the JSON
data['custom_devicetree'] = devicetree

# Write back
with open('keymap.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nUpdated length: {len(devicetree)} characters")
print("✓ Fixed #ifdef directives in custom_devicetree!")
