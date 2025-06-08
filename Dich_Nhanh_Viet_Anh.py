import streamlit as st
import os
from googletrans import Translator
import openai
import requests
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ROUTER_API_KEY = os.getenv("ROUTER_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Cấu hình các API
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Streamlit UI
st.set_page_config(page_title="AI-Library360 Translator", page_icon="🌐")
st.title("🌐 AI-Library360 Translator")

# Sidebar
with st.sidebar:
    st.markdown("### 🧠 Chọn mô hình dịch")
    api_choice = st.selectbox("🔗 Nguồn dịch", ["Google Translate", "OpenAI GPT", "OpenRouter", "Gemini"])
    st.markdown("### 🔄 Chiều dịch")
    direction = st.radio("Dịch từ:", ["Việt → Anh", "Anh → Việt"])

    st.markdown("---")
    st.markdown("### ☕ Thông tin ủng hộ")
    st.markdown("- 💸 **VCB 0121001367936**  \nCTK: NGUYEN HOANG")
    st.markdown("- 📱 Zalo: 0933314451")
    st.markdown("- 📧 Mail: stephane.hoangnguyen@gmail.com")

# Thiết lập ngôn ngữ
src_lang, tgt_lang = ("vi", "en") if direction == "Việt → Anh" else ("en", "vi")

# Nhập liệu
input_text = st.text_area("✍️ Nhập văn bản cần dịch", height=150)

if "history" not in st.session_state:
    st.session_state.history = []

# Các hàm dịch
def translate_google(text, src, tgt):
    translator = Translator()
    result = translator.translate(text, src=src, dest=tgt)
    return result.text

def translate_openai(text, src, tgt):
    prompt = f"Dịch từ {src} sang {tgt}: {text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def translate_openrouter(text, src, tgt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {ROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"Dịch từ {src} sang {tgt}: {text}"}]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"].strip()

def translate_gemini(text, src, tgt):
    prompt = f"Dịch từ {src} sang {tgt}: {text}"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

# Xử lý dịch
translated_text = ""
if st.button("📤 Dịch ngay"):
    if not input_text.strip():
        st.warning("⚠️ Vui lòng nhập nội dung để dịch.")
    else:
        try:
            if api_choice == "Google Translate":
                translated_text = translate_google(input_text, src_lang, tgt_lang)
            elif api_choice == "OpenAI GPT":
                translated_text = translate_openai(input_text, src_lang, tgt_lang)
            elif api_choice == "OpenRouter":
                translated_text = translate_openrouter(input_text, src_lang, tgt_lang)
            elif api_choice == "Gemini":
                translated_text = translate_gemini(input_text, src_lang, tgt_lang)

            st.success("✅ Đã dịch:")
            st.text_area("📝 Kết quả", value=translated_text, height=150)

            # Lưu lịch sử
            st.session_state.history.insert(0, {
                "input": input_text,
                "output": translated_text,
                "src": src_lang,
                "tgt": tgt_lang,
                "api": api_choice
            })
        except Exception as e:
            st.error(f"❌ Lỗi: {str(e)}")

# Hiển thị lịch sử
if st.session_state.history:
    with st.expander("🕘 Lịch sử dịch gần đây"):
        for item in st.session_state.history[:10]:
            st.markdown(f"**[{item['api']}] {item['src']} → {item['tgt']}**")
            st.markdown(f"🔹 Gốc: {item['input']}")
            st.markdown(f"🔸 Dịch: {item['output']}")
            st.markdown("---")
