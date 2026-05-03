import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN DE ELITE (AETHER BLACK THEME) ---
st.set_page_config(page_title="AETHER AUDIT | Global Enterprise", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 8px; font-weight: bold; height: 3.5em; 
    }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; color: #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA COM RESET DE VERSÃO ---
try:
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("Chave API não encontrada nos Secrets!")
    else:
        # Forçamos a configuração global a ignorar betas
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        
        # PROTOCOLO DE LIMPEZA: Criamos o modelo chamando explicitamente a versão de produção
        model = genai.GenerativeModel(
            model_name='models/gemini-1.5-flash', # Caminho completo de produção
        )
except Exception as e:
    st.error(f"Erro de Configuração: {e}")

def preparar_download(texto, titulo):
    doc = Document()
    doc.add_heading(titulo, 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.title("🛡️ AETHER AUDIT ENTERPRISE v45.4")
st.markdown("##### *Standard for High-Frequency Auditing & Global Intelligence*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivo = st.file_uploader("Upload de Evidências", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.divider()
    
    st.markdown("### ⚙️ Sniper Config")
    st.toggle("Extração Inteligente de Tabelas", value=True)
    st.toggle("Score de Risco Automático", value=True)
    st.toggle("Detecção de Anomalias (Assinaturas/Forense)", value=True)
    st.toggle("Cruzamento SPED/XML", value=False)

with col2:
    st.subheader("🔍 Central de Inteligência")
    tipo_saida = st.selectbox("🎯 Ação Pós-Auditoria (Filtro)", [
        "Apenas Relatório de Auditoria", 
        "Auditoria + Gerar Contrato Corrigido", 
        "Auditoria + Gerar Petição/Processo",
        "Análise Grafotécnica (Assinaturas)"
    ])
    
    pergunta = st.text_area("Instrução para a IA:", placeholder="Ex: Analise este documento...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Conectando ao Arsenal Aether..."):
                try:
                    conteudo_extra = ""
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    prompt_final = f"Atue como AUDITOR SUPREMO e ADVOGADO SÊNIOR. MISSÃO: {tipo_saida}. Instrução: {pergunta} {conteudo_extra}."
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_final, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_final)
                    
                    st.success("Análise Concluída!")
                    tab1, tab2 = st.tabs(["📝 Relatório Inteligente", "📥 Exportar"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 BAIXAR DOCUMENTO (.DOCX)", preparar_download(response.text, tipo_saida), "aether_result.docx")
                except Exception as e:
                    st.error(f"Erro Crítico: {e}")
        else:
            st.warning("Aguardando comando.")

with st.sidebar:
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    st.caption("AETHER AUDIT v45.4 | Master Edition")
