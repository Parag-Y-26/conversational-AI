"""
Configuration for Windows Voice-Controlled Desktop Assistant
"""
import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class APIConfig:
    """API configuration for AI models"""
    # Kimi K2.5 (Moonshot AI) - Primary
    kimi_api_key: str = "sk-tTz2G35OPLdIqYyhVazxxz3g3KLnuU8CM1doK3lyK792M3Kq"
    kimi_base_url: str = "https://api.moonshot.ai/v1"
    kimi_model: str = "moonshot-v1-8k"
    
    # Ollama Cloud - Fallback
    ollama_api_key: str = "cd826e7a76244edebdf1ba1802410746.8hLndyNjWNmOKkpRBkJ1Vqpl"
    ollama_base_url: str = "https://ollama.com/api"
    ollama_model: str = "llama3"
    
    # OpenRouter API - For Whisper STT
    openrouter_api_key: str = "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"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

@dataclass
class WakeWordConfig:
    """Wake word detection settings"""
    enabled: bool = True
    model_name: str = "hey_nebula"  # Custom wake word
    threshold: float = 0.5  # Detection confidence threshold
    sample_rate: int = 16000
    chunk_size: int = 1280  # ~80ms at 16kHz

@dataclass
class AudioConfig:
    """Audio settings"""
    sample_rate: int = 16000
    channels: int = 1
    chunk_size: int = 1024
    format: str = "int16"
    
    # TTS settings
    tts_rate: int = 175  # Words per minute
    tts_volume: float = 1.0  # 0.0 to 1.0
    tts_voice_index: int = 0  # 0=Male, 1=Female (SAPI5)

@dataclass
class ScreenConfig:
    """Screen capture settings"""
    monitor_index: int = 1  # Primary monitor
    max_width: int = 1920
    max_height: int = 1080
    jpeg_quality: int = 85
    ocr_languages: list = field(default_factory=lambda: ["en"])

@dataclass
class AssistantConfig:
    """Main assistant configuration"""
    name: str = "Nebula"
    wake_phrase: str = "Hey Nebula"
    
    # Behavior
    listen_timeout: float = 5.0  # Seconds to wait for speech
    phrase_timeout: float = 3.0  # Max seconds for a phrase
    silence_threshold: int = 300  # Energy threshold for silence
    
    # Responses
    greeting: str = "Hello! How can I help you?"
    processing_message: str = "Let me think about that..."
    error_message: str = "I'm sorry, I didn't catch that. Could you repeat?"
    goodbye_message: str = "Goodbye!"
    
    # Sub-configs
    api: APIConfig = field(default_factory=APIConfig)
    wake_word: WakeWordConfig = field(default_factory=WakeWordConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    screen: ScreenConfig = field(default_factory=ScreenConfig)

# Global config instance
config = AssistantConfig()

def load_config_from_env():
    """Load configuration from environment variables if available"""
    global config
    
    # Override API keys from environment if set
    if os.getenv("KIMI_API_KEY"):
        config.api.kimi_api_key = os.getenv("KIMI_API_KEY")
    if os.getenv("OLLAMA_API_KEY"):
        config.api.ollama_api_key = os.getenv("OLLAMA_API_KEY")
    
    # Override wake word settings
    if os.getenv("WAKE_WORD_MODEL"):
        config.wake_word.model_name = os.getenv("WAKE_WORD_MODEL")
    if os.getenv("WAKE_WORD_THRESHOLD"):
        config.wake_word.threshold = float(os.getenv("WAKE_WORD_THRESHOLD"))
    
    return config
