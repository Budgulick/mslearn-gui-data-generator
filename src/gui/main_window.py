"""
Main window for MS Learn GUI Data Generator
Phase 1.4 implementation with Output Panel integration
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import Settings
from gui.components import URLManager, OutputPanel
from core.mslearn_generator import MSLearnTrainingDataGenerator

class MSLearnGUIApp:
    """
    Main application window for MS Learn Data Generator
    Phase 1.4: Enhanced with Output Panel component integration
    """
    
    def __init__(self):
        """Initialize the main application window"""
        # Set appearance mode and color theme from settings
        self.settings = Settings()
        
        theme = self.settings.get("theme", "system")
        color_theme = self.settings.get("color_theme", "blue")
        
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme(color_theme)
        
        # Initialize backend generator
        self.backend_generator = MSLearnTrainingDataGenerator()
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("MS Learn Training Data Generator")
        
        # Set window icon (using default tkinter icon for now)
        try:
            # This can be enhanced with a custom icon later
            self.root.iconname("MS Learn Generator")
        except:
            pass  # Icon setting is optional
        
        # Setup window configuration
        self._setup_window_geometry()
        
        # Create menu bar
        self._create_menu_bar()
        
        # Setup main UI layout
        self._setup_main_layout()
        
        # Setup status bar
        self._setup_status_bar()
        
        # Bind events
        self._bind_events()
        
        # Initialize component state
        self.processing_active = False
        
        # Update status
        self._update_status("Ready - Phase 1.4 with Output Panel")
    
    def _setup_window_geometry(self):
        """Setup window size and position from settings"""
        window_size = self.settings.get("window_size", [1200, 800])
        window_pos = self.settings.get("window_position", None)
        
        # Set minimum size
        self.root.minsize(1000, 750)  # Increased for Output Panel
        
        if window_pos:
            # Use saved position
            self.root.geometry(f"{window_size[0]}x{window_size[1]}+{window_pos[0]}+{window_pos[1]}")
        else:
            # Center on screen
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - window_size[0]) // 2
            y = (screen_height - window_size[1]) // 2
            self.root.geometry(f"{window_size[0]}x{window_size[1]}+{x}+{y}")
    
    def _create_menu_bar(self):
        """Create the application menu bar"""
        # Create menu bar frame
        self.menu_frame = ctk.CTkFrame(self.root, height=30)
        self.menu_frame.pack(fill="x", padx=5, pady=(5, 0))
        self.menu_frame.pack_propagate(False)
        
        # File menu button
        self.file_menu_btn = ctk.CTkOptionMenu(
            self.menu_frame,
            values=["New Session", "Open URL List...", "Save URL List...", "separator", "Exit"],
            command=self._handle_file_menu,
            width=80
        )
        self.file_menu_btn.set("File")
        self.file_menu_btn.pack(side="left", padx=(10, 5), pady=5)
        
        # Edit menu button
        self.edit_menu_btn = ctk.CTkOptionMenu(
            self.menu_frame,
            values=["Add URL", "Remove Selected", "Clear All", "Validate All", "separator", "Validate Settings", "Preferences..."],
            command=self._handle_edit_menu,
            width=80
        )
        self.edit_menu_btn.set("Edit")
        self.edit_menu_btn.pack(side="left", padx=5, pady=5)
        
        # View menu button
        self.view_menu_btn = ctk.CTkOptionMenu(
            self.menu_frame,
            values=["Light Mode", "Dark Mode", "System Mode", "separator", "Show Log", "Show Statistics"],
            command=self._handle_view_menu,
            width=80
        )
        self.view_menu_btn.set("View")
        self.view_menu_btn.pack(side="left", padx=5, pady=5)
        
        # Help menu button
        self.help_menu_btn = ctk.CTkOptionMenu(
            self.menu_frame,
            values=["User Guide", "Keyboard Shortcuts", "separator", "About"],
            command=self._handle_help_menu,
            width=80
        )
        self.help_menu_btn.set("Help")
        self.help_menu_btn.pack(side="left", padx=5, pady=5)
        
        # Add title in center
        self.title_label = ctk.CTkLabel(
            self.menu_frame,
            text="MS Learn Training Data Generator v0.1.4",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.pack(side="right", padx=10, pady=5)
    
    def _setup_main_layout(self):
        """Setup the main application layout with tabs"""
        # Create main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create tabbed interface
        self.tab_view = ctk.CTkTabview(self.main_container)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.processing_tab = self.tab_view.add("Processing")
        self.results_tab = self.tab_view.add("Results") 
        self.settings_tab = self.tab_view.add("Settings")
        
        # Setup Processing tab layout
        self._setup_processing_tab()
        
        # Setup Results tab layout
        self._setup_results_tab()
        
        # Setup Settings tab layout
        self._setup_settings_tab()
    
    def _setup_processing_tab(self):
        """Setup the main processing tab layout"""
        # Create main sections using grid layout
        self.processing_tab.grid_columnconfigure(1, weight=1)
        self.processing_tab.grid_rowconfigure(0, weight=1)
        
        # URL Management section (left side)
        self.url_manager = URLManager(
            self.processing_tab, 
            backend_generator=self.backend_generator
        )
        self.url_manager.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 5), pady=5)
        
        # Add status change callback for URL manager
        self.url_manager.add_status_change_callback(self._on_url_status_change)
        
        # Output & Settings Panel (top right) - NEW INTEGRATION
        self.output_panel = OutputPanel(
            self.processing_tab,
            settings_manager=self.settings
        )
        self.output_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Add change callback for output panel
        self.output_panel.add_change_callback(self._on_output_setting_change)
        
        # Progress and Control section (bottom right)
        self.control_section = ctk.CTkFrame(self.processing_tab)
        self.control_section.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.control_section.grid_columnconfigure(0, weight=1)
        self.control_section.grid_rowconfigure(1, weight=1)
        
        control_title = ctk.CTkLabel(
            self.control_section,
            text="Progress & Control",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        control_title.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")
        
        # Progress placeholder (Phase 1.5)
        self.progress_placeholder = ctk.CTkLabel(
            self.control_section,
            text="Progress tracking components\nwill be added in Phase 1.5\n\nUse the Output Panel above to\nconfigure processing settings",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.progress_placeholder.grid(row=1, column=0, pady=20, padx=20)
        
        # Control buttons
        self.button_frame = ctk.CTkFrame(self.control_section)
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.start_btn = ctk.CTkButton(
            self.button_frame,
            text="▶ Start Processing",
            command=self._start_processing,
            state="disabled"  # Disabled until Phase 1.5
        )
        self.start_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.pause_btn = ctk.CTkButton(
            self.button_frame,
            text="⏸ Pause",
            command=self._pause_processing,
            state="disabled"
        )
        self.pause_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.stop_btn = ctk.CTkButton(
            self.button_frame,
            text="⏹ Stop",
            command=self._stop_processing,
            state="disabled"
        )
        self.stop_btn.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
    
    def _setup_results_tab(self):
        """Setup the results tab layout"""
        # Results section
        results_title = ctk.CTkLabel(
            self.results_tab,
            text="Processing Results",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        results_title.pack(pady=(20, 10))
        
        # Results placeholder
        self.results_placeholder = ctk.CTkLabel(
            self.results_tab,
            text="Results preview and analytics\nwill be available after\nPhase 2 implementation",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.results_placeholder.pack(pady=50)
    
    def _setup_settings_tab(self):
        """Setup the settings tab layout"""
        # Settings section
        settings_title = ctk.CTkLabel(
            self.settings_tab,
            text="Application Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        settings_title.pack(pady=(20, 20))
        
        # Settings frame
        settings_frame = ctk.CTkFrame(self.settings_tab)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Appearance settings
        appearance_frame = ctk.CTkFrame(settings_frame)
        appearance_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            appearance_frame,
            text="Appearance",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Theme selection
        theme_frame = ctk.CTkFrame(appearance_frame)
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(theme_frame, text="Theme:").pack(side="left", padx=10)
        
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "system"))
        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            variable=self.theme_var,
            values=["system", "light", "dark"],
            command=self._change_theme
        )
        self.theme_menu.pack(side="left", padx=10)
        
        # Color theme selection
        color_frame = ctk.CTkFrame(appearance_frame)
        color_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(color_frame, text="Color Theme:").pack(side="left", padx=10)
        
        self.color_theme_var = tk.StringVar(value=self.settings.get("color_theme", "blue"))
        self.color_theme_menu = ctk.CTkOptionMenu(
            color_frame,
            variable=self.color_theme_var,
            values=["blue", "dark-blue", "green"],
            command=self._change_color_theme
        )
        self.color_theme_menu.pack(side="left", padx=10)
        
        # Processing note
        processing_note = ctk.CTkFrame(settings_frame)
        processing_note.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            processing_note,
            text="Processing Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(
            processing_note,
            text="Processing settings have been moved to the Output Panel\nin the Processing tab for better workflow integration.",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        ).pack(anchor="w", padx=10, pady=(0, 10))
    
    def _setup_status_bar(self):
        """Setup the status bar at the bottom"""
        self.status_frame = ctk.CTkFrame(self.root, height=35)
        self.status_frame.pack(fill="x", side="bottom", padx=10, pady=(0, 10))
        self.status_frame.pack_propagate(False)
        
        # Status sections
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Progress info (right side)
        self.progress_info_label = ctk.CTkLabel(
            self.status_frame,
            text="0 URLs | 0 ready | Settings: Not configured",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.progress_info_label.pack(side="right", padx=10, pady=5)
    
    def _bind_events(self):
        """Bind keyboard shortcuts and window events"""
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self._handle_file_menu("New Session"))
        self.root.bind('<Control-o>', lambda e: self._handle_file_menu("Open URL List..."))
        self.root.bind('<Control-s>', lambda e: self._handle_file_menu("Save URL List..."))
        self.root.bind('<Control-q>', lambda e: self._on_closing())
        self.root.bind('<F1>', lambda e: self._handle_help_menu("User Guide"))
        
        # URL management shortcuts
        self.root.bind('<Control-u>', lambda e: self._focus_url_entry())
        self.root.bind('<F5>', lambda e: self._handle_edit_menu("Validate All"))
        
        # Output panel shortcuts
        self.root.bind('<Control-b>', lambda e: self._browse_output_folder())
        self.root.bind('<F6>', lambda e: self._handle_edit_menu("Validate Settings"))
    
    def _handle_file_menu(self, choice):
        """Handle file menu selections"""
        if choice == "New Session":
            self._new_session()
        elif choice == "Open URL List...":
            self._open_url_list()
        elif choice == "Save URL List...":
            self._save_url_list()
        elif choice == "Exit":
            self._on_closing()
    
    def _handle_edit_menu(self, choice):
        """Handle edit menu selections"""
        if choice == "Add URL":
            self._focus_url_entry()
        elif choice == "Remove Selected":
            self._remove_selected_urls()
        elif choice == "Clear All":
            self._clear_all_urls()
        elif choice == "Validate All":
            self._validate_all_urls()
        elif choice == "Validate Settings":
            self._validate_settings()
        elif choice == "Preferences...":
            self.tab_view.set("Settings")
    
    def _handle_view_menu(self, choice):
        """Handle view menu selections"""
        if choice in ["Light Mode", "Dark Mode", "System Mode"]:
            theme_map = {"Light Mode": "light", "Dark Mode": "dark", "System Mode": "system"}
            self._change_theme(theme_map[choice])
        elif choice == "Show Log":
            # Will be implemented in Phase 1.6
            self._update_status("Log view will be available in Phase 1.6")
        elif choice == "Show Statistics":
            # Will be implemented in Phase 2
            self._update_status("Statistics will be available in Phase 2")
    
    def _handle_help_menu(self, choice):
        """Handle help menu selections"""
        if choice == "User Guide":
            messagebox.showinfo(
                "User Guide",
                "MS Learn Training Data Generator\n\n"
                "This application extracts high-quality training data from Microsoft Learn documentation.\n\n"
                "Current Phase: 1.4 - Output & Settings Panel\n"
                "✓ Add/remove URLs with validation\n"
                "✓ Output folder configuration\n"
                "✓ Category selection and customization\n"
                "✓ Processing settings with validation\n\n"
                "Next: Phase 1.5 - Progress & Processing Control"
            )
        elif choice == "Keyboard Shortcuts":
            messagebox.showinfo(
                "Keyboard Shortcuts",
                "File Operations:\n"
                "Ctrl+N - New Session\n"
                "Ctrl+O - Open URL List\n"
                "Ctrl+S - Save URL List\n"
                "Ctrl+Q - Exit\n\n"
                "URL Management:\n"
                "Ctrl+U - Focus URL entry\n"
                "F5 - Validate all URLs\n\n"
                "Output Settings:\n"
                "Ctrl+B - Browse output folder\n"
                "F6 - Validate settings\n\n"
                "Help:\n"
                "F1 - User Guide"
            )
        elif choice == "About":
            messagebox.showinfo(
                "About",
                "MS Learn Training Data Generator\n"
                "Version: 0.1.4 (Phase 1.4)\n\n"
                "A professional GUI for extracting high-quality training data\n"
                "from Microsoft Learn documentation.\n\n"
                "✓ URL Management with validation\n"
                "✓ Output & settings configuration\n"
                "✓ Category selection and customization\n"
                "✓ Processing parameter validation\n\n"
                "Built with CustomTkinter\n"
                "© 2025 MS Learn GUI Team"
            )
    
    def _change_theme(self, theme):
        """Change application theme"""
        ctk.set_appearance_mode(theme)
        self.settings.set("theme", theme)
        self.theme_var.set(theme)
        self._update_status(f"Theme changed to {theme}")
    
    def _change_color_theme(self, color_theme):
        """Change color theme (requires restart)"""
        self.settings.set("color_theme", color_theme)
        self._update_status(f"Color theme changed to {color_theme} (restart required)")
    
    def _new_session(self):
        """Start a new session"""
        self.url_manager.clear_all()
        self._update_status("New session started")
    
    def _open_url_list(self):
        """Open URL list from file"""
        file_path = filedialog.askopenfilename(
            title="Open URL List",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f.readlines() if line.strip()]
                
                for url in urls:
                    self.url_manager.add_url(url)
                
                self.settings.add_recent_url_list(file_path)
                self._update_status(f"Loaded {len(urls)} URLs from {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load URL list:\n{str(e)}")
                self._update_status("Failed to load URL list")
    
    def _save_url_list(self):
        """Save current URL list"""
        urls = self.url_manager.get_urls()
        if not urls:
            self._update_status("No URLs to save")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save URL List",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for url in urls:
                        f.write(f"{url}\n")
                
                self._update_status(f"Saved {len(urls)} URLs to {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save URL list:\n{str(e)}")
                self._update_status("Failed to save URL list")
    
    def _focus_url_entry(self):
        """Focus the URL entry field"""
        self.tab_view.set("Processing")
        self.url_manager.url_entry.focus()
        self._update_status("Add URL by typing in the entry field")
    
    def _browse_output_folder(self):
        """Focus the output panel folder browser"""
        self.tab_view.set("Processing")
        self.output_panel._browse_output_folder()
    
    def _remove_selected_urls(self):
        """Remove selected URLs"""
        # For now, show info about functionality
        self._update_status("Individual URL removal available via × button on each URL")
    
    def _clear_all_urls(self):
        """Clear all URLs"""
        if self.url_manager.get_urls():
            result = messagebox.askyesno(
                "Clear All URLs",
                f"Are you sure you want to clear all {len(self.url_manager.get_urls())} URLs?"
            )
            if result:
                self.url_manager.clear_all()
                self._update_status("All URLs cleared")
        else:
            self._update_status("No URLs to clear")
    
    def _validate_all_urls(self):
        """Validate all URLs using backend"""
        urls = self.url_manager.get_urls()
        if not urls:
            self._update_status("No URLs to validate")
            return
        
        self.url_manager._validate_all_urls()
        self._update_status(f"Validating {len(urls)} URLs...")
    
    def _validate_settings(self):
        """Validate output panel settings"""
        self.tab_view.set("Processing")
        self.output_panel._validate_settings()
    
    def _start_processing(self):
        """Start URL processing"""
        ready_urls = self.url_manager.get_ready_urls()
        if not ready_urls:
            messagebox.showwarning(
                "No Ready URLs",
                "No URLs are ready for processing.\n\nPlease add and validate URLs first."
            )
            return
        
        if not self.output_panel.is_ready_for_processing():
            messagebox.showwarning(
                "Settings Not Ready",
                "Output settings are not properly configured.\n\nPlease configure output folder and validate settings."
            )
            return
        
        # This will be implemented in Phase 1.5
        settings = self.output_panel.get_all_settings()
        self._update_status(f"Processing control will be available in Phase 1.5 ({len(ready_urls)} URLs ready, settings configured)")
    
    def _pause_processing(self):
        """Pause processing"""
        # This will be implemented in Phase 1.5
        self._update_status("Processing control will be available in Phase 1.5")
    
    def _stop_processing(self):
        """Stop processing"""
        # This will be implemented in Phase 1.5
        self._update_status("Processing control will be available in Phase 1.5")
    
    def _on_url_status_change(self):
        """Handle URL status changes from URL manager"""
        self._update_status_info()
    
    def _on_output_setting_change(self, setting_name, value):
        """Handle output panel setting changes"""
        self._update_status(f"Setting updated: {setting_name}")
        self._update_status_info()
    
    def _update_status(self, message):
        """Update status bar message"""
        self.status_label.configure(text=message)
        self._update_status_info()
    
    def _update_status_info(self):
        """Update status bar progress information"""
        url_items = self.url_manager.get_url_items()
        url_count = len(url_items)
        
        # Count by status
        status_counts = {}
        for item in url_items:
            status_counts[item.status] = status_counts.get(item.status, 0) + 1
        
        ready_count = status_counts.get("ready", 0)
        failed_count = status_counts.get("failed", 0) + status_counts.get("invalid", 0)
        processing_count = status_counts.get("processing", 0)
        completed_count = status_counts.get("completed", 0)
        
        # Check settings status
        settings_ready = self.output_panel.is_ready_for_processing()
        settings_status = "✓ Ready" if settings_ready else "⚠️ Check Settings"
        
        if processing_count > 0:
            status_text = f"{url_count} URLs | {ready_count} ready | {processing_count} processing | {failed_count} failed | Settings: {settings_status}"
        else:
            status_text = f"{url_count} URLs | {ready_count} ready | {completed_count} completed | {failed_count} failed | Settings: {settings_status}"
        
        self.progress_info_label.configure(text=status_text)
    
    def _on_closing(self):
        """Handle window closing event"""
        # Save window geometry and position
        geometry = self.root.geometry()
        if '+' in geometry and 'x' in geometry:
            try:
                size_and_pos = geometry.split('+')
                size_str = size_and_pos[0]
                pos_x, pos_y = int(size_and_pos[1]), int(size_and_pos[2])
                
                if 'x' in size_str:
                    width, height = map(int, size_str.split('x'))
                    self.settings.set("window_size", [width, height])
                    self.settings.set("window_position", [pos_x, pos_y])
            except (ValueError, IndexError):
                pass  # Keep existing settings if parsing fails
        
        # Settings are automatically saved by the output panel
        
        # Save and exit
        self.settings.save()
        self.root.destroy()
    
    def run(self):
        """Run the application main loop"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MSLearnGUIApp()
    app.run()