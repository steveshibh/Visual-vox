"""Speech-to-Text (STT) and fuzzy semantic intent resolution for Visual Vox."""

import os
from typing import Any, List, Optional


class VoiceRecognizer:
    """
    Visual Vox Voice Input and Intent Parsing Engine.
    - Transcribes audio inputs via OpenAI Whisper-1.
    - Resolves natural language user requests to candidate image components.
    """

    def __init__(self, openai_client: Optional[Any] = None):
        self.client = openai_client

    def transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribes an audio recording using OpenAI Whisper."""
        if self.client and os.path.exists(audio_file_path):
            try:
                with open(audio_file_path, "rb") as f:
                    transcript = self.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f,
                    )
                return transcript.text.strip()
            except Exception as e:
                print(f"[STT 识别异常]: {e}")
        return ""

    def parse_target(self, user_text: str, candidate_objects: List[str]) -> Optional[str]:
        """Resolves natural user utterance to the closest candidate sub-component."""
        clean = user_text.strip().lower()
        if not clean:
            return None

        # 1. Exact or substring match
        for cand in candidate_objects:
            if cand.lower() in clean or clean in cand.lower():
                return cand

        # 2. Domain semantic aliases
        fuzzy_dict = {
            "猫": ["猫咪", "小猫", "猫猫", "宠物", "kitty", "cat"],
            "爪": ["肉垫", "手", "脚", "爪子", "掌心", "paw", "paws"],
            "眼": ["眼睛", "目光", "瞳孔", "眼神", "eye", "eyes"],
            "鼻": ["鼻子", "鼻头", "小鼻子", "nose"],
            "耳": ["耳朵", "毛毛耳", "ear", "ears"],
            "毛": ["毛发", "皮毛", "绒毛", "fur"],
            "毯": ["毯子", "背景", "床单", "垫子", "blanket", "carpet"],
        }
        for key, aliases in fuzzy_dict.items():
            if any(a in clean for a in aliases):
                for cand in candidate_objects:
                    if key in cand:
                        return cand
        return None
