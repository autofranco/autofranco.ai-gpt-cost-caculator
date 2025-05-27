import streamlit as st
from calculate import model_list, get_input_price_per_M, get_output_price_per_M, get_cached_price_per_M, get_web_search_price_per_K, get_code_run_price_per_session, get_file_search_price_per_K, get_file_search_storage_GB_per_day, get_usd_to_ntd
import pandas as pd
import streamlit.components.v1 as components # 導入 components 模組

st.set_page_config(page_title="ChatGPT 收費計算機", layout="wide")
# Reducing whitespace on the top of the page
st.markdown("""
<style>
.block-container
{
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-top: 1rem;
    margin-bottom: 3rem;
}
</style>
""", unsafe_allow_html=True)

# 定義你從網站獲取的完整的 HTML 片段
counter_html = """
<div style="
    display: flex; /* 使用 Flexbox 讓內容在同一行 */
    align-items: center; /* 垂直居中對齊 */
    height: 24px; /* 設定整個容器的高度 */
    background-color: #101216;
">
    <span style="
        color: white; /* 文字顏色設為白色 */
        font-size: 12px; /* 調整字體大小，可以根據圖片大小微調 */
        line-height: 24px; /* 行高與容器高度一致，幫助垂直對齊 */
        white-space: nowrap; /* 防止文字換行 */
    ">by <a href="https://www.youtube.com/@autofranco" target="_blank"
    style="
    margin-right: 30px;
    color: #0AFF2C;
    font-weight: bold;">Frankie全自動</a>造訪人次：</span>

    <div id="sfcn8y7ze3nr5bkt99dg8xd2j14k8t5u2es"></div>
    <script type="text/javascript" src="https://counter4.optistats.ovh/private/counter.js?c=n8y7ze3nr5bkt99dg8xd2j14k8t5u2es&down=async" async></script>
    <noscript><a href="https://www.freecounterstat.com" title="free counters for websites"><img src="https://counter4.optistats.ovh/private/freecounterstat.php?c=n8y7ze3nr5bkt99dg8xd2j14k8t5u2es" border="0" title="free counters for websites" alt="free counters for websites"></a></noscript>
</div>
"""

# 使用 components.html 嵌入這段 HTML
# height 和 scrolling 可以根據你的需求調整
components.html(counter_html, height=25, scrolling=False)
st.title('GPT收費試算')

# 初始化 session_state（只會執行一次）
st.session_state.setdefault("daily_interactions", 100)
st.session_state.setdefault("model_name", "gpt-4.1")
st.session_state.setdefault("input_tokens", 2000)
st.session_state.setdefault("output_tokens", 100)
st.session_state.setdefault("cached_tokens", 0)
st.session_state.setdefault("web_search_content_size", "none")
st.session_state.setdefault("code_interpreter_used", False)
st.session_state.setdefault("file_search_storage", 0)

# 輸入區
with st.sidebar:
    with st.container(border = True):
        # model name - option input UI
        st.selectbox("使用哪個 GPT 模型?", model_list, key="model_name", index=0, placeholder="選擇 GPT 模型")

        # Input fields
        st.number_input("每天傳送幾則用戶訊息", step=1, key="daily_interactions", min_value=1)
        st.number_input("每則用戶訊息使用多少 input token", step=1, key="input_tokens")
        st.number_input("每則 AI 回覆使用多少 output token", step=1, key="output_tokens")
        st.number_input("每則 AI 回覆使用多少 cached token", step=1, key="cached_tokens")
        st.slider("知識庫大小 (GB)", min_value=0, max_value=100, key="file_search_storage")
        st.select_slider("網路搜索內容規模", options=["none", "low", "medium", "high"], key="web_search_content_size")
        st.toggle("是否會用到執行程式碼", key="code_interpreter_used")

