import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- CONFIGURAÇÃO VISUAL PREMIUM (INTER FONT & BORDAS ARREDONDADAS) ---
st.set_page_config(page_title="AETHER OMNI | Enterprise Evolution", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.8em; border: none;
    }
    .report-card { padding: 30px; border-radius: 18px; background-color: #1a1c24; border: 1px solid #2d2f39; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .sidebar-box { padding: 15px; background: #262730; border-radius: 12px; border-left: 5px solid #00c6ff; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO ESTÁVEL V1 (MIGRAÇÃO COMPLETA) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Migração para a versão estável v1 sem sufixos beta
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    st.error("🔄 Conexão instável, tentando reiniciar o motor...")

def gerar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO DE AUDITORIA', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- PAINEL LATERAL (CONFIGURAÇÕES E PESSOAS) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    persona = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Auditor Trabalhista", "Auditor Imobiliário", "Auditor Tributário", "Especialista em LGPD"])
    
    st.divider()
    st.subheader("📂 Ingestão de Dados")
    arquivos = st.file_uploader("Upload de Evidências (Múltiplos arquivos)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    
    st.divider()
    st.subheader("⚙️ Sniper Mode")
    st.toggle("Checklist de Compliance Automático", value=True)
    st.toggle("Extração Inteligente de Tabelas", value=True)
    st.toggle("Score de Risco (%)", value=True)
    
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()

# --- INTERFACE CENTRAL (FOCO NO RESULTADO) ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.caption(f"Operando como: **{persona}** | Versão Estável v1")

# Sugestões rápidas em colunas discretas
c1, c2, c3 = st.columns(3)
with c1: st.caption("💡 *'Analise riscos trabalhistas'*")
with c2: st.caption("💡 *'Verifique multas de rescisão'*")
with c3: st.caption("💡 *'Valide cláusulas de LGPD'*")

pergunta = st.text_area("O que o sistema deve analisar ou auditar?", placeholder="Instrução do Auditor...", height=120)

if st.button("🚀 INICIAR VARREDURA OMNI"):
    if pergunta:
        with st.spinner(f"O {persona} está processando as evidências..."):
            try:
                time.sleep(1)
                conteudo_total = ""
                # Processamento de múltiplos arquivos
                if arquivos:
                    for arq in arquivos:
                        if arq.name.endswith(('.xlsx', '.csv')):
                            df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                            conteudo_total += f"\n\nARQUIVO {arq.name}:\n{df.to_string()}"
                
                prompt_master = f"""
                Atue como um {persona} sênior. 
                Instrução: {pergunta}
                Dados Adicionais: {conteudo_total}
                
                REQUISITOS:
                1. Checklist de Compliance (LGPD, Multas, Vigência).
                2. Sugestão de Redação Jurídica Correta (Pronta para copiar).
                3. Score de Risco de 0 a 100%.
                Use linguagem profissional e cite leis brasileiras.
                """
                
                # Chamada multimodal básica
                response = model.generate_content(prompt_master)
                
                st.markdown("### 📝 Resultado da Auditoria")
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                
                st.divider()
                col_down1, col_down2 = st.columns(2)
                with col_down1:
                    st.download_button("📥 Exportar para .DOCX", gerar_docx(response.text), "aether_report.docx")
                with col_down2:
                    st.button("📋 Copiar Redação Jurídica")
                    
            except Exception as e:
                st.error("Conexão instável com a rede Omni. Por favor, desative o tradutor e tente novamente.")
    else:
        st.warning("Aguardando instrução do auditor.")

st.divider()
st.caption("Aether Omni - Inteligência de Classe Mundial para Auditoria Forense")
