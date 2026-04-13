# SS3：视觉/声音特征锁（CHARACTER_DNA / VOICE_DNA）

**Skill ID**：`SS3`  
**核心定位**：提炼逝者物理与声音特征，作为全局变量注入后续环节，保证画面与声音一致性。  
**前置依赖**：[SS0] 上传的肖像照与语音样本（或用户手填特征）。

## 精确落地流程

1. 优先调用 CV，从肖像照提取面部、身体、着装特征。
2. 调用语音相关能力，从样本提取语速、音调、音色、口音。
3. 自动提取失败时，引导用户手动输入 3–5 个关键特征。
4. 输出标准化特征字典；后续 AI 生成画面须强制拼接 `character_dna` 描述。

## 输出规范（仅输出合法 JSON）

```json
{
  "character_dna": {
    "facial_features": "75-year-old Chinese man, silver hair combed back, silver-rimmed rectangular glasses, deep smile lines at the corners of eyes, a small mole on the chin",
    "body_features": "about 170cm tall, slightly thin, slightly hunched when walking",
    "clothing_style": "often wears a dark grey Zhongshan suit, black cloth shoes, a Shanghai brand watch on his left wrist",
    "mannerisms": "likes to put his hands behind his back when talking, squints his eyes when smiling"
  },
  "voice_dna": {
    "pace": "slow",
    "pitch": "low",
    "texture": "slightly_raspy",
    "accent": "Shandong_dialect_mild",
    "sample_audio_ref": "audio_01"
  },
  "extraction_method": "auto_from_photo_and_audio",
  "confidence_score": 0.92
}
```