# 結果區
with st.container(border = True):
    daily_interactions=st.session_state.daily_interactions
    model_name=st.session_state.model_name
    input_tokens=st.session_state.input_tokens
    output_tokens=st.session_state.output_tokens
    cached_tokens=st.session_state.cached_tokens
    web_search_content_size=st.session_state.web_search_content_size
    code_interpreter_used=st.session_state.code_interpreter_used
    file_search_storage=st.session_state.file_search_storage
    
    input_cost_per_call = round(input_tokens * get_input_price_per_M(model_name) / 1000000 ,5)
    output_cost_per_call = round(output_tokens * get_output_price_per_M(model_name) / 1000000 ,5)
    cached_cost_per_call = round(cached_tokens * get_cached_price_per_M(model_name) / 1000000 ,5)
    web_search_cost_per_call = (get_web_search_price_per_K(model_name, web_search_content_size) / 1000)
    code_run_cost_per_call = get_code_run_price_per_session() if code_interpreter_used else 0
    file_search_cost_per_call = (get_file_search_price_per_K() / 1000) if file_search_storage >= 1 else 0
    call_cost_per_call = round(input_cost_per_call + output_cost_per_call + cached_cost_per_call + web_search_cost_per_call + code_run_cost_per_call + file_search_cost_per_call ,5)
    call_cost_per_day = round(daily_interactions * call_cost_per_call ,5)
    storage_cost_per_day = get_file_search_storage_GB_per_day(file_search_storage) 
    total_cost_per_day = call_cost_per_day + storage_cost_per_day
    
    

    # 計算結果並顯示在下方
    df = pd.DataFrame(
        {
            "動作": ["**+ input token**", #1
                   "**+ output token**", #2
                   "**+ cached token**", #3
                   "**+ 網路搜尋**", #4
                   "**+ 程式執行**", #5
                   "**+ 知識庫搜尋**", #6
                   "**= 單次執行成本**", #7
                   "**\* 每日訊息數**", #8
                   "**+ 知識庫儲存**", #9
                   "**= 每日成本**", #10
                   "**= 每月成本**"], #12
            "算式": [f"`{input_tokens}` 個input token * `{get_input_price_per_M(model_name)}/1M` ({model_name}定價) = 每次 `${input_cost_per_call}`", #1
                   f"`{output_tokens}` 個output token * `{get_output_price_per_M(model_name)}/1M` ({model_name}定價) = 每次 `${output_cost_per_call}`", #2 
                   f"`{cached_tokens}` 個cache token * `{get_cached_price_per_M(model_name)}/1M` ({model_name}定價) = 每次 `${cached_cost_per_call}`", #3 
                   f"每次 `${web_search_cost_per_call}` (only for: gpt-4.1, 4o, 4.1-mini, 4o-mini)", #4
                   f"每次 `${code_run_cost_per_call}`", #5
                   f"每次 `${file_search_cost_per_call}`", #6 
                   f"`${call_cost_per_call}`", #7 

                   f"\* `{daily_interactions}` = `${call_cost_per_day}`", #8
                   f"\+ `{file_search_storage}GB` * `$0.1/GB每天(<1GB免費)` = `${round(storage_cost_per_day, 5)}`", #9  <-- HARDCODE HERE
                   f"= `${round(total_cost_per_day,5)}`", #10 
                   f"= `{round(total_cost_per_day * 30, 5)}`USD = `{round(total_cost_per_day * 30 * get_usd_to_ntd(), 5)}`NTD"] #12
        }
    ).set_index('動作')
    st.metric(label="💵 每月預估成本", value=f"{round(total_cost_per_day * 30 * get_usd_to_ntd(), 5)}NTD")
    st.table(df)
    

