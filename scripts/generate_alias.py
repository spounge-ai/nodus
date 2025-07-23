#!/usr/bin/env python3
"""
Generate simple alias exports for Nodus protobuf modules.
Creates flat import/export file for production builds.
"""

import pathlib
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO, format="%(message)s")

# Configuration
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
SPOUNGE_PATH = PROJECT_ROOT / "venv" / "lib" / "python3.10" / "site-packages" / "spounge"
ALIAS_OUTPUT_DIR = PROJECT_ROOT / "src" / "nodus" / "protos"

def discover_nodus_modules(spounge_path: pathlib.Path) -> List[Dict[str, str]]:
    """Find all nodus protobuf modules and create alias mappings."""
    nodus_path = spounge_path / "nodus" / "v1"
    if not nodus_path.exists():
        return []
    
    modules = []
    seen_aliases = set()
    
    for proto_file in nodus_path.rglob("*_pb2*.py"):
        rel_path = proto_file.relative_to(spounge_path).with_suffix("")
        parts = rel_path.parts
        
        module_name = parts[-1]
        import_path = ".".join(parts)
        
        # Remove _pb2 from all, add _grpc suffix for grpc modules
        if module_name.endswith("_pb2_grpc"):
            base_name = module_name.replace("_pb2_grpc", "")
            alias = f"{base_name}_grpc"
        else:
            alias = module_name.replace("_pb2", "")
            
        alias = alias.replace("service", "svc")

        modules.append({
            "import_path": import_path,
            "module_name": module_name,
            "alias": alias
        })
    
    return sorted(modules, key=lambda x: x["alias"])

def generate_category_files(modules: List[Dict[str, str]], output_dir: pathlib.Path):
    """Generate separate files by category."""
    from collections import defaultdict
    
    categories = defaultdict(list)
    
    # Group by category from import path
    for mod in modules:
        parts = mod['import_path'].split('.')
        category = parts[2] if len(parts) > 2 else 'core'
        categories[category].append(mod)
    
    total_count = 0
    category_exports = []
    
    for category, cat_modules in categories.items():
        imports = []
        aliases = []
        exports = []
        
        for mod in cat_modules:
            imports.append(f"from spounge.{mod['import_path']} import {mod['module_name']}")
            aliases.append(f"{mod['alias']} = {mod['module_name']}")
            exports.append(f'    "{mod["alias"]}",')
        
        content = f'''"""
Nodus {category.title()} Protocol Buffer Aliases.
"""

# Imports
{chr(10).join(imports)}

# Aliases
{chr(10).join(aliases)}

# Exports
__all__ = [
{chr(10).join(exports)}
]
'''
        
        output_file = output_dir / f"{category}.py"
        with open(output_file, "w") as f:
            f.write(content)
        
        total_count += len(cat_modules)
        category_exports.append(f"from .{category} import *")
    
    # Generate main __init__.py that imports all categories
    init_content = f'''"""
Nodus Protocol Buffer Aliases.
Organized by service categories.
"""

{chr(10).join(category_exports)}
'''
    
    with open(output_dir / "__init__.py", "w") as f:
        f.write(init_content)
    
    return total_count, len(categories)

def generate_init_file(output_dir: pathlib.Path):
    """Generate package init."""
    content = '''"""Nodus aliases package."""

from . import *
'''
    
    with open(output_dir / "__init__.py", "w") as f:
        f.write(content)

def main():
    if not SPOUNGE_PATH.exists():
        logging.error(f"Spounge package not found: {SPOUNGE_PATH}")
        return 1
    
    ALIAS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    modules = discover_nodus_modules(SPOUNGE_PATH)
    if not modules:
        logging.error("No nodus modules found")
        return 1
    
    count, categories = generate_category_files(modules, ALIAS_OUTPUT_DIR)
    
    logging.info(f"✅ Generated {count} aliases in {categories} category files at {ALIAS_OUTPUT_DIR}")
    return 0

if __name__ == "__main__":
    exit(main())