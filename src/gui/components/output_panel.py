"""
Output Panel Component for MS Learn GUI Data Generator

This component provides output configuration functionality including:
- Output folder selection with browser dialog
- Category selection and recent categories management
- Processing settings (quality threshold, delay)
- Settings persistence and validation
- Preview output functionality
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from typing import Callable, Optional, List
import os


class OutputPanel(ctk.CTkFrame):
    """
    Output Configuration Panel Component
    
    Features:
    - Output folder browser with validation
    - Category selection with recent items
    - Processing settings configuration
    - Settings persistence integration
    - Real-time validation feedback
    """
    
    def __init__(self, parent, settings_manager=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.settings_manager = settings_manager
        self.change_callbacks = []
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        self._setup_ui()
        self._load_settings()
        
    def _setup_ui(self):
        """Setup the output panel UI components"""
        
        # Header section
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Output & Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            self.header_frame,
            text="✓ Ready",
            font=ctk.CTkFont(size=12),
            text_color="green"
        )
        self.status_label.grid(row=0, column=1, sticky="e", padx=10, pady=10)
        
        # Output Folder Section
        self._create_output_folder_section()
        
        # Category Selection Section
        self._create_category_section()
        
        # Processing Settings Section
        self._create_processing_settings_section()
        
        # Preview Section
        self._create_preview_section()
        
    def _create_output_folder_section(self):
        """Create output folder selection section"""
        # Output folder frame
        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.output_frame.grid_columnconfigure(1, weight=1)
        
        # Section title
        folder_title = ctk.CTkLabel(
            self.output_frame,
            text="📁 Output Folder",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        folder_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 5))
        
        # Folder path label
        ctk.CTkLabel(
            self.output_frame,
            text="Output Directory:",
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # Folder path entry
        self.folder_var = tk.StringVar()
        self.folder_entry = ctk.CTkEntry(
            self.output_frame,
            textvariable=self.folder_var,
            placeholder_text="Select output folder...",
            height=32,
            state="readonly"
        )
        self.folder_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Browse button
        self.browse_button = ctk.CTkButton(
            self.output_frame,
            text="📂 Browse",
            command=self._browse_output_folder,
            width=100,
            height=32
        )
        self.browse_button.grid(row=1, column=2, padx=(5, 10), pady=5)
        
        # Folder validation status
        self.folder_status_frame = ctk.CTkFrame(self.output_frame)
        self.folder_status_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        
        self.folder_status_label = ctk.CTkLabel(
            self.folder_status_frame,
            text="",
            font=ctk.CTkFont(size=10)
        )
        self.folder_status_label.pack(padx=10, pady=5)
        
        # Quick folder options
        self.quick_folders_frame = ctk.CTkFrame(self.output_frame)
        self.quick_folders_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(
            self.quick_folders_frame,
            text="Quick Options:",
            font=ctk.CTkFont(size=10)
        ).pack(side="left", padx=(10, 5), pady=5)
        
        # Desktop button
        self.desktop_btn = ctk.CTkButton(
            self.quick_folders_frame,
            text="Desktop",
            command=lambda: self._set_quick_folder("Desktop"),
            width=80,
            height=25,
            font=ctk.CTkFont(size=10)
        )
        self.desktop_btn.pack(side="left", padx=2, pady=5)
        
        # Documents button
        self.documents_btn = ctk.CTkButton(
            self.quick_folders_frame,
            text="Documents",
            command=lambda: self._set_quick_folder("Documents"),
            width=80,
            height=25,
            font=ctk.CTkFont(size=10)
        )
        self.documents_btn.pack(side="left", padx=2, pady=5)
        
        # Default button
        self.default_btn = ctk.CTkButton(
            self.quick_folders_frame,
            text="Default",
            command=lambda: self._set_quick_folder("Default"),
            width=80,
            height=25,
            font=ctk.CTkFont(size=10)
        )
        self.default_btn.pack(side="left", padx=2, pady=5)
        
    def _create_category_section(self):
        """Create category selection section"""
        # Category frame
        self.category_frame = ctk.CTkFrame(self)
        self.category_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.category_frame.grid_columnconfigure(1, weight=1)
        
        # Section title
        category_title = ctk.CTkLabel(
            self.category_frame,
            text="🏷️ Category Selection",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        category_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 5))
        
        # Category label
        ctk.CTkLabel(
            self.category_frame,
            text="Category Name:",
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # Category dropdown
        self.category_var = tk.StringVar(value="General")
        self.category_menu = ctk.CTkOptionMenu(
            self.category_frame,
            variable=self.category_var,
            values=["General", "Active_Directory", "DNS", "DHCP", "PowerShell", "Security", "Networking"],
            command=self._on_category_change
        )
        self.category_menu.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Custom category button
        self.custom_category_btn = ctk.CTkButton(
            self.category_frame,
            text="✏️ Custom",
            command=self._create_custom_category,
            width=80,
            height=32
        )
        self.custom_category_btn.grid(row=1, column=2, padx=(5, 10), pady=5)
        
        # Category description
        self.category_desc_frame = ctk.CTkFrame(self.category_frame)
        self.category_desc_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=5)
        
        self.category_desc_label = ctk.CTkLabel(
            self.category_desc_frame,
            text="General purpose training data generation",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.category_desc_label.pack(padx=10, pady=5)
        
    def _create_processing_settings_section(self):
        """Create processing settings section"""
        # Processing settings frame
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        self.settings_frame.grid_columnconfigure((1, 3), weight=1)
        
        # Section title
        settings_title = ctk.CTkLabel(
            self.settings_frame,
            text="⚙️ Processing Settings",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        settings_title.grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(10, 5))
        
        # Quality threshold
        ctk.CTkLabel(
            self.settings_frame,
            text="Quality Threshold:",
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        self.quality_var = tk.StringVar(value="100")
        self.quality_entry = ctk.CTkEntry(
            self.settings_frame,
            textvariable=self.quality_var,
            width=80,
            height=32
        )
        self.quality_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.quality_entry.bind("<KeyRelease>", self._validate_quality_threshold)
        
        # Processing delay
        ctk.CTkLabel(
            self.settings_frame,
            text="Processing Delay:",
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=2, sticky="w", padx=(20, 5), pady=5)
        
        delay_frame = ctk.CTkFrame(self.settings_frame)
        delay_frame.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        self.delay_var = tk.StringVar(value="2")
        self.delay_entry = ctk.CTkEntry(
            delay_frame,
            textvariable=self.delay_var,
            width=60,
            height=32
        )
        self.delay_entry.pack(side="left", padx=(5, 2))
        self.delay_entry.bind("<KeyRelease>", self._validate_delay)
        
        ctk.CTkLabel(
            delay_frame,
            text="seconds",
            font=ctk.CTkFont(size=10)
        ).pack(side="left", padx=(0, 5))
        
        # Advanced settings toggle
        self.advanced_var = tk.BooleanVar()
        self.advanced_checkbox = ctk.CTkCheckBox(
            self.settings_frame,
            text="Advanced Settings",
            variable=self.advanced_var,
            command=self._toggle_advanced_settings
        )
        self.advanced_checkbox.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        # Advanced settings frame (initially hidden)
        self.advanced_frame = ctk.CTkFrame(self.settings_frame)
        # Will be shown/hidden based on checkbox
        
        # Content length limits
        ctk.CTkLabel(
            self.advanced_frame,
            text="Max Content Length:",
            font=ctk.CTkFont(size=11)
        ).grid(row=0, column=0, sticky="w", padx=10, pady=2)
        
        self.max_content_var = tk.StringVar(value="6000")
        self.max_content_entry = ctk.CTkEntry(
            self.advanced_frame,
            textvariable=self.max_content_var,
            width=80,
            height=28
        )
        self.max_content_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ctk.CTkLabel(
            self.advanced_frame,
            text="characters",
            font=ctk.CTkFont(size=10)
        ).grid(row=0, column=2, sticky="w", padx=5, pady=2)
        
        # Min content length
        ctk.CTkLabel(
            self.advanced_frame,
            text="Min Content Length:",
            font=ctk.CTkFont(size=11)
        ).grid(row=1, column=0, sticky="w", padx=10, pady=2)
        
        self.min_content_var = tk.StringVar(value="300")
        self.min_content_entry = ctk.CTkEntry(
            self.advanced_frame,
            textvariable=self.min_content_var,
            width=80,
            height=28
        )
        self.min_content_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        ctk.CTkLabel(
            self.advanced_frame,
            text="characters",
            font=ctk.CTkFont(size=10)
        ).grid(row=1, column=2, sticky="w", padx=5, pady=2)
        
    def _create_preview_section(self):
        """Create output preview section"""
        # Preview frame
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.preview_frame.grid_columnconfigure(1, weight=1)
        
        # Section title
        preview_title = ctk.CTkLabel(
            self.preview_frame,
            text="👁️ Output Preview",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        preview_title.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(10, 5))
        
        # Output filename preview
        ctk.CTkLabel(
            self.preview_frame,
            text="Training Data File:",
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        self.filename_label = ctk.CTkLabel(
            self.preview_frame,
            text="general_training_data.jsonl",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.filename_label.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Metadata file preview
        ctk.CTkLabel(
            self.preview_frame,
            text="Metadata File:",
            font=ctk.CTkFont(size=12)
        ).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        self.metadata_label = ctk.CTkLabel(
            self.preview_frame,
            text="general_metadata.json",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.metadata_label.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Settings validation button
        self.validate_btn = ctk.CTkButton(
            self.preview_frame,
            text="✓ Validate Settings",
            command=self._validate_settings,
            width=120,
            height=32
        )
        self.validate_btn.grid(row=1, column=2, rowspan=2, padx=(10, 10), pady=5)
        
        # Initialize with current values
        self._update_filename_preview()
        
    def _browse_output_folder(self):
        """Open folder browser dialog"""
        initial_dir = self.folder_var.get() or str(Path.home())
        
        folder = filedialog.askdirectory(
            title="Select Output Folder",
            initialdir=initial_dir
        )
        
        if folder:
            self.folder_var.set(folder)
            self._validate_output_folder()
            self._update_filename_preview()
            self._save_setting("default_output_dir", folder)
            self._notify_change("output_folder", folder)
    
    def _set_quick_folder(self, folder_type):
        """Set quick folder option"""
        if folder_type == "Desktop":
            folder = str(Path.home() / "Desktop" / "MSLearn_Output")
        elif folder_type == "Documents":
            folder = str(Path.home() / "Documents" / "MSLearn_Output")
        elif folder_type == "Default":
            folder = str(Path.cwd() / "output")
        
        # Create folder if it doesn't exist
        Path(folder).mkdir(parents=True, exist_ok=True)
        
        self.folder_var.set(folder)
        self._validate_output_folder()
        self._update_filename_preview()
        self._save_setting("default_output_dir", folder)
        self._notify_change("output_folder", folder)
    
    def _validate_output_folder(self):
        """Validate the selected output folder"""
        folder_path = self.folder_var.get()
        
        if not folder_path:
            self.folder_status_label.configure(
                text="⚠️ No output folder selected",
                text_color="orange"
            )
            self.status_label.configure(text="⚠️ Setup Required", text_color="orange")
            return False
        
        path = Path(folder_path)
        
        try:
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
            
            # Test write permission
            test_file = path / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            
            self.folder_status_label.configure(
                text="✓ Folder is valid and writable",
                text_color="green"
            )
            self._update_status()
            return True
            
        except PermissionError:
            self.folder_status_label.configure(
                text="❌ Permission denied - cannot write to folder",
                text_color="red"
            )
            self.status_label.configure(text="❌ Invalid Setup", text_color="red")
            return False
        except Exception as e:
            self.folder_status_label.configure(
                text=f"❌ Error: {str(e)[:50]}...",
                text_color="red"
            )
            self.status_label.configure(text="❌ Invalid Setup", text_color="red")
            return False
    
    def _on_category_change(self, category):
        """Handle category selection change"""
        self._update_category_description(category)
        self._update_filename_preview()
        self._save_setting("last_category", category)
        self._add_recent_category(category)
        self._notify_change("category", category)
    
    def _update_category_description(self, category):
        """Update category description text"""
        descriptions = {
            "General": "General purpose training data generation",
            "Active_Directory": "Active Directory administration and management",
            "DNS": "Domain Name System configuration and troubleshooting",
            "DHCP": "Dynamic Host Configuration Protocol management",
            "PowerShell": "PowerShell scripting and automation",
            "Security": "Windows Server security and authentication",
            "Networking": "Network configuration and management"
        }
        
        desc = descriptions.get(category, "Custom training data category")
        self.category_desc_label.configure(text=desc)
    
    def _create_custom_category(self):
        """Create a custom category"""
        dialog = ctk.CTkInputDialog(
            text="Enter custom category name:",
            title="Custom Category"
        )
        
        custom_category = dialog.get_input()
        
        if custom_category:
            # Clean up the category name
            custom_category = custom_category.strip().replace(" ", "_")
            
            if custom_category:
                # Add to the option menu
                current_values = self.category_menu._values
                if custom_category not in current_values:
                    new_values = current_values + [custom_category]
                    self.category_menu.configure(values=new_values)
                
                self.category_var.set(custom_category)
                self._update_category_description(custom_category)
                self._update_filename_preview()
                self._add_recent_category(custom_category)
                self._notify_change("category", custom_category)
    
    def _validate_quality_threshold(self, event=None):
        """Validate quality threshold input"""
        try:
            value = int(self.quality_var.get())
            if value < 0 or value > 1000:
                raise ValueError("Out of range")
            
            self.quality_entry.configure(border_color=("gray60", "gray40"))
            self._save_setting("quality_threshold", value)
            self._notify_change("quality_threshold", value)
            self._update_status()
            
        except ValueError:
            self.quality_entry.configure(border_color="red")
    
    def _validate_delay(self, event=None):
        """Validate processing delay input"""
        try:
            value = float(self.delay_var.get())
            if value < 0.5 or value > 60:
                raise ValueError("Out of range")
            
            self.delay_entry.configure(border_color=("gray60", "gray40"))
            self._save_setting("delay_seconds", value)
            self._notify_change("delay_seconds", value)
            self._update_status()
            
        except ValueError:
            self.delay_entry.configure(border_color="red")
    
    def _toggle_advanced_settings(self):
        """Toggle advanced settings visibility"""
        if self.advanced_var.get():
            self.advanced_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=10, pady=5)
        else:
            self.advanced_frame.grid_remove()
    
    def _update_filename_preview(self):
        """Update the filename preview based on current settings"""
        category = self.category_var.get().lower()
        
        training_filename = f"{category}_training_data.jsonl"
        metadata_filename = f"{category}_metadata.json"
        
        self.filename_label.configure(text=training_filename)
        self.metadata_label.configure(text=metadata_filename)
    
    def _validate_settings(self):
        """Validate all current settings"""
        issues = []
        
        # Validate output folder
        if not self._validate_output_folder():
            issues.append("Invalid output folder")
        
        # Validate quality threshold
        try:
            quality = int(self.quality_var.get())
            if quality < 0 or quality > 1000:
                issues.append("Quality threshold must be between 0-1000")
        except ValueError:
            issues.append("Invalid quality threshold")
        
        # Validate delay
        try:
            delay = float(self.delay_var.get())
            if delay < 0.5 or delay > 60:
                issues.append("Processing delay must be between 0.5-60 seconds")
        except ValueError:
            issues.append("Invalid processing delay")
        
        if issues:
            messagebox.showwarning(
                "Settings Validation",
                "Issues found:\\n• " + "\\n• ".join(issues)
            )
        else:
            messagebox.showinfo(
                "Settings Validation",
                "✓ All settings are valid and ready for processing!"
            )
            self._update_status()
    
    def _update_status(self):
        """Update the overall status indicator"""
        # Check if all required settings are valid
        has_folder = bool(self.folder_var.get())
        folder_valid = has_folder and Path(self.folder_var.get()).exists()
        
        try:
            quality_valid = 0 <= int(self.quality_var.get()) <= 1000
        except ValueError:
            quality_valid = False
        
        try:
            delay_valid = 0.5 <= float(self.delay_var.get()) <= 60
        except ValueError:
            delay_valid = False
        
        if folder_valid and quality_valid and delay_valid:
            self.status_label.configure(text="✓ Ready", text_color="green")
        elif has_folder and quality_valid and delay_valid:
            self.status_label.configure(text="⚠️ Check Folder", text_color="orange")
        else:
            self.status_label.configure(text="❌ Setup Required", text_color="red")
    
    def _load_settings(self):
        """Load settings from settings manager"""
        if not self.settings_manager:
            return
        
        # Load output folder
        output_dir = self.settings_manager.get("default_output_dir", "")
        if output_dir:
            self.folder_var.set(output_dir)
            self._validate_output_folder()
        
        # Load category
        category = self.settings_manager.get("last_category", "General")
        self.category_var.set(category)
        self._update_category_description(category)
        
        # Load processing settings
        quality = self.settings_manager.get("quality_threshold", 100)
        self.quality_var.set(str(quality))
        
        delay = self.settings_manager.get("delay_seconds", 2)
        self.delay_var.set(str(delay))
        
        # Load advanced settings
        max_content = self.settings_manager.get("max_content_length", 6000)
        self.max_content_var.set(str(max_content))
        
        min_content = self.settings_manager.get("min_content_length", 300)
        self.min_content_var.set(str(min_content))
        
        # Load recent categories for dropdown
        recent_categories = self.settings_manager.get("recent_categories", [])
        if recent_categories:
            all_categories = list(set(
                ["General", "Active_Directory", "DNS", "DHCP", "PowerShell", "Security", "Networking"] + 
                recent_categories
            ))
            self.category_menu.configure(values=all_categories)
        
        self._update_filename_preview()
        self._update_status()
    
    def _save_setting(self, key, value):
        """Save a setting to the settings manager"""
        if self.settings_manager:
            self.settings_manager.set(key, value)
            self.settings_manager.save()
    
    def _add_recent_category(self, category):
        """Add category to recent categories list"""
        if not self.settings_manager:
            return
        
        recent = self.settings_manager.get("recent_categories", [])
        
        # Remove if exists (to move to front)
        if category in recent:
            recent.remove(category)
        
        # Add to front
        recent.insert(0, category)
        
        # Keep only last 10
        recent = recent[:10]
        
        self.settings_manager.set("recent_categories", recent)
        self.settings_manager.save()
    
    def _notify_change(self, setting_name, value):
        """Notify listeners of setting changes"""
        for callback in self.change_callbacks:
            try:
                callback(setting_name, value)
            except Exception as e:
                print(f"Error in change callback: {e}")
    
    def add_change_callback(self, callback: Callable):
        """Add callback for setting changes"""
        self.change_callbacks.append(callback)
    
    def get_output_folder(self) -> str:
        """Get current output folder"""
        return self.folder_var.get()
    
    def get_category(self) -> str:
        """Get current category"""
        return self.category_var.get()
    
    def get_quality_threshold(self) -> int:
        """Get current quality threshold"""
        try:
            return int(self.quality_var.get())
        except ValueError:
            return 100
    
    def get_delay_seconds(self) -> float:
        """Get current processing delay"""
        try:
            return float(self.delay_var.get())
        except ValueError:
            return 2.0
    
    def get_all_settings(self) -> dict:
        """Get all current settings as dictionary"""
        return {
            "output_folder": self.get_output_folder(),
            "category": self.get_category(),
            "quality_threshold": self.get_quality_threshold(),
            "delay_seconds": self.get_delay_seconds(),
            "max_content_length": int(self.max_content_var.get()) if self.max_content_var.get().isdigit() else 6000,
            "min_content_length": int(self.min_content_var.get()) if self.min_content_var.get().isdigit() else 300
        }
    
    def is_ready_for_processing(self) -> bool:
        """Check if settings are ready for processing"""
        folder = self.get_output_folder()
        return (
            folder and 
            Path(folder).exists() and
            0 <= self.get_quality_threshold() <= 1000 and
            0.5 <= self.get_delay_seconds() <= 60
        )


# Test the component if run directly
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'config'))
    
    from settings import Settings
    
    # Test application
    app = ctk.CTk()
    app.title("Output Panel Test")
    app.geometry("600x700")
    
    # Create settings manager
    settings = Settings()
    
    # Create output panel
    output_panel = OutputPanel(app, settings_manager=settings)
    output_panel.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Add change callback for testing
    def on_setting_change(setting_name, value):
        print(f"Setting changed: {setting_name} = {value}")
    
    output_panel.add_change_callback(on_setting_change)
    
    app.mainloop()