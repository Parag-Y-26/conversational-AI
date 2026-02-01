"""
Windows Voice-Controlled Desktop Assistant
Main entry point - integrates all components

Features:
- Wake word activation ("Hey Jarvis")
- Speech-to-speech communication
- Screen reading capability
- AI-powered responses (Kimi K2.5 + Ollama)
"""
import sys
import time
import threading
import asyncio
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(__file__).replace("\\main.py", ""))

from config import config, load_config_from_env
from core.text_to_speech import TextToSpeech
from core.speech_to_text import SpeechToText
from core.ai_engine import AIEngine
from core.screen_reader import ScreenReader
from core.wake_word import WakeWordDetector, SimpleWakeWordDetector
from ui.tray_app import TrayApp

class VoiceAssistant:
    """
    Main Voice Assistant class
    Orchestrates all components for a complete voice assistant experience
    """
    
    def __init__(self):
        """Initialize the voice assistant"""
        print("=" * 50)
        print("  Windows Voice-Controlled Desktop Assistant")
        print("=" * 50)
        print()
        
        # Load configuration
        load_config_from_env()
        
        # Initialize components
        print("[Init] Initializing components...")
        
        # Text-to-Speech (using edge-tts)
        self.tts = TextToSpeech()
        
        # Speech-to-Text
        self.stt = SpeechToText(
            timeout=config.listen_timeout,
            phrase_time_limit=config.phrase_timeout
        )
        
        # AI Engine (Kimi K2.5 via Ollama Cloud)
        self.ai = AIEngine()
        
        # Screen Reader
        self.screen_reader = ScreenReader(
            monitor_index=config.screen.monitor_index,
            ocr_languages=config.screen.ocr_languages
        )
        
        # Wake Word Detector
        self.wake_detector: Optional[WakeWordDetector] = None
        self.simple_wake_detector = SimpleWakeWordDetector(config.wake_phrase)
        
        # System Tray
        self.tray = TrayApp(
            app_name=f"{config.name} Assistant",
            on_show=self._on_show,
            on_quit=self._on_quit,
            on_toggle_listening=self._on_toggle_listening
        )
        
        # State
        self._running = False
        self._listening_enabled = True
        self._processing = False
        self._event_loop: Optional[asyncio.AbstractEventLoop] = None
        
        print("[Init] All components initialized!")
        print()
    
    def _on_show(self):
        """Callback when tray 'Show' is clicked"""
        print("[Tray] Show window requested")
        # Could show a GUI window here if implemented
    
    def _on_quit(self):
        """Callback when tray 'Quit' is clicked"""
        print("[Tray] Quit requested")
        self.stop()
    
    def _on_toggle_listening(self, is_listening: bool):
        """Callback when listening is toggled from tray"""
        self._listening_enabled = is_listening
        status = "enabled" if is_listening else "disabled"
        print(f"[Tray] Listening {status}")
        
        if is_listening:
            self.tts.speak("Listening enabled")
        else:
            self.tts.speak("Listening paused")
    
    def _on_wake_word_detected(self):
        """Callback when wake word is detected"""
        if not self._listening_enabled or self._processing:
            return
        
        print("\n*** Wake word detected! ***")
        self.tray.set_status("listening")
        
        # Play acknowledgment sound/speech
        self.tts.speak("Yes?", block=True)
        
        # Start listening for command
        self._process_voice_command()
    
    def _process_voice_command(self):
        """Process a voice command after wake word"""
        if self._processing:
            return
        
        self._processing = True
        
        try:
            # Listen for user input
            print("[Assistant] Listening for command...")
            self.tray.set_status("listening")
            
            success, text = self.stt.listen()
            
            if not success:
                print(f"[Assistant] Could not understand: {text}")
                self.tts.speak(config.error_message)
                self.tray.set_status("idle")
                return
            
            print(f"[Assistant] User said: {text}")
            
            # Check for screen-related commands
            screen_context = None
            if any(kw in text.lower() for kw in ["screen", "see", "show", "read", "what's on", "look at"]):
                print("[Assistant] Screen-related command detected, capturing screen...")
                self.tray.set_status("processing")
                screen_context = self.screen_reader.get_screen_summary()
                print(f"[Assistant] Screen context: {screen_context[:100]}...")
            
            # Get AI response
            print("[Assistant] Getting AI response...")
            self.tray.set_status("processing")
            self.tts.speak(config.processing_message, block=False)
            
            response = self._event_loop.run_until_complete(
                self.ai.get_response(text, screen_context)
            )
            
            if response.success:
                print(f"[Assistant] Response ({response.provider.value}): {response.content[:100]}...")
                
                # Speak the response
                self.tray.set_status("speaking")
                self.tts.speak(response.content)
            else:
                print(f"[Assistant] AI error: {response.error}")
                self.tts.speak("I'm sorry, I couldn't get a response. Please try again.")
            
        except Exception as e:
            print(f"[Assistant] Error processing command: {e}")
            self.tts.speak("Sorry, something went wrong.")
        
        finally:
            self._processing = False
            self.tray.set_status("idle")
    
    def _run_wake_word_loop(self):
        """Direct conversation mode - responds to all speech (Blue Machine AI style)
        
        Features:
        - No wake word required - responds to everything
        - Interruption handling - stops when you speak
        - Contextual continuity - remembers conversation
        """
        print("[Assistant] Direct mode - just speak, Nebula will respond!")
        print("[Assistant] Speak naturally - 3s pause submits your message\n")
        
        while self._running and self._listening_enabled:
            try:
                # Listen for speech
                success, text = self.stt.listen()
                
                if success and text and len(text.strip()) > 2:
                    # Skip noise/very short utterances
                    if len(text.strip()) < 3:
                        continue
                    
                    print(f"\n[You] {text}")
                    
                    # Process the speech as a command
                    self._process_command_text(text)
                
            except Exception as e:
                print(f"[Error] {e}")
                time.sleep(0.5)
    
    def _listen_for_command(self, silence_timeout: float = 5.0) -> Optional[str]:
        """Listen for a command until silence_timeout seconds of silence"""
        import time
        
        command_parts = []
        last_speech_time = time.time()
        
        print("[Listening]", end=" ", flush=True)
        
        while time.time() - last_speech_time < silence_timeout:
            try:
                success, text = self.stt.listen(timeout=2)
                
                if success and text and len(text.strip()) > 1:
                    command_parts.append(text)
                    last_speech_time = time.time()
                    print(".", end="", flush=True)
                    
            except Exception:
                pass
        
        print()  # Newline after dots
        
        if command_parts:
            return " ".join(command_parts)
        return None
    
    def _process_command_text(self, text: str):
        """Process a command given as text"""
        if self._processing:
            return
        
        self._processing = True
        
        try:
            # Check for screen-related commands
            screen_context = None
            if any(kw in text.lower() for kw in ["screen", "see", "show", "read", "what's on"]):
                screen_context = self.screen_reader.get_screen_summary()
            
            # Get AI response
            self.tray.set_status("processing")
            
            response = self._event_loop.run_until_complete(
                self.ai.get_response(text, screen_context)
            )
            
            if response.success:
                print(f"[Nebula] {response.content}")
                self.tray.set_status("speaking")
                self.tts.speak(response.content)
            else:
                print(f"[Error] AI failed: {response.error}")
                self.tts.speak("I couldn't get a response.")
            
        finally:
            self._processing = False
            self.tray.set_status("idle")
    
    def start(self):
        """Start the voice assistant"""
        print("[Assistant] Starting...")
        
        # Create event loop for async operations
        self._event_loop = asyncio.new_event_loop()
        
        # Start system tray
        self.tray.start()
        
        # Try to start OpenWakeWord detector
        use_advanced_wake = False
        try:
            # Check if openwakeword is installed
            import openwakeword
            self.wake_detector = WakeWordDetector(
                model_name=config.wake_word.model_name,
                threshold=config.wake_word.threshold
            )
            self.wake_detector.on_wake_word(self._on_wake_word_detected)
            self.wake_detector.start()
            use_advanced_wake = self.wake_detector._use_openwakeword
            if not use_advanced_wake:
                print("[Assistant] OpenWakeWord model not found, using speech fallback")
        except ImportError:
            print("[Assistant] OpenWakeWord not installed, using speech recognition fallback")
        except Exception as e:
            print(f"[Assistant] Wake word error: {e}")
            print("[Assistant] Using fallback speech recognition mode")
        
        # Greeting
        self.tts.speak(config.greeting)
        
        print()
        print("=" * 50)
        print(f"  {config.name} is ready!")
        print(f"  Say '{config.wake_phrase}' to activate")
        print("  Press Ctrl+C to quit")
        print("=" * 50)
        print()
        
        self._running = True
        self.tray.set_status("idle")
        
        try:
            if use_advanced_wake:
                # OpenWakeWord handles listening in background
                print("[Assistant] Listening with OpenWakeWord...")
                while self._running:
                    time.sleep(0.1)
            else:
                # Fallback: use speech recognition for wake word
                print("[Assistant] Starting speech recognition loop...")
                self._run_wake_word_loop()
                
        except KeyboardInterrupt:
            print("\n[Assistant] Interrupted by user")
        
        self.stop()
    
    def stop(self):
        """Stop the voice assistant"""
        print("[Assistant] Stopping...")
        
        self._running = False
        
        # Goodbye
        self.tts.speak(config.goodbye_message)
        
        # Cleanup components
        if self.wake_detector:
            self.wake_detector.cleanup()
        
        self.tray.stop()
        self.tts.cleanup()
        
        if self._event_loop:
            self._event_loop.run_until_complete(self.ai.cleanup())
            self._event_loop.close()
        
        print("[Assistant] Goodbye!")


def main():
    """Main entry point"""
    assistant = VoiceAssistant()
    assistant.start()


if __name__ == "__main__":
    main()
