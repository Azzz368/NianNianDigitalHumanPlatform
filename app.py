import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import streamlit as st

import gate_manager
import pipeline_runner

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_PATH = BASE_DIR / "sample_inputs" / "sample_interview.json"

MV_STEPS = [
    {"id": "MV01", "name": "MV01 家属访谈结构化"},
    {"id": "MV02", "name": "MV02 信息校验与补全"},
    {"id": "MV03", "name": "MV03 分镜脚本生成"},
    {"id": "MV04", "name": "MV04 三要素定稿"},
    {"id": "MV05", "name": "MV05 数字人渲染编排"},
    {"id": "MV06", "name": "MV06 最终时间轴"},
]

STATUS_BADGE = {
    "pending": "⚬ 待命",
    "running": "🟡 运行中",
    "awaiting_review": "🔵 需确认",
    "approved": "✅ 达成",
    "rejected": "✖ 已退回",
}


st.set_page_config(page_title="MV 流水线审核看板", layout="wide")

st.markdown(
    """
<style>
/* 引用类似 LegacyRemembered 的字体与极简风格 */
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Noto+Sans+SC:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Lato', 'Noto Sans SC', sans-serif !important;
}

/* 背景与排版重置 */
.stApp {
    background-color: #Fdfdfc;
    color: #232425;
}

/* 卡片样式，参考前端交互审计 (.hover-card) */
.mv-card {
    padding: 20px 24px;
    border-radius: 12px;
    background: #FFFFFF;
    border: 1px solid rgba(0,0,0,0.06);
    margin-bottom: 20px;
    box-shadow: 0px 2px 4px -1px rgba(0,0,0,0.02);
    transition: all 300ms cubic-bezier(0.4, 0, 0.2, 1);
}
.mv-card:hover {
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
    transform: translateY(-2px);
    border-color: rgba(0,0,0,0.1);
}

/* 卡片头部 */
.mv-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 12px;
}
.mv-header strong, .mv-header h3 {
    margin: 0;
    font-weight: 600;
    color: #111111;
    font-size: 1.1rem;
}

/* 标签胶囊样式 (.mv-pill) */
.mv-pill {
    padding: 4px 12px;
    border-radius: 999px;
    background: #f3f4f6;
    font-size: 13px;
    font-weight: 500;
    color: #4b5563;
    border: 1px solid #e5e7eb;
}

/* 按钮全局覆盖 */
div.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 150ms cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 品牌主色调按钮 (Primary Button) */
div.stButton > button[kind="primary"] {
    background-color: #111111 !important;
    color: #FFFFFF !important;
    border: 1px solid #111111 !important;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #333333 !important;
    border-color: #333333 !important;
}

/* 次要按钮弱化 */
div.stButton > button[kind="secondary"] {
    background: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    color: #374151 !important;
}
div.stButton > button[kind="secondary"]:hover {
    border-color: #d1d5db !important;
    background: #f9fafb !important;
    color: #111111 !important;
}

/* 输入框和 Expander 弱化边框 */
.stTextInput > div > div > input {
    border-radius: 6px;
    border: 1px solid #e5e7eb;
}
.streamlit-expanderHeader {
    font-weight: 500;
    color: #374151;
}

</style>
""",
    unsafe_allow_html=True,
)


def load_sample() -> Dict[str, Any]:
    if SAMPLE_PATH.exists():
        return json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    return {}


def parse_json(text: str) -> Tuple[Dict[str, Any], str]:
    try:
        data = json.loads(text) if text.strip() else {}
        if not isinstance(data, dict):
            return {}, "请输入 JSON 对象作为输入。"
        return data, ""
    except json.JSONDecodeError as exc:
        return {}, f"JSON 解析失败：{exc}"


def render_sidebar() -> None:
    st.sidebar.markdown("## 流水线进度")
    for step in MV_STEPS:
        status = gate_manager.get_status(step["id"])
        badge = STATUS_BADGE.get(status, "⚪ 未开始")
        st.sidebar.markdown(f"**{badge}**  {step['id']} · {step['name']}")
    st.sidebar.divider()
    if st.sidebar.button("🔄 重置全部阶段", use_container_width=True):
        pipeline_runner.reset_state()
        st.rerun()


