#!/usr/bin/env python3
import json
import re

# Current layer mapping after removals
layer_mapping = {
    'LAYER_Enthium': 0,
    'LAYER_Typing': 1,
    'LAYER_Cursor': 2,
    'LAYER_Number': 3,
    'LAYER_Function': 4,
    'LAYER_Symbol': 5,
    'LAYER_System': 6,
    'LAYER_Gaming': 7,
    'LAYER_Factory': 8,
    'LAYER_Lower': 9,
    'LAYER_Magic': 10
}

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get the custom_defined_behaviors field
behaviors = data.get('custom_defined_behaviors', '')

print("Smart layer fix - adding #define statements")
print(f"Original length: {len(behaviors)} characters")

# First, check if there are existing #define statements for layers
existing_defines = re.findall(r'#define\s+(LAYER_\w+)\s+(\d+)', behaviors)
print(f"\nFound {len(existing_defines)} existing layer #define statements:")
for define_name, define_value in existing_defines:
    print(f"  {define_name} = {define_value}")

# Create #define statements for all our layers
layer_defines = "\n// Layer definitions\n"
for layer_name, layer_id in sorted(layer_mapping.items(), key=lambda x: x[1]):
    layer_defines += f"#define {layer_name} {layer_id}\n"

# Insert the defines at the beginning, after any existing header comments
# Look for the first #define or #include to insert before it
first_directive = re.search(r'^#(?:define|include|ifndef|ifdef)', behaviors, re.MULTILINE)
if first_directive:
    insert_pos = first_directive.start()
    behaviors = behaviors[:insert_pos] + layer_defines + "\n" + behaviors[insert_pos:]
else:
    # No directives found, insert at the beginning
    behaviors = layer_defines + "\n" + behaviors

# Update the JSON
data['custom_defined_behaviors'] = behaviors

# Write back
with open('keymap.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"\nAdded {len(layer_mapping)} layer #define statements")
print(f"New length: {len(behaviors)} characters")
print("\nLayer definitions added successfully!")
