# SS8：数字人驱动代码生成

**Skill ID**：`SS8`  
**核心定位**：为 TTS / 数字人 API 生成带停顿、表情与动作标签的驱动任务 JSON（如 SSML）。  
**前置依赖**：[SS3] `voice_dna`、[SS5] 家属致辞、[SS0] 遗愿等文本来源。

## 精确落地流程

1. 将致辞与遗愿文本转为带 SSML（或平台等价）的语音脚本。
2. 按情感标签匹配表情、动作标签。
3. 指定音色（克隆参考或系统预设）。
4. 支持逝者数字人与多位家属数字人并行任务。
5. 输出标准化 `avatar_tasks` 数组。

## 输出规范（仅输出合法 JSON）

```json
{
  "avatar_tasks": [
    {
      "task_id": "avatar_01",
      "speaker": "deceased_avatar",
      "time": "02:30-03:15",
      "ssml_script": "<speak><p>大家别难过。<break time=\"1s\"/>我这辈子，吃过苦，也享过福，挺值了。</p><p><break time=\"0.5s\"/>我最放心不下的，就是你们。希望你们都能健健康康的，开开心心的。</p></speak>",
      "emotion_tags": ["peaceful", "gentle_smile"],
      "action_tags": ["hands_at_sides", "slow_head_nod"],
      "voice_model": "voice_clone_audio_01"
    },
    {
      "task_id": "avatar_02",
      "speaker": "daughter_avatar",
      "time": "01:30-02:30",
      "ssml_script": "<speak><p>爸，您走的那天，家里那盆您养了10年的君子兰开花了。<break time=\"1s\"/>您看，连它都在送您最后一程。</p></speak>",
      "emotion_tags": ["sad", "teary"],
      "action_tags": ["hands_clasped", "slight_head_bow"],
      "voice_model": "system_female_01"
    }
  ]
}
```
