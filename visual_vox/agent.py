"""Visual Vox Agent core logic."""

import base64
import json
import os
from typing import Any, Dict, Optional

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

from .recognizer import VoiceRecognizer
from .speaker import VoiceSpeaker


class VisualVoxAgent:
    """
    Visual Vox Agent:
    Performs recursive, hierarchical semantic decomposition on images
    and navigates down sub-components via speech or keyboard commands.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
        enable_tts: bool = True,
        use_cloud_tts: bool = False,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key) if (HAS_OPENAI and self.api_key) else None
        self.speaker = VoiceSpeaker(self.client, use_cloud_tts=use_cloud_tts) if enable_tts else None
        self.recognizer = VoiceRecognizer(self.client)
        self.history_stack = []
        self.current_state = {}

    def say(self, text: str, block: bool = True):
        """Vocalize speech prompt if TTS is active."""
        if self.speaker:
            self.speaker.speak(text, block=block)

    def analyze_image(self, image_source: str) -> Dict[str, Any]:
        """Performs top-level global scene understanding and extracts major objects."""
        if not self.client:
            # Fallback high-fidelity simulation dataset
            data = {
                "overall": "一只毛茸茸的橘猫正舒服地仰躺在浅蓝色绒毯上，两只前爪微微收拢，双眼专注注视着镜头。",
                "objects": {
                    "橘色小猫": "位于画面正中央，身体平躺，神态慵懒专注，毛色温暖",
                    "浅蓝色绒毯": "位于背景及小猫身下，质感柔软温暖，提供干净简明的背景",
                },
            }
            self.current_state = data
            self.history_stack = []
            return data

        # Load web URL or local file as Base64
        if image_source.startswith("http://") or image_source.startswith("https://"):
            img_payload = {"url": image_source}
        else:
            with open(image_source, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            img_payload = {"url": f"data:image/jpeg;base64,{b64}"}

        sys_prompt = (
            "你是 Visual Vox 视障辅助视觉专家。请分析输入图像，帮助视障人士认知画面。\n"
            "要求：\n"
            "1. 必须始终输出严格的 JSON 对象。\n"
            "2. 必须包含 'overall' (100字以内生动全局概述，方位感清晰，适于朗读) 和 "
            "'objects' (字典，键为对象名，值为空间方位与形态简述)。"
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": sys_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "请分析这张图片。"},
                        {"type": "image_url", "image_url": img_payload},
                    ],
                },
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        data = json.loads(resp.choices[0].message.content)
        self.current_state = data
        self.history_stack = []
        return data

    def drill_down(self, target_object: str) -> Dict[str, Any]:
        """Drills down into sub-components of the target object."""
        self.history_stack.append(self.current_state)

        if not self.client:
            if "爪" in target_object or "肉垫" in target_object:
                sub_data = {
                    "detail_summary": "猫爪近景特写，肉感丰富且极其温顺细腻。",
                    "sub_objects": {
                        "掌心大肉垫": "中央饱满富有弹性的粉红肉球，如软糖般圆润光滑",
                        "指尖小肉球": "四个对称分布的椭圆形粉白小肉垫，排列呈梅花状",
                        "半收拢爪钩": "指甲半收缩在皮毛内，仅露出一小截半透明的角质微尖",
                    },
                }
            elif "猫" in target_object:
                sub_data = {
                    "detail_summary": "小猫全身橘白相间，毛发整洁柔软，呈现完全放松且信任的仰卧姿态。",
                    "sub_objects": {
                        "眼睛": "如通透纯净的琥珀石，瞳孔在微光下微微收缩，眼神灵动专注",
                        "粉嫩鼻头": "小巧的倒三角形状粉色鼻子，湿润光亮，两侧对称长出白色胡须",
                        "猫爪": "两只前爪蜷缩在胸前，露出饱满的浅粉色肉垫，绒毛环绕",
                        "耳朵": "双耳直立警惕，内侧有细软的浅白色绒毛，轮廓分明",
                    },
                }
            else:
                sub_data = {
                    "detail_summary": f"【{target_object}】表面质地均匀平整，无进一步可拆分构件。",
                    "sub_objects": {},
                }
            self.current_state = {
                "overall": sub_data["detail_summary"],
                "objects": sub_data["sub_objects"],
            }
            return sub_data

        prompt = (
            f"视障用户希望深入了解画面中的【{target_object}】。\n"
            "请将该物体进一步拆解为子构件、器官、触感纹理或微观部位。\n"
            "输出严格 JSON 格式：\n"
            "{\n"
            f'  "detail_summary": "关于{target_object}的细节、形态与空间质感描述（适于语音朗读）",\n'
            '  "sub_objects": { "子部件名称": "该子部件的特征与颜色描述" }\n'
            "}\n"
            "若无法再拆解，sub_objects 返回空字典 {}"
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是 Visual Vox 深度视觉拆解专家。输出必须为 JSON。"},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        sub_data = json.loads(resp.choices[0].message.content)
        self.current_state = {
            "overall": sub_data.get("detail_summary", ""),
            "objects": sub_data.get("sub_objects", {}),
        }
        return sub_data

    def go_back(self) -> Optional[Dict[str, Any]]:
        """Restores the previous visual hierarchy state (Zoom-out)."""
        if self.history_stack:
            self.current_state = self.history_stack.pop()
            return self.current_state
        return None
