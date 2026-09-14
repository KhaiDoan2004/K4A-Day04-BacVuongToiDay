from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

from chat import run_model_tool_loop, trim_history
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import build_artifact_version


ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = ROOT / "artifacts"
load_lab_env(ROOT)

st.set_page_config(
    page_title="IT Helpdesk AI Agent — Northstar Labs",
    page_icon="🛠️",
    layout="wide",
)

st.title("🛠️ IT Helpdesk AI Agent — Northstar Labs")
st.caption("Prompt Engineering & Structured Tool Calling Studio (with 4 Bonus Tools)")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    provider_name = st.selectbox("Provider", ["openrouter", "openai", "anthropic", "gemini"], index=0)
    version_label = st.selectbox("Artifact Version", ["v3", "v2", "v1", "v0"], index=0)
    model_override = st.text_input("Custom Model (optional)", value="", placeholder="e.g. gpt-4o-mini")

    prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"

    if prompt_path.exists() and tools_path.exists():
        version_info = build_artifact_version(version_label, prompt_path, tools_path)
        st.markdown(f"**Version Label:** `{version_info.version}`")
        st.markdown(f"**Prompt Hash:** `{version_info.prompt_hash[:8]}`")
        st.markdown(f"**Tools Hash:** `{version_info.tools_hash[:8]}`")

    with st.expander("Active Tools List", expanded=False):
        declarations = load_tool_declarations(tools_path)
        for d in declarations:
            st.markdown(f"- **`{d['name']}`**: {d.get('description', '')[:70]}...")

    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.rerun()

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Display conversation messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tool_events" in msg and msg["tool_events"]:
            with st.expander(f"🔧 Tool Traces ({len(msg['tool_events'])} calls)", expanded=False):
                for idx, event in enumerate(msg["tool_events"], start=1):
                    st.markdown(f"**Call {idx}: `{event.get('tool')}`**")
                    st.json({"args": event.get("args"), "result": event.get("result")})

# User input
if user_query := st.chat_input("Nhập câu hỏi hỗ trợ kỹ thuật (VD: kiểm tra mạng Hà Nội, kiểm tra phòng MR-101)..."):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Đang suy luận và gọi tools..."):
            try:
                system_prompt = prompt_path.read_text(encoding="utf-8")
                declarations = load_tool_declarations(tools_path)
                provider = make_provider(provider_name)
                tools_schema = to_openai_tools(declarations)

                recent_history = trim_history(st.session_state.conversation_history, window=5)
                full_messages = [
                    {"role": "system", "content": system_prompt},
                    *recent_history,
                    {"role": "user", "content": user_query},
                ]

                result = run_model_tool_loop(
                    provider=provider,
                    messages=full_messages,
                    tools=tools_schema,
                    model=model_override.strip() or None,
                    max_tool_rounds=4,
                )

                reply_text = result.get("assistant_text", "")
                tool_events = result.get("tool_events", [])

                st.markdown(reply_text)
                if tool_events:
                    with st.expander(f"🔧 Tool Traces ({len(tool_events)} calls)", expanded=True):
                        for idx, event in enumerate(tool_events, start=1):
                            st.markdown(f"**Call {idx}: `{event.get('tool')}`**")
                            st.json({"args": event.get("args"), "result": event.get("result")})

                # Record in session
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply_text,
                    "tool_events": tool_events,
                })
                st.session_state.conversation_history.append({"role": "user", "content": user_query})
                st.session_state.conversation_history.append({"role": "assistant", "content": reply_text})

            except Exception as exc:
                err_msg = f"⚠️ Lỗi thực thi: {type(exc).__name__} - {str(exc)}"
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})
