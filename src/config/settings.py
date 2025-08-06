"""
Settings management for MS Learn GUI Data Generator
Handles persistent configuration storage and retrieval
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class Settings:
    """
    Manages application settings with JSON persistence
    """
    
    DEFAULT_SETTINGS = {
        "window_size": [1200, 800],
        "default_output_dir": str(Path.home() / "Documents" / "MSLearn_Output"),
        "quality_threshold": 100,
        "delay_seconds": 2,
        "recent_url_lists": [],
        "recent_categories": ["DNS_Administration", "Active_Directory", "PowerShell"],
        "theme": "system",
        "color_theme": "blue",
        "auto_save": True,
        "max_retries": 3,
        "timeout_seconds": 30
    }
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize settings manager
        
        Args:
            config_file: Optional path to configuration file
        """
        if config_file:
            self.config_file = Path(config_file)
        else:
            # Default config location
            config_dir = Path.home() / ".mslearn_gui"
            config_dir.mkdir(exist_ok=True)
            self.config_file = config_dir / "settings.json"
        
        self.settings: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """
        Load settings from configuration file
        """
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self.settings = {**self.DEFAULT_SETTINGS, **loaded_settings}
                logger.info(f"Settings loaded from {self.config_file}")
            except Exception as e:
                logger.error(f"Error loading settings: {e}")
                self.settings = self.DEFAULT_SETTINGS.copy()
        else:
            self.settings = self.DEFAULT_SETTINGS.copy()
            self.save()  # Create initial config file
    
    def save(self) -> None:
        """
        Save current settings to configuration file
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            logger.info(f"Settings saved to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value
        
        Args:
            key: Setting key
            default: Default value if key not found
        
        Returns:
            Setting value or default
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a setting value
        
        Args:
            key: Setting key
            value: Setting value
        """
        self.settings[key] = value
        if self.get("auto_save", True):
            self.save()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update multiple settings at once
        
        Args:
            updates: Dictionary of settings to update
        """
        self.settings.update(updates)
        if self.get("auto_save", True):
            self.save()
    
    def reset(self) -> None:
        """
        Reset settings to defaults
        """
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.save()
    
    def add_recent_url_list(self, file_path: str, max_items: int = 10) -> None:
        """
        Add a file to recent URL lists
        
        Args:
            file_path: Path to URL list file
            max_items: Maximum number of recent items to keep
        """
        recent = self.get("recent_url_lists", [])
        
        # Remove if already exists
        if file_path in recent:
            recent.remove(file_path)
        
        # Add to beginning
        recent.insert(0, file_path)
        
        # Limit size
        recent = recent[:max_items]
        
        self.set("recent_url_lists", recent)
    
    def add_recent_category(self, category: str, max_items: int = 10) -> None:
        """
        Add a category to recent categories
        
        Args:
            category: Category name
            max_items: Maximum number of recent items to keep
        """
        recent = self.get("recent_categories", [])
        
        # Remove if already exists
        if category in recent:
            recent.remove(category)
        
        # Add to beginning
        recent.insert(0, category)
        
        # Limit size
        recent = recent[:max_items]
        
        self.set("recent_categories", recent)
