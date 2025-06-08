import streamlit as st
from googletrans import Translator
import openai
import requests

# Hàm gọi OpenAI GPT
def call_openai_api(text, target_lang):
    openai_key = st.session_state.get("OPENAI_API_KEY", "")
    if not openai_key:
        return "Vui lòng nhập OpenAI API Key!"
    openai.api_key = openai_key
    prompt = f"Translate the following text to {target_lang}:\n{text}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Lỗi OpenAI API: {e}"

# Hàm gọi Google Gemini (giả lập, bạn thay bằng code thật)
def call_gemini_api(text, target_lang):
    gemini_key = st.session_state.get("GEMINI_API_KEY", "")
    if not gemini_key:
        return "Vui lòng nhập Google Gemini API Key!"
    # TODO: Thêm gọi API Gemini thật ở đây
    return f"[Gemini] Dịch '{text}' sang {target_lang}"

# Hàm gọi OpenRouter API GPT4
def call_openrouter_api(text, target_lang):
    router_key = st.session_state.get("OPENROUTER_API_KEY", "")
    if not router_key:
        return "Vui lòng nhập OpenRouter API Key!"
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {router_key}",
        "Content-Type": "application/json"
    }
    prompt = f"Translate the following text to {target_lang}:\n{text}"
    json_data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
    }
    try:
        response = requests.post(url, headers=headers, json=json_data)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Lỗi OpenRouter API: {e}"

def main():
    st.title("Dịch Nhanh Việt ↔ Anh - Gemini + GPT + OpenRouter + Google Translate")
    st.markdown("Nhập API key bên dưới để sử dụng GPT, Gemini và OpenRouter")

    # Nhập API Key
    openai_key = st.text_input("OpenAI API Key", type="password", key="openai_input")
    gemini_key = st.text_input("Google Gemini API Key", type="password", key="gemini_input")
    openrouter_key = st.text_input("OpenRouter API Key", type="password", key="openrouter_input")

    # Lưu API key vào session_state
    if openai_key:
        st.session_state["OPENAI_API_KEY"] = openai_key
    if gemini_key:
        st.session_state["GEMINI_API_KEY"] = gemini_key
    if openrouter_key:
        st.session_state["OPENROUTER_API_KEY"] = openrouter_key

    # Chọn chiều dịch
    lang_dir = st.selectbox("Chọn chiều dịch", ["Việt -> Anh", "Anh -> Việt"])

    # Chọn API dịch
    api_choice = st.selectbox("Chọn API dịch", [
        "Google Translate (Không cần API key)",
        "OpenAI GPT",
        "Google Gemini",
        "OpenRouter GPT4"
    ])

    text = st.text_area("Nhập văn bản cần dịch", height=150)

    if st.button("Dịch"):
        if not text.strip():
            st.warning("Vui lòng nhập văn bản cần dịch!")
        else:
            target_lang = "en" if lang_dir == "Việt -> Anh" else "vi"

            if api_choice == "Google Translate (Không cần API key)":
                translator = Translator()
                try:
                    translated = translator.translate(text, dest=target_lang).text
                    st.success(translated)
                    result = translated
                except Exception as e:
                    st.error(f"Lỗi dịch với Google Translate: {e}")
                    result = ""

            elif api_choice == "OpenAI GPT":
                result = call_openai_api(text, target_lang)
                st.success(result)

            elif api_choice == "Google Gemini":
                result = call_gemini_api(text, target_lang)
                st.success(result)

            elif api_choice == "OpenRouter GPT4":
                result = call_openrouter_api(text, target_lang)
                st.success(result)

            # Lưu lịch sử dịch
            history = st.session_state.get("history", [])
            history.append({
                "input": text,
                "output": result,
                "api": api_choice,
                "lang": lang_dir
            })
            st.session_state["history"] = history

    # Hiển thị lịch sử dịch (10 mục gần nh
