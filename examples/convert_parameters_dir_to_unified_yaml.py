"""
Example script to convert a legacy parameters/ directory (with multiple YAML/.par files)
to a single unified parameters.yaml file, and back for backward compatibility.
"""
from openptv.parameters import UnifiedParameters
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Convert legacy parameters/ dir to unified YAML and back.")
parser.add_argument('param_dir', type=str, help='Path to parameters/ directory')
parser.add_argument('--to-unified', action='store_true', help='Convert to single parameters.yaml')
parser.add_argument('--to-legacy', action='store_true', help='Convert parameters.yaml to legacy directory')
parser.add_argument('--unified-path', type=str, default='parameters.yaml', help='Unified YAML file path')

args = parser.parse_args()

if args.to_unified:
    up = UnifiedParameters(args.unified_path)
    up.from_legacy_dir(args.param_dir)
    up.write()
    print(f"Unified YAML written to {args.unified_path}")

if args.to_legacy:
    up = UnifiedParameters(args.unified_path)
    up.read()
    up.to_legacy_dir(args.param_dir)
    print(f"Legacy YAML files written to {args.param_dir}")
