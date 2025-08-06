"""
Unit tests for settings management
"""

import unittest
import tempfile
import json
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config.settings import Settings

class TestSettings(unittest.TestCase):
    """
    Test cases for Settings class
    """
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary config file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.settings = Settings(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Remove temporary file
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_default_settings(self):
        """Test that default settings are loaded"""
        self.assertIsNotNone(self.settings.get("window_size"))
        self.assertEqual(self.settings.get("window_size"), [1200, 800])
        self.assertEqual(self.settings.get("delay_seconds"), 2)
    
    def test_set_and_get(self):
        """Test setting and getting values"""
        self.settings.set("test_key", "test_value")
        self.assertEqual(self.settings.get("test_key"), "test_value")
    
    def test_save_and_load(self):
        """Test saving and loading settings"""
        self.settings.set("test_key", "test_value")
        self.settings.save()
        
        # Create new settings instance with same file
        new_settings = Settings(self.temp_file.name)
        self.assertEqual(new_settings.get("test_key"), "test_value")
    
    def test_update(self):
        """Test updating multiple settings"""
        updates = {
            "key1": "value1",
            "key2": "value2",
            "key3": 123
        }
        self.settings.update(updates)
        
        self.assertEqual(self.settings.get("key1"), "value1")
        self.assertEqual(self.settings.get("key2"), "value2")
        self.assertEqual(self.settings.get("key3"), 123)
    
    def test_reset(self):
        """Test resetting to defaults"""
        self.settings.set("custom_key", "custom_value")
        self.settings.reset()
        
        self.assertIsNone(self.settings.get("custom_key"))
        self.assertEqual(self.settings.get("window_size"), [1200, 800])
    
    def test_recent_url_lists(self):
        """Test managing recent URL lists"""
        self.settings.add_recent_url_list("file1.txt")
        self.settings.add_recent_url_list("file2.txt")
        self.settings.add_recent_url_list("file3.txt")
        
        recent = self.settings.get("recent_url_lists")
        self.assertEqual(recent[0], "file3.txt")
        self.assertEqual(recent[1], "file2.txt")
        self.assertEqual(recent[2], "file1.txt")
        
        # Test duplicate handling
        self.settings.add_recent_url_list("file1.txt")
        recent = self.settings.get("recent_url_lists")
        self.assertEqual(recent[0], "file1.txt")
        self.assertEqual(len([f for f in recent if f == "file1.txt"]), 1)
    
    def test_recent_categories(self):
        """Test managing recent categories"""
        self.settings.add_recent_category("Category1")
        self.settings.add_recent_category("Category2")
        
        recent = self.settings.get("recent_categories")
        self.assertEqual(recent[0], "Category2")
        self.assertEqual(recent[1], "Category1")

if __name__ == '__main__':
    unittest.main()
