# SS2：全局风格参数化定义

**Skill ID**：`SS2`  
**核心定位**：将用户风格选择转化为模型与视频引擎可用的参数化风格字典。  
**前置依赖**：[SS0] 的 `style_preference`、`emotional_intensity`。

## 精确落地流程

1. 接收风格类型：温情回忆 / 庄重肃穆 / 青春活力 / 军旅生涯 / 书香儒雅。
2. 接收情感强度：轻柔 / 适中 / 浓烈。
3. 映射视觉 Prompt 后缀、色彩字典、文案语调、转场风格。
4. 输出标准化风格参数，供后续子 Skill 引用。

## 输出规范（仅输出合法 JSON）

```json
{
  "style_id": "warm_nostalgia",
  "emotional_intensity": "moderate",
  "visual_suffix": "vintage 2000s Chinese home video aesthetic, warm golden sunlight, soft focus, nostalgic vibe, realistic texture --v 6.0",
  "color_palette": ["#FFD700", "#FFF8DC", "#D2B48C", "#8B4513"],
  "tone": "empathetic, gentle, first-person narrative, conversational",
  "transition_style": "slow_crossfade",
  "bgm_genre": "piano_solo",
  "subtitle_style": "simple_white"
}
```
