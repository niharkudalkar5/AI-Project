"""Repository Scanner module."""
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class RepositoryScanner:
    """Scans and analyzes repository structure and metadata."""
    
    @staticmethod
    def scan_repository(repo_path: str) -> Dict[str, Any]:
        """Scan a repository for metadata and structure."""
        info = {
            "path": repo_path,
            "name": os.path.basename(repo_path),
            "structure": {},
            "config_files": [],
            "build_files": [],
            "test_files": [],
            "documentation": [],
            "dependencies": {},
            "file_count": 0,
            "total_size": 0,
        }
        
        try:
            # Scan directory structure
            for root, dirs, files in os.walk(repo_path):
                # Skip common ignored directories
                dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules', '.venv', 'venv']]
                
                info["file_count"] += len(files)
                
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, repo_path)
                    
                    # Count size
                    try:
                        info["total_size"] += os.path.getsize(file_path)
                    except:
                        pass
                    
                    # Categorize files
                    if file in ['package.json', 'requirements.txt', 'go.mod', 'Cargo.toml', 'pom.xml']:
                        info["config_files"].append(rel_path)
                    elif file in ['Makefile', 'build.sh', 'build.gradle', 'webpack.config.js', 'next.config.js']:
                        info["build_files"].append(rel_path)
                    elif 'test' in file.lower() or file.endswith('.test.js') or file.endswith('_test.go'):
                        info["test_files"].append(rel_path)
                    elif file in ['README.md', 'README.txt', 'CONTRIBUTING.md', 'CHANGELOG.md']:
                        info["documentation"].append(rel_path)
        
        except Exception as e:
            logger.error(f"Repository scan failed: {e}")
            info["error"] = str(e)
        
        return info
    
    @staticmethod
    def detect_tech_stack(repo_path: str) -> Dict[str, Any]:
        """Detect technology stack from repository."""
        stack = {
            "languages": [],
            "frameworks": [],
            "build_tools": [],
            "test_frameworks": [],
            "package_managers": []
        }
        
        try:
            # Check for language indicators
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    if file.endswith('.py'):
                        if "languages" not in stack or "Python" not in stack["languages"]:
                            stack["languages"].append("Python")
                    elif file.endswith('.js') or file.endswith('.ts') or file.endswith('.tsx'):
                        if "JavaScript/TypeScript" not in stack["languages"]:
                            stack["languages"].append("JavaScript/TypeScript")
                    elif file.endswith('.go'):
                        if "Go" not in stack["languages"]:
                            stack["languages"].append("Go")
                    elif file.endswith('.rs'):
                        if "Rust" not in stack["languages"]:
                            stack["languages"].append("Rust")
                    
                    # Check for frameworks
                    if file == "package.json":
                        try:
                            with open(os.path.join(root, file), 'r') as f:
                                pkg = json.load(f)
                                deps = pkg.get("dependencies", {})
                                if "react" in deps:
                                    stack["frameworks"].append("React")
                                if "django" in deps:
                                    stack["frameworks"].append("Django")
                                if "fastapi" in deps:
                                    stack["frameworks"].append("FastAPI")
                        except:
                            pass
        
        except Exception as e:
            logger.error(f"Tech stack detection failed: {e}")
        
        return stack
