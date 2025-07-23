#!/usr/bin/env python3
"""
Generate modular Nodus SDK from protobuf files.
Follows July 2025 best practices for microservice SDKs.
"""

import pathlib
import logging
from typing import Dict, List, NamedTuple
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(message)s")

# Configuration
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()  # Go up one level from scripts/
SPOUNGE_PATH = PROJECT_ROOT / "venv" / "lib" / "python3.10" / "site-packages" / "spounge"
SDK_OUTPUT_DIR = PROJECT_ROOT / "utils" / "sdk"

class ProtoModule(NamedTuple):
    """Represents a protobuf module with metadata."""
    import_path: str
    module_name: str
    service_name: str
    category: str
    is_service: bool

def categorize_nodus_modules(spounge_path: pathlib.Path) -> Dict[str, List[ProtoModule]]:
    """Discover and categorize all nodus protobuf modules."""
    nodus_path = spounge_path / "nodus" / "v1"
    if not nodus_path.exists():
        return {}
    
    categories = defaultdict(list)
    
    for proto_file in nodus_path.rglob("*_pb2*.py"):
        rel_path = proto_file.relative_to(spounge_path).with_suffix("")
        parts = rel_path.parts
        
        # Extract service info
        module_name = parts[-1]
        is_service = module_name.endswith("_pb2_grpc")
        
        # Clean naming
        if is_service:
            service_name = module_name.replace("_pb2_grpc", "")
        else:
            service_name = module_name.replace("_pb2", "")
        
        # Categorize by path structure
        category = parts[2] if len(parts) > 2 else "core"  # nodus/v1/[category]
        
        proto_module = ProtoModule(
            import_path=".".join(parts),
            module_name=module_name,
            service_name=service_name,
            category=category,
            is_service=is_service
        )
        
        categories[category].append(proto_module)
    
    return dict(categories)

def generate_category_module(category: str, modules: List[ProtoModule], output_dir: pathlib.Path):
    """Generate a category-specific module with services and types."""
    
    # Separate services and types
    services = [m for m in modules if m.is_service]
    types = [m for m in modules if not m.is_service]
    
    imports = []
    service_exports = []
    type_exports = []
    
    # Import all modules
    for module in modules:
        imports.append(f"from spounge.{module.import_path} import {module.module_name}")
    
    # Create service and type mappings
    for service in services:
        service_exports.append(f"    '{service.service_name}': {service.module_name},")
    
    for type_mod in types:
        type_exports.append(f"    '{type_mod.service_name}': {type_mod.module_name},")
    
    content = f'''"""
Nodus {category.title()} - Protobuf services and types.
Auto-generated SDK module for microservice integration.
"""

from typing import Dict, Any
{chr(10).join(imports)}

# Service stubs for {category}
SERVICES: Dict[str, Any] = {{
{chr(10).join(service_exports)}
}}

# Message types for {category}  
TYPES: Dict[str, Any] = {{
{chr(10).join(type_exports)}
}}

def get_service(name: str):
    """Get service stub by name."""
    return SERVICES.get(name)

def get_type(name: str):
    """Get message type by name.""" 
    return TYPES.get(name)

# Direct exports
{chr(10).join(f"{m.service_name} = {m.module_name}" for m in modules)}

__all__ = [
    "SERVICES", "TYPES", "get_service", "get_type",
{chr(10).join(f'    "{m.service_name}",' for m in modules)}
]
'''
    
    output_file = output_dir / f"{category}.py"
    with open(output_file, "w") as f:
        f.write(content)
    
    return [m.service_name for m in modules]

def generate_main_client(categories: Dict[str, List[str]], output_dir: pathlib.Path):
    """Generate main client with factory methods."""
    
    imports = [f"from .{cat} import SERVICES as {cat.upper()}_SERVICES, TYPES as {cat.upper()}_TYPES" 
               for cat in categories.keys()]
    
    service_maps = [f"    **{cat.upper()}_SERVICES," for cat in categories.keys()]
    type_maps = [f"    **{cat.upper()}_TYPES," for cat in categories.keys()]
    
    content = f'''"""
Nodus Protocol Buffer Client SDK.
Provides unified access to all Nodus microservices.
"""

from typing import Dict, Any, Optional, List
import grpc
{chr(10).join(imports)}

class NodusClient:
    """Main client for Nodus microservices."""
    
    # All available services
    _SERVICES: Dict[str, Any] = {{
{chr(10).join(service_maps)}
    }}
    
    # All available types
    _TYPES: Dict[str, Any] = {{
{chr(10).join(type_maps)}
    }}
    
    def __init__(self, channel: Optional[grpc.Channel] = None):
        """Initialize client with gRPC channel."""
        self.channel = channel
        self._service_instances = {{}}
    
    def service(self, name: str):
        """Get service stub instance."""
        if name not in self._service_instances:
            service_class = self._SERVICES.get(name)
            if not service_class:
                raise ValueError(f"Service '{{name}}' not found")
            if not self.channel:
                raise ValueError("gRPC channel required for service calls")
            self._service_instances[name] = service_class(self.channel)
        return self._service_instances[name]
    
    def type(self, name: str):
        """Get message type class."""
        type_class = self._TYPES.get(name)
        if not type_class:
            raise ValueError(f"Type '{{name}}' not found")
        return type_class
    
    @property
    def available_services(self) -> List[str]:
        """List all available service names."""
        return list(self._SERVICES.keys())
    
    @property  
    def available_types(self) -> List[str]:
        """List all available type names."""
        return list(self._TYPES.keys())

# Factory function
def create_client(endpoint: str, **kwargs) -> NodusClient:
    """Create Nodus client with gRPC channel."""
    channel = grpc.insecure_channel(endpoint, **kwargs)
    return NodusClient(channel)

__all__ = ["NodusClient", "create_client"]
'''
    
    with open(output_dir / "client.py", "w") as f:
        f.write(content)

def generate_init_file(categories: Dict[str, List[str]], output_dir: pathlib.Path):
    """Generate package __init__.py."""
    
    category_imports = [f"from . import {cat}" for cat in categories.keys()]
    
    content = f'''"""
Nodus Protocol Buffer SDK.
Modern microservice client library following July 2025 best practices.
"""

from .client import NodusClient, create_client
{chr(10).join(category_imports)}

__version__ = "1.0.0"
__all__ = ["NodusClient", "create_client"] + {list(categories.keys())}
'''
    
    with open(output_dir / "__init__.py", "w") as f:
        f.write(content)

def main():
    if not SPOUNGE_PATH.exists():
        logging.error(f"Spounge package not found: {SPOUNGE_PATH}")
        return 1
    
    SDK_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    categories = categorize_nodus_modules(SPOUNGE_PATH)
    if not categories:
        logging.error("No nodus modules found")
        return 1
    
    logging.info(f"Found {sum(len(mods) for mods in categories.values())} modules in {len(categories)} categories")
    
    # Generate category modules
    all_exports = {}
    for category, modules in categories.items():
        exports = generate_category_module(category, modules, SDK_OUTPUT_DIR)
        all_exports[category] = exports
        logging.info(f"Generated {category}.py with {len(modules)} modules")
    
    # Generate main client and init
    generate_main_client(all_exports, SDK_OUTPUT_DIR)
    generate_init_file(all_exports, SDK_OUTPUT_DIR)
    
    # Create py.typed for type checking
    (SDK_OUTPUT_DIR / "py.typed").touch()
    
    logging.info(f"✅ Nodus SDK generated at {SDK_OUTPUT_DIR}")
    return 0

if __name__ == "__main__":
    exit(main())