pricing = pd.DataFrame(
    {
        "model": ["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano", "gpt-4.5-preview", "gpt-4o", "gpt-4o-audio-preview", "gpt-4o-realtime-preview", "gpt-4o-mini", "gpt-4o-mini-audio-preview", "gpt-4o-mini-realtime-preview", "o1", "o1-pro", "o3", "o4-mini", "o3-mini", "o1-mini", "codex-mini-latest", "gpt-4o-mini-search-preview", "gpt-4o-search-preview", "computer-use-preview", "gpt-image-1-text", "gpt-image-1-image", "chatgpt-4o-latest", "gpt-4-turbo", "gpt-4", "gpt-4-32k", "gpt-3.5-turbo", "gpt-3.5-turbo-instruct", "gpt-3.5-turbo-16k-0613", "davinci-002", "babbage-002"],
        "input": [2.0, 0.4, 0.1, 75.0, 2.5, 2.5, 5.0, 0.15, 0.15, 0.6, 15.0, 150.0, 10.0, 1.1, 1.1, 1.1, 1.5, 0.15, 2.5, 3.0, 5.0, 10.0, 5.0, 10.0, 30.0, 60.0, 0.5, 1.5, 3.0, 2.0, 0.4],
        "cached": [0.5, 0.1, 0.025, 37.5, 1.25, "-", 2.5, 0.075, "-", 0.3, 7.5, "-", 2.5, 0.275, 0.55, 0.55, 0.375, "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        "output": [8.0, 1.6, 0.4, 150.0, 10.0, 10.0, 20.0, 0.6, 0.6, 2.4, 60.0, 600.0, 40.0, 4.4, 4.4, 4.4, 6.0, 0.6, 10.0, 12.0, "-", 40.0, 15.0, 30.0, 60.0, 120.0, 1.5, 2.0, 4.0, 2.0, 0.4],
        "info" : [
                        "複雜推理、高準確性，適合學術研究、程式碼生成。",
                        "輕量、成本效益高、速度快，適合智慧客服、快速內容。",
                        "最輕量、極致成本效益，適合大規模、低延遲應用。",
                        "最新技術預覽，前沿功能，適合探索與測試。",
                        "原生多模態，即時語音、視覺。適合多模態交互應用。",
                        "音訊處理專注，語音辨識、合成。適合語音助理。",
                        "即時響應、極低延遲，適合即時對話、線上輔助。",
                        "輕量多模態、成本低速快。適合小型多模態應用。",
                        "成本效益語音處理，適合小型語音聊天。",
                        "成本效益即時響應，適合簡單即時翻譯。",
                        "通用基礎模型，適合中等文本任務，如內容生成、摘要。",
                        "'o1'專業版，處理複雜任務、大規模資料。適合專業內容分析。",
                        "平衡性能與成本，適合多種日常文本處理任務。",
                        "輕量級、成本效益高，適合大量基礎重複任務。",
                        "效率、成本控制，適合簡單文本生成分析。",
                        "高效能、低成本，適合基本文本任務、自動化。",
                        "輕量程式碼生成，程式碼補全、bug修復。",
                        "結合搜尋，提供即時資訊問答。",
                        "多模態與搜尋結合，綜合資訊查詢。",
                        "輔助電腦操作，自動化工作流程。",
                        "圖片文字提取，OCR，圖片內容分析。",
                        "圖片生成、創意設計。適合藝術創作。",
                        "最新旗艦多模態，高階AI能力應用。",
                        "長上下文、高速度、成本效益。適合大型文檔處理。",
                        "卓越推理、知識廣、解決複雜問題。適合高智能應用。",
                        "32k上下文，處理極長文本。適合法律審閱、文獻分析。",
                        "高效能、成本效益，適合聊天、摘要、問答。",
                        "指令微調優化，精確遵循指令。適合自動化任務。",
                        "16k上下文，處理中長文本。適合長文章。",
                        "早期通用模型，基礎內容創建、簡單程式碼。",
                        "早期基礎模型，成本低、速度快。適合簡單分類。"
                        ]
    }
)
pricing = pricing.astype(str)
st.write("**GPT model 定價**  (最後更新時間：2025/5月)")
st.table(pricing.set_index('model'))