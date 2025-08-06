"""
URL Manager Component for MS Learn GUI Data Generator

This component provides URL management functionality including:
- URL list display with status indicators
- Add/Remove/Clear operations
- URL validation
- Visual feedback for processing status
"""

import customtkinter as ctk
from typing import List, Callable, Optional
import threading
from urllib.parse import urlparse
import re


class URLItem:
    """Represents a single URL with its status and metadata"""
    
    def __init__(self, url: str):
        self.url = url
        self.status = "ready"  # ready, processing, completed, failed, invalid
        self.title = ""
        self.category = ""
        self.error_message = ""
        
    def __str__(self):
        return f"{self.url} ({self.status})"


class URLManager(ctk.CTkFrame):
    """
    URL Management Component
    
    Features:
    - Scrollable URL list with status indicators
    - Add/Remove/Clear operations
    - URL validation
    - Visual status feedback
    - Integration with backend generator
    """
    
    def __init__(self, parent, backend_generator=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.backend_generator = backend_generator
        self.url_items: List[URLItem] = []
        self.validation_callbacks = []
        self.status_change_callbacks = []
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the URL manager UI components"""
        
        # Header section
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="URL Management",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        # URL Counter
        self.counter_label = ctk.CTkLabel(
            self.header_frame,
            text="0 URLs",
            font=ctk.CTkFont(size=12)
        )
        self.counter_label.grid(row=0, column=1, sticky="e", padx=10, pady=10)
        
        # Input section
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # URL input
        self.url_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Enter MS Learn URL here...",
            height=32
        )
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10)
        self.url_entry.bind("<Return>", self._on_add_url)
        
        # Add button
        self.add_button = ctk.CTkButton(
            self.input_frame,
            text="Add URL",
            command=self._on_add_url,
            width=100
        )
        self.add_button.grid(row=0, column=1, padx=(5, 10), pady=10)
        
        # URL List section (scrollable)
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.list_frame.grid_columnconfigure(0, weight=1)
        self.list_frame.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame for URL items
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.list_frame,
            label_text="URLs to Process"
        )
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        # Control buttons
        self.controls_frame = ctk.CTkFrame(self)
        self.controls_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(5, 10))
        
        # Control buttons
        self.validate_all_button = ctk.CTkButton(
            self.controls_frame,
            text="Validate All",
            command=self._validate_all_urls,
            width=100
        )
        self.validate_all_button.grid(row=0, column=0, padx=(10, 5), pady=10)
        
        self.clear_all_button = ctk.CTkButton(
            self.controls_frame,
            text="Clear All",
            command=self._clear_all_urls,
            width=100,
            fg_color="transparent",
            border_width=2
        )
        self.clear_all_button.grid(row=0, column=1, padx=5, pady=10)
        
        self.remove_failed_button = ctk.CTkButton(
            self.controls_frame,
            text="Remove Failed",
            command=self._remove_failed_urls,
            width=100,
            fg_color="transparent",
            border_width=2
        )
        self.remove_failed_button.grid(row=0, column=2, padx=(5, 10), pady=10)
        
        # Status legend
        self.legend_frame = ctk.CTkFrame(self.controls_frame)
        self.legend_frame.grid(row=0, column=3, sticky="e", padx=(20, 10), pady=10)
        
        # Status indicators legend
        status_colors = {
            "Ready": "#1f538d",      # Blue
            "Processing": "#f59e0b", # Yellow/Orange  
            "Completed": "#059669",  # Green
            "Failed": "#dc2626",     # Red
            "Invalid": "#6b7280"     # Gray
        }
        
        legend_col = 0
        for status, color in status_colors.items():
            indicator = ctk.CTkLabel(
                self.legend_frame,
                text="●",
                font=ctk.CTkFont(size=12),
                text_color=color
            )
            indicator.grid(row=0, column=legend_col, padx=(5, 2), pady=5)
            
            label = ctk.CTkLabel(
                self.legend_frame,
                text=status,
                font=ctk.CTkFont(size=10)
            )
            label.grid(row=0, column=legend_col + 1, padx=(0, 10), pady=5)
            legend_col += 2
        
        # Initial UI update
        self._update_counter()
        
    def _on_add_url(self, event=None):
        """Handle adding a new URL"""
        url = self.url_entry.get().strip()
        if url:
            self.add_url(url)
            self.url_entry.delete(0, ctk.END)
    
    def add_url(self, url: str) -> bool:
        """
        Add a URL to the list
        
        Args:
            url: URL to add
            
        Returns:
            True if URL was added, False if duplicate or invalid
        """
        # Check for duplicates
        if any(item.url == url for item in self.url_items):
            return False
            
        # Create URL item
        url_item = URLItem(url)
        
        # Basic validation
        if not self._is_valid_mslearn_url(url):
            url_item.status = "invalid"
            url_item.error_message = "Not a valid MS Learn URL"
        
        self.url_items.append(url_item)
        self._create_url_widget(url_item, len(self.url_items) - 1)
        self._update_counter()
        
        return True
    
    def remove_url(self, index: int):
        """Remove URL at specific index"""
        if 0 <= index < len(self.url_items):
            self.url_items.pop(index)
            self._refresh_url_list()
            self._update_counter()
    
    def clear_all(self):
        """Clear all URLs"""
        self.url_items.clear()
        self._refresh_url_list()
        self._update_counter()
    
    def _clear_all_urls(self):
        """Handle clear all button click"""
        if self.url_items:
            # Simple confirmation (in real app, might want a dialog)
            self.clear_all()
    
    def _remove_failed_urls(self):
        """Remove all URLs with failed status"""
        self.url_items = [item for item in self.url_items if item.status != "failed"]
        self._refresh_url_list()
        self._update_counter()
    
    def _validate_all_urls(self):
        """Validate all URLs in background thread"""
        if not self.backend_generator:
            return
            
        # Update UI to show validation in progress
        for item in self.url_items:
            if item.status == "ready":
                item.status = "processing"
        
        self._refresh_url_list()
        
        # Run validation in background
        threading.Thread(
            target=self._background_validation,
            daemon=True
        ).start()
    
    def _background_validation(self):
        """Background thread for URL validation"""
        for i, item in enumerate(self.url_items):
            if item.status == "processing":
                try:
                    # Use backend generator for validation
                    if self.backend_generator:
                        # Simulate validation using categorize_url method
                        category = self.backend_generator.categorize_url(item.url)
                        item.category = category
                        item.status = "ready" if category else "invalid"
                        
                        if item.status == "invalid":
                            item.error_message = "Unable to categorize content"
                    else:
                        # Fallback validation
                        if self._is_valid_mslearn_url(item.url):
                            item.status = "ready"
                        else:
                            item.status = "invalid"
                            item.error_message = "Invalid MS Learn URL format"
                            
                except Exception as e:
                    item.status = "failed"
                    item.error_message = str(e)
        
        # Schedule UI update on main thread
        self.after(0, self._refresh_url_list)
    
    def _is_valid_mslearn_url(self, url: str) -> bool:
        """Validate if URL is a valid MS Learn URL"""
        try:
            parsed = urlparse(url)
            return (
                parsed.scheme in ['http', 'https'] and
                'learn.microsoft.com' in parsed.netloc and
                len(parsed.path) > 1
            )
        except:
            return False
    
    def _create_url_widget(self, url_item: URLItem, index: int):
        """Create widget for a single URL item"""
        # Container frame for this URL
        url_frame = ctk.CTkFrame(self.scrollable_frame)
        url_frame.grid(row=index, column=0, sticky="ew", padx=5, pady=2)
        url_frame.grid_columnconfigure(1, weight=1)
        
        # Status indicator
        status_colors = {
            "ready": "#1f538d",
            "processing": "#f59e0b",
            "completed": "#059669",
            "failed": "#dc2626",
            "invalid": "#6b7280"
        }
        
        status_indicator = ctk.CTkLabel(
            url_frame,
            text="●",
            font=ctk.CTkFont(size=14),
            text_color=status_colors.get(url_item.status, "#6b7280"),
            width=20
        )
        status_indicator.grid(row=0, column=0, padx=(10, 5), pady=10)
        
        # URL display (truncated if too long)
        display_url = url_item.url
        if len(display_url) > 80:
            display_url = display_url[:77] + "..."
            
        url_label = ctk.CTkLabel(
            url_frame,
            text=display_url,
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        url_label.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        
        # Category/Status info
        if url_item.category:
            info_text = f"[{url_item.category}]"
        elif url_item.error_message:
            info_text = f"Error: {url_item.error_message[:30]}..."
        else:
            info_text = url_item.status.title()
            
        info_label = ctk.CTkLabel(
            url_frame,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info_label.grid(row=0, column=2, padx=5, pady=10)
        
        # Remove button
        remove_button = ctk.CTkButton(
            url_frame,
            text="×",
            command=lambda i=index: self.remove_url(i),
            width=30,
            height=30,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray20", "gray70")
        )
        remove_button.grid(row=0, column=3, padx=(5, 10), pady=10)
    
    def _refresh_url_list(self):
        """Refresh the entire URL list display"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Recreate all URL widgets
        for i, url_item in enumerate(self.url_items):
            self._create_url_widget(url_item, i)
    
    def _update_counter(self):
        """Update the URL counter display"""
        count = len(self.url_items)
        status_counts = {}
        for item in self.url_items:
            status_counts[item.status] = status_counts.get(item.status, 0) + 1
        
        if count == 0:
            counter_text = "0 URLs"
        else:
            ready_count = status_counts.get("ready", 0)
            counter_text = f"{count} URLs ({ready_count} ready)"
        
        self.counter_label.configure(text=counter_text)
    
    def get_urls(self) -> List[str]:
        """Get all URLs as strings"""
        return [item.url for item in self.url_items]
    
    def get_ready_urls(self) -> List[str]:
        """Get URLs that are ready for processing"""
        return [item.url for item in self.url_items if item.status == "ready"]
    
    def get_url_items(self) -> List[URLItem]:
        """Get all URL items with metadata"""
        return self.url_items.copy()
    
    def update_url_status(self, url: str, status: str, **kwargs):
        """Update the status of a specific URL"""
        for item in self.url_items:
            if item.url == url:
                item.status = status
                if 'title' in kwargs:
                    item.title = kwargs['title']
                if 'category' in kwargs:
                    item.category = kwargs['category']
                if 'error_message' in kwargs:
                    item.error_message = kwargs['error_message']
                break
        
        # Refresh display
        self.after(0, self._refresh_url_list)
        self.after(0, self._update_counter)
    
    def add_status_change_callback(self, callback: Callable):
        """Add callback for status changes"""
        self.status_change_callbacks.append(callback)
    
    def set_backend_generator(self, generator):
        """Set the backend generator for validation"""
        self.backend_generator = generator


# Test the component if run directly
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))
    
    from mslearn_generator import MSLearnTrainingDataGenerator
    
    # Test application
    app = ctk.CTk()
    app.title("URL Manager Test")
    app.geometry("800x600")
    
    # Create backend generator
    generator = MSLearnTrainingDataGenerator()
    
    # Create URL manager
    url_manager = URLManager(app, backend_generator=generator)
    url_manager.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Add some test URLs
    test_urls = [
        "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/get-started/adac/Advanced-AD-DS-Management-Using-Active-Directory-Administrative-Center--Level-200-",
        "https://learn.microsoft.com/en-us/windows-server/networking/dns/dns-overview",
        "https://example.com/invalid-url"
    ]
    
    for url in test_urls:
        url_manager.add_url(url)
    
    app.mainloop()