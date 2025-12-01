#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

# Get custom_devicetree
devicetree = data.get('custom_devicetree', '')
lines = devicetree.splitlines()

print("Analyzing devicetree syntax:")
print(f"Total lines: {len(lines)}\n")

# Check for any syntax issues
issues = []

# Check for unclosed braces
open_braces = devicetree.count('{')
close_braces = devicetree.count('}')
print(f"Braces: {open_braces} open, {close_braces} close")
if open_braces != close_braces:
    issues.append(f"Unbalanced braces: {open_braces} open, {close_braces} close")

# Check for unclosed angle brackets
open_angle = devicetree.count('<')
close_angle = devicetree.count('>')
print(f"Angle brackets: {open_angle} open, {close_angle} close")
if open_angle != close_angle:
    issues.append(f"Unbalanced angle brackets: {open_angle} open, {close_angle} close")

# Check for unclosed parens
open_paren = devicetree.count('(')
close_paren = devicetree.count(')')
print(f"Parentheses: {open_paren} open, {close_paren} close")
if open_paren != close_paren:
    issues.append(f"Unbalanced parentheses: {open_paren} open, {close_paren} close")

# Check for unmatched preprocessor directives
ifdefs = len(re.findall(r'#ifdef', devicetree))
endifs = len(re.findall(r'#endif', devicetree))
print(f"Preprocessor: {ifdefs} #ifdef, {endifs} #endif")
if ifdefs != endifs:
    issues.append(f"Unmatched #ifdef/#endif: {ifdefs} #ifdef, {endifs} #endif")

# Look for layer-id assignments with non-numeric values (except LAYER_Template in comment)
print("\nChecking layer-id assignments:")
layer_id_pattern = re.compile(r'layer-id\s*=\s*<([^>]+)>')
for match in layer_id_pattern.finditer(devicetree):
    value = match.group(1).strip()
    # Check if it's in a comment
    start_pos = match.start()
    # Look backwards for /* and forwards for */
    before = devicetree[:start_pos]
    after = devicetree[start_pos:]

    last_comment_start = before.rfind('/*')
    last_comment_end = before.rfind('*/')
    next_comment_end = after.find('*/')

    in_comment = (last_comment_start > last_comment_end)

    if not value.isdigit() and not in_comment:
        line_num = before.count('\n') + 1
        issues.append(f"Line {line_num}: layer-id = <{value}> is not numeric")
        print(f"  Line {line_num}: layer-id = <{value}> {'[IN COMMENT]' if in_comment else '[NOT IN COMMENT]'}")
    else:
        line_num = before.count('\n') + 1
        print(f"  Line {line_num}: layer-id = <{value}> {'[IN COMMENT - OK]' if in_comment else '[OK]'}")

if issues:
    print("\n⚠ Found issues:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("\n✓ No obvious syntax issues found")

# Check for any remaining LAYER_ references outside comments
print("\nChecking for LAYER_ references outside comments:")
# Remove all comments first
no_comments = re.sub(r'/\*.*?\*/', '', devicetree, flags=re.DOTALL)
no_comments = re.sub(r'//.*?$', '', no_comments, flags=re.MULTILINE)

layer_refs = re.findall(r'LAYER_\w+', no_comments)
if layer_refs:
    print(f"  Found {len(layer_refs)} LAYER_ references outside comments:")
    for ref in sorted(set(layer_refs)):
        count = layer_refs.count(ref)
        print(f"    {ref}: {count} times")
else:
    print("  ✓ No LAYER_ references outside comments")
