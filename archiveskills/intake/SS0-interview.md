# SS0：家属智能采访引导

**Skill ID**：`SS0`  
**核心定位**：替代冰冷表单，通过共情式引导对话采集逝者信息、家属情感记忆与多媒体素材，输出结构化数据字典。  
**前置依赖**：无（用户首次进入即触发）。

## 精确落地流程

1. 开场共情问候，说明采访目的、预计时长与数据隐私保护规则。
2. 提供「快速模式」（约 5 分钟，核心信息）与「深度模式」（约 15 分钟，丰富记忆）供选择。
3. 分 4 个阶段逐步引导提问，每阶段不超过 3 个问题；每题后主动给出 2–3 个具体示例。
4. 自动识别用户上传的照片、录音、视频，引导标注素材对应时间与事件。
5. 支持随时中断、保存进度、继续采访；支持跳过非必填问题。
6. 采访结束后，将对话转化为结构化 JSON，并生成信息摘要供用户确认。

## 输出规范（仅输出下列结构的合法 JSON，无 Markdown 代码块、无注释）

```json
{
  "interview_status": "completed",
  "interview_mode": "deep_mode",
  "basic_info": {
    "name": "张建国",
    "birth_date": "1948-05-12",
    "death_date": "2023-10-25",
    "age": 75,
    "ceremony_date": "2023-10-29",
    "ceremony_type": "family_memorial",
    "ceremony_location": "XX殡仪馆告别厅"
  },
  "core_memories": [
    {
      "content": "每天早上5点起床，为全家煮小米粥和茶叶蛋，坚持了40年",
      "emotion": "warm",
      "time_period": "retirement",
      "related_assets": ["photo_03"]
    },
    {
      "content": "退休后自学木工，为孙女打了一套全套的儿童家具",
      "emotion": "proud",
      "time_period": "retirement",
      "related_assets": ["photo_05", "video_01"]
    }
  ],
  "relatives": [
    {
      "relation": "daughter",
      "name": "张敏",
      "is_main_speaker": true,
      "speech_preference": "gentle_and_sincere"
    },
    {
      "relation": "son",
      "name": "张伟",
      "is_main_speaker": false
    }
  ],
  "last_wishes": "希望家人身体健康，孙女能考上好大学",
  "special_experiences": ["1970-1980年参军入伍", "1985年被评为单位先进工作者"],
  "uploaded_assets": [
    {
      "asset_id": "photo_01",
      "type": "portrait",
      "description": "2018年全家合影，爷爷坐在中间",
      "time_period": "2010s"
    },
    {
      "asset_id": "audio_01",
      "type": "voice_sample",
      "description": "爷爷70岁生日时的讲话录音",
      "duration_sec": 120
    }
  ],
  "style_preference": "warm_nostalgia",
  "emotional_intensity": "moderate"
}
```
