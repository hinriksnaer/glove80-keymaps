#!/usr/bin/env python3
import json

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Extract custom_devicetree
devicetree = data.get('custom_devicetree', '')

# Write to a separate file for easier inspection
with open('extracted_devicetree.dtsi', 'w') as f:
    f.write(devicetree)

print(f"Extracted {len(devicetree)} characters to extracted_devicetree.dtsi")
print(f"Total lines: {len(devicetree.splitlines())}")
