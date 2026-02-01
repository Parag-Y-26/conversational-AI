# Windows Voice-Controlled Desktop Assistant

A voice-controlled AI desktop assistant for Windows with screen reading, wake word activation, and speech-to-speech communication.

## Features

- 🎤 **Wake Word Activation** - Say "Hey Nebula" to activate
- 🗣️ **Speech-to-Speech** - Natural voice conversation
- 🖥️ **Screen Reading** - Read and analyze screen content
- 🤖 **Dual AI Backend** - Kimi K2.5 (primary) + Ollama (fallback)
- 📌 **System Tray** - Runs silently in background

## Quick Start

### 1. Install Dependencies

```powershell
cd voice_assistant
pip install -r requirements.txt
```

> ⚠️ **Note**: PyAudio may require manual installation on Windows:
>
> ```powershell
> pip install pipwin
> pipwin install pyaudio
> ```

### 2. Run the Assistant

```powershell
python main.py
```

### 3. Usage

1. Wait for "Hello! How can I help you?"
2. Say **"Hey Nebula"** to activate
3. Ask your question or give a command
4. The assistant will respond via voice

## Commands Examples

- "Hey Nebula, what time is it?"
- "Hey Nebula, what's on my screen?"
- "Hey Nebula, explain quantum computing"
- "Hey Nebula, read the text on screen"

## Configuration

Edit `config.py` to customize:

- API keys
- Wake word threshold
- Voice settings (rate, volume)
- TTS voice selection

## Project Structure

```
voice_assistant/
├── main.py              # Entry point
├── config.py            # Configuration
├── requirements.txt     # Dependencies
├── core/
│   ├── wake_word.py     # Wake word detection
│   ├── speech_to_text.py # Voice input
│   ├── text_to_speech.py # Voice output
│   ├── screen_reader.py  # Screen capture & OCR
│   └── ai_engine.py      # Kimi K2.5 & Ollama APIs
└── ui/
    └── tray_app.py       # System tray
```

## API Keys

Built-in API keys for:

- **Kimi K2.5** (Moonshot AI)
- **Ollama** (Cloud)

## Requirements

- Windows 10/11
- Python 3.10+
- Microphone
- Internet connection (for AI APIs)

## License

MIT License
