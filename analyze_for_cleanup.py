#!/usr/bin/env python3
import json
import re

# Read the keymap.json file
with open('keymap.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("KEYMAP CONFIGURATION ANALYSIS FOR CLEANUP")
print("=" * 80)

# 1. Layer usage analysis
print("\n1. LAYERS (11 total):")
print("-" * 40)
layer_names = data.get('layer_names', [])
for i, name in enumerate(layer_names):
    print(f"  {i}. {name}")

# 2. Check for potentially unused features
behaviors = data.get('custom_defined_behaviors', '')
devicetree = data.get('custom_devicetree', '')

print("\n2. COMPLEX FEATURES THAT COULD BE SIMPLIFIED:")
print("-" * 40)

# RGB underglow
if 'rgb' in devicetree.lower() or 'underglow' in devicetree.lower():
    rgb_lines = len([line for line in devicetree.splitlines() if 'rgb' in line.lower() or '&ug' in line])
    print(f"  • RGB underglow configuration: ~{rgb_lines} lines")
    print(f"    └─ Custom per-key RGB for each layer")

# Mouse keys
if 'mouse' in behaviors.lower():
    print(f"  • Mouse key macros (from deleted Mouse layers)")

# Emoji/Unicode
if 'unicode' in behaviors.lower() or 'emoji' in behaviors.lower():
    emoji_count = len(re.findall(r'emoji', behaviors.lower()))
    print(f"  • Unicode/Emoji support: ~{emoji_count} references")

# Complex timing configurations
timing_defines = len(re.findall(r'#define \w+_(HOLDING_TIME|DECAY|RESOLUTION)', behaviors))
print(f"  • Timing configurations: {timing_defines} #define statements")
print(f"    └─ Separate timings for each finger position")

# Home row mods
if 'homey' in behaviors.lower():
    print(f"  • Home row mod behaviors (positional hold-tap)")

# Combos
combos = data.get('combos', [])
print(f"  • Combos: {len(combos)} defined")

# Macros
macros = data.get('macros', [])
print(f"  • Macros: {len(macros)} defined")

# 3. Check layer usage in bindings
print("\n3. LAYER ACTIVATION ANALYSIS:")
print("-" * 40)

layers_str = json.dumps(data['layers'])
layer_activations = {}

for i in range(11):
    # Count how many times each layer is activated
    count = layers_str.count(f'&mo {i}') + layers_str.count(f'&tog {i}') + layers_str.count(f'&thumb {i}')
    if count > 0:
        layer_activations[i] = count

print("  Layers accessed from key bindings:")
for layer_id, count in sorted(layer_activations.items()):
    layer_name = layer_names[layer_id] if layer_id < len(layer_names) else f"Layer {layer_id}"
    print(f"    {layer_id}. {layer_name}: {count} activations")

# 4. Size analysis
print("\n4. FILE SIZE ANALYSIS:")
print("-" * 40)
print(f"  • keymap.json: {len(json.dumps(data)) / 1024:.1f} KB")
print(f"  • custom_defined_behaviors: {len(behaviors) / 1024:.1f} KB ({len(behaviors.splitlines())} lines)")
print(f"  • custom_devicetree: {len(devicetree) / 1024:.1f} KB ({len(devicetree.splitlines())} lines)")

# 5. Custom behaviors
custom_behaviors = data.get('custom_defined_behaviors', '')
print("\n5. CUSTOM BEHAVIOR DEFINITIONS:")
print("-" * 40)

# Count different types
behavior_types = {
    'hold-tap (home row mods)': len(re.findall(r'compatible\s*=\s*"zmk,behavior-hold-tap"', custom_behaviors)),
    'mod-morph': len(re.findall(r'compatible\s*=\s*"zmk,behavior-mod-morph"', custom_behaviors)),
    'macros': len(re.findall(r'compatible\s*=\s*"zmk,behavior-macro"', custom_behaviors)),
    'tap-dance': len(re.findall(r'compatible\s*=\s*"zmk,behavior-tap-dance"', custom_behaviors)),
}

for behavior_type, count in behavior_types.items():
    if count > 0:
        print(f"  • {behavior_type}: {count}")

print("\n" + "=" * 80)
