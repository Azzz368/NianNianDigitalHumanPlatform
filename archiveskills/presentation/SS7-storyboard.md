# SS7：工业级分镜与 Prompt 引擎

**Skill ID**：`SS7`  
**核心定位**：将剧本拆解为镜头级描述与可执行绘图/视频 Prompt；优先复用用户上传素材。  
**前置依赖**：[SS3] `character_dna` 与 `visual_suffix`（来自 [SS2]）、[SS4][SS5] 剧本。

## 精确落地流程

1. 将每段剧本拆为单镜头，计算镜头时长。
2. 为每镜指定景别（特写/中景/全景等）与画面内容。
3. 优先使用用户原始照片，标记 `user_asset` 并关联 `asset_ref`。
4. AI 生成镜头须在 Prompt 中强制拼接人物特征与 `visual_suffix`，并附带统一负面词。
5. 为每镜定义动效与备用资产；镜头间转场与 [SS2] `transition_style` 一致。

## 输出规范（仅输出合法 JSON）

```json
{
  "total_scenes": 7,
  "scenes": {
    "scene_01": {
      "time": "00:00-00:15",
      "shot_type": "Extreme close-up shot",
      "description": "小米粥在砂锅里慢慢沸腾",
      "asset_type": "ai_generated_video",
      "mj_prompt": "Extreme close-up shot of millet porridge boiling slowly in a clay pot, steam rising, warm golden sunlight, vintage 2000s Chinese home video aesthetic --ar 16:9 --v 6.0",
      "negative_prompt": "ugly, deformed, blurry, extra limbs, disfigured, cartoon, anime, illustration",
      "motion": "slow_pan_right",
      "fallback_asset": "default_porridge.jpg"
    },
    "scene_02": {
      "time": "00:15-00:30",
      "shot_type": "Medium shot",
      "description": "爷爷在厨房盛粥",
      "asset_type": "ai_generated_video",
      "mj_prompt": "Medium shot of 75-year-old Chinese man, silver hair combed back, silver-rimmed rectangular glasses, dark grey Zhongshan suit, serving porridge in a kitchen, warm sunlight --ar 16:9 --v 6.0",
      "negative_prompt": "ugly, deformed, blurry, extra limbs, disfigured, cartoon, anime, illustration",
      "motion": "slow_zoom_in",
      "fallback_asset": "photo_01"
    },
    "scene_03": {
      "time": "00:30-00:45",
      "shot_type": "Medium shot",
      "description": "爷爷为孙女打家具",
      "asset_type": "user_asset",
      "asset_ref": "video_01",
      "motion": "slow_zoom_out",
      "fallback_asset": "photo_05"
    }
  }
}
```
