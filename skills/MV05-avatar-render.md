# MV05：数字人驱动与画面生成

**步骤序号**：`5 / 6`  
**Skill ID**：`MV05`  
**适用范围**：大屏数字人短片。

## 本子 Skill 的范围（与甲方一致）

在已定稿的 **叙事脚本** 上，细化 **口播朗读稿结构**（停顿、情感标签）与 **每镜画面叙事说明**（上屏意图、与分镜的对应关系）。字段中若出现资源名，仅作文案级占位。**不写**渲染队列、三视图文件上传协议、存储与合成实现。

## 核心定位

在 **MV03** 分镜与口播、**MV04** 三大圣经（人物/场景/道具）锁定基础上，产出：

1. **画面叙事任务说明**：按镜说明画面要讲述的内容与上屏方式（模板枚举由产品与工程约定，本子 Skill 只填语义）。  
2. **数字人朗读脚本**：将 `voice_script` 转为带停顿与情感标签的结构化稿（如 SSML），服务口型与讲述节奏；**终轨剪辑意图**在 **MV06** 的脚本结构中收束。

## 前置依赖

**MV03**（G3）、**MV04**（G4，且 `lock_manifest.locked_gate` 必须为 `G4`）。

## 人类闸门 G5

预览**关键镜画面小样 + 数字人片段**；通过后方可进入 **MV06**。

**局部循环**：可仅驳回指定 `scene_id` 的叙事任务说明、仅重改数字人某段朗读稿、或只重述三视图相关的**文字约束**；未驳回部分保持已批准版本。

## 落地流程

1. 对齐 **MV04** 的三大圣经锁定版本与 **MV03** 分镜，避免叙事矛盾；本步不得擅自新增“未在 MV04 锁定的场景/道具”。  
2. 将各镜 `voice_script` 串联为符合时长与气口的讲述脚本；按镜切分数字人段落。  
3. 为每段绑定朗读音色/角色标识（`voice_model` 为逻辑名，工程映射真实模型）。  
4. `scene_visual_tasks` 与 MV03 `scene_id` 对齐，用简短语义说明上屏关系（枚举由工程提供清单即可）。  
5. 若某镜必须引入新场景/新道具（MV04 未锁定），则本步应输出 `requires_unlock_and_relock: true` 并点名缺失项，流程回到 MV04 局部循环补齐并重锁后再继续。  
6. G5 未通过时，仅对点名范围重跑本子 Skill 对应片段。

## 输出规范（仅输出合法 JSON）

```json
{
  "lock_manifest_ref": {
    "locked_gate": "G4",
    "character_bible_version": "1.0.0",
    "scene_library_version": "1.0.0",
    "prop_library_version": "1.0.0"
  },
  "layout_mode": "dh_with_b_roll",
  "scene_visual_tasks": [
    {
      "scene_id": "scene_01",
      "render_role": "b_roll_fullscreen",
      "expected_asset": "scene_01_result.mp4",
      "notes": "粥锅特写，无数字人叠画"
    },
    {
      "scene_id": "scene_02",
      "render_role": "dh_over_b_roll",
      "expected_asset": "scene_02_result.mp4",
      "notes": "数字人半身叠加厨房背景"
    }
  ],
  "avatar_tasks": [
    {
      "task_id": "avatar_01",
      "speaker": "deceased_avatar",
      "scene_range": "scene_01-scene_02",
      "ssml_script": "<speak><p>退休后，他成了家里的依靠。<break time=\"0.5s\"/>每天早上五点起床煮粥，这一煮，就是四十年。</p></speak>",
      "emotion_tags": ["warm", "gentle_smile"],
      "action_tags": ["hands_at_sides", "slow_head_nod"],
      "voice_model": "voice_clone_audio_01"
    }
  ],
  "requires_unlock_and_relock": false,
  "missing_library_items": []
}
```

**说明**：本步必须引用 MV04 的锁定版本；如需新增场景/道具，必须回到 MV04 先锁定再继续。
