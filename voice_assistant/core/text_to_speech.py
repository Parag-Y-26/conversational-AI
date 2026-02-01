"""
Text-to-Speech Engine using edge-tts with Windows native audio playback
"""
import asyncio
import subprocess
import tempfile
import os
from typing import Optional

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# Fallback to pyttsx3
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except:
    PYTTSX3_AVAILABLE = False


class TextToSpeech:
    """
    Text-to-Speech engine using edge-tts with Windows native playback
    """
    
    def __init__(self, voice: str = "en-US-GuyNeural", rate: str = "+0%"):
        """
        Initialize TTS
        
        Args:
            voice: Edge TTS voice (e.g., en-US-GuyNeural, en-US-JennyNeural)
            rate: Speech rate adjustment (e.g., +10%, -10%)
        """
        self.voice = voice
        self.rate = rate
        self.temp_dir = tempfile.gettempdir()
        self._pyttsx_engine = None
        
        if EDGE_TTS_AVAILABLE:
            print(f"[TTS] Using Edge TTS ({voice})")
            self.use_edge = True
        elif PYTTSX3_AVAILABLE:
            print("[TTS] Edge TTS unavailable, using pyttsx3")
            self.use_edge = False
            self._pyttsx_engine = pyttsx3.init()
            self._pyttsx_engine.setProperty('rate', 175)
            voices = self._pyttsx_engine.getProperty('voices')
            print(f"[TTS] Initialized with {len(voices)} voices")
        else:
            print("[TTS] No TTS engine available!")
            self.use_edge = False
    
    def speak(self, text: str, block: bool = True):
        """
        Speak the given text
        
        Args:
            text: Text to speak
            block: If True, wait until speech completes
        """
        if not text or not text.strip():
            return
        
        # Clean text for speech
        text = self._clean_text(text)
        
        if self.use_edge:
            self._speak_edge(text)
        elif self._pyttsx_engine:
            self._speak_pyttsx(text, block)
        else:
            print(f"[TTS] Would say: {text}")
    
    def _clean_text(self, text: str) -> str:
        """Clean text for speech output"""
        import re
        text = re.sub(r'\*+', '', text)
        text = re.sub(r'#+', '', text)
        text = re.sub(r'`+', '', text)
        text = re.sub(r'\[|\]|\(|\)', '', text)
        text = text.replace('\n', ' ').strip()
        return text[:500]
    
    def _speak_edge(self, text: str):
        """Speak using edge-tts with Windows native playback"""
        try:
            audio_file = os.path.join(self.temp_dir, "nebula_speech.mp3")
            
            print(f"[TTS] Speaking: {text[:40]}...")
            
            # Generate speech
            async def generate():
                communicate = edge_tts.Communicate(text, self.voice, rate=self.rate)
                await communicate.save(audio_file)
            
            asyncio.run(generate())
            
            # Play audio using Windows native player (wmplayer or PowerShell)
            try:
                # Use PowerShell to play audio (most reliable on Windows)
                cmd = f'''powershell -c "(New-Object Media.SoundPlayer '{audio_file}').PlaySync()"'''
                
                # For MP3 files, use Windows Media Player
                if audio_file.endswith('.mp3'):
                    # Use ffplay if available, else PowerShell with MediaPlayer
                    import shutil
                    if shutil.which('ffplay'):
                        subprocess.run(['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', audio_file], 
                                      check=True, capture_output=True)
                    else:
                        # Use PowerShell MediaPlayer for MP3
                        ps_script = f'''
Add-Type -AssemblyName presentationCore
$player = New-Object System.Windows.Media.MediaPlayer
$player.Open('{audio_file}')
Start-Sleep -Milliseconds 500
$player.Play()
while ($player.NaturalDuration.HasTimeSpan -eq $false) {{ Start-Sleep -Milliseconds 100 }}
$duration = $player.NaturalDuration.TimeSpan.TotalSeconds
Start-Sleep -Seconds ($duration + 0.5)
$player.Close()
'''
                        subprocess.run(['powershell', '-Command', ps_script], 
                                      capture_output=True, timeout=30)
                
                print("[TTS] Done speaking")
                
            except Exception as e:
                print(f"[TTS] Playback error: {e}")
                # Fallback to pyttsx3
                if PYTTSX3_AVAILABLE:
                    if not self._pyttsx_engine:
                        self._pyttsx_engine = pyttsx3.init()
                    self._speak_pyttsx(text, True)
            
            # Cleanup
            try:
                os.remove(audio_file)
            except:
                pass
                
        except Exception as e:
            print(f"[TTS] Error: {e}")
            if PYTTSX3_AVAILABLE:
                if not self._pyttsx_engine:
                    self._pyttsx_engine = pyttsx3.init()
                self._speak_pyttsx(text, True)
    
    def _speak_pyttsx(self, text: str, block: bool):
        """Speak using pyttsx3"""
        try:
            print(f"[TTS] Speaking: {text[:40]}...")
            self._pyttsx_engine.say(text)
            if block:
                self._pyttsx_engine.runAndWait()
            print("[TTS] Done speaking")
        except Exception as e:
            print(f"[TTS] Error: {e}")
    
    def stop(self):
        """Stop current speech"""
        if self._pyttsx_engine:
            try:
                self._pyttsx_engine.stop()
            except:
                pass
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop()


# Test
if __name__ == "__main__":
    print("Testing Text-to-Speech...")
    tts = TextToSpeech()
    tts.speak("Hello! I am Nebula, your voice assistant. Can you hear me now?")
    print("Test completed!")
