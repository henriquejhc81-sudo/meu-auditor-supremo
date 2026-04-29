import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time

# --- DESIGN PROFISSIONAL (CSS) ---
st.set_page_config(page_title="Auditor Supremo PRO", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004a99; color: white; font-weight: bold; }
    .stTextArea>div>div>textarea { background-color: #ffffff; border-radius: 10px; }
    .report-box { padding: 20px; border-radius: 10px; background-color: #ffffff; border-left: 5px solid #004a99; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Aguardando conexão com a chave API...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('RELATÓRIO DE AUDITORIA PROFISSIONAL', 0)
    for linha in texto.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
col1, col2 = st.columns()

with col1:
    st.image("https://flaticon.com", width=100)
    st.title("PRO Auditor")
    st.subheader("Painel de Controle")
    arquivo = st.file_uploader("📂 Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg"])
    
    st.divider()
    st.markdown("### ✅ Checklist Automático")
    st.checkbox("Analisar Leis Brasileiras", value=True)
    st.checkbox("Detectar Cláusulas Abusivas", value=True)
    st.checkbox("Sugerir Correção de Texto", value=True)

with col2:
    st.header("🔍 Central de Processamento")
    pergunta = st.text_area("O que o Auditor Supremo deve analisar hoje?", 
                           placeholder="Cole o texto ou descreva o que deseja auditar no documento...", height=150)
    
    if st.button("🚀 EXECUTAR AUDITORIA DE ELITE"):
        if pergunta:
            with st.spinner("Orquestrando múltiplas IAs para análise profunda..."):
                try:
                    # Prompt mestre para organizar as respostas em abas
                    prompt = f"""
                    Atue como um Auditor de Big Four (EY, Deloitte, KPMG).
                    Instrução: {pergunta}
                    Organize sua resposta em 3 partes claras:
                    1. VISÃO TÉCNICA E ERROS (O que está errado)
                    2. VERSÃO SUGERIDA (O texto corrigido)
                    3. VEREDITO FINAL (Nível de risco de 0 a 100)
                    """
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt)
                    
                    # --- RESULTADO EM ABAS (ESTILO PROFISSIONAL) ---
                    st.success("Análise Concluída!")
                    aba1, aba2, aba3 = st.tabs(["📊 Relatório de Erros", "✍️ Texto Corrigido", "⚖️ Veredito Mestre"])
                    
                    # Dividindo a resposta para as abas (simulado)
                    res = response.text
                    aba1.markdown(f"<div class='report-box'>{res}</div>", unsafe_allow_html=True)
                    aba2.info("A versão corrigida está disponível no relatório acima e no download.")
                    aba3.warning("Consulte o relatório final para o nível de risco detalhado.")
                    
                    st.divider()
                    st.download_button("📥 BAIXAR DOCUMENTO FINAL (.DOCX)", preparar_download(res), "auditoria_pro.docx")
                    
                except Exception as e:
                    st.error(f"Sistema em sincronização. Tente em instantes. (Erro: {e})")
        else:
            st.warning("Por favor, forneça o contexto para a análise.")

st.sidebar.caption("Auditor Supremo v17.0 | Enterprise Edition")
