#!/usr/bin/env python3
import json

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get layer 0 (Enthium base layer)
layer0 = data['layers'][0]

print("Restoring original thumb cluster configuration:\n")

# Position 57: Restore to System layer + ENTER
# LAYER_System is now layer 6
print("Position 57:")
print(f"  Before: {layer0[57]}")
layer0[57] = {
    "value": "Custom",
    "params": [
        {
            "value": "&thumb 6 ENTER",
            "params": []
        }
    ]
}
print(f"  After:  {layer0[57]}")
print("  → Restored to System layer (6) + ENTER\n")

# Position 68: Since Emoji layer was deleted, change to just BSLH key
# or we could use System layer here too
print("Position 68:")
print(f"  Before: {layer0[68]}")
layer0[68] = {
    "value": "&kp",
    "params": [
        {
            "value": "BSLH",
            "params": []
        }
    ]
}
print(f"  After:  {layer0[68]}")
print("  → Changed to simple BSLH key (Emoji layer was deleted)\n")

# Update the layers array
data['layers'][0] = layer0

# Write back
with open('keymap.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✓ Thumb cluster restored to original configuration")
