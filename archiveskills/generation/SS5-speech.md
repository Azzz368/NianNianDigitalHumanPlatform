# SS5：家属第一视角情感致辞

**Skill ID**：`SS5`  
**核心定位**：将家属追忆转化为数字人或旁白可用的第一人称致辞文案。  
**前置依赖**：[SS0] 结构化数据、[SS2] `tone`、[SS6] 各环节时长配额。

## 精确落地流程

1. 按 [SS6]「家属致辞」总时长为每位主致辞人分配时长。
2. 严格使用对应致辞人的第一人称。
3. 结合核心记忆与遗愿，避免空洞套话。
4. 适当加入停顿与情感标签，符合口语习惯。
5. 支持多位致辞人分段输出。

## 输出规范（仅输出合法 JSON）

```json
{
  "script_type": "family_speech",
  "total_duration_sec": 90,
  "speeches": [
    {
      "speaker": "daughter",
      "speaker_name": "张敏",
      "duration_sec": 60,
      "segments": [
        {
          "time": "01:30-01:45",
          "text": "爸，您走的那天，家里那盆您养了10年的君子兰开花了。您看，连它都在送您最后一程。",
          "emotion_tag": "sad"
        },
        {
          "time": "01:45-02:00",
          "text": "您常说，做人要踏实，要对得起自己的良心。这句话，我会记一辈子。您放心，我会照顾好妈妈。",
          "emotion_tag": "resolute"
        }
      ]
    },
    {
      "speaker": "granddaughter",
      "speaker_name": "张小雨",
      "duration_sec": 30,
      "segments": [
        {
          "time": "02:00-02:30",
          "text": "爷爷，我会好好学习，不辜负您的期望。您在那边，也要好好的。",
          "emotion_tag": "gentle"
        }
      ]
    }
  ]
}
```
