# Visual Vox 🌟

> **Multimodal Voice-Guided Visual Accessibility Assistant for the Visually Impaired**  
> *让声音成为视障人士探索微观世界的明眸。*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o%20%7C%20Whisper%20%7C%20TTS-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 1. 背景与核心理念 (Mission)

传统辅助视障人士的图像识别系统通常只能提供**单次、扁平的整体概述**（例如：“画面中有一只猫”）。如果视障用户希望了解更多细节：
- *“这只猫是什么品种？它的眼睛是什么颜色？”*
- *“它的爪子长什么样？肉垫是不是粉色的？”*
- *“它现在处于什么姿态和情绪中？”*

传统系统对此无能为力。

**Visual Vox** 提出了**“分层递归树状感知（Hierarchical Recursive Zoom-in）”**架构：
1. **全局印象（Overall Scene）**：初次感知图像，输出生动的全局空间描述，并自动提取画面的主要物体与环境。
2. **交互下钻（Recursive Drill-down）**：用户通过语音指令或按键深入指定部位，模型在微观层面上将其进一步拆解为子构件、物理纹理与触觉细节。
3. **全流程无障碍交互**：高保真语音朗读（TTS）结合模糊语义理解（STT），视障用户无需注视屏幕，即可自由“漫游”图像世界。

---

## 📐 2. 系统工作流架构 (Architecture)

```
                       ┌──────────────────────┐
                       │   输入图像 (URL/本地)   │
                       └──────────┬───────────┘
                                  │
                                  ▼
                   ┌──────────────────────────────┐
                   │  多模态视觉引擎 (GPT-4o)      │
                   │  Strict JSON Mode            │
                   └──────────────┬───────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
【第 1 层：全局空间印象】                            【宏观对象提取】
"一只毛茸茸的橘猫平躺在浅蓝绒毯上..."            [1] 橘色小猫   [2] 浅蓝绒毯
         │                                                 │
         │ (语音播报 TTS: macOS Tingting / OpenAI Nova)   │
         │                                                 │
         └────────────────────────┬────────────────────────┘
                                  │
                  视障用户语音提问: "看看小猫的细节"
                  (Whisper STT / 模糊意图匹配)
                                  │
                                  ▼
                   ┌──────────────────────────────┐
                   │    【第 2 层：局部深度拆解】   │
                   │  - 眼睛：琥珀色清澈双眸       │
                   │  - 鼻子：粉嫩微润倒三角       │
                   │  - 猫爪：前爪蜷缩露肉垫       │
                   │  - 耳朵：双耳直立微倾         │
                   └──────────────┬───────────────┘
                                  │
                  视障用户语音提问: "摸摸它的爪爪"
                                  │
                                  ▼
                   ┌──────────────────────────────┐
                   │   【第 3 层：微观特写感知】    │
                   │  - 掌心大肉垫：饱满弹性粉红球  │
                   │  - 指尖小肉球：四瓣梅花状分布  │
                   │  - 爪尖：半透明微露角质尖端    │
                   └──────────────────────────────┘
```

---

## ✨ 3. 核心功能特点 (Key Features)

* **分层递归语义拆解 (Semantic Tree Decomposition)**：突破传统 Flat Description 的限制，支持多级缩放、叶子节点检测与一键返回上一级（Zoom-out）。
* **高保真语音播报引擎 (Dual TTS Engine)**：
  * **macOS 原生零延迟合成**：优先调用系统底层普通话发音库 **`Tingting`**（零依赖、无需联网、开箱即响）。
  * **OpenAI 云端人声合成**：支持 `model="tts-1"`（如 `nova` 拟真人声），带来广播级听觉体验。
* **自然语音意图理解 (STT & Fuzzy Matching)**：
  * 支持 Whisper-1 麦克风录音文件转文字。
  * 内置领域同义词模糊联想字典，无论是说“爪爪”、“肉垫”还是输入数字编号，均可准确导航。
* **双模平滑演示保障 (Dual Mode Execution)**：
  * **在线模式**：输入 `OPENAI_API_KEY`，直连官方最新多模态接口。
  * **离线仿真模式**：未配置 Key 时自动启用高质量本地 Mock 数据，确保答辩、展示 100% 稳定运行。

---

## 🚀 4. 快速开始 (Quickstart)

### 环境安装

```bash
git clone https://github.com/steveshibh/Visual-vox.git
cd visual-vox
pip install -r requirements.txt
```

### 1. 运行交互式终端演示

```bash
# （可选）配置 OpenAI API 密钥，若不配置将自动进入离线仿真模式
export OPENAI_API_KEY="sk-..."

python demo.py
```

### 2. 在 Jupyter Notebook 中交互

打开项目中的 Notebook 文件：
```bash
jupyter notebook notebooks/Visual_Vox.ipynb
```

### 3. 在 Python 代码中作为模块调用

```python
from visual_vox import VisualVoxAgent

# 创建 Agent 实例（默认启用语音朗读）
agent = VisualVoxAgent(api_key="your_api_key", enable_tts=True)

# 1. 解析初始图像
state = agent.analyze_image("https://example.com/sample.jpg")
print("全局描述:", state["overall"])
print("主要对象:", state["objects"])

# 2. 深入下钻指定部件
sub_detail = agent.drill_down("橘色小猫")
print("细节描述:", sub_detail["detail_summary"])
print("细分子部件:", sub_detail["sub_objects"])

# 3. 返回上一层
agent.go_back()
```

---

## 📂 5. 项目代码结构 (Directory Structure)

```
visual-vox/
├── LICENSE                 # MIT 开源协议
├── README.md               # 项目主说明文档
├── requirements.txt        # Python 依赖清单
├── demo.py                 # 交互式终端应用入口
├── notebooks/
│   └── Visual_Vox.ipynb    # Jupyter Notebook 实验与教学演示
└── visual_vox/             # 核心工程包
    ├── __init__.py         # 导出对外接口与版本号
    ├── agent.py            # VisualVoxAgent 递归感知核心
    ├── speaker.py          # 语音朗读与多后端 TTS 引擎
    └── recognizer.py       # 语音识别 (STT) 与模糊意图匹配器
```

---

## 📄 6. 开源协议 (License)

本项目采用 [MIT License](LICENSE) 开源协议。

