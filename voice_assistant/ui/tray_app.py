"""
System Tray Application UI using pystray
Provides background app with tray icon, status indicators, and menu
"""
import threading
from typing import Optional, Callable
import sys

# Use PIL for icon
from PIL import Image, ImageDraw

class TrayApp:
    """
    System tray application for the Voice Assistant
    Runs in background with tray icon and context menu
    """
    
    # Status colors
    STATUS_IDLE = (100, 100, 100)      # Gray
    STATUS_LISTENING = (0, 200, 0)      # Green  
    STATUS_PROCESSING = (255, 165, 0)   # Orange
    STATUS_SPEAKING = (0, 100, 255)     # Blue
    STATUS_ERROR = (255, 0, 0)          # Red
    
    def __init__(
        self,
        app_name: str = "Voice Assistant",
        on_show: Optional[Callable] = None,
        on_quit: Optional[Callable] = None,
        on_toggle_listening: Optional[Callable] = None
    ):
        """
        Initialize tray application
        
        Args:
            app_name: Name shown in tray tooltip
            on_show: Callback when "Show" is clicked
            on_quit: Callback when "Quit" is clicked
            on_toggle_listening: Callback to toggle listening
        """
        self.app_name = app_name
        self._on_show = on_show
        self._on_quit = on_quit
        self._on_toggle_listening = on_toggle_listening
        
        self._icon = None
        self._status = "idle"
        self._is_listening = True
        self._thread: Optional[threading.Thread] = None
        
        self._pystray_available = False
        self._check_pystray()
    
    def _check_pystray(self):
        """Check if pystray is available"""
        try:
            import pystray
            self._pystray_available = True
        except ImportError:
            print("[Tray] pystray not installed, tray icon disabled")
            self._pystray_available = False
    
    def _create_icon_image(self, color: tuple = STATUS_IDLE, size: int = 64) -> Image.Image:
        """
        Create a simple icon image with status color
        
        Args:
            color: RGB tuple for icon color
            size: Icon size in pixels
        
        Returns:
            PIL Image
        """
        # Create circular icon with microphone symbol
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw outer circle
        padding = 4
        draw.ellipse(
            [padding, padding, size - padding, size - padding],
            fill=color
        )
        
        # Draw inner circle (lighter)
        inner_color = tuple(min(255, c + 50) for c in color)
        inner_padding = size // 4
        draw.ellipse(
            [inner_padding, inner_padding, size - inner_padding, size - inner_padding],
            fill=inner_color
        )
        
        # Draw microphone shape
        mic_color = (255, 255, 255)
        center_x = size // 2
        
        # Mic body
        mic_width = size // 6
        mic_height = size // 3
        mic_top = size // 3
        draw.rectangle(
            [
                center_x - mic_width // 2,
                mic_top,
                center_x + mic_width // 2,
                mic_top + mic_height
            ],
            fill=mic_color
        )
        
        # Mic base
        base_y = mic_top + mic_height + 2
        draw.line(
            [center_x, base_y, center_x, base_y + size // 8],
            fill=mic_color,
            width=2
        )
        
        return img
    
    def _get_status_color(self) -> tuple:
        """Get color for current status"""
        status_colors = {
            "idle": self.STATUS_IDLE,
            "listening": self.STATUS_LISTENING,
            "processing": self.STATUS_PROCESSING,
            "speaking": self.STATUS_SPEAKING,
            "error": self.STATUS_ERROR
        }
        return status_colors.get(self._status, self.STATUS_IDLE)
    
    def _create_menu(self):
        """Create tray context menu"""
        import pystray
        
        def show_action(icon, item):
            if self._on_show:
                self._on_show()
        
        def toggle_listening(icon, item):
            self._is_listening = not self._is_listening
            if self._on_toggle_listening:
                self._on_toggle_listening(self._is_listening)
            self._update_icon()
        
        def quit_action(icon, item):
            if self._on_quit:
                self._on_quit()
            icon.stop()
        
        menu = pystray.Menu(
            pystray.MenuItem(
                lambda text: "🎤 Listening" if self._is_listening else "🔇 Paused",
                toggle_listening
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Show Window", show_action, default=True),
            pystray.MenuItem("Quit", quit_action)
        )
        
        return menu
    
    def _update_icon(self):
        """Update icon image based on current status"""
        if self._icon:
            color = self._get_status_color()
            self._icon.icon = self._create_icon_image(color)
            
            status_text = self._status.capitalize()
            if not self._is_listening:
                status_text = "Paused"
            self._icon.title = f"{self.app_name} - {status_text}"
    
    def start(self):
        """Start the tray application"""
        if not self._pystray_available:
            print("[Tray] Running without system tray (pystray not available)")
            return
        
        import pystray
        
        # Create icon
        icon_image = self._create_icon_image(self._get_status_color())
        
        self._icon = pystray.Icon(
            self.app_name,
            icon_image,
            f"{self.app_name} - Ready",
            self._create_menu()
        )
        
        # Run in separate thread
        self._thread = threading.Thread(target=self._icon.run, daemon=True)
        self._thread.start()
        
        print(f"[Tray] Started - {self.app_name}")
    
    def stop(self):
        """Stop the tray application"""
        if self._icon:
            self._icon.stop()
            self._icon = None
        print("[Tray] Stopped")
    
    def set_status(self, status: str):
        """
        Set current status (updates icon color)
        
        Args:
            status: One of "idle", "listening", "processing", "speaking", "error"
        """
        self._status = status
        self._update_icon()
    
    def show_notification(self, title: str, message: str):
        """Show a notification from the tray icon"""
        if self._icon and hasattr(self._icon, 'notify'):
            self._icon.notify(message, title)
    
    def is_running(self) -> bool:
        """Check if tray is running"""
        return self._icon is not None


# Test
if __name__ == "__main__":
    import time
    
    print("Testing System Tray...")
    
    def on_show():
        print("Show window clicked!")
    
    def on_quit():
        print("Quitting...")
    
    def on_toggle(is_listening):
        print(f"Listening: {is_listening}")
    
    tray = TrayApp(
        app_name="Test Assistant",
        on_show=on_show,
        on_quit=on_quit,
        on_toggle_listening=on_toggle
    )
    
    tray.start()
    
    # Test status changes
    print("Look for the tray icon!")
    print("Testing status changes...")
    
    try:
        for status in ["idle", "listening", "processing", "speaking", "error", "idle"]:
            print(f"  Status: {status}")
            tray.set_status(status)
            time.sleep(2)
        
        print("Tray test complete. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nExiting...")
        tray.stop()
