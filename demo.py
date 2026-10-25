#!/usr/bin/env python3
"""Interactive command line runner for Visual Vox."""

import os
import sys

from visual_vox import VisualVoxAgent


def main():
    print("=" * 65)
    print("           🌟 Visual Vox 视障全语音多模态无障碍系统")
    print("=" * 65)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[提示] 未检测到 OPENAI_API_KEY 环境变量，启动【内置高保真仿真模式】。")
        print("      若需连接真实 GPT-4o 模型，请在终端执行: export OPENAI_API_KEY='sk-...'")

    agent = VisualVoxAgent(api_key=api_key, enable_tts=True)

    default_image = "https://images.unsplash.com/photo-1543852786-1cf6624b9987?auto=format&fit=crop&w=800&q=80"
    user_img = input(f"\n请输入图片文件路径或网络 URL (回车使用默认猫咪图): ").strip()
    if not user_img:
        user_img = default_image

    agent.say("正在为您感知图像内容，请稍候。")
    state = agent.analyze_image(user_img)

    while True:
        print("\n" + "=" * 55)
        print(f"【当前层级感知】: {state.get('overall')}")
        print("=" * 55)
        agent.say(state.get("overall"))

        objects = state.get("objects", {})
        obj_keys = list(objects.keys())

        if not obj_keys:
            msg = "该部位已达最细微构件，无法继续下钻。输入 b 可返回上一层。"
            print(msg)
            agent.say(msg)
        else:
            print("\n可供探查的部件列表:")
            for idx, k in enumerate(obj_keys, 1):
                print(f"  [{idx}] {k} -> {objects[k]}")
            menu_speech = "当前可观察：" + "，".join(obj_keys) + "。请输入数字或说出想看的部位。"
            agent.say(menu_speech)

        user_input = input("\n[指令输入] 请输入编号或部位名称（'b' 返回上一级，'q' 退出）: ").strip()

        if not user_input or user_input.lower() == "q":
            agent.say("感谢使用 Visual Vox，愿声音成为您探索世界的明眸！")
            print("会话已退出。")
            break

        if user_input.lower() == "b":
            prev = agent.go_back()
            if prev:
                agent.say("已返回上一层。")
                state = prev
            else:
                agent.say("当前已经是全局顶层，无法继续返回。")
            continue

        # 1. Number index matching
        chosen_target = None
        if user_input.isdigit() and 1 <= int(user_input) <= len(obj_keys):
            chosen_target = obj_keys[int(user_input) - 1]
        else:
            # 2. Fuzzy semantic resolution
            chosen_target = agent.recognizer.parse_target(user_input, obj_keys)

        if chosen_target:
            agent.say(f"正在为您深入探查：【{chosen_target}】。")
            agent.drill_down(chosen_target)
            state = agent.current_state
        else:
            err_msg = f"未能在当前列表中识别到与‘{user_input}’相关的部位，请重新选择。"
            print(err_msg)
            agent.say(err_msg)


if __name__ == "__main__":
    main()
