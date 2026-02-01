"""Quick test script for Nebula Voice Assistant components"""
import sys
import asyncio

print("=" * 50)
print("  Nebula Voice Assistant - Component Tests")
print("=" * 50)
print()

# Test 1: TTS
print("[TEST 1] Text-to-Speech (pyttsx3)")
try:
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f"  ✓ Initialized with {len(voices)} voices")
    # Don't actually speak during test to save time
    print("  ✓ TTS ready")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 2: Screen Capture
print("\n[TEST 2] Screen Capture (mss)")
try:
    import mss
    with mss.mss() as sct:
        monitors = sct.monitors
        print(f"  ✓ Found {len(monitors)-1} monitor(s)")
        screenshot = sct.grab(sct.monitors[1])
        print(f"  ✓ Captured {screenshot.width}x{screenshot.height} screenshot")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 3: AI Engine (Kimi K2.5)
print("\n[TEST 3] AI Engine (Kimi K2.5)")
try:
    import httpx
    
    async def test_kimi():
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://api.moonshot.ai/v1/chat/completions",
                headers={
                    "Authorization": "Bearer sk-tTz2G35OPLdIqYyhVazxxz3g3KLnuU8CM1doK3lyK792M3Kq",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "moonshot-v1-8k",
                    "messages": [{"role": "user", "content": "Say hello in 5 words"}],
                    "max_tokens": 50
                }
            )
            if resp.status_code == 200:
                data = resp.json()
                content = data["choices"][0]["message"]["content"]
                print(f"  ✓ API responded: {content[:50]}")
            else:
                print(f"  ✗ API error: {resp.status_code} - {resp.text[:100]}")
    
    asyncio.run(test_kimi())
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 4: Speech Recognition with sounddevice
print("\n[TEST 4] Speech Recognition (sounddevice)")
try:
    import sounddevice as sd
    devices = sd.query_devices()
    input_device = sd.query_devices(kind='input')
    print(f"  ✓ Found {len([d for d in devices if d['max_input_channels'] > 0])} input device(s)")
    print(f"  ✓ Default: {input_device['name'][:40]}...")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test 5: System Tray
print("\n[TEST 5] System Tray (pystray)")
try:
    import pystray
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (64, 64), color=(100, 100, 100))
    print("  ✓ pystray available")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "=" * 50)
print("  Tests Complete!")
print("=" * 50)
