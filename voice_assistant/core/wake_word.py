"""
Wake Word Detection using sounddevice and OpenWakeWord
Provides always-on listening for trigger phrases like "Hey Nebula"
"""
import threading
import time
from typing import Optional, Callable
import numpy as np

class WakeWordDetector:
    """
    Wake word detection using OpenWakeWord with sounddevice backend
    Listens continuously in background for activation phrase
    """
    
    def __init__(
        self,
        model_name: str = "hey_nebula",
        threshold: float = 0.5,
        sample_rate: int = 16000,
        chunk_size: int = 1280
    ):
        """
        Initialize wake word detector
        
        Args:
            model_name: Pre-trained model name
            threshold: Detection confidence threshold (0.0 to 1.0)
            sample_rate: Audio sample rate (16000 for OpenWakeWord)
            chunk_size: Audio chunk size (1280 = 80ms at 16kHz)
        """
        self.model_name = model_name
        self.threshold = threshold
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        
        self._model = None
        self._is_listening = False
        self._stop_flag = threading.Event()
        self._listen_thread: Optional[threading.Thread] = None
        
        # Callbacks
        self._on_wake_word: Optional[Callable] = None
        self._on_error: Optional[Callable[[str], None]] = None
        
        self._initialized = False
        self._use_openwakeword = False
    
    def _initialize(self) -> bool:
        """Initialize the wake word model"""
        if self._initialized:
            return True
        
        # Try OpenWakeWord first
        try:
            from openwakeword.model import Model
            print(f"[WakeWord] Loading OpenWakeWord model: {self.model_name}")
            self._model = Model(
                wakeword_models=[self.model_name],
                inference_framework="onnx"
            )
            self._use_openwakeword = True
            self._initialized = True
            print("[WakeWord] OpenWakeWord initialized")
            return True
        except Exception as e:
            print(f"[WakeWord] OpenWakeWord not available: {e}")
            print("[WakeWord] Using simple keyword detection fallback")
            self._use_openwakeword = False
            self._initialized = True
            return True
    
    def _listen_loop_openwakeword(self):
        """Listen loop using OpenWakeWord"""
        import sounddevice as sd
        
        try:
            print("[WakeWord] Listening for wake word...")
            
            def audio_callback(indata, frames, time_info, status):
                if status:
                    print(f"[WakeWord] Audio status: {status}")
                
                audio_array = indata[:, 0].astype(np.int16)
                prediction = self._model.predict(audio_array)
                
                for wakeword, score in prediction.items():
                    if score > self.threshold:
                        print(f"[WakeWord] Detected '{wakeword}' ({score:.2f})")
                        if self._on_wake_word:
                            self._on_wake_word()
                        self._model.reset()
                        time.sleep(1.0)  # Debounce
                        break
            
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.int16,
                blocksize=self.chunk_size,
                callback=audio_callback
            ):
                while not self._stop_flag.is_set():
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"[WakeWord] Error: {e}")
            if self._on_error:
                self._on_error(str(e))
    
    def _listen_loop_simple(self):
        """Simple fallback listening (uses STT for wake word)"""
        # This will be handled by main.py using the SimpleWakeWordDetector
        while not self._stop_flag.is_set():
            time.sleep(0.5)
    
    def start(self):
        """Start wake word detection in background"""
        if self._is_listening:
            print("[WakeWord] Already listening")
            return
        
        if not self._initialize():
            return
        
        self._stop_flag.clear()
        self._is_listening = True
        
        if self._use_openwakeword:
            self._listen_thread = threading.Thread(
                target=self._listen_loop_openwakeword,
                daemon=True
            )
        else:
            self._listen_thread = threading.Thread(
                target=self._listen_loop_simple,
                daemon=True
            )
        
        self._listen_thread.start()
        print("[WakeWord] Started listening")
    
    def stop(self):
        """Stop wake word detection"""
        if not self._is_listening:
            return
        
        print("[WakeWord] Stopping...")
        self._stop_flag.set()
        self._is_listening = False
        
        if self._listen_thread:
            self._listen_thread.join(timeout=2.0)
            self._listen_thread = None
        
        print("[WakeWord] Stopped")
    
    def is_listening(self) -> bool:
        return self._is_listening
    
    def set_threshold(self, threshold: float):
        self.threshold = max(0.0, min(1.0, threshold))
    
    def on_wake_word(self, callback: Callable):
        self._on_wake_word = callback
    
    def on_error(self, callback: Callable[[str], None]):
        self._on_error = callback
    
    def cleanup(self):
        self.stop()
        self._initialized = False


class SimpleWakeWordDetector:
    """
    Simple wake word detector using keyword matching in transcribed speech
    Works without OpenWakeWord
    """
    
    def __init__(self, wake_phrase: str = "hey nebula"):
        self.wake_phrase = wake_phrase.lower()
        self._on_wake_word: Optional[Callable] = None
    
    def check_for_wake_word(self, text: str) -> bool:
        """Check if text contains wake word"""
        return self.wake_phrase in text.lower()
    
    def on_wake_word(self, callback: Callable):
        self._on_wake_word = callback
    
    def trigger_if_detected(self, text: str) -> bool:
        if self.check_for_wake_word(text):
            if self._on_wake_word:
                self._on_wake_word()
            return True
        return False


# Test
if __name__ == "__main__":
    print("Testing Wake Word Detector with sounddevice...")
    print("Say 'Hey Nebula' to test detection")
    print("Press Ctrl+C to stop\n")
    
    detector = WakeWordDetector()
    
    def on_wake():
        print("\n*** WAKE WORD DETECTED! ***\n")
    
    detector.on_wake_word(on_wake)
    detector.start()
    
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping...")
        detector.cleanup()
        print("Done!")
