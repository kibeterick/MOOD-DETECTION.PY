import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class MoodLogger:
    """Logs mood detection history for tracking patterns over time"""
    
    def __init__(self, history_file: str = "mood_history.json"):
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self) -> List[Dict]:
        """Load existing mood history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def log_mood(self, mood: str, confidence: float = 0.0, 
                 method: str = "unknown", notes: str = ""):
        """Log a mood detection event"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "mood": mood,
            "confidence": confidence,
            "method": method,
            "notes": notes
        }
        self.history.append(entry)
        self._save_history()
    
    def _save_history(self):
        """Save mood history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def get_recent_moods(self, count: int = 10) -> List[Dict]:
        """Get the most recent mood entries"""
        return self.history[-count:] if self.history else []
    
    def get_mood_summary(self) -> Dict[str, int]:
        """Get a summary count of all moods"""
        summary = {}
        for entry in self.history:
            mood = entry.get("mood", "Unknown")
            summary[mood] = summary.get(mood, 0) + 1
        return summary
    
    def get_today_moods(self) -> List[Dict]:
        """Get all mood entries from today"""
        today = datetime.now().date()
        return [
            entry for entry in self.history
            if datetime.fromisoformat(entry["timestamp"]).date() == today
        ]
