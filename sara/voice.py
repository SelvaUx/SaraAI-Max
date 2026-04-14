"""
SaraAI Max — Voice I/O
Optional voice input/output via --voice flag.
"""

import threading


class VoiceHandler:
    def __init__(self, tts_rate: int = 165, voice_index: int = 0):
        self.tts_rate = tts_rate
        self.voice_index = voice_index
        self._tts_engine = None
        self._recognizer = None
        self._microphone = None
        self.available = False
        self._init()

    def _init(self):
        try:
            import pyttsx3
            self._tts_engine = pyttsx3.init()
            self._tts_engine.setProperty("rate", self.tts_rate)
            voices = self._tts_engine.getProperty("voices")
            if voices and self.voice_index < len(voices):
                self._tts_engine.setProperty("voice", voices[self.voice_index].id)
            self.available = True
        except ImportError:
            pass
        except Exception:
            pass

    def speak(self, text: str):
        if not self._tts_engine:
            return
        try:
            # Strip markdown for TTS
            import re
            clean = re.sub(r"```[\s\S]*?```", "code block", text)
            clean = re.sub(r"`[^`]+`", "", clean)
            clean = re.sub(r"[#*_~>|]", "", clean)
            clean = clean.strip()
            if clean:
                self._tts_engine.say(clean)
                self._tts_engine.runAndWait()
        except Exception:
            pass

    def listen(self, timeout: int = 10) -> str | None:
        try:
            import speech_recognition as sr
            if self._recognizer is None:
                self._recognizer = sr.Recognizer()

            with sr.Microphone() as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self._recognizer.listen(source, timeout=timeout, phrase_time_limit=15)

            # Try Google first, then fall back
            try:
                text = self._recognizer.recognize_google(audio)
                return text
            except Exception:
                pass

            # Try Vosk if available
            try:
                import vosk
                # Vosk integration (if model available)
                pass
            except ImportError:
                pass

            return None
        except ImportError:
            return None
        except Exception:
            return None

    def list_voices(self) -> list[str]:
        if not self._tts_engine:
            return []
        voices = self._tts_engine.getProperty("voices")
        return [f"{i}: {v.name}" for i, v in enumerate(voices)]
