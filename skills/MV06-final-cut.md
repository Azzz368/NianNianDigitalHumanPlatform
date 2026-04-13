# MV06：成片剪辑与交付

**步骤序号**：`6 / 6`  
**Skill ID**：`MV06`  
**适用范围**：大屏数字人短片终稿。

## 本子 Skill 的范围（与甲方一致）

产出 **成片级叙事节奏脚本**：每段时长意图、口播/字幕文案、情绪与转场意图；若使用与工程对接的 JSON，其中的轨级字段表示 **脚本如何映射到音画**，**不**在本文件中规定 FFmpeg 命令、文件路径或服务端合成实现（见 `平台集成与数据编排说明.md`）。

## 核心定位

把 MV03–MV05 已定稿内容收束为 **一条时间线上的叙事与音画脚本表**：各段说什么、显示什么字幕、BGM 情绪与音量**意图**；工程可据此生成合成轨或调用剪辑服务。

## 前置依赖

**MV03**（G3）、**MV04**（G4）、**MV05**（G5）。总时长须与 **MV03 `target_duration_sec`** 一致（±5 秒）。

## 人类闸门 G6

终审：时间码、音量、字幕与情绪；通过后导出成片，禁止跳过。

**局部循环**：可仅驳回某一 `clip_id` 的入出点、单轨音量或字幕条，重剪后再次提交 G6；未点名轨道保持已批准状态。

## 落地流程

1. 按叙事顺序排列各段的起止时间意图，对齐口播与画面内容说明。  
2. 标注 BGM/音效**情绪与音量意图**（如 ducking），具体资源 ID 由曲库与工程绑定。  
3. `project_settings` 与 MV03 `aspect_ratio`、目标时长一致。  
4. 输出单一 JSON 对象，无外层说明文字。

## 输出规范（仅输出合法 JSON）

下列结构便于 **脚本与工程对齐**（与仓库内时间轴校验脚本字段兼容）；**校验与合成实现**见《平台集成…》§5。

```json
{
  "project_settings": {
    "resolution": "1920x1080",
    "fps": 25,
    "aspect_ratio": "16:9",
    "output_format": "mp4",
    "bitrate": "8Mbps",
    "target_duration_sec": 300
  },
  "bgm_program": {
    "main_bgm": {
      "asset_ref": "royalty_free_piano_02.mp3",
      "base_volume": 0.3,
      "fade_in_sec": 3.0,
      "fade_out_sec": 5.0,
      "ducking_enabled": true,
      "ducking_volume": 0.15
    },
    "sound_effects": []
  },
  "project_timeline": [
    {
      "clip_id": "001",
      "start_time_sec": 0.0,
      "end_time_sec": 15.0,
      "video_layer": {
        "type": "ai_video",
        "asset_ref": "scene_01_result.mp4",
        "motion": "slow_pan_right"
      },
      "audio_layers": [
        {
          "type": "bgm",
          "asset_ref": "royalty_free_piano_02.mp3",
          "volume": 0.3,
          "fade_in_sec": 3.0
        }
      ],
      "transition_out": {
        "type": "crossfade",
        "duration_sec": 1.0
      }
    }
  ]
}
```
