"""Text-to-Speech (TTS) engine for Visual Vox."""

import os
import platform
import shutil
import subprocess
from typing import Any, Optional


class VoiceSpeaker:
    """
    Visual Vox Speech Synthesis Engine (TTS)
    - Zero-dependency native macOS speech synthesizer (/usr/bin/say -v Tingting).
    - Cloud high-fidelity OpenAI TTS-1 integration (e.g. voice="nova").
    - Cross-platform terminal fallback.
    """

    def __init__(self, openai_client: Optional[Any] = None, use_cloud_tts: bool = False):
        self.client = openai_client
        self.use_cloud_tts = use_cloud_tts
        self.system = platform.system()
        self.has_say = shutil.which("say") is not None

    def speak(self, text: str, block: bool = True):
        """Vocalizes the provided text with feedback indicator."""
        if not text or not text.strip():
            return

        clean_text = text.strip()
        print(f"\n🔊 [Visual Vox 朗读]: \"{clean_text}\"")

        # 1. Cloud-based high-fidelity OpenAI TTS
        if self.use_cloud_tts and self.client:
            try:
                speech_file = "/tmp/visualvox_speech.mp3"
                resp = self.client.audio.speech.create(
                    model="tts-1",
                    voice="nova",
                    input=clean_text,
                )
                resp.stream_to_file(speech_file)
                if self.system == "Darwin":
                    subprocess.run(["afplay", speech_file], check=False)
                return
            except Exception as e:
                print(f"[TTS 降级] 云端语音合成异常 ({e})，切换为系统本地发音。")

        # 2. Native macOS speech (Zero dependency, offline, zero latency)
        if self.system == "Darwin" and self.has_say:
            try:
                cmd = ["say", "-v", "Tingting", "-r", "185", clean_text]
                if block:
                    subprocess.run(cmd, check=False)
                else:
                    subprocess.Popen(cmd)
                return
            except Exception:
                pass

