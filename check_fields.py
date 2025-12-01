#!/usr/bin/env python3
import json

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# List all top-level fields
print("Top-level fields in keymap.json:")
for key in data.keys():
    value = data[key]
    if isinstance(value, str):
        length = len(value)
        print(f"  {key}: string, {length} characters")
    elif isinstance(value, list):
        print(f"  {key}: list, {len(value)} items")
    elif isinstance(value, dict):
        print(f"  {key}: dict, {len(value)} keys")
    else:
        print(f"  {key}: {type(value).__name__}")

# Check for devicetree-related fields
print("\nDevicetree-related fields:")
for key in data.keys():
    if 'device' in key.lower() or 'tree' in key.lower():
        print(f"  {key}")
