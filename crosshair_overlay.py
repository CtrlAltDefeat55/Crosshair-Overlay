import tkinter as tk
from tkinter import ttk
import sys
import json
import os

class CrosshairOverlay:
    def __init__(self):
        # Create the main window for UI controls
        self.root = tk.Tk()
        self.root.title("Crosshair Overlay Controller")
        self.root.geometry("400x700")  # Increased height to show all settings
        self.root.resizable(True, True)  # Make resizable
        
        # Crosshair types
        self.crosshair_types = [
            "Standard", "Circle", "Dot", "Plus", "X", 
            "Cross", "Target", "Square", "Diamond", "Arrow"
        ]
        
        # Initialize overlay window as None
        self.overlay = None
        self.overlay_window = None
        
        # Store drag coordinates
        self.drag_data = {"x": 0, "y": 0}
        
        # Preset management
        self.presets = {}
        self.current_preset = "Default"
        
        # Create UI elements first
        self.create_ui()
        
        # Load presets and last state after UI is created
        self.load_presets()
        self.load_last_state()
        
        # Apply loaded state to UI
        self.apply_loaded_state()
        
        # Track overlay state
        self.is_overlay_active = False
        self.is_locked = True  # Locked by default
        
        # Current crosshair type (index)
        self.current_crosshair = 0  # Default to Standard
        
        # Start the overlay automatically
        self.root.after(100, self.start_overlay)
        
    def apply_loaded_state(self):
        """Apply the loaded state to the UI elements"""
        if self.current_preset in self.presets:
            preset = self.presets[self.current_preset]
            self.type_var.set(preset.get("type", "Standard"))
            self.color_var.set(preset.get("color", "red"))
            self.size_var.set(preset.get("size", "20"))
            self.opacity_var.set(preset.get("opacity", "1.0"))
        elif self.current_preset == "Default":
            # Use default values
            self.type_var.set("Standard")
            self.color_var.set("red")
            self.size_var.set("20")
            self.opacity_var.set("1.0")
            
        # Update sliders to match
        self.size_slider.set(int(self.size_var.get()))
        self.opacity_slider.set(float(self.opacity_var.get()))
        
        # Update preset combobox
        self.preset_var.set(self.current_preset)
        
    def create_ui(self):
        # Title label
        title_label = tk.Label(self.root, text="Crosshair Overlay", font=("Arial", 16))
        title_label.pack(pady=10)
        
        # Status indicator
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=5)
        
        tk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.status_indicator = tk.Label(status_frame, text="●", fg="red", font=("Arial", 16))
        self.status_indicator.pack(side=tk.LEFT, padx=(5, 0))
        self.status_label = tk.Label(status_frame, text="Overlay: Stopped")
        self.status_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        self.toggle_button = tk.Button(button_frame, text="Start Overlay", command=self.toggle_overlay, width=15)
        self.toggle_button.pack(pady=5)
        
        # Lock/Unlock button
        self.lock_button = tk.Button(button_frame, text="Unlock Position", command=self.toggle_lock, width=15)
        self.lock_button.pack(pady=5)
        
        # Reset position button
        self.reset_button = tk.Button(button_frame, text="Reset Position", command=self.reset_position, width=15, state=tk.DISABLED)
        self.reset_button.pack(pady=5)
        
        self.exit_button = tk.Button(button_frame, text="Exit", command=self.exit_app, width=15)
        self.exit_button.pack(pady=5)
        
        # Preset management
        preset_frame = tk.LabelFrame(self.root, text="Presets")
        preset_frame.pack(pady=10, padx=20, fill="x")
        
        # New preset creation
        new_preset_frame = tk.Frame(preset_frame)
        new_preset_frame.pack(pady=5, fill="x")
        
        tk.Label(new_preset_frame, text="New Preset:").pack(side=tk.LEFT)
        self.new_preset_entry = tk.Entry(new_preset_frame, width=10)
        self.new_preset_entry.pack(side=tk.LEFT, padx=(5, 5))
        tk.Button(new_preset_frame, text="Create", command=self.create_preset, width=8).pack(side=tk.LEFT)
        
        # Preset selection and management
        preset_buttons_frame = tk.Frame(preset_frame)
        preset_buttons_frame.pack(pady=5)
        
        self.preset_var = tk.StringVar(value="Default")
        self.preset_combo = ttk.Combobox(preset_buttons_frame, textvariable=self.preset_var, 
                                   values=["Default"], 
                                   state="readonly", width=12)
        self.preset_combo.pack(side=tk.LEFT, padx=(0, 5))
        self.preset_combo.bind('<<ComboboxSelected>>', self.load_preset)
        
        tk.Button(preset_buttons_frame, text="Save", command=self.save_preset, width=8).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(preset_buttons_frame, text="Delete", command=self.delete_preset, width=8).pack(side=tk.LEFT)
        
        # Crosshair settings
        settings_frame = tk.LabelFrame(self.root, text="Crosshair Settings")
        settings_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Crosshair type selection
        type_frame = tk.Frame(settings_frame)
        type_frame.pack(pady=5, fill="x")
        
        tk.Label(type_frame, text="Type:").pack(side=tk.LEFT)
        self.type_var = tk.StringVar(value="Standard")
        type_combo = ttk.Combobox(type_frame, textvariable=self.type_var, 
                                 values=self.crosshair_types, 
                                 state="readonly", width=12)
        type_combo.pack(side=tk.LEFT, padx=(5, 0))
        type_combo.bind('<<ComboboxSelected>>', self.on_type_change)
        
        # Color selection
        color_frame = tk.Frame(settings_frame)
        color_frame.pack(pady=5, fill="x")
        
        tk.Label(color_frame, text="Color:").pack(side=tk.LEFT)
        self.color_var = tk.StringVar(value="red")
        color_combo = ttk.Combobox(color_frame, textvariable=self.color_var, 
                                  values=["red", "green", "blue", "white", "yellow", "cyan", "magenta"], 
                                  state="readonly", width=12)
        color_combo.pack(side=tk.LEFT, padx=(5, 0))
        color_combo.bind('<<ComboboxSelected>>', self.on_setting_change)
        
        # Size selection with slider
        size_frame = tk.Frame(settings_frame)
        size_frame.pack(pady=5, fill="x")
        
        tk.Label(size_frame, text="Size:").pack(side=tk.LEFT)
        self.size_var = tk.StringVar(value="20")
        size_entry = tk.Entry(size_frame, textvariable=self.size_var, width=5)
        size_entry.pack(side=tk.LEFT, padx=(5, 0))
        size_entry.bind('<Return>', self.on_setting_change)
        size_entry.bind('<FocusOut>', self.on_setting_change)
        
        # Size slider
        self.size_slider = tk.Scale(size_frame, from_=5, to=50, orient=tk.HORIZONTAL, 
                                   variable=self.size_var, command=self.on_size_slider_change,
                                   length=100)
        self.size_slider.set(20)
        self.size_slider.pack(side=tk.LEFT, padx=(5, 0))
        
        # Opacity selection with slider
        opacity_frame = tk.Frame(settings_frame)
        opacity_frame.pack(pady=5, fill="x")
        
        tk.Label(opacity_frame, text="Opacity:").pack(side=tk.LEFT)
        self.opacity_var = tk.StringVar(value="1.0")
        opacity_entry = tk.Entry(opacity_frame, textvariable=self.opacity_var, width=5)
        opacity_entry.pack(side=tk.LEFT, padx=(5, 0))
        opacity_entry.bind('<Return>', self.on_setting_change)
        opacity_entry.bind('<FocusOut>', self.on_setting_change)
        
        # Opacity slider
        self.opacity_slider = tk.Scale(opacity_frame, from_=0.1, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, 
                                      variable=self.opacity_var, command=self.on_opacity_slider_change,
                                      length=100)
        self.opacity_slider.set(1.0)
        self.opacity_slider.pack(side=tk.LEFT, padx=(5, 0))
        
        # Feedback label
        self.feedback_label = tk.Label(self.root, text="", fg="blue")
        self.feedback_label.pack(pady=5)
        
    def show_feedback(self, message):
        self.feedback_label.config(text=message)
        self.root.after(2000, lambda: self.feedback_label.config(text=""))  # Clear after 2 seconds
        
    def on_type_change(self, event=None):
        if self.is_overlay_active:
            self.draw_crosshair()
        self.show_feedback(f"Crosshair type changed to {self.type_var.get()}")
        
    def on_size_slider_change(self, value):
        self.size_var.set(int(float(value)))
        self.on_setting_change()
        
    def on_opacity_slider_change(self, value):
        self.opacity_var.set(float(value))
        self.on_setting_change()
        
    def toggle_overlay(self):
        if self.is_overlay_active:
            self.stop_overlay()
        else:
            self.start_overlay()
            
    def start_overlay(self):
        # Create overlay window if it doesn't exist
        if self.overlay_window is None:
            self.create_overlay()
        else:
            # If overlay exists, update its properties
            self.update_overlay_properties()
            
        # Show the overlay
        self.overlay_window.deiconify()
        self.is_overlay_active = True
        self.toggle_button.config(text="Stop Overlay")
        self.status_label.config(text="Overlay: Running")
        self.status_indicator.config(fg="green")
        self.reset_button.config(state=tk.NORMAL if not self.is_locked else tk.DISABLED)
        self.show_feedback("Overlay started")
        
        # Force a redraw of the crosshair
        self.root.after(50, self.draw_crosshair)
        
    def stop_overlay(self):
        if self.overlay_window:
            self.overlay_window.withdraw()
            self.is_overlay_active = False
            self.toggle_button.config(text="Start Overlay")
            self.status_label.config(text="Overlay: Stopped")
            self.status_indicator.config(fg="red")
            self.reset_button.config(state=tk.DISABLED)
            self.show_feedback("Overlay stopped")
            
    def toggle_lock(self):
        self.is_locked = not self.is_locked
        if self.is_locked:
            self.lock_button.config(text="Unlock Position")
            self.reset_button.config(state=tk.DISABLED)
            # Remove drag bindings when locked
            if self.overlay_window:
                self.overlay_window.unbind('<Button-1>')
                self.overlay_window.unbind('<B1-Motion>')
            self.show_feedback("Overlay locked in place")
        else:
            self.lock_button.config(text="Lock Position")
            self.reset_button.config(state=tk.NORMAL if self.is_overlay_active else tk.DISABLED)
            # Add drag bindings when unlocked
            if self.overlay_window:
                self.overlay_window.bind('<Button-1>', self.drag_start)
                self.overlay_window.bind('<B1-Motion>', self.drag_move)
            self.show_feedback("Overlay unlocked - can be moved")
            
    def reset_position(self):
        if self.overlay_window:
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Get window size
            size = int(self.size_var.get())
            window_size = size * 4  # Larger window for better visibility
            
            # Center the window
            x = screen_width // 2 - window_size // 2
            y = screen_height // 2 - window_size // 2
            
            self.overlay_window.geometry(f"{window_size}x{window_size}+{x}+{y}")
            self.show_feedback("Overlay position reset to center")
            
    def create_overlay(self):
        # Create a transparent overlay window
        self.overlay_window = tk.Toplevel(self.root)
        self.overlay_window.title("Crosshair Overlay")
        
        # Remove window decorations
        self.overlay_window.overrideredirect(True)
        
        # Make it transparent with alpha
        self.overlay_window.attributes('-alpha', float(self.opacity_var.get()))
        
        # Keep on top
        self.overlay_window.attributes('-topmost', True)
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set window size (adjust as needed)
        size = int(self.size_var.get())
        window_size = size * 4  # Larger window for better visibility
        self.overlay_window.geometry(f"{window_size}x{window_size}+{screen_width//2 - window_size//2}+{screen_height//2 - window_size//2}")
        
        # Create canvas for crosshair with a transparent background
        self.overlay = tk.Canvas(self.overlay_window, bg='white', highlightthickness=0)
        self.overlay.pack(fill=tk.BOTH, expand=True)
        
        # Make the window background transparent
        self.overlay_window.wm_attributes("-transparentcolor", "white")
        
        # Draw crosshair
        self.draw_crosshair()
        
        # Hide initially
        self.overlay_window.withdraw()
        
        # Bind events only if unlocked
        if not self.is_locked:
            self.overlay_window.bind('<Button-1>', self.drag_start)
            self.overlay_window.bind('<B1-Motion>', self.drag_move)
            
    def update_overlay_properties(self):
        """Update the overlay properties without recreating it"""
        if self.overlay_window:
            # Update opacity
            self.overlay_window.attributes('-alpha', float(self.opacity_var.get()))
            
            # Update size and position
            size = int(self.size_var.get())
            window_size = size * 4
            x = self.overlay_window.winfo_x()
            y = self.overlay_window.winfo_y()
            self.overlay_window.geometry(f"{window_size}x{window_size}+{x}+{y}")
            
            # Update transparency color
            self.overlay_window.wm_attributes("-transparentcolor", "white")
            
    def draw_crosshair(self):
        if self.overlay:
            # Clear canvas
            self.overlay.delete("all")
            
            # Get current settings
            color = self.color_var.get()
            size = int(self.size_var.get())
            crosshair_type = self.type_var.get()
            
            # Get canvas dimensions
            canvas_width = self.overlay.winfo_width()
            canvas_height = self.overlay.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:  # Only draw if canvas has size
                center_x = canvas_width // 2
                center_y = canvas_height // 2
                
                # Draw different crosshair types
                if crosshair_type == "Standard":
                    # Horizontal line
                    self.overlay.create_line(center_x - size, center_y, center_x + size, center_y, 
                                           fill=color, width=2)
                    # Vertical line
                    self.overlay.create_line(center_x, center_y - size, center_x, center_y + size, 
                                           fill=color, width=2)
                    # Center dot
                    self.overlay.create_oval(center_x - 2, center_y - 2, center_x + 2, center_y + 2, 
                                           fill=color, outline=color)
                                           
                elif crosshair_type == "Circle":
                    # Outer circle
                    self.overlay.create_oval(center_x - size, center_y - size, center_x + size, center_y + size, 
                                           outline=color, width=2)
                    # Inner circle
                    self.overlay.create_oval(center_x - size//2, center_y - size//2, center_x + size//2, center_y + size//2, 
                                           outline=color, width=1)
                    # Center dot
                    self.overlay.create_oval(center_x - 2, center_y - 2, center_x + 2, center_y + 2, 
                                           fill=color, outline=color)
                                           
                elif crosshair_type == "Dot":
                    # Large center dot
                    self.overlay.create_oval(center_x - size//4, center_y - size//4, center_x + size//4, center_y + size//4, 
                                           fill=color, outline=color)
                                           
                elif crosshair_type == "Plus":
                    # Thick plus sign
                    self.overlay.create_line(center_x - size, center_y, center_x + size, center_y, 
                                           fill=color, width=4)
                    self.overlay.create_line(center_x, center_y - size, center_x, center_y + size, 
                                           fill=color, width=4)
                                           
                elif crosshair_type == "X":
                    # X shape
                    self.overlay.create_line(center_x - size, center_y - size, center_x + size, center_y + size, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x + size, center_y - size, center_x - size, center_y + size, 
                                           fill=color, width=2)
                                           
                elif crosshair_type == "Cross":
                    # Cross with arrows
                    # Horizontal line with arrows
                    self.overlay.create_line(center_x - size, center_y, center_x + size, center_y, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x - size, center_y, center_x - size + 5, center_y - 5, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x - size, center_y, center_x - size + 5, center_y + 5, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x + size, center_y, center_x + size - 5, center_y - 5, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x + size, center_y, center_x + size - 5, center_y + 5, 
                                           fill=color, width=2)
                                           
                    # Vertical line with arrows
                    self.overlay.create_line(center_x, center_y - size, center_x, center_y + size, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x, center_y - size, center_x - 5, center_y - size + 5, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x, center_y - size, center_x + 5, center_y - size + 5, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x, center_y + size, center_x - 5, center_y + size - 5, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x, center_y + size, center_x + 5, center_y + size - 5, 
                                           fill=color, width=2)
                                           
                elif crosshair_type == "Target":
                    # Concentric circles
                    for i in range(1, 4):
                        radius = size * i // 3
                        self.overlay.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, 
                                               outline=color, width=1)
                    # Center dot
                    self.overlay.create_oval(center_x - 2, center_y - 2, center_x + 2, center_y + 2, 
                                           fill=color, outline=color)
                                           
                elif crosshair_type == "Square":
                    # Square outline
                    self.overlay.create_rectangle(center_x - size, center_y - size, center_x + size, center_y + size, 
                                                outline=color, width=2)
                    # Center dot
                    self.overlay.create_oval(center_x - 2, center_y - 2, center_x + 2, center_y + 2, 
                                           fill=color, outline=color)
                                           
                elif crosshair_type == "Diamond":
                    # Diamond shape
                    self.overlay.create_line(center_x, center_y - size, center_x - size, center_y, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x - size, center_y, center_x, center_y + size, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x, center_y + size, center_x + size, center_y, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x + size, center_y, center_x, center_y - size, 
                                           fill=color, width=2)
                    # Center dot
                    self.overlay.create_oval(center_x - 2, center_y - 2, center_x + 2, center_y + 2, 
                                           fill=color, outline=color)
                                           
                elif crosshair_type == "Arrow":
                    # Arrow pointing up
                    self.overlay.create_line(center_x, center_y - size, center_x, center_y + size, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x, center_y - size, center_x - 10, center_y - size + 15, 
                                           fill=color, width=2)
                    self.overlay.create_line(center_x, center_y - size, center_x + 10, center_y - size + 15, 
                                           fill=color, width=2)
                    # Center dot
                    self.overlay.create_oval(center_x - 2, center_y - 2, center_x + 2, center_y + 2, 
                                           fill=color, outline=color)
        
    def on_setting_change(self, event=None):
        # Validate size input
        try:
            size = int(self.size_var.get())
            if size < 1:
                size = 1
                self.size_var.set("1")
            elif size > 100:
                size = 100
                self.size_var.set("100")
        except ValueError:
            size = 20
            self.size_var.set("20")
            
        # Validate opacity input
        try:
            opacity = float(self.opacity_var.get())
            if opacity < 0.1:
                opacity = 0.1
                self.opacity_var.set("0.1")
            elif opacity > 1.0:
                opacity = 1.0
                self.opacity_var.set("1.0")
        except ValueError:
            opacity = 1.0
            self.opacity_var.set("1.0")
            
        # Update slider positions
        self.size_slider.set(size)
        self.opacity_slider.set(opacity)
        
        # Update overlay when settings change
        if self.is_overlay_active:
            # Update opacity
            if self.overlay_window:
                self.overlay_window.attributes('-alpha', opacity)
                # Update size and recenter if locked
                window_size = size * 4
                if self.is_locked:
                    # If locked, recenter the window
                    screen_width = self.root.winfo_screenwidth()
                    screen_height = self.root.winfo_screenheight()
                    x = screen_width // 2 - window_size // 2
                    y = screen_height // 2 - window_size // 2
                    self.overlay_window.geometry(f"{window_size}x{window_size}+{x}+{y}")
                else:
                    # If unlocked, just resize maintaining position
                    x = self.overlay_window.winfo_x()
                    y = self.overlay_window.winfo_y()
                    self.overlay_window.geometry(f"{window_size}x{window_size}+{x}+{y}")
            
            # Redraw crosshair
            self.draw_crosshair()
            
        # Show feedback
        if event:
            self.show_feedback("Settings updated")
            
    def drag_start(self, event):
        # Record the starting position
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        
    def drag_move(self, event):
        # Calculate the new position
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        
        # Move the window
        x = self.overlay_window.winfo_x() + delta_x
        y = self.overlay_window.winfo_y() + delta_y
        self.overlay_window.geometry(f"+{x}+{y}")
        
    def create_preset(self):
        """Create a new preset"""
        preset_name = self.new_preset_entry.get().strip()
        if not preset_name or preset_name == "Default":
            self.show_feedback("Please enter a valid preset name")
            return
            
        if preset_name in self.presets:
            self.show_feedback(f"Preset '{preset_name}' already exists")
            return
            
        self.presets[preset_name] = {
            "type": self.type_var.get(),
            "color": self.color_var.get(),
            "size": self.size_var.get(),
            "opacity": self.opacity_var.get()
        }
        
        self.save_presets()
        self.update_preset_combo()
        self.show_feedback(f"Preset '{preset_name}' created")
        self.new_preset_entry.delete(0, tk.END)
        
    def save_preset(self):
        """Save current settings to the selected preset"""
        preset_name = self.preset_var.get()
        if preset_name == "Default":
            self.show_feedback("Cannot overwrite Default preset. Create a new one instead.")
            return
            
        self.presets[preset_name] = {
            "type": self.type_var.get(),
            "color": self.color_var.get(),
            "size": self.size_var.get(),
            "opacity": self.opacity_var.get()
        }
        
        self.save_presets()
        self.show_feedback(f"Preset '{preset_name}' saved")
        
    def load_preset(self, event=None):
        """Load settings from a preset"""
        preset_name = self.preset_var.get()
        self.current_preset = preset_name
        
        if preset_name in self.presets:
            preset = self.presets[preset_name]
            self.type_var.set(preset["type"])
            self.color_var.set(preset["color"])
            self.size_var.set(preset["size"])
            self.opacity_var.set(preset["opacity"])
            
            # Update sliders
            self.size_slider.set(int(preset["size"]))
            self.opacity_slider.set(float(preset["opacity"]))
            
            # Apply settings to overlay if active
            if self.is_overlay_active:
                self.on_setting_change()
                
            self.show_feedback(f"Preset '{preset_name}' loaded")
        elif preset_name == "Default":
            # Reset to default values
            self.type_var.set("Standard")
            self.color_var.set("red")
            self.size_var.set("20")
            self.opacity_var.set("1.0")
            
            # Update sliders
            self.size_slider.set(20)
            self.opacity_slider.set(1.0)
            
            # Apply settings to overlay if active
            if self.is_overlay_active:
                self.on_setting_change()
                
            self.show_feedback("Default preset loaded")
            
    def delete_preset(self):
        """Delete the current preset"""
        preset_name = self.preset_var.get()
        if preset_name == "Default":
            self.show_feedback("Cannot delete Default preset")
            return
            
        if preset_name in self.presets:
            del self.presets[preset_name]
            self.save_presets()
            self.update_preset_combo()
            self.preset_var.set("Default")
            self.show_feedback(f"Preset '{preset_name}' deleted")
            
    def update_preset_combo(self):
        """Update the preset combobox with current presets"""
        # Update the values in the combobox
        preset_names = list(self.presets.keys()) + ["Default"]
        self.preset_combo['values'] = preset_names
        
    def save_presets(self):
        """Save presets to a JSON file"""
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            presets_file = os.path.join(script_dir, "crosshair_presets.json")
            
            with open(presets_file, 'w') as f:
                json.dump(self.presets, f, indent=2)
                
            # Also save the last state
            self.save_last_state()
        except Exception as e:
            print(f"Error saving presets: {str(e)}")
            # We can't use show_feedback here because it might not be available during initialization
            
    def load_presets(self):
        """Load presets from a JSON file"""
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            presets_file = os.path.join(script_dir, "crosshair_presets.json")
            
            if os.path.exists(presets_file):
                with open(presets_file, 'r') as f:
                    self.presets = json.load(f)
            else:
                # Create default presets file
                self.presets = {}
                self.save_presets()
        except Exception as e:
            print(f"Error loading presets: {str(e)}")
            self.presets = {}
            
    def save_last_state(self):
        """Save the last state (current preset or settings)"""
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            state_file = os.path.join(script_dir, "crosshair_last_state.json")
            
            state = {
                "current_preset": self.current_preset,
                "settings": {
                    "type": self.type_var.get(),
                    "color": self.color_var.get(),
                    "size": self.size_var.get(),
                    "opacity": self.opacity_var.get()
                }
            }
            
            with open(state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"Error saving state: {str(e)}")
            # We can't use show_feedback here because it might cause issues during initialization
            
    def load_last_state(self):
        """Load the last state (current preset or settings)"""
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            state_file = os.path.join(script_dir, "crosshair_last_state.json")
            
            if os.path.exists(state_file):
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    
                self.current_preset = state.get("current_preset", "Default")
                
                # Load settings if not using a named preset
                if self.current_preset == "Default" or self.current_preset not in self.presets:
                    settings = state.get("settings", {})
                    if settings:
                        # These will be applied in apply_loaded_state
                        pass
        except Exception as e:
            print(f"Error loading state: {str(e)}")
            
    def exit_app(self):
        # Save the current state before exiting
        self.save_last_state()
        
        # Properly close the application
        if self.overlay_window:
            self.overlay_window.destroy()
        self.root.destroy()
        sys.exit()
        
    def run(self):
        # Bind the configure event to redraw crosshair when window is resized
        if self.overlay_window:
            self.overlay_window.bind('<Configure>', lambda e: self.draw_crosshair())
            
        # Start the main loop
        self.root.mainloop()

def main():
    app = CrosshairOverlay()
    app.run()

if __name__ == "__main__":
    main()