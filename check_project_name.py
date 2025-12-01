#!/usr/bin/env python3
import json

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

print("Current project information in keymap.json:\n")

# Check common fields that might contain the project name
fields_to_check = ['title', 'name', 'notes', 'creator', 'description']

for field in fields_to_check:
    if field in data:
        value = data[field]
        print(f"{field}: {value}")