def render_key_cards(output: Dict[str, Any], keys: List[str]) -> None:
    if not output:
        return
    cols = st.columns(len(keys)) if keys else []
    for idx, key in enumerate(keys):
        value = output.get(key, "-")
        with cols[idx]:
            st.markdown(
                f"<div class='mv-card'><strong>{key}</strong><br/>{value}</div>",
                unsafe_allow_html=True,
            )


def render_mv03_scenes(output: Dict[str, Any]) -> None:
    scenes = output.get("scenes", []) if isinstance(output, dict) else []
    if isinstance(scenes, dict):
        ordered_keys = sorted(scenes.keys())
        scenes = [scenes[key] for key in ordered_keys]
    if not isinstance(scenes, list) or not scenes:
        st.info("暂无分镜数据。")
        return
    for scene in scenes:
        if not isinstance(scene, dict):
            st.markdown(
                "<div class='mv-card'><div class='mv-header'><strong>分镜内容</strong></div>",
                unsafe_allow_html=True,
            )
            st.write(scene)
            st.markdown("</div>", unsafe_allow_html=True)
            continue
        scene_id = scene.get("scene_id") or scene.get("id") or scene.get("scene") or "unknown"
        timecode = scene.get("time") or scene.get("timecode") or "-"
        narration = scene.get("voice_script") or scene.get("narration") or scene.get("voice_over") or "-"
        st.markdown(
            f"<div class='mv-card'><div class='mv-header'><strong>分镜片段：Scene {scene_id}</strong></div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"**⏱️ 时间码**：{timecode}&nbsp;&nbsp;&nbsp;&nbsp;**🎥 景别**：{scene.get('shot_type', '-')}")
        st.markdown(f"**📝 画面描写**：<span style='color:#4b5563'>{scene.get('description', '-')}</span>", unsafe_allow_html=True)
        st.markdown(f"**🎙️ 语音旁白**：<span style='color:#4b5563'>{narration}</span>", unsafe_allow_html=True)
        st.markdown(f"**🔖 资产类型**：<span style='color:#6b7280; font-size:14px'>{scene.get('asset_type', '-')}</span>", unsafe_allow_html=True)
        with st.expander("查看 mj_prompt", expanded=False):
            st.write(scene.get("mj_prompt", "-"))
        if st.button(f"↩️ 退回此镜 {scene_id}", key=f"reject_scene_{scene_id}"):
            gate_manager.reject("MV03", {"ids": [scene_id]})
            st.warning(f"已标记退回镜头：{scene_id}")
        st.markdown("</div>", unsafe_allow_html=True)


def render_mv04_bibles(output: Dict[str, Any], approved: bool) -> None:
    cols = st.columns(3)
    with cols[0]:
        st.markdown("### 人物要素")
        st.json(output.get("character_bible", {}))
    with cols[1]:
        st.markdown("### 场景要素")
        st.json(output.get("scene_library", {}))
    with cols[2]:
        st.markdown("### 道具要素")
        st.json(output.get("prop_library", {}))
    if approved:
        st.success("已确认三要素")


def render_step(step: Dict[str, str], mv01_input: Dict[str, Any], input_ok: bool) -> None:
    mv_id = step["id"]
    next_index = pipeline_runner.MV_ORDER.index(mv_id) + 1
    next_gate = pipeline_runner.MV_ORDER[next_index] if next_index < len(pipeline_runner.MV_ORDER) else None
    status = gate_manager.get_status(mv_id)
    state = pipeline_runner.get_status().get(mv_id, {})
    duration = state.get("duration_sec")
    duration_text = f"{duration:.2f}s" if duration else "-"
    badge = STATUS_BADGE.get(status, "⚪ 未开始")

    st.markdown(
        f"""
        <div class='mv-card'>
            <div class='mv-header'>
                <div style="display:flex; align-items:center; gap:12px;">
                    <h3>{mv_id} · {step['name']}</h3>
                    <span class='mv-pill'>{badge}</span>
                </div>
            </div>
            <p style="color:#6b7280; font-size:14px; margin-top:-8px;">耗时记录：{duration_text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    output = pipeline_runner.read_output(mv_id)
    if state.get("error"):
        st.error(state.get("error"))

    if mv_id == "MV03":
        render_mv03_scenes(output)
    elif mv_id == "MV04":
        render_mv04_bibles(output, status == "approved")
    else:
        with st.expander("查看 JSON 输出", expanded=True):
            st.json(output or {})

    if mv_id == "MV05" and output.get("requires_unlock_and_relock") is True:
        st.error("⚠️ 需返回MV04补齐三要素再重跑")

    if mv_id == "MV02" and output.get("status") == "needs_input":
        prompts = output.get("prompts", [])
        st.warning("补全建议：" + ("、".join(prompts) if prompts else "请补全缺失字段"))

    with st.expander("关键字段摘要", expanded=False):
        render_key_cards(output, list(output.keys())[:3])

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        rerun_disabled = (mv_id == "MV01" and not input_ok) or status == "running"
        if st.button("🔁 重新执行", key=f"rerun_{mv_id}", use_container_width=True, disabled=rerun_disabled):
            scope_text = st.session_state.get(f"scope_{mv_id}", "")
            scope_ids = [item.strip() for item in scope_text.split(",") if item.strip()]
            if scope_ids:
                pipeline_runner.rerun_partial(mv_id, {"ids": scope_ids}, output)
            else:
                pipeline_runner.run_step(mv_id, mv01_input if mv_id == "MV01" else None)
            st.rerun()

    with col2:
        scope_text = st.text_input(
            "退回字段/scene_id",
            key=f"scope_{mv_id}",
            placeholder="scene_01, field_name",
            label_visibility="collapsed",
        )
    if st.button("⬅ 退回", key=f"reject_{mv_id}", use_container_width=True):
            scope_ids = [item.strip() for item in scope_text.split(",") if item.strip()]
            scope = {"ids": scope_ids} if scope_ids else {"reason": "manual_reject"}
            gate_manager.reject(mv_id, scope)
            if next_gate:
                gate_manager.reset_from(next_gate)
            st.rerun()

    with col3:
        approve_disabled = status != "awaiting_review" or (mv_id == "MV02" and output.get("status") == "needs_input")
        approve_label = "✅ 通过 →"
        if mv_id == "MV04":
            approve_label = "✅ 确认三要素"
        if mv_id == "MV06":
            approve_label = "✅ 终审通过，导出最终JSON"
        if not (mv_id == "MV05" and output.get("requires_unlock_and_relock") is True):
            if st.button(approve_label, key=f"approve_{mv_id}", use_container_width=True, disabled=approve_disabled):
                gate_manager.approve(mv_id)
                st.rerun()

    if mv_id == "MV06" and status == "approved" and output:
        download_payload = json.dumps(output, ensure_ascii=False, indent=2)
        st.download_button(
            "下载 mv06_final_timeline.json",
            data=download_payload,
            file_name="mv06_final_timeline.json",
            mime="application/json",
        )


sample_inputs = load_sample()
render_sidebar()

st.title("追悼会 MV 执行层 Demo")

input_default = json.dumps(sample_inputs, ensure_ascii=False, indent=2)
mv01_text = st.text_area("MV01 输入 JSON", value=input_default, height=240)
mv01_input, mv01_error = parse_json(mv01_text)
if mv01_error:
    st.warning(mv01_error)

if st.button("▶ 从 MV01 开始执行", type="primary"):
    pipeline_runner.run_step("MV01", mv01_input)
    st.rerun()

st.divider()

for step in MV_STEPS:
    if step["id"] != "MV01" and not gate_manager.can_run(step["id"]):
        st.info(f"{step['id']} 需等待上一环节审核通过。")
    render_step(step, mv01_input, not bool(mv01_error))
