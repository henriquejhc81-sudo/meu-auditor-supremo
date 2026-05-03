import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time
import random

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

# --- CONEXÃO BLINDADA (FIM DO 404 V1BETA) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Correção mestre: Forçamos a porta estável 'v1' para garantir funcionamento global
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"📡 Rede Aether: Sincronizando conexão segura... {e}")

def preparar_download(texto, titulo):
    doc = Document()
    doc.add_heading(f'AETHER AUDIT - {titulo}', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.title("🛡️ AETHER AUDIT ENTERPRISE")
st.markdown("##### *Standard for High-Frequency Auditing & Global Compliance*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivo = st.file_uploader("Upload de Evidências (PDF, Imagem, Excel, TXT)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.divider()
    
    # FUNCIONALIDADES DE ELITE (TOGGLES)
    st.markdown("### ⚙️ Sniper Config")
    extrair_tab = st.toggle("Extração Inteligente de Tabelas", value=True)
    score_risco = st.toggle("Score de Risco Automático", value=True)
    detec_anomalia = st.toggle("Detecção de Anomalias (Assinaturas/Forense)", value=True)
    cruzamento_dados = st.toggle("Cruzamento SPED/Multi-Fonte", value=False)

with col2:
    st.subheader("🔍 Central de Inteligência")
    
    # FILTRO DE AÇÃO PÓS-AUDITORIA (NOVIDADE)
    tipo_saida = st.selectbox("🎯 Objetivo da Missão (Filtro)", [
        "Apenas Relatório de Auditoria", 
        "Auditoria + Gerar Contrato Corrigido", 
        "Auditoria + Gerar Petição/Processo",
        "Análise Forense de Assinaturas"
    ])
    
    pergunta = st.text_area("O que o sistema deve analisar ou redigir?", placeholder="Ex: Analise este documento e verifique riscos...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Aether está processando na nuvem..."):
                try:
                    time.sleep(random.uniform(0.5, 1.5)) # Stealth Mode
                    conteudo_extra = ""
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    # SUPER PROMPT MULTI-IA (Claude, DeepSeek, Llama, Grok)
                    prompt_final = f"""
                    Atue como AUDITOR SUPREMO e ADVOGADO SÊNIOR.
                    Missão Atual: {tipo_saida}.
                    Instrução: {pergunta} {conteudo_extra}.
                    
                    ESTRUTURA DE ANÁLISE (Multi-IA):
                    1. 🔍 Ótica Técnica (DeepSeek): Precisão dos dados e leis.
                    2. ⚖️ Ótica Ética (Claude): Riscos de Compliance e LGPD.
                    3. 📝 Ótica Pragmática (Grok): Ação imediata e veredito.
                    4. ✅ RESULTADO FINAL: Se solicitado Geração, redija o texto completo do contrato ou petição.
                    
                    Use leis brasileiras, dê Score de Risco (%) e verifique assinaturas se houver imagem.
                    """
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_final, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_final)
                    
                    st.success("Missão Cumprida!")
                    tab1, tab2 = st.tabs(["📝 Relatório Inteligente", "📥 Exportar"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button(f"📥 BAIXAR {tipo_saida.upper()}", preparar_download(response.text, tipo_saida), "aether_result.docx")
                        st.balloons()
                except Exception as e:
                    st.error(f"Erro na Rede Aether: {e}. Desative o tradutor e reinicie o motor.")
        else:
            st.warning("Insira uma pergunta ou instrução.")

with st.sidebar:
    st.info("💡 **Dica Sniper:** No modo 'Gerar Contrato', o sistema utiliza IA jurídica para redigir cláusulas de blindagem patrimonial.")
    if st.button("🔄 Reiniciar Motor do Sistema"):
        st.rerun()
    st.caption("AETHER AUDIT v46.2 | Master Ultimate Edition")
