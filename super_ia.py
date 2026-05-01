import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN OMNISCIENCE PRO ---
st.set_page_config(page_title="AETHER OMNI", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    [data-testid="stSidebar"] { background-color: #1a1c24; }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; }
    </style>
    """, unsafe_allow_html=True)

# --- SMART CONNECTION (END OF 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # It asks Google: "Which models can I use?"
    live_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Choose the first one (usually gemini-1.5-flash or gemini-pro)
    model = genai.GenerativeModel(modelos_vivos)
except Exception as e:
    st.error(f"📡 Omni Network: Synchronizing secure connection...")

def prepare_download(text):
    doc = Document()
    doc.add_heading('AETHER OMNI - OFFICIAL REPORT', 0)
    for line in text.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    if st.button("🔄 Restart Engine"):
        st.rerun()
    
    st.divider()
    with st.expander("🎯 SNIPER ARSENAL", expanded=True):
        st.info("• Table Extraction\n• Contract Analysis\n• Risk Score")
    
    st.divider()
    st.subheader("📜 Mission History")
    st.caption("v40.2 | Omniscience Edition Active")

# --- MAIN INTERFACE ---
st.title("🛡️ Aether Omni")
st.selectbox("Operation Mode", ["Contract & PDF Audit", "Financial Analysis", "Computer Vision"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Multimodal Input")
    arquivo = st.file_uploader("Document Upload", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.divider()
    st.write("📊 **System Status:** Operational")

with col2:
    st.subheader("🔍 Sniper Central")
    pergunta = st.text_area("What should Aether Omni process now?", placeholder="Ex: Analyze this document...", height=150)
    
    if st.button("🚀 EXECUTE OMNI SCAN"):
        if pergunta:
            with st.spinner("Connecting to the Sniper Arsenal..."):
                try:
                    time.sleep(1)
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([pergunta, Image.open(arquivo)])
                    else:
                        response = model.generate_content(pergunta)
                    
                    st.success("Mission Accomplished!")
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 DOWNLOAD REPORT", preparar_download(response.text), "aether_report.docx")
                except Exception as e:
                    st.error(f"Omni Network Error: {e}. Disable Chrome translator.")
        else:
            st.warning("Enter a question.")
