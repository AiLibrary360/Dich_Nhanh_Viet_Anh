import streamlit as st
from googletrans import Translator
import openai
import requests

st.set_page_config(page_title="🌍 Dịch Việt → Anh - Ai-Library360", layout="centered")

st.markdown("## 🤖 Ai-Library360 - Ứng dụng Dịch tiếng Việt → tiếng Anh")
st.markdown("Chọn công cụ dịch: Google Translate, OpenAI ChatGPT hoặc OpenRouter GPT")

if "history" not in st.session_state:
    st.session_state.history = []

text_input = st.text_area("📝 Nhập văn bản tiếng Việt cần dịch:")

engine = st.selectbox("📌 Chọn công cụ dịch:", ["Google Translate", "OpenAI ChatGPT", "OpenRouter GPT"])

# Nhập API key nếu cần
openai_api_key = ""
openrouter_api_key = ""

if engine == "OpenAI ChatGPT":
    openai_api_key = st.text_input("🔑 Nhập OpenAI API Key:", type="password")
elif engine == "OpenRouter GPT":
    openrouter_api_key = st.text_input("🔑 Nhập OpenRouter API Key:", type="password")

def translate_with_openrouter(text, api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Bạn là trợ lý dịch thuật, dịch từ tiếng Việt sang tiếng Anh."},
            {"role": "user", "content": text}
        ]
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    else:
        raise Exception(f"Lỗi API OpenRouter: {response.status_code} {response.text}")

if st.button("🔁 Dịch"):
    if not text_input.strip():
        st.warning("⚠️ Vui lòng nhập văn bản để dịch.")
    else:
        try:
            if engine == "Google Translate":
                translator = Translator()
                result = translator.translate(text_input, src='vi', dest='en')
                translated_text = result.text

            elif engine == "OpenAI ChatGPT":
                if not openai_api_key:
                    st.warning("⚠️ Vui lòng nhập OpenAI API Key.")
                    st.stop()
                openai.api_key = openai_api_key
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Bạn là trợ lý dịch thuật, dịch từ tiếng Việt sang tiếng Anh."},
                        {"role": "user", "content": text_input}
                    ]
                )
                translated_text = response['choices'][0]['message']['content'].strip()

            else:  # OpenRouter GPT
                if not openrouter_api_key:
                    st.warning("⚠️ Vui lòng nhập OpenRouter API Key.")
                    st.stop()
                translated_text = translate_with_openrouter(text_input, openrouter_api_key)

            st.success("✅ Bản dịch:")
            st.markdown(f"**{translated_text}**")

            # Lưu vào lịch sử
            st.session_state.history.append({
                "source": text_input,
                "translated": translated_text,
                "engine": engine
            })

        except Exception as e:
            st.error(f"❌ Lỗi khi dịch: {e}")

if st.session_state.history:
    st.markdown("---")
    st.subheader("🕘 Lịch sử dịch")
    for i, item in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"Đoạn #{i} ({item['engine']})"):
            st.markdown(f"**Tiếng Việt:** {item['source']}")
            st.markdown(f"**Tiếng Anh:** {item['translated']}")

st.markdown("---")
st.markdown("### ☕ MỜI MÌNH LY CAFE NHÉ")
st.markdown("""
- 💳 **VCB:** `0121001367936`  
- 👤 **Chủ TK:** NGUYEN HOANG
- 📱 **Zalo:** [0933 314 451](https://zalo.me/0933314451)
- 📧 **Email:** [stephane.hoangnguyen@gmail.com](mailto:stephane.hoangnguyen@gmail.com)
""")
st.markdown("<center>🧠 Powered by Ai-Library360</center>", unsafe_allow_html=True)
