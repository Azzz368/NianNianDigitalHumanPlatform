# MV03：分镜、提示词与口播文稿

**步骤序号**：`3 / 6`  
**Skill ID**：`MV03`  
**适用范围**：大屏数字人短片（单线叙事 + 画面蒙太奇 + 数字人口播）。

## 本子 Skill 的范围（与甲方一致）

**核心交付**：在用户信息之上生成 **视频级叙事模板**——分镜结构、每镜口播、画面文字描述与可作绘图提示的**纯文本**（`mj_prompt` 等）。**不写**具体调用哪家绘图 API、参数拼接、出图任务与存储（见 `平台集成与数据编排说明.md`）。

## 核心定位

在 **MV01 / MV02** 定稿数据上，一次性产出：

1. **风格与画面参数**（内嵌 `style_profile`，不拆独立 Skill）：视觉后缀、转场、色调与文案基调。  
2. **工业分镜表**：每镜时长、景别、画面描述、绘图/视频用 `mj_prompt`、运动、素材引用。  
3. **口播文稿**：与镜头对齐的旁白/讲述文本（数字人面向观者的讲述），**每镜 `voice_script` 与分镜一一对应**。

不再单独维护「整场追悼会仪式流」或「家属致辞 Skill」；若需第一人称金句，写入对应镜的 `voice_script` 即可。

## 前置依赖

**MV01**、**MV02**（**G2 已通过**）。可选：`target_duration_sec` 来自 MV02 或产品默认（如 300）。

## 人类闸门 G3

家属审阅：**分镜顺序 + 每镜提示词 + 每镜口播**；通过后方可进入 **MV04**。

**局部循环**：可按 **`scene_id`** 驳回单镜或仅驳回「提示词 / 口播 / 时长」之一并重算该镜；未驳回镜头保持冻结版本。

## 落地流程

1. 根据 `target_duration_sec` 拆镜并分配时长；总时长误差建议 ±5 秒内。  
2. 填写 `style_profile`（由原 `style_preference` / `emotional_intensity` 映射）。  
3. 每镜写 `mj_prompt`：人物外观可先用 MV01 肖像描述；**MV04 会把人物/场景/道具锁定为圣经**，MV05 画面生成必须以 MV04 锁定版本为准，因此 MV03 中出现的新场景/新道具应尽量显式写出，便于 MV04 收敛去重。  
4. `mj_prompt` 句末不手写死画幅参数；顶层 `aspect_ratio` 表达成片比例意图，具体如何传给出图服务由工程处理。  
5. 优先引用 `user_asset`；否则标记 AI 生成。  
6. 负面提示词统一置于 `negative_prompt`（可全局一份）。

## 画面提示词（叙事模板的一部分）

- **画幅意图**：顶层 `aspect_ratio`（如 `16:9`），供脚本与分镜一致。  
- **风格后缀**：`style_profile.visual_suffix` 可为英文提示词片段；若内含模型版本占位，仅作文本约定，**不由本子 Skill 定义推理服务参数**。  
- **拼接顺序建议**（供人复制或工程拼接）：`mj_prompt` + 风格后缀 + 画幅相关参数——实现细节见《平台集成…》。

## 输出规范（仅输出合法 JSON）

```json
{
  "target_duration_sec": 300,
  "aspect_ratio": "16:9",
  "style_profile": {
    "style_id": "warm_nostalgia",
    "emotional_intensity": "moderate",
    "visual_suffix": "vintage 2000s Chinese home video aesthetic, warm golden sunlight, soft focus, nostalgic vibe, realistic texture --v 7",
    "color_palette": ["#FFD700", "#FFF8DC", "#D2B48C", "#8B4513"],
    "tone": "empathetic, gentle, conversational",
    "transition_style": "slow_crossfade"
  },
  "total_scenes": 3,
  "scenes": {
    "scene_01": {
      "scene_id": "scene_01",
      "time": "00:00-00:15",
      "shot_type": "Extreme close-up shot",
      "description": "小米粥在砂锅里慢慢沸腾",
      "voice_script": "退休后，他成了家里的依靠。每天早上五点起床煮粥，这一煮，就是四十年。",
      "asset_type": "ai_generated_video",
      "mj_prompt": "Extreme close-up shot of millet porridge boiling slowly in a clay pot, steam rising, warm golden sunlight",
      "negative_prompt": "ugly, deformed, blurry, extra limbs, disfigured, cartoon, anime, illustration",
      "motion": "slow_pan_right",
      "fallback_asset": "default_porridge.jpg"
    },
    "scene_02": {
      "scene_id": "scene_02",
      "time": "00:15-00:30",
      "shot_type": "Medium shot",
      "description": "他在厨房忙碌的身影",
      "voice_script": "他话不多，却把爱都煮进了粥里。",
      "asset_type": "ai_generated_video",
      "mj_prompt": "Medium shot of 75-year-old Chinese man, silver hair, dark grey Zhongshan suit, kitchen, warm sunlight",
      "negative_prompt": "ugly, deformed, blurry, extra limbs, disfigured, cartoon, anime, illustration",
      "motion": "slow_zoom_in",
      "fallback_asset": "photo_01"
    },
    "scene_03": {
      "scene_id": "scene_03",
      "time": "00:30-00:45",
      "shot_type": "Medium shot",
      "description": "旧照：与孙辈合影",
      "voice_script": "",
      "asset_type": "user_asset",
      "asset_ref": "photo_05",
      "mj_prompt": null,
      "negative_prompt": null,
      "motion": "slow_zoom_out",
      "fallback_asset": "photo_05"
    }
  }
}
```

**说明**：纯资料镜可无口播，`voice_script` 为空串；与成片时长、朗读气口的对齐在 **MV05 / MV06** 的脚本结构中体现，具体 TTS/合成由工程执行。
