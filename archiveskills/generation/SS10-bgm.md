# SS10：背景音乐与音效匹配

**Skill ID**：`SS10`  
**核心定位**：根据仪式类型与风格参数匹配无版权（或已授权）背景音乐与关键节点音效。  
**前置依赖**：[SS2] `style_id`、[SS6] 仪式流程。

## 精确落地流程

1. 按风格 ID 与情感强度选择曲库/标签。
2. 匹配一首主 BGM，配置全局淡入淡出。
3. 为关键情感节点配置音效。
4. 素材须为已授权或无版权争议资源（由资产库侧保证）。
5. 人声段落启用闪避（ducking），降低 BGM 音量。

## 输出规范（仅输出合法 JSON）

```json
{
  "bgm_tracks": [
    {
      "track_id": "main_bgm",
      "asset_ref": "royalty_free_piano_02.mp3",
      "start_time_sec": 0.0,
      "end_time_sec": 330.0,
      "base_volume": 0.3,
      "fade_in_sec": 3.0,
      "fade_out_sec": 5.0,
      "ducking_enabled": true,
      "ducking_volume": 0.15
    }
  ],
  "sound_effects": [
    {
      "effect_id": "se_01",
      "asset_ref": "soft_piano_note.mp3",
      "start_time_sec": 30.0,
      "volume": 0.5
    },
    {
      "effect_id": "se_02",
      "asset_ref": "gentle_wind.mp3",
      "start_time_sec": 285.0,
      "volume": 0.2
    }
  ]
}
```
