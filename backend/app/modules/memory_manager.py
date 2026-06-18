"""Memory Management module."""
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class MemoryManager:
    """Manages session history and reusable memory."""
    
    def __init__(self, memory_dir: str):
        """Initialize the memory manager."""
        self.memory_dir = memory_dir
        Path(memory_dir).mkdir(parents=True, exist_ok=True)
    
    def save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save a session to memory."""
        try:
            session_file = os.path.join(self.memory_dir, f"{session_id}.json")
            session_data["saved_at"] = datetime.now().isoformat()
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            logger.info(f"Session saved: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            return False
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a session from memory."""
        try:
            session_file = os.path.join(self.memory_dir, f"{session_id}.json")
            
            if not os.path.exists(session_file):
                return None
            
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            logger.info(f"Session loaded: {session_id}")
            return session_data
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return None
    
    def create_memory_summary(self, session_data: Dict[str, Any]) -> str:
        """Create a summary of a session for memory."""
        try:
            summary = f"""
Session Summary:
- Created: {session_data.get('created_at', 'unknown')}
- Messages: {len(session_data.get('messages', []))}
- Key Topics: {', '.join(session_data.get('topics', []))}
- Outcomes: {', '.join(session_data.get('outcomes', []))}

Last Updated: {datetime.now().isoformat()}
"""
            return summary
        except Exception as e:
            logger.error(f"Failed to create memory summary: {e}")
            return ""
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all saved sessions."""
        try:
            sessions = []
            for file in os.listdir(self.memory_dir):
                if file.endswith('.json'):
                    session_id = file.replace('.json', '')
                    file_path = os.path.join(self.memory_dir, file)
                    stat = os.stat(file_path)
                    
                    sessions.append({
                        "id": session_id,
                        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        "size": stat.st_size
                    })
            
            return sorted(sessions, key=lambda x: x['modified'], reverse=True)
        except Exception as e:
            logger.error(f"Failed to list sessions: {e}")
            return []
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session from memory."""
        try:
            session_file = os.path.join(self.memory_dir, f"{session_id}.json")
            
            if os.path.exists(session_file):
                os.remove(session_file)
                logger.info(f"Session deleted: {session_id}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Failed to delete session: {e}")
            return False
