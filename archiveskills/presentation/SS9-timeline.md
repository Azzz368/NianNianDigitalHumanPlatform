# SS9：终极自动化时间轴阵列

**Skill ID**：`SS9`  
**核心定位**：整合视频、音频、字幕、特效等多轨，输出可直接对接 FFmpeg 或专业合成 API 的时间轴 JSON。  
**前置依赖**：SS1–SS8 及 SS10 的约定输出（审核通过后定稿）。

## 精确落地流程

1. 对齐视频轨、音频轨、字幕轨、特效轨。
2. 为每个片段定义精确起止时间（秒）。
3. 配置转场、淡入淡出、音量曲线。
4. 定义全局渲染参数（分辨率、帧率、码率等）。
5. 输出单一 JSON 对象，无外层说明文字。

## 输出规范（仅输出合法 JSON）

```json
{
  "project_settings": {
    "resolution": "1920x1080",
    "fps": 25,
    "aspect_ratio": "16:9",
    "output_format": "mp4",
    "bitrate": "8Mbps"
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
          "asset_ref": "warm_piano_02.mp3",
          "volume": 0.3,
          "fade_in_sec": 3.0
        }
      ],
      "transition_out": {
        "type": "crossfade",
        "duration_sec": 1.0
      }
    },
    {
      "clip_id": "002",
      "start_time_sec": 15.0,
      "end_time_sec": 30.0,
      "video_layer": {
        "type": "ai_video",
        "asset_ref": "scene_02_result.mp4",
        "motion": "slow_zoom_in"
      },
      "audio_layers": [
        {
          "type": "bgm",
          "asset_ref": "warm_piano_02.mp3",
          "volume": 0.3
        },
        {
          "type": "narration",
          "text": "1948年，他出生在山东的一个小山村。",
          "volume": 0.8
        }
      ],
      "subtitle_layer": {
        "text": "1948年 出生于山东",
        "font": "SimHei",
        "font_size": 36,
        "color": "#FFFFFF",
        "position": "bottom_center",
        "stroke_color": "#000000",
        "stroke_width": 2
      },
      "transition_out": {
        "type": "crossfade",
        "duration_sec": 1.0
      }
    }
  ]
}
```
