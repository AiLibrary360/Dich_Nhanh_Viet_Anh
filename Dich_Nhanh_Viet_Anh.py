import streamlit as st
from googletrans import Translator
import openai
import requests
from dotenv import load_dotenv
import os
import io

load_dotenv()

st.set_page_config(page_title="Ai-Library360 Quick Translator", layout="wide", page_icon="🌐")

# Custom CSS
st.markdown(
    """
    <style>
    .block-container {
        padding: 1.5rem 3rem;
        max-width: 900px;
    }
    .stTextInput>div>div>input {
        font-size: 1rem;
        padding: 8px 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar cấu hình + Thông tin liên hệ luôn nằm trong sidebar
with st.sidebar:
    st.header("⚙️ Cấu hình API & Dịch vụ")
    openai_api_key = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY"), type="password")
    router_api_key = st.text_input("OpenRouter API Key", value=os.getenv("ROUTER_API_KEY"), type="password")
    gemini_api_key = st.text_input("Google Gemini API Key", value=os.getenv("GEMINI_API_KEY"), type="password")

    service = st.selectbox("Chọn dịch vụ dịch", ["Google Translate", "OpenAI GPT", "OpenRouter GPT", "Google Gemini"])
    translate_dir = st.radio("Chọn chiều dịch", ("Việt → Anh", "Anh → Việt"))

    st.markdown("---")  # dòng phân cách

    st.markdown(
        """
        <div style="
            background-color:#111; 
            padding: 12px 15px; 
            border-radius: 12px; 
            border: 1px solid #444; 
            color:#ccc; 
            font-size: 0.9rem; 
            line-height: 1.4;
            ">
            <b style="color:#fff;">Ai-Library360</b> ☕<br>
            MỜI MÌNH LY CAFE NHÉ<br>
            🏦 VCB 0121001367936<br>
            🙋‍♂️ NGUYEN HOANG<br>
            📱 Zalo: 0933314451<br>
            📧 Mail: stephane.hoangnguyen@gmail.com
        </div>
        """,
        unsafe_allow_html=True,
    )

# Tiêu đề và hướng dẫn
with st.container():
    st.title("🌐 Ai-Library360 Quick Translator")
    st.markdown("**Dịch nhanh Việt - Anh, Anh - Việt với nhiều dịch vụ AI**")
    st.markdown("*Bạn có thể chọn dịch vụ: Google Translate, OpenAI GPT, OpenRouter GPT hoặc Google Gemini.*")
    st.caption("Nhập API key cho từng dịch vụ trong phần bên trái.")

# Chia 2 cột nhập và kết quả
col1, col2 = st.columns([1, 1])

with col1:
    text_input = st.text_area("Nhập đoạn văn cần dịch:", height=250)

with col2:
    st.markdown("### Kết quả dịch")
    result_container = st.empty()

def call_gemini_api(api_key, prompt_text):
    url = "https://generativelanguage.googleapis.com/v1beta2/models/chat-bison-001:generateMessage"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": {
            "messages": [{"author": "user", "content": prompt_text}]
        },
        "temperature": 0.3,
        "maxTokens": 1000,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]
    else:
        raise Exception(f"Gemini API error {response.status_code}: {response.text}")

# Nút dịch
if st.button("🚀 Dịch ngay"):
    if not text_input.strip():
        st.warning("Vui lòng nhập đoạn văn cần dịch trước khi dịch.")
    else:
        with st.spinner("Đang dịch..."):
            try:
                if translate_dir == "Việt → Anh":
                    src_lang, tgt_lang = "vi", "en"
                else:
                    src_lang, tgt_lang = "en", "vi"

                translator = Translator()
                result = ""

                if service == "Google Translate":
                    result = translator.translate(text_input, src=src_lang, dest=tgt_lang).text

                elif service == "OpenAI GPT":
                    if not openai_api_key:
                        st.error("Vui lòng nhập OpenAI API Key ở sidebar!")
                    else:
                        openai.api_key = openai_api_key
                        prompt = f"Translate this text from {src_lang} to {tgt_lang}: {text_input}"
                        response = openai.ChatCompletion.create(
                            model="gpt-4o-mini",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.3,
                            max_tokens=1000,
                        )
                        result = response.choices[0].message.content.strip()

                elif service == "OpenRouter GPT":
                    if not router_api_key:
                        st.error("Vui lòng nhập OpenRouter API Key ở sidebar!")
                    else:
                        url = "https://openrouter.ai/api/v1/chat/completions"
                        headers = {
                            "Authorization": f"Bearer {router_api_key}",
                            "Content-Type": "application/json"
                        }
                        prompt = f"Translate this text from {src_lang} to {tgt_lang}: {text_input}"
                        data = {
                            "model": "gpt-4o-mini",
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.3,
                            "max_tokens": 1000
                        }
                        res = requests.post(url, headers=headers, json=data)
                        if res.status_code == 200:
                            result = res.json()["choices"][0]["message"]["content"].strip()
                        else:
                            st.error(f"OpenRouter API error: {res.status_code} {res.text}")

                elif service == "Google Gemini":
                    if not gemini_api_key:
                        st.error("Vui lòng nhập Google Gemini API Key ở sidebar!")
                    else:
                        prompt = f"Translate this text from {src_lang} to {tgt_lang}: {text_input}"
                        result = call_gemini_api(gemini_api_key, prompt)

                if result:
                    result_container.success(result)

                    # Lưu vào session_state.history
                    if "history" not in st.session_state:
                        st.session_state.history = []

                    st.session_state.history.insert(0, {
                        "direction": translate_dir,
                        "service": service,
                        "input": text_input.strip(),
                        "output": result.strip()
                    })

                    # Giữ 10 bản gần nhất
                    st.session_state.history = st.session_state.history[:10]

            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")

# Lịch sử dịch gần đây
if "history" in st.session_state and st.session_state.history:
    st.markdown("### 🕘 Lịch sử dịch gần đây")
    for item in st.session_state.history:
        st.markdown(f"**[{item['direction']}] {item['service']}**\n\n📝 `{item['input']}`\n➡️ `{item['output']}`\n---")

    # Tạo file txt để tải
    history_text = ""
    for i, item in enumerate(st.session_state.history, start=1):
        history_text += (
            f"[{i}] {item['direction']} - {item['service']}\n"
            f"Input: {item['input']}\n"
            f"Output: {item['output']}\n\n"
        )

    history_bytes = io.BytesIO(history_text.encode("utf-8"))
    st.download_button(
        label="📥 Tải lịch sử dưới dạng TXT",
        data=history_bytes,
        file_name="lich_su_dich.txt",
        mime="text/plain"
    )
