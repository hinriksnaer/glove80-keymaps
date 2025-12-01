#!/usr/bin/env python3
import json

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

print("Updating project name to 'glovepunk':\n")

# Update title
old_title = data.get('title', '')
data['title'] = 'glovepunk'
print(f"title: '{old_title}' → 'glovepunk'")

# Update notes to remove old references
old_notes = data.get('notes', '')
data['notes'] = 'Custom Glove80 keymap configuration'
print(f"\nnotes: Updated to generic description")

# Write back
with open('keymap.json', 'w') as f:
    json.dump(data, f, indent=2)

print("\n✓ Project name updated to 'glovepunk'")
