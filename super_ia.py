import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import os

# --- DESIGN AETHER ---
st.set_page_config(page_title="AETHER AUDIT", layout="wide", page_icon="🛡️")

# Estilo para o botão de reboot ficar discreto
st.markdown("""
    <style>
    .reboot-btn { color: #555; font-size: 10px; text-align: center; margin-top: 50px; opacity: 0.5; }
    .reboot-btn:hover { opacity: 1; color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (ANTI-404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Comando que força a versão estável na nuvem
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
except:
    st.error("Conectando ao Cérebro IA...")

def gerar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO', 0)
    for linha in texto.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.title("🛡️ AETHER AUDIT")

col1, col2 = st.columns(2)

with col1:
    arquivo = st.file_uploader("Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.toggle("Modo Profundo", value=True)
    
    # BOTÃO DE REBOOT DISCRETO NA LATERAL
    with st.sidebar:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("🔄 Reiniciar Sistema", help="Clique aqui se o erro 404 persistir"):
            st.rerun()
        st.caption("v26.5 | Emergency Reboot Active")

with col2:
    pergunta = st.text_area("O que devo analisar?", placeholder="Ex: Analise este contrato...", height=150)
    
    if st.button("🚀 INICIAR VARREDURA"):
        if pergunta:
            with st.spinner("Varrendo dados..."):
                try:
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([pergunta, img])
                    else:
                        # Processamento de texto da v10 estável
                        conteudo = arquivo.read().decode("utf-8", errors="ignore") if arquivo else ""
                        final_prompt = f"{pergunta}\n\nDADOS DO ARQUIVO: {conteudo}"
                        response = model.generate_content(final_prompt)
                    
                    st.success("Concluído!")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR WORD", gerar_docx(response.text), "aether_report.docx")
                except Exception as e:
                    st.error(f"Erro: {e}. Use o botão Reiniciar na lateral se necessário.")
        else:
            st.warning("Digite uma instrução.")
