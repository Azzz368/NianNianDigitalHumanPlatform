# SS6：追悼会仪式流程编译

**Skill ID**：`SS6`  
**核心定位**：输出标准化仪式流，为总时长与各环节内容生成提供刚性骨架。  
**前置依赖**：[SS0] 的 `ceremony_type`、`ceremony_date`。

## 精确落地流程

1. 按仪式类型（家庭追思会 / 单位追悼会 / 小型告别会 / 线上追思会等）选择预设模板。
2. 与用户确认总时长（默认约 5 分钟，支持约 3–20 分钟自定义）。
3. 为各环节分配时长配额；生平回顾、家属致辞等核心环节优先。
4. 标记必填与可选环节；支持用户自定义环节。
5. 输出 JSON，供前端拖拽调整后再锁定。

## 输出规范（仅输出合法 JSON）

```json
{
  "ceremony_type": "family_memorial",
  "total_duration_sec": 330,
  "ceremony_flow": [
    {"step": 1, "name": "入场静默", "duration_sec": 30, "action": "空镜头+轻柔背景音乐", "required": true, "editable": false},
    {"step": 2, "name": "生平回顾", "duration_sec": 120, "action": "照片/AI分镜蒙太奇+旁白", "required": true, "editable": true},
    {"step": 3, "name": "家属致辞", "duration_sec": 90, "action": "数字人/家属画面+致辞", "required": false, "editable": true},
    {"step": 4, "name": "遗愿传达", "duration_sec": 45, "action": "逝者数字人+口播", "required": false, "editable": true},
    {"step": 5, "name": "亲友寄语", "duration_sec": 30, "action": "亲友照片轮播+文字", "required": false, "editable": true},
    {"step": 6, "name": "最后告别", "duration_sec": 45, "action": "遗像特写+背景音乐渐弱", "required": true, "editable": false}
  ]
}
```
