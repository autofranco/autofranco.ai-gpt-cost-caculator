import streamlit as st
from calculate import run

st.title('ChatGPT 收費計算機')

# 初始化 session_state（只會執行一次）
st.session_state.setdefault("daily_interactions", 100)
st.session_state.setdefault("model_name", "gpt-4.1")
st.session_state.setdefault("input_tokens", 2000)
st.session_state.setdefault("output_tokens", 100)
st.session_state.setdefault("cached_tokens", 0)
st.session_state.setdefault("web_search_content_size", "none")
st.session_state.setdefault("code_interpreter_used", False)
st.session_state.setdefault("file_search_storage", 0)

with st.container(border=True):
    # model name - option input UI
    st.selectbox(
        "使用哪個 GPT 模型?",
        (
            "gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-4.5-preview",
            "gpt-4o", "gpt-4o-audio-preview", "gpt-4o-realtime-preview",
            "gpt-4o-mini", "gpt-4o-mini-audio-preview", "gpt-4o-mini-realtime-preview",
            "o1", "o1-pro", "o3", "o4-mini", "o3-mini", "o1-mini",
            "codex-mini-latest", "gpt-4o-mini-search-preview", "gpt-4o-search-preview",
            "computer-use-preview", "gpt-image-1-text", "gpt-image-1-image",
            "chatgpt-4o-latest", "gpt-4-turbo", "gpt-4", "gpt-4-32k",
            "gpt-3.5-turbo", "gpt-3.5-turbo-instruct", "gpt-3.5-turbo-16k-0613",
            "davinci-002", "babbage-002"
        ),
        key="model_name",
        index=0,
        placeholder="選擇 GPT 模型",
    )

    # Input fields
    st.number_input("每天傳送幾則用戶訊息", value=100, step=1, key="daily_interactions")
    st.number_input("每則用戶訊息使用多少 input token", value=2000, step=1, key="input_tokens")
    st.number_input("每則 AI 回覆使用多少 output token", value=100, step=1, key="output_tokens")
    st.number_input("每則 AI 回覆使用多少 cached token", value=0, step=1, key="cached_tokens")

    st.slider("知識庫大小 (GB)", 0, 100, 0, key="file_search_storage")
    st.select_slider("網路搜索內容規模", options=["none", "low", "medium", "high"], value="none", key="web_search_content_size")
    st.toggle("是否會用到執行程式碼", key="code_interpreter_used")

# 計算結果並顯示在下方
result = run(
    daily_interactions=st.session_state.daily_interactions,
    model_name=st.session_state.model_name,
    input_tokens=st.session_state.input_tokens,
    output_tokens=st.session_state.output_tokens,
    cached_tokens=st.session_state.cached_tokens,
    web_search_content_size=st.session_state.web_search_content_size,
    code_interpreter_used=st.session_state.code_interpreter_used,
    file_search_storage=st.session_state.file_search_storage
)

st.markdown("---")
st.subheader("💵 預估成本")
st.write("新台幣成本：", result["total_cost_ntd"])
