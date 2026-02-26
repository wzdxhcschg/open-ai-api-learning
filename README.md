# OpenAI API 全覆盖测试项目

全面测试 OpenAI 各类 API 的 Python 示例，每个 API 类别独立文件，代码注释详细，开箱即用。

## 项目结构

```
open-ai-api-learning/
│
├── chat/
│   ├── basic_completion.py     # 单轮/多轮对话、temperature、system prompt
│   ├── streaming.py            # 流式输出 + token 用量
│   ├── function_calling.py     # 工具调用：单工具、并行调用、强制指定
│   ├── structured_output.py    # JSON mode + JSON Schema 精确输出
│   └── vision.py               # 图片理解：URL / Base64 / detail 对比
│
├── audio/
│   ├── tts.py                  # TTS：声音对比、格式、语速、模型质量
│   └── stt.py                  # Whisper：转录、翻译、时间戳、prompt
│
├── images/
│   └── dalle.py                # DALL·E 3/2：生成、变体、编辑、B64
│
├── embeddings/
│   └── embeddings_demo.py      # 嵌入：相似度、语义搜索、降维、批量
│
├── moderations/
│   └── moderations_demo.py     # 内容安全：批量检测、安全对话流程
│
├── files/
│   └── files_demo.py           # Files API 完整生命周期
│
├── fine_tuning/
│   └── fine_tuning_demo.py     # 微调：创建/等待/使用自定义模型
│
├── assistants/
│   └── assistants_demo.py      # Assistants v2：问答、代码解释器、多轮对话
│
├── utils/
│   └── client.py               # 公用 OpenAI client（所有模块共用）
│
├── outputs/                    # 生成的文件输出目录（自动创建，已 gitignore）
├── requirements.txt
├── .env.example
└── .gitignore
```

## 快速开始

```bash
# 1. 配置 API Key
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY=sk-...

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行任意示例
python chat/basic_completion.py
python chat/streaming.py
python chat/function_calling.py
python embeddings/embeddings_demo.py
python moderations/moderations_demo.py
```

## API 类别说明

| 文件 | API | 主要功能 |
|------|-----|---------|
| `chat/basic_completion.py` | Chat Completions | 基础对话、system prompt、temperature |
| `chat/streaming.py` | Chat Completions | 流式输出 |
| `chat/function_calling.py` | Chat Completions | Tool Use，并行工具调用 |
| `chat/structured_output.py` | Chat Completions | JSON mode，JSON Schema |
| `chat/vision.py` | Chat Completions | 多模态图片理解 |
| `audio/tts.py` | Audio | Text-to-Speech，6种声音 |
| `audio/stt.py` | Audio | Whisper 转录 + 翻译 |
| `images/dalle.py` | Images | DALL·E 3/2 图片生成 |
| `embeddings/embeddings_demo.py` | Embeddings | 语义搜索，相似度计算 |
| `moderations/moderations_demo.py` | Moderations | 内容安全检测 |
| `files/files_demo.py` | Files | 上传/列举/删除文件 |
| `fine_tuning/fine_tuning_demo.py` | Fine-tuning | 微调流程全覆盖 |
| `assistants/assistants_demo.py` | Assistants v2 | 多工具 Agent 对话 |

## 注意事项

- 部分 API（DALL·E 3、Fine-tuning、Assistants）会产生较高费用，请按需运行
- Fine-tuning 需要至少 10 条训练数据，微调过程需数分钟到数小时
- Audio STT / 图片编辑功能需提供本地文件，取消注释相应代码行
- 所有生成文件（音频、图片）保存在 `outputs/` 目录（已加入 .gitignore）
