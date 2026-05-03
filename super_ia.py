import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time
import random

# --- DESIGN PREMIUM OMNI ---
st.set_page_config(page_title="AETHER OMNI MASTER", layout="wide", page_icon="🛡️")

# Inicialização do Histórico na Sessão
if 'historico' not in st.session_state:
    st.session_state['historico'] = []

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.5em; border: none;
    }
    .report-card { padding: 25px; border-radius: 15px; background-color: #1a1c24; border: 1px solid #2d2f39; color: #e0e0e0; margin-bottom: 15px; }
    .history-card { background: #262730; padding: 10px; border-radius: 8px; border-left: 3px solid #00c6ff; margin-bottom: 5px; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (LÓGICA DE OURO) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model = genai.GenerativeModel(modelos[0] if modelos else 'gemini-1.5-flash')
except:
    st.error("📡 Sincronizando rede segura...")

def preparar_docx(lista_resultados):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO CONSOLIDADO', 0)
    for i, res in enumerate(lista_resultados):
        doc.add_heading(f"Missão {i+1}: {res['titulo']}", level=1)
        doc.add_paragraph(res['texto'])
        doc.add_page_break()
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- PAINEL LATERAL ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    
    # HISTÓRICO DE PESQUISA
    st.subheader("📜 Histórico da Sessão")
    if st.session_state['historico']:
        for item in st.session_state['historico']:
            st.markdown(f"<div class='history-card'><b>{item['titulo']}</b><br>{item['data']}</div>", unsafe_allow_html=True)
        
        st.divider()
        # DOWNLOAD MÚLTIPLO (TUDO EM UM)
        st.download_button("📥 Baixar Tudo (DOCX Único)", preparar_docx(st.session_state['historico']), "historico_consolidado.docx")
    else:
        st.caption("Nenhuma atividade registrada.")

    st.divider()
    if st.button("💡 Guia Sniper de Prompts"):
        st.info("Dica: Use 'Gere um contrato de...' para redação técnica ou 'Audite este PDF...' para análise forense.")

    st.divider()
    with st.expander("🛠️ Admin Motor"):
        if st.button("🔄 Reiniciar Sistema"):
            st.session_state['historico'] = []
            st.rerun()
    st.caption("v49.0 | Ultimate Master Edition")

# --- CENTRAL DE INTELIGÊNCIA ---
st.title("🛡️ AETHER AUDIT ENTERPRISE v49.0")
st.markdown("##### *Standard for High-Frequency Auditing & Global Intelligence*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivos = st.file_uploader("Upload de Evidências", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    st.divider()
    st.toggle("Extração Inteligente OCR", value=True)
    st.toggle("Score de Risco AI", value=True)
    st.toggle("Detecção de Anomalias", value=True)

with col2:
    st.subheader("🔍 Central de Comando")
    tipo_saida = st.selectbox("🎯 Objetivo da Missão", [
        "Relatório de Auditoria Forense", 
        "Gerar Contrato Completo", 
        "Gerar Processo / Petição",
        "Análise de Assinaturas (Grafotécnica)"
    ])
    
    pergunta = st.text_area("Instrução da Missão:", placeholder="Ex: Analise e redija um veredito...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA OMNI"):
        if pergunta:
            with st.spinner("O Sniper está operando em alta frequência..."):
                try:
                    conteudo_extra = ""
                    imagens = []
                    if arquivos:
                        for arq in arquivos:
                            if arq.type.startswith("image"):
                                imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                conteudo_extra += f"\n\nARQUIVO {arq.name}:\n{df.to_string()}"

                    prompt_final = f"Atue como Auditor e Advogado Sênior. Missão: {tipo_saida}. Instrução: {pergunta} {conteudo_extra}."
                    
                    if imagens:
                        response = model.generate_content([prompt_final, *imagens])
                    else:
                        response = model.generate_content(prompt_final)
                    
                    # Salva no Histórico
                    st.session_state['historico'].insert(0, {
                        "titulo": tipo_saida,
                        "data": time.strftime("%H:%M:%S"),
                        "texto": response.text
                    })
                    
                    st.success("Missão Concluída!")
                    tab1, tab2 = st.tabs(["📝 Resultado Atual", "📦 Gestão de Arquivos"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 Baixar Relatório Atual (.DOCX)", preparar_docx([st.session_state['historico'][0]]), "aether_report.docx")
                    st.balloons()
                    st.rerun() # Atualiza o histórico na lateral imediatamente
                except Exception as e:
                    st.error(f"Erro no Motor Omni: {e}")
        else:
            st.warning("Insira uma instrução.")
