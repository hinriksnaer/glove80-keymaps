#!/bin/bash
# Safe cleanup script for glovepunk keymap
# Removes debugging files and outdated documentation

set -e

echo "============================================"
echo "glovepunk Cleanup Script"
echo "============================================"
echo ""

# Count files before
echo "Current state:"
echo "  Python scripts: $(ls *.py 2>/dev/null | wc -l)"
echo "  README files: $(ls README/ 2>/dev/null | wc -l)"
echo "  Directory size: $(du -sh . | cut -f1)"
echo ""

read -p "Remove debugging Python scripts? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "  Removing Python scripts..."
    rm -f *.py
    echo "  ✓ Done"
fi

read -p "Remove extracted analysis files? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "  Removing extracted files..."
    rm -f extracted_devicetree.dtsi
    echo "  ✓ Done"
fi

read -p "Remove old layout diagrams (keep Enthium only)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "  Cleaning README directory..."
    cd README
    # Remove everything except Enthium files
    ls | grep -v "Enthium" | grep -v "^\." | xargs -r rm -f
    cd ..
    echo "  ✓ Done"
fi

read -p "Remove build system files (Rakefile, device.dtsi, etc.)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "  Removing build system files..."
    rm -f Rakefile device.dtsi keymap.dtsi keymap.zmk *.erb *.yaml
    echo "  ✓ Done"
fi

echo ""
echo "============================================"
echo "Cleanup complete!"
echo "============================================"
echo ""
echo "Final state:"
echo "  Python scripts: $(ls *.py 2>/dev/null | wc -l)"
echo "  README files: $(ls README/ 2>/dev/null | wc -l)"
echo "  Directory size: $(du -sh . | cut -f1)"
echo ""
echo "Essential files kept:"
echo "  ✓ keymap.json (your main configuration)"
echo "  ✓ README.md (documentation)"
echo "  ✓ flash script (for flashing firmware)"
echo ""
