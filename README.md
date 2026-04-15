# 追悼会 AIGC 管线本地测试看板

这是一个用于调试与评估「追悼会 / 生命回顾视频」端到端 AI 管线的本地 Streamlit 应用。

## 功能概览
- 按阶段顺序执行 SS0 → SS1/SS2/SS3/SS6 → SS4/SS5/SS10（并行）→ SS7/SS8 → SS9
- 每一步输出 JSON 文件写入 `outputs/`
- 支持 SS1 缺失校验人工确认，以及 SS9 前的人工审核节点

## 准备工作
1. 复制技能 Prompt 文件到 `skills/`（项目不自带）
2. 复制并填写环境变量（默认支持 LM Studio + OpenRouter 备选）：
  - `OPENAI_API_KEY`（LM Studio 通常可填写 `lm-studio`）
  - `OPENAI_BASE_URL`（如 `http://localhost:1234/v1`）
  - `OPENAI_MODEL`（如 `qwen3.5:9b`）
  - 可选：`OPENAI_FALLBACK_BASE_URL`、`OPENAI_FALLBACK_API_KEY`、`OPENAI_FALLBACK_MODELS`

## 运行
- 安装依赖并启动：
  - 运行 `pip install -r requirements.txt`
  - 运行 `streamlit run app.py`

## 目录结构
```
memorial-pipeline-test/
├── app.py
├── pipeline_runner.py
├── llm_client.py
├── skill_loader.py
├── skills/
├── outputs/
├── sample_inputs/
└── requirements.txt
```
