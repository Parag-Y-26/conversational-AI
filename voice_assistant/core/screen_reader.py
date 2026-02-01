"""
Screen Reader - Captures screen content and extracts text using OCR
"""
import mss
import base64
from io import BytesIO
from PIL import Image
from typing import Optional, Dict, Tuple
import numpy as np

class ScreenReader:
    """
    Screen capture and OCR for reading screen content
    Uses mss for fast capture and EasyOCR for text extraction
    """
    
    def __init__(
        self,
        monitor_index: int = 1,
        max_width: int = 1920,
        max_height: int = 1080,
        jpeg_quality: int = 85,
        ocr_languages: list = None
    ):
        """
        Initialize screen reader
        
        Args:
            monitor_index: Monitor to capture (1 = primary)
            max_width: Max width for resizing
            max_height: Max height for resizing
            jpeg_quality: JPEG quality for encoding
            ocr_languages: List of language codes for OCR
        """
        self.monitor_index = monitor_index
        self.max_width = max_width
        self.max_height = max_height
        self.jpeg_quality = jpeg_quality
        self.ocr_languages = ocr_languages or ["en"]
        
        self._sct = mss.mss()
        self._ocr_reader = None
        
        # Lazy load EasyOCR (it's heavy)
        self._ocr_initialized = False
    
    def _init_ocr(self):
        """Initialize OCR reader (lazy loading)"""
        if not self._ocr_initialized:
            try:
                import easyocr
                print("[Screen] Initializing EasyOCR (this may take a moment)...")
                self._ocr_reader = easyocr.Reader(self.ocr_languages, gpu=False)
                self._ocr_initialized = True
                print("[Screen] EasyOCR initialized")
            except ImportError:
                print("[Screen] EasyOCR not installed, falling back to pytesseract")
                try:
                    import pytesseract
                    self._ocr_reader = "pytesseract"
                    self._ocr_initialized = True
                except ImportError:
                    print("[Screen] No OCR library available")
    
    def capture_screen(self, region: Optional[Dict] = None) -> Image.Image:
        """
        Capture screenshot
        
        Args:
            region: Optional {top, left, width, height} dict
        
        Returns:
            PIL Image of the screenshot
        """
        if region:
            monitor = region
        else:
            monitor = self._sct.monitors[self.monitor_index]
        
        screenshot = self._sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        
        # Resize if necessary
        if img.width > self.max_width or img.height > self.max_height:
            img.thumbnail((self.max_width, self.max_height), Image.Resampling.LANCZOS)
        
        return img
    
    def capture_to_base64(self, region: Optional[Dict] = None) -> str:
        """
        Capture screenshot and return as base64 string
        
        Returns:
            Base64 encoded JPEG image
        """
        img = self.capture_screen(region)
        
        buffered = BytesIO()
        img.save(buffered, format="JPEG", quality=self.jpeg_quality)
        return base64.b64encode(buffered.getvalue()).decode()
    
    def read_screen_text(self, region: Optional[Dict] = None) -> str:
        """
        Capture screen and extract text using OCR
        
        Args:
            region: Optional region to capture
        
        Returns:
            Extracted text from screen
        """
        self._init_ocr()
        
        if not self._ocr_initialized:
            return "OCR not available"
        
        img = self.capture_screen(region)
        img_array = np.array(img)
        
        try:
            if self._ocr_reader == "pytesseract":
                import pytesseract
                text = pytesseract.image_to_string(img)
            else:
                # EasyOCR
                results = self._ocr_reader.readtext(img_array)
                # Extract just the text from results
                text = " ".join([item[1] for item in results])
            
            return text.strip() if text else "No text found on screen"
            
        except Exception as e:
            print(f"[Screen] OCR error: {e}")
            return f"Error reading screen: {e}"
    
    def get_screen_summary(self, region: Optional[Dict] = None) -> str:
        """
        Get a brief summary of screen content
        
        Returns:
            Summary string suitable for AI context
        """
        text = self.read_screen_text(region)
        
        # Truncate if too long
        if len(text) > 1000:
            text = text[:1000] + "..."
        
        return text
    
    def capture_active_window(self) -> Tuple[Optional[Image.Image], str]:
        """
        Capture the active/foreground window
        
        Returns:
            Tuple of (image, window_title)
        """
        try:
            import pygetwindow as gw
            
            active = gw.getActiveWindow()
            if active:
                region = {
                    "left": active.left,
                    "top": active.top,
                    "width": active.width,
                    "height": active.height
                }
                img = self.capture_screen(region)
                return img, active.title
            else:
                return self.capture_screen(), "Unknown"
                
        except ImportError:
            # pygetwindow not available, capture full screen
            return self.capture_screen(), "Full Screen"
        except Exception as e:
            print(f"[Screen] Error getting active window: {e}")
            return self.capture_screen(), "Full Screen"
    
    def get_monitors(self) -> list:
        """Get list of available monitors"""
        return [
            {
                "index": i,
                "left": m["left"],
                "top": m["top"],
                "width": m["width"],
                "height": m["height"]
            }
            for i, m in enumerate(self._sct.monitors)
        ]
    
    def save_screenshot(self, path: str, region: Optional[Dict] = None):
        """Save screenshot to file"""
        img = self.capture_screen(region)
        img.save(path)
        print(f"[Screen] Screenshot saved to {path}")


# Test
if __name__ == "__main__":
    print("Testing Screen Reader...")
    
    reader = ScreenReader()
    
    print("\nAvailable monitors:")
    for mon in reader.get_monitors():
        print(f"  Monitor {mon['index']}: {mon['width']}x{mon['height']}")
    
    print("\nCapturing screen...")
    img = reader.capture_screen()
    print(f"Captured: {img.size}")
    
    print("\nReading text from screen...")
    text = reader.read_screen_text()
    print(f"Found text: {text[:200]}..." if len(text) > 200 else f"Found text: {text}")
