#!/usr/bin/env python3
import json

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get custom_defined_behaviors
behaviors = data.get('custom_defined_behaviors', '')
lines = behaviors.splitlines()

print("Examining devicetree sections starting around line 9888:")
print("="*80)

# Show lines 9880-9960 (around the devicetree sections)
start_line = 9880
end_line = 9960

for i in range(start_line - 1, min(end_line, len(lines))):
    line = lines[i]
    line_num = i + 1
    length = len(line)

    # Mark lines that are suspicious
    marker = ""
    if length >= 121:
        char_121 = line[120]
        marker = f"  <-- LENGTH {length}, char at 121: '{char_121}'"

    print(f"{line_num:5d}: {line}{marker}")

# Now specifically check if any of these lines have issues
print("\n" + "="*80)
print("Lines with length >= 121 in the devicetree section:")
print("="*80)

for i in range(9880 - 1, min(9960, len(lines))):
    line = lines[i]
    line_num = i + 1

    if len(line) >= 121:
        char_121 = line[120]
        print(f"\nLine {line_num} (length {len(line)}):")
        print(f"  Full line: {line}")
        print(f"  Char at 121: '{char_121}' (ASCII {ord(char_121)})")
        print(f"  Context [110-135]: ...{line[110:135]}...")
