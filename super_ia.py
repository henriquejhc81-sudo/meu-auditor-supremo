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

# Inicialização da Sessão
if 'historico' not in st.session_state:
    st.session_state['historico'] = []
if 'show_history' not in st.session_state:
    st.session_state['show_history'] = False

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

def preparar_docx(lista_resultados, unico=True):
    doc = Document()
    if unico:
        doc.add_heading('AETHER OMNI - DOCUMENTO INDIVIDUAL', 0)
        doc.add_paragraph(lista_resultados[-1]['texto'] if isinstance(lista_resultados, list) else lista_resultados)
    else:
        doc.add_heading('AETHER OMNI - RELATÓRIO CONSOLIDADO', 0)
        for res in lista_resultados:
            doc.add_heading(f"Missão: {res['titulo']} | Fonte: {res['fonte']}", level=1)
            doc.add_paragraph(res['texto'])
            doc.add_page_break()
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- PAINEL LATERAL ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    
    # BOTAO PARA MOSTRAR HISTORICO
    if st.button("📜 Ver Histórico de Missões"):
        st.session_state['show_history'] = not st.session_state['show_history']

    if st.session_state['show_history']:
        st.subheader("Histórico Recente")
        if st.session_state['historico']:
            for item in st.session_state['historico']:
                st.markdown(f"<div class='history-card'><b>{item['fonte']}</b><br>{item['titulo']} | {item['data']}</div>", unsafe_allow_html=True)
            st.divider()
            st.download_button("📥 Baixar Tudo (DOCX Único)", preparar_docx(st.session_state['historico'], unico=False), "historico_total.docx")
        else:
            st.caption("Nenhum registro encontrado.")

    st.divider()
    st.subheader("⚙️ Sniper Config")
    st.toggle("Extração Inteligente OCR", value=True)
    st.toggle("Score de Risco AI", value=True)
    st.toggle("Detecção de Anomalias", value=True)
    
    # FILTRO DE ACÃO ABAIXO DOS TOGGLES
    st.divider()
    st.subheader("⚡ Ação Imediata")
    acao_filtro = st.selectbox("Escolha o comportamento:", [
        "Apenas Auditoria Técnica",
        "Auditoria + Gerar Contrato Corrigido",
        "Auditoria + Gerar Processo Corrigido"
    ])

    st.divider()
    with st.expander("🛠️ Admin"):
        if st.button("🔄 Reiniciar Motor"):
            st.session_state['historico'] = []
            st.rerun()
    st.caption("v50.0 | Master Ultimate Edition")

# --- CENTRAL DE INTELIGÊNCIA ---
st.title("🛡️ AETHER AUDIT ENTERPRISE v50.0")
st.markdown("##### *Standard for High-Frequency Auditing & Global Compliance*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivos = st.file_uploader("Upload de Evidências", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    st.info("Envie arquivos para auditoria ou utilize a central para geração direta.")

with col2:
    st.subheader("🔍 Central de Comando")
    tipo_missao = st.selectbox("🎯 Objetivo da Missão", [
        "Auditoria Forense (Padrão)", 
        "Auditar e Corrigir Processo Judicial", 
        "Auditar e Corrigir Contrato",
        "Análise Grafotécnica de Assinaturas",
        "Gerar Documento do Zero"
    ])
    
    pergunta = st.text_area("Instruções específicas:", placeholder="Ex: Analise este documento e aplique as correções do filtro lateral...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA OMNI"):
        if pergunta or arquivos:
            with st.spinner("O Sniper está operando..."):
                try:
                    conteudo_extra = ""
                    imagens = []
                    nome_fonte = "Input de Texto"
                    
                    if arquivos:
                        nome_fonte = arquivos[0].name
                        for arq in arquivos:
                            if arq.type.startswith("image"):
                                imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                conteudo_extra += f"\n\nARQUIVO {arq.name}:\n{df.to_string()}"

                    prompt_final = f"""
                    Atue como Auditor Sênior e Advogado Sênior. 
                    MISSÃO: {tipo_missao}. 
                    AÇÃO REQUERIDA: {acao_filtro}.
                    INSTRUÇÃO DO USUÁRIO: {pergunta}
                    CONTEXTO DOS DADOS: {conteudo_extra}
                    
                    REQUISITOS: Se o filtro for 'Gerar Corrigido', forneça primeiro a auditoria e depois o texto completo corrigido sob as leis brasileiras.
                    """
                    
                    response = model.generate_content([prompt_final, *imagens]) if imagens else model.generate_content(prompt_final)
                    
                    # Salva no Histórico com nome da fonte
                    st.session_state['historico'].insert(0, {
                        "titulo": tipo_missao,
                        "fonte": nome_fonte,
                        "data": time.strftime("%H:%M:%S"),
                        "texto": response.text
                    })
                    
                    st.success("Missão Concluída!")
                    tab1, tab2 = st.tabs(["📝 Resultado Atual", "📦 Gestão de Exportação"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        # Baixa apenas o documento ATUAL
                        st.download_button("📥 Baixar Este Relatório (.DOCX)", preparar_docx(response.text, unico=True), f"aether_{nome_fonte}.docx")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro no Motor: {e}")
        else:
            st.warning("Insira dados ou envie um arquivo.")
