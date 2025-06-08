# 🚀 Hướng dẫn cài đặt AI-Library360 Translator

Ứng dụng dịch nhanh Việt ↔ Anh sử dụng Google Translate, OpenAI GPT và OpenRouter API. Giao diện bằng Streamlit.

---

## 🛠️ Thiết lập cục bộ bằng Conda

### 1. Tải mã nguồn từ GitHub

```bash
git clone https://github.com/AiLibrary360/Dich_Nhanh_Viet_Anh.git
cd Dich_Nhanh_Viet_Anh
conda create -n ai360 python=3.10 -y
conda activate ai360
pip install -r requirements.txt
pip install google-generativeai
streamlit run Dich_Nhanh_Viet_Anh.py
