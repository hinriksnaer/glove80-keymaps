# Comprehensive Cleanup Checklist for glovepunk

## Priority 1: Remove Debugging Files (Safe to delete immediately)

### Python Scripts (31 files - created during debugging)
Delete all `.py` files in the root directory:
```bash
rm *.py
```

Files to remove:
- analyze_behaviors.py
- analyze_devicetree.py
- analyze_devicetree_syntax.py
- check_current_state.py
- check_devicetree.py
- check_fields.py
- check_layer_macros_in_dt.py
- check_project_name.py
- check_template.py
- check_thumb_cluster.py
- debug_devicetree_column.py
- examine_dt_sections.py
- extract_devicetree.py
- find_all_col121_issues.py
- find_all_conditionals.py
- find_line_10668.py
- find_unmatched_endif.py
- fix_all_layer_refs.py
- fix_behaviors_layers.py
- fix_devicetree_ifdefs.py
- fix_layer_ids.py
- fix_layers_array.py
- fix_preprocessor_layers.py
- restore_thumb_cluster.py
- search_devicetree_in_behaviors.py
- smart_fix_layers.py
- update_project_name.py
- verify_all_fixed.py
- analyze_for_cleanup.py

### Extracted Files
- extracted_devicetree.dtsi (temporary analysis file)

**Impact**: None - these were only used for debugging
**Command**: `rm *.py extracted_devicetree.dtsi`

---

## Priority 2: Remove Unused Documentation

### README Directory (53 files, ~17MB)
Contains layer diagrams for deleted layouts:
- ColemakDH, Colemak, Dvorak, QWERTY diagrams (no longer needed)
- Engrammer, Engram, Canary diagrams (layouts you removed)
- all-layer-diagrams.pdf (5.9MB, outdated)

**Keep**:
- base-layer-diagram-Enthium.png (your layout)
- base-layer-diagram-Enthium.json

**Delete the rest**:
```bash
cd README
ls | grep -v "Enthium" | xargs rm
cd ..
```

**Impact**: Saves ~16MB, removes confusion from deleted layouts

---

## Priority 3: Simplify Layers (Requires testing)

### Currently Unused Layers
Based on activation analysis, consider removing:

**Layer 7: Gaming** (not activated by any keys currently)
**Layer 8: Factory** (not activated by any keys currently)
**Layer 10: Magic** (activated only 0 times, but &magic might be special)

**How to verify usage**:
1. Check if you actually use Gaming layer
2. Factory layer is usually for RGB/bluetooth controls
3. Magic layer is for system controls

**If removing**, you'll need to:
1. Delete from layer_names array
2. Delete from layers array
3. Re-index remaining layers
4. Update all layer references

**Impact**: Further simplifies configuration (11 → 8 layers)

---

## Priority 4: Simplify Complex Features (Advanced)

### RGB Underglow Configuration (~98 lines in custom_devicetree)
If you don't use per-key RGB lighting:
- Remove entire `underglow-layer` section from custom_devicetree
- Keep simple solid color underglow only

**Impact**: Cleaner devicetree, ~3KB savings
**Risk**: Lose per-layer RGB colors
**Recommendation**: Keep if you like the visual feedback

### Emoji/Unicode Support (~827 references)
If you never type emoji or special Unicode characters:
- Remove Unicode macro definitions
- Simplifies custom_defined_behaviors significantly

**Impact**: ~50KB+ savings, much simpler configuration
**Risk**: Can't type special characters/emoji
**Recommendation**: Remove if you don't use

### Timing Configurations (165 #define statements)
The configuration has separate timing for each finger position:
- PINKY_HOLDING_TIME, RINGY_HOLDING_TIME, MIDDY_HOLDING_TIME, etc.

Could simplify to:
- Single HOLDING_TIME for all fingers
- Reduces from ~165 to ~10 timing parameters

**Impact**: Simpler configuration, easier to tune
**Risk**: Less precise control per finger
**Recommendation**: Simplify after you're comfortable with the keymap

