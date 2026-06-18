"""Workspace Mapping module."""
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class WorkspaceMapper:
    """Maps and manages repositories and modules in the workspace."""
    
    def __init__(self, workspace_root: str):
        """Initialize the workspace mapper."""
        self.workspace_root = workspace_root
        self.modules_dir = os.path.join(workspace_root, "modules")
        self.registered_modules: Dict[str, Dict[str, Any]] = {}
    
    async def scan_modules(self) -> Dict[str, Any]:
        """Scan workspace/modules directory for repositories."""
        try:
            if not os.path.exists(self.modules_dir):
                os.makedirs(self.modules_dir)
                return {"modules": [], "count": 0}
            
            modules = []
            for item in os.listdir(self.modules_dir):
                item_path = os.path.join(self.modules_dir, item)
                if os.path.isdir(item_path):
                    module_info = await self._analyze_module(item, item_path)
                    modules.append(module_info)
                    self.registered_modules[item] = module_info
            
            logger.info(f"Scanned {len(modules)} modules in workspace")
            return {
                "modules": modules,
                "count": len(modules),
                "workspace_root": self.workspace_root
            }
        except Exception as e:
            logger.error(f"Module scanning failed: {e}")
            return {"error": str(e), "modules": []}
    
    async def _analyze_module(self, name: str, path: str) -> Dict[str, Any]:
        """Analyze a module directory."""
        info = {
            "name": name,
            "path": path,
            "type": None,
            "language": None,
            "has_git": False,
            "has_package_json": False,
            "has_requirements": False,
            "has_go_mod": False,
            "has_cargo": False,
            "files": []
        }
        
        # Check for version control
        if os.path.exists(os.path.join(path, ".git")):
            info["has_git"] = True
        
        # Detect project type and language
        for root, dirs, files in os.walk(path):
            for file in files:
                if file == "package.json":
                    info["has_package_json"] = True
                    info["language"] = "JavaScript/Node.js"
                    info["type"] = "Node.js Project"
                elif file == "requirements.txt":
                    info["has_requirements"] = True
                    if not info["language"]:
                        info["language"] = "Python"
                        info["type"] = "Python Project"
                elif file == "go.mod":
                    info["has_go_mod"] = True
                    info["language"] = "Go"
                    info["type"] = "Go Project"
                elif file == "Cargo.toml":
                    info["has_cargo"] = True
                    info["language"] = "Rust"
                    info["type"] = "Rust Project"
                
                # Collect files
                if len(info["files"]) < 100:  # Limit to first 100 files
                    file_path = os.path.join(root, file)
                    info["files"].append(os.path.relpath(file_path, path))
        
        return info
    
    def get_registered_modules(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered modules."""
        return self.registered_modules
    
    def get_module(self, module_name: str) -> Dict[str, Any]:
        """Get details of a specific module."""
        return self.registered_modules.get(module_name, {})
