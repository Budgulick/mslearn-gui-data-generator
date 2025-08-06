"""
Main window for MS Learn GUI Data Generator
Phase 1.2 implementation
"""

import customtkinter as ctk
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import Settings

class MSLearnGUIApp:
    """
    Main application window for MS Learn Data Generator
    """
    
    def __init__(self):
        """Initialize the main application window"""
        # Set appearance mode and color theme
        ctk.set_appearance_mode("system")  # Modes: system, light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue, dark-blue, green
        
        # Initialize settings
        self.settings = Settings()
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("MS Learn Training Data Generator")
        
        # Set window size and position
        self._setup_window_geometry()
        
        # Setup UI components
        self._setup_ui()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_window_geometry(self):
        """Setup window size and position from settings"""
        window_size = self.settings.get("window_size", [1200, 800])
        
        # Calculate center position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_size[0]) // 2
        y = (screen_height - window_size[1]) // 2
        
        self.root.geometry(f"{window_size[0]}x{window_size[1]}+{x}+{y}")
        self.root.minsize(800, 600)
    
    def _setup_ui(self):
        """Setup the main UI components"""
        # Create main container frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title label
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="MS Learn Training Data Generator",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(10, 20))
        
        # Placeholder for components (Phase 1.3+)
        self.placeholder_label = ctk.CTkLabel(
            self.main_frame,
            text="Components will be added in Phase 1.3+",
            font=ctk.CTkFont(size=14)
        )
        self.placeholder_label.pack(pady=50)
        
        # Status bar at bottom
        self.status_frame = ctk.CTkFrame(self.root, height=30)
        self.status_frame.pack(fill="x", side="bottom", padx=10, pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(side="left", padx=10)
    
    def _on_closing(self):
        """Handle window closing event"""
        # Save window geometry
        geometry = self.root.geometry()
        if '+' in geometry:
            size_str = geometry.split('+')[0]
            if 'x' in size_str:
                width, height = map(int, size_str.split('x'))
                self.settings.set("window_size", [width, height])
        
        # Save settings and close
        self.settings.save()
        self.root.destroy()
    
    def run(self):
        """Run the application main loop"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MSLearnGUIApp()
    app.run()