### Home Row Mod Behaviors (73 hold-tap definitions)
Positional hold-tap with per-finger customization

Could simplify to:
- One hold-tap behavior for all home row keys
- Reduces complexity significantly

**Impact**: Much simpler configuration
**Risk**: Less precise timing control
**Recommendation**: Keep for now, simplify later if needed

---

## Priority 5: Build System Files (Optional)

### Files You Don't Need Locally
- `device.dtsi` - large file (24KB), only needed for reference
- `keymap.dtsi` - generated file, not needed in repo
- `Rakefile` - build system you're not using
- `flash` script - custom flash script (might be useful)
- `keymap.zmk`, `keymap.json.erb` - template files

**What to keep**:
- `keymap.json` - your main configuration
- `README.md` - documentation
- `.github/` - CI/CD workflows (if you want auto-builds)

**What you can delete**:
```bash
rm device.dtsi keymap.dtsi Rakefile keymap.zmk *.erb *.yaml
```

**Impact**: Cleaner repo, only essential files remain

---

## Priority 6: Git History Cleanup (Optional)

Your git history has 20+ commits from debugging sessions.

Options:
1. **Keep as-is**: Preserves full history
2. **Squash recent commits**: Combine debugging commits into one
3. **Fresh start**: Create new initial commit with clean state

**Recommendation**: Keep as-is, it documents the journey

---

## Priority 7: Original Source Files (Optional)

### Layouts Directory
Check if `layouts/` contains anything you need:
```bash
ls layouts/
```

If it's just template files from the original repo, you can remove it.

---

## Quick Cleanup Script

```bash
#!/bin/bash
# Quick cleanup - removes only safe-to-delete files

echo "Removing debugging Python scripts..."
rm -f *.py

echo "Removing extracted analysis files..."
rm -f extracted_devicetree.dtsi

echo "Cleaning up old layout diagrams..."
cd README
ls | grep -v "Enthium" | grep -v "^\." | xargs rm -f
cd ..

echo "Cleanup complete!"
echo ""
echo "Current directory size:"
du -sh .
```

Save as `cleanup.sh`, run with: `chmod +x cleanup.sh && ./cleanup.sh`

---

## Summary by Impact

### Low Risk (Do First):
✅ Delete all .py debugging scripts
✅ Delete extracted_devicetree.dtsi
✅ Remove old layout diagrams from README/
✅ Remove build system files (Rakefile, *.erb, device.dtsi)

### Medium Risk (Test First):
⚠️ Remove unused layers (Gaming, Factory)
⚠️ Remove Unicode/Emoji support if not used
⚠️ Simplify RGB underglow

### High Risk (Advanced Users):
🔴 Simplify timing configurations
🔴 Consolidate home row mod behaviors
🔴 Squash git history

---

## Size Savings Estimate

| Action | Current | After | Savings |
|--------|---------|-------|---------|
| Remove .py files | 31 files | 0 files | ~200KB |
| Clean README/ | 53 files/17MB | 2 files/500KB | ~16.5MB |
| Remove Unicode | 409KB json | ~360KB json | ~50KB |
| Remove RGB config | 13.2KB devicetree | ~10KB | ~3KB |
| **Total** | **~17.7MB** | **~1.1MB** | **~16.6MB** |

---

## Your Current Configuration Stats

- **Total Layers**: 11 (could reduce to 8-9)
- **keymap.json Size**: 409KB
- **Active Features**:
  - ✅ Home row mods (73 behaviors)
  - ✅ RGB underglow per-layer
  - ✅ Unicode/Emoji support (827 references)
  - ✅ Custom timing per finger (165 parameters)
  - ✅ 372 mod-morph behaviors
  - ❌ Combos (0 defined)
  - ❌ Macros (0 defined)

**Activated Layers**: Enthium, Typing, Cursor, Number, Function, Symbol, System, Lower
**Potentially Unused**: Gaming, Factory, Magic
