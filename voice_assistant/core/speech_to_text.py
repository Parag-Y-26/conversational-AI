"""
Speech-to-Text Engine using Google Speech Recognition
Uses sounddevice for audio capture (no PyAudio required)
"""
import io
import wave
import threading
from typing import Optional, Callable, Tuple
import numpy as np
import speech_recognition as sr

class SpeechToText:
    """
    Speech-to-Text engine using Google Speech Recognition
    Uses sounddevice for audio capture
    """
    
    def __init__(
        self,
        timeout: float = 5.0,
        phrase_time_limit: float = 5.0,
        sample_rate: int = 16000
    ):
        """
        Initialize STT engine
        
        Args:
            timeout: Seconds to wait for phrase to start
            phrase_time_limit: Max seconds for a phrase
            sample_rate: Audio sample rate
        """
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit
        self.sample_rate = sample_rate
        
        self._is_listening = False
        self.recognizer = sr.Recognizer()
        
        # Callbacks
        self._on_listening: Optional[Callable] = None
        self._on_result: Optional[Callable[[str], None]] = None
        self._on_error: Optional[Callable[[str], None]] = None
        
        # Check sounddevice
        try:
            import sounddevice as sd
            input_device = sd.query_devices(kind='input')
            print(f"[STT] Ready (sounddevice + Google)")
            print(f"[STT] Mic: {input_device['name'][:35]}...")
        except Exception as e:
            print(f"[STT] Error: {e}")
    
    def _record_audio(self, duration: float) -> Optional[np.ndarray]:
        """Record audio using sounddevice"""
        import sounddevice as sd
        
        try:
            recording = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype=np.int16
            )
            sd.wait()
            return recording.flatten()
        except Exception as e:
            print(f"[STT] Recording error: {e}")
            return None
    
    def listen(self, timeout: Optional[float] = None) -> Tuple[bool, str]:
        """
        Listen for speech and return transcription
        
        Args:
            timeout: Optional override for phrase time limit
        
        Returns:
            Tuple of (success: bool, text: str or error message)
        """
        self._is_listening = True
        phrase_limit = timeout if timeout else self.phrase_time_limit
        
        if self._on_listening:
            self._on_listening()
        
        try:
            # Record audio
            audio_data = self._record_audio(phrase_limit)
            
            if audio_data is None:
                return False, "Failed to record audio"
            
            # Check if audio has content (not just silence)
            if np.abs(audio_data).mean() < 100:
                return False, "Silence"
            
            # Convert to AudioData for speech_recognition
            audio_bytes = audio_data.tobytes()
            audio = sr.AudioData(audio_bytes, self.sample_rate, 2)
            
            # Transcribe with Google
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"[STT] You said: {text}")
                
                if self._on_result:
                    self._on_result(text)
                
                return True, text
                
            except sr.UnknownValueError:
                return False, "Could not understand"
            except sr.RequestError as e:
                return False, f"API error: {e}"
                
        except Exception as e:
            error = f"Error: {e}"
            if self._on_error:
                self._on_error(error)
            return False, error
            
        finally:
            self._is_listening = False
    
    def listen_async(self, callback: Callable[[bool, str], None]):
        """Listen for speech asynchronously"""
        def _listen_thread():
            result = self.listen()
            callback(*result)
        
        thread = threading.Thread(target=_listen_thread, daemon=True)
        thread.start()
        return thread
    
    def is_listening(self) -> bool:
        return self._is_listening
    
    def on_listening(self, callback: Callable):
        self._on_listening = callback
    
    def on_result(self, callback: Callable[[str], None]):
        self._on_result = callback
    
    def on_error(self, callback: Callable[[str], None]):
        self._on_error = callback
    
    def cleanup(self):
        pass
    
    @staticmethod
    def list_devices() -> list:
        try:
            import sounddevice as sd
            devices = sd.query_devices()
            return [
                {"index": i, "name": d["name"], "inputs": d["max_input_channels"]}
                for i, d in enumerate(devices) if d["max_input_channels"] > 0
            ]
        except:
            return []


if __name__ == "__main__":
    print("Testing Speech-to-Text...")
    stt = SpeechToText()
    print("\nSay something...")
    success, result = stt.listen()
    print(f"\nResult: {result}" if success else f"\nError: {result}")
