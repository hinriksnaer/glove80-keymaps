#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get the custom_defined_behaviors field
behaviors = data.get('custom_defined_behaviors', '')

print("Custom defined behaviors analysis:")
print(f"Total length: {len(behaviors)} characters")
print(f"Total lines: {len(behaviors.splitlines())}")
print()

# Split into lines and check lines around the error location
# Error is at line 10655, but we need to account for what comes before
lines = behaviors.splitlines()

# Check lines with potential issues around column 121
print("Looking for lines with potential syntax issues at column 121:")
issue_count = 0
for i, line in enumerate(lines, 1):
    if len(line) >= 121:
        # Check what's at column 121 (index 120)
        char_at_121 = line[120] if len(line) > 120 else ''

        # Look for suspicious patterns
        context_before = line[100:121] if len(line) > 100 else line
        context_after = line[121:141] if len(line) > 121 else ''

        # Check for syntax issues
        has_issue = False

        # Check for LAYER_ references
        if 'LAYER_' in context_before or 'LAYER_' in context_after:
            has_issue = True
            print(f"\nLine {i} (length {len(line)}):")
            print(f"  Has LAYER_ reference near column 121")
            print(f"  Context: ...{context_before}[{char_at_121}]{context_after}...")
            issue_count += 1

        # Check for unbalanced brackets
        elif char_at_121 in '<>':
            print(f"\nLine {i} (length {len(line)}):")
            print(f"  Bracket at column 121: '{char_at_121}'")
            print(f"  Context: ...{context_before}[{char_at_121}]{context_after}...")
            issue_count += 1

        # Check for unexpected characters at 121
        elif not char_at_121.isalnum() and char_at_121 not in ' \t_-,.;:(){}[]<>/*&|=+':
            print(f"\nLine {i} (length {len(line)}):")
            print(f"  Unusual character at column 121: '{char_at_121}' (ord={ord(char_at_121)})")
            print(f"  Context: ...{context_before}[{char_at_121}]{context_after}...")
            issue_count += 1

if issue_count == 0:
    print("No obvious syntax issues found at column 121")
    print("\nShowing first 10 lines longer than 120 characters:")
    count = 0
    for i, line in enumerate(lines, 1):
        if len(line) > 120 and count < 10:
            char_at_121 = line[120] if len(line) > 120 else ''
            context = line[110:135] if len(line) > 110 else line
            print(f"\nLine {i} (length {len(line)}):")
            print(f"  Column 121: '{char_at_121}'")
            print(f"  Context [110-135]: ...{context}...")
            count += 1

# Check for any remaining LAYER_ references anywhere
print("\n\nSearching for all LAYER_ references:")
layer_refs = re.findall(r'LAYER_\w+', behaviors)
if layer_refs:
    print(f"Found {len(layer_refs)} LAYER_ references:")
    for ref in sorted(set(layer_refs)):
        count = layer_refs.count(ref)
        print(f"  {ref}: {count} occurrences")
else:
    print("No LAYER_ references found")
