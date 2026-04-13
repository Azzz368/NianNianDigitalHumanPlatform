# 平台集成与数据编排说明（非子 Skill）

> **定位**：本文档给 **后端 / API / 合成引擎 / 数据层** 使用。  
> **与甲方约定一致**：**子 Skill（MV01–MV06 各 `.md`）不扩展为后端与数据处理规范**；子 Skill 专注 **用户信息 + 内容 → 视频脚本与叙事模板**（含分镜级文案、口播、画面文字描述等）。  
> 下列内容**不得**并入对模型加载的「子 Skill」正文中，以免混淆职责。

## 1. 子 Skill 产物如何进入工程

| 子 Skill | 内容侧重（给模型） | 工程侧典型用途（本文档范围） |
|----------|-------------------|------------------------------|
| MV01 | 用户信息与素材目录 | 入库、权限、对象存储 `asset_id` 解析 |
| MV02 | 是否可写脚本、补全建议、人读总结 | 审核流、表单、状态机 |
| MV03 | **核心**：分镜叙事 + 口播 + 画面提示词文本 | 写脚本库、驱动 UI 审片；提示词交给出图/出视频服务 |
| MV04 | 人物/声线的**文字化一致描述** + 试听引用字段 | CV/TTS/克隆管线、试听文件生成与存储 |
| MV05 | 口播结构化（如 SSML）、镜头叙事与画面任务说明 | 数字人 API、渲染队列、三视图资产落盘 |
| MV06 | 若需：成片轨级 JSON（时间线） | FFmpeg、多轨合成、BGM ducking、导出任务 |

## 2. 编排与人工审核（状态机）

- **G1–G6** 的通过/驳回、**局部循环**（按 `scene_id` / `clip_id` 等点名重跑）由 **产品 + 后端状态机** 实现。  
- 子 Skill 只描述 **在各闸门下要审什么内容**；不写 Webhook、数据库表结构、重试队列。

## 3. 三库持久化（可选工程实现）

在内容侧，**人物库/场景库/道具库**均由 **MV04** 输出并在 **G4** 通过时视为“锁定版本”（`lock_manifest`）。工程侧可选择将其持久化为单一真源，以支撑后续渲染、复用与审计。

### 3.1 建议的持久化结构（工程约定）

- **人物库**：对应 MV04 `character_bible`
- **场景库**：对应 MV04 `scene_library`
- **道具库**：对应 MV04 `prop_library`
- **锁定清单**：对应 MV04 `lock_manifest`（版本号 + locked_gate）

### 3.2 合并与版本

- 使用 **PATCH 语义** + **乐观锁**；局部循环仅更新被点名条目（如单个 `scene_id` / `prop_id`）。  
- **G4 未通过**不得覆盖已锁定版本；MV05 若输出 `requires_unlock_and_relock: true`，应回到 MV04 完成补齐与重锁再继续。

### 3.3 JSON 示例（持久化，可选）

```json
{
  "bible_set_id": "bible_zhangjianguo_001",
  "bible_set_version": "1.0.0",
  "character_bible": { "character_id": "deceased_01" },
  "scene_library": [{ "scene_id": "scn_kitchen_morning" }],
  "prop_library": [{ "prop_id": "prop_clay_pot" }],
  "lock_manifest": {
    "locked_gate": "G4",
    "character_bible_version": "1.0.0",
    "scene_library_version": "1.0.0",
    "prop_library_version": "1.0.0"
  }
}
```

## 4. MV05 的缺口回流（工程提示）

MV05 若输出 `requires_unlock_and_relock: true` 与 `missing_library_items`，工程应把这些缺口回流到 MV04 的局部循环输入，以完成补齐与重锁。

## 5. MV06 与时间轴校验

- 仓库内 `verify-ss9-json.js` / `verify_ss9_json.py` 校验的是 **工程合成轨** `project_settings` + `project_timeline`。  
- 该结构可在 **后端由叙事脚本映射生成**，不必作为「内容子 Skill」的必背篇幅；映射规则由实现团队维护。

## 6. API / 异步任务（提示）

- 出图、克隆试听、渲染、导出等应 **异步 Job + 回调或轮询**；不在子 Skill 中定义。  
- 合规：语音克隆授权、数据留存与删除策略，在 **隐私与合规接口** 中单独定义。
