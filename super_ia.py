import streamlit as st
import pandas as pd
import os, time, base64
import docx2txt

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO & LIBS TÁTICAS ---
try:
    from groq import Groq
except ImportError:
    pass

st.set_page_config(page_title="AETHER KARV V124", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# --- 🧠 ESTADO DA SESSÃO (Memória Core) ---
if "cmd_input" not in st.session_state: st.session_state.cmd_input = ""
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "telemetria" not in st.session_state: st.session_state.telemetria = None

# --- ⚡ EXTRATOR NEXUS (Ingestão de Dados) ---
def extrator_nexus(arquivos_upados):
    texto_extraido = ""
    sucesso = 0
    for arquivo in arquivos_upados:
        try:
            if arquivo.name.endswith('.csv'):
                df = pd.read_csv(arquivo)
                texto_extraido += f"\n\n--- MATRIZ CSV: {arquivo.name} ---\n{df.to_string()}"
            elif arquivo.name.endswith('.xlsx'):
                df = pd.read_excel(arquivo)
                texto_extraido += f"\n\n--- MATRIZ XLSX: {arquivo.name} ---\n{df.to_string()}"
            elif arquivo.name.endswith('.docx'):
                texto = docx2txt.process(arquivo)
                texto_extraido += f"\n\n--- DOCX: {arquivo.name} ---\n{texto}"
            elif arquivo.name.endswith('.txt'):
                texto_extraido += f"\n\n--- TXT: {arquivo.name} ---\n{arquivo.getvalue().decode('utf-8')}"
            sucesso += 1
        except Exception as e:
            texto_extraido += f"\n[ERRO DE LEITURA EM {arquivo.name}: {str(e)}]"
    return texto_extraido, sucesso

# --- ⚡ MOTOR AETHER KARV (Processamento Neural) ---
def aether_karv_engine(comando, contexto_arquivos):
    if not contexto_arquivos.strip():
        contexto_arquivos = "[Nenhum dado de arquivo injetado. Operando apenas com o comando jurídico.]"
    
    groq_api_key = os.environ.get("GROQ_API_KEY") 
    
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            prompt_tatico = f"Você é o AETHER KARV, um sistema de auditoria avançada.\nComando Jurídico: {comando}\nDados Injetados: {contexto_arquivos}"
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_tatico}],
                model="llama3-70b-8192", 
                temperature=0.2,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ FALHA NO LINK NEURAL GROQ: {str(e)}"
    else:
        time.sleep(2.5) 
        return f"**AUDITORIA SINTÉTICA (MODO OFFLINE):**\nO sistema processou o comando tático com sucesso. Configure a variável de ambiente GROQ_API_KEY para acesso neural."

# --- 🎨 IMAGENS E FUNDO ---
back_apex_b64 = get_base64_image("back_apex.png")

# TÉCNICA DE PROFUNDIDADE: Escurecemos a imagem de fundo em 60% para ela não "gritar" na tela.
bg_css = f"background: linear-gradient(rgba(2, 6, 23, 0.6), rgba(2, 6, 23, 0.6)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;" if back_apex_b64 else "background-color: #020617;"

# --- 🎨 CSS APEX V124: LIMPEZA ABSOLUTA ---
css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

/* RESET GERAL */
.stApp {{ {bg_css} color: #f3f4f6; font-family: 'Inter', sans-serif; }}

/* ⚠️ EMPURRA TUDO PARA BAIXO PARA NÃO SOBREPOR O LOGO DA IMAGEM ⚠️ */
.block-container {{ padding-top: 15rem !important; padding-bottom: 2rem !important; max-width: 1150px !important; margin: 0 auto; }}

[data-testid="stHeader"] {{ display: none !important; }}

/* ESCONDE O TÍTULO DO MENU ("Seletor") */
div[data-testid="stRadio"] > label {{ display: none !important; }}

/* MENU CÁPSULAS NATIVO (Escuro e opaco para não misturar com o fundo) */
div[role="radiogroup"] {{ 
    display: flex !important; flex-direction: row !important; justify-content: center !important; gap: 5px !important; 
    background: rgba(5, 10, 18, 0.95) !important; border-radius: 50px !important; padding: 6px !important; 
    border: 1px solid rgba(16,185,129,0.4) !important; width: fit-content !important; margin: 0 auto 40px auto !important; 
    box-shadow: 0 10px 30px rgba(0,0,0,0.8) !important;
}}
div[role="radiogroup"] label div[dir="auto"]:first-child, div[role="radio"] div:first-child, span[data-baseweb="radio"] {{ display: none !important; }}
div[data-testid="stRadio"] label {{ background-color: transparent !important; color: #8b9eb3 !important; padding: 10px 35px !important; margin: 0 !important; cursor: pointer; border-radius: 50px; display: flex; align-items: center; justify-content: center; transition: all 0.3s ease; }}
div[data-testid="stRadio"] label:has(input:checked) {{ background: linear-gradient(90deg, #10b981, #34d399) !important; color: #020617 !important; font-weight: 900 !important; box-shadow: 0 0 20px rgba(16, 185, 129, 0.4) !important; }}
div[data-testid="stRadio"] label p {{ font-size: 0.95rem !important; font-weight: 700 !important; margin: 0 !important; text-transform: uppercase; letter-spacing: 1px; }}

/* ⚠️ CAIXAS DE VIDRO BLINDADO (PAINÉIS COM 95% DE OPACIDADE) ⚠️ */
[data-testid="column"] {{
    background: rgba(5, 10, 18, 0.95) !important; /* Quase preto sólido para bloquear a poluição do fundo */
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
    border-radius: 16px !important;
    padding: 30px !important;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(16, 185, 129, 0.05) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
}}

/* TÍTULOS DOS PAINÉIS */
.panel-header {{ color: #ffffff; font-weight: 800; font-size: 1.05rem; letter-spacing: 1px; margin-bottom: 25px; text-transform: uppercase; border-bottom: 1px solid rgba(16,185,129,0.3); padding-bottom: 10px; display: flex; align-items: center; }}

/* UPLOADER DE ARQUIVOS */
[data-testid="stFileUploadDropzone"] {{
    background-color: rgba(0, 0, 0, 0.5) !important;
    border: 2px dashed rgba(16, 185, 129, 0.4) !important;
    border-radius: 12px !important;
    padding: 25px !important;
    transition: all 0.3s ease;
}}
[data-testid="stFileUploadDropzone"]:hover {{ border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.1) !important; }}

/* CAIXA DE COMANDO */
.stTextArea label {{ font-size: 0.8rem !important; margin-bottom: 8px !important; margin-top: 15px !important; font-weight: 800 !important; letter-spacing: 1px; color: #fff !important; text-transform: uppercase; }}
.stTextArea textarea {{ background-color: rgba(0, 0, 0, 0.6) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; color: #ffffff !important; font-size: 0.9rem !important; border-radius: 10px !important; padding: 15px !important; height: 130px !important; min-height: 130px !important; resize: none; }}
.stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 15px rgba(16, 185, 129, 0.3) !important; outline: none !important; }}

/* BOTÃO VERDE PRINCIPAL (PROCESSAR) */
.stButton > button[kind="primary"] {{
    background: linear-gradient(90deg, #10b981, #34d399) !important; border-radius: 50px !important; font-weight: 900 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 1.5px !important; padding: 12px !important; border: none !important; font-size: 0.95rem !important; width: 100% !important; margin-top: 20px !important; box-shadow: 0 5px 20px rgba(16, 185, 129, 0.3) !important; transition: all 0.3s ease;
}}
.stButton > button[kind="primary"]:hover {{ transform: translateY(-3px); filter: brightness(1.1); box-shadow: 0 10px 25px rgba(16, 185, 129, 0.5) !important; }}

/* BOTÃO SECUNDÁRIO E DOWNLOADS */
.stButton > button[kind="secondary"], .stDownloadButton > button {{
    background: rgba(30, 41, 59, 0.6) !important; color: #cbd5e1 !important; border: 1px solid rgba(16, 185, 129, 0.4) !important; border-radius: 50px !important; font-weight: 600 !important; width: 100% !important; transition: all 0.3s ease; font-size: 0.8rem !important;
}}
.stButton > button[kind="secondary"]:hover, .stDownloadButton > button:hover {{ border-color: #10b981 !important; color: #10b981 !important; background: rgba(16, 185, 129, 0.1) !important; }}

/* ELEMENTOS DO DOSSIÊ */
.telemetry-badge {{ display: inline-block; background: rgba(16, 185, 129, 0.15); color: #34d399; font-size: 0.8rem; padding: 8px 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid rgba(16, 185, 129, 0.4); font-weight: bold; width: 100%; text-align: center; letter-spacing: 1px; }}
[data-testid="stCodeBlock"] {{ background: rgba(0, 0, 0, 0.7) !important; border: 1px solid rgba(16,185,129,0.5) !important; border-radius: 8px !important; margin-bottom: 20px; }}
.nexus-center {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 380px; text-align: center; }}
</style>
"""

st.markdown(css_code, unsafe_allow_html=True)

# Removemos o título "AETHER KARV" gerado por código para não duplicar com a sua imagem!

# --- NAVEGAÇÃO DE MÓDULOS ---
menu = st.radio("Seletor", ["🛡️ AUDITORIA", "🔍 FORENSE", "⚙️ ENGENHARIA"], index=0, horizontal=True)

# --- ESTRUTURA DE COLUNAS (Painéis Sólidos) ---
col_ing, col_dos = st.columns(2, gap="large")

# === PAINEL ESQUERDO: INGESTÃO ===
with col_ing:
    st.markdown('<div class="panel-header">INGESTÃO NEXUS</div>', unsafe_allow_html=True)
    
    up = st.file_uploader("Upload de Arquivos", accept_multiple_files=True, label_visibility="collapsed")
    
    cmd = st.text_area("COMANDO JURÍDICO ESTRATÉGICO:", key="cmd_input", placeholder="Descreva sua análise jurídica profunda e cruze os dados dos arquivos injetados...")

    if st.button("🚀 PROCESSAR AUDITORIA", type="primary"):
        if cmd:
            with st.status("🧠 Inicializando Motores AETHER KARV...", expanded=False):
                texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                resposta = aether_karv_engine(cmd, texto_arquivos)
                
                st.session_state.res_aether = resposta
                st.session_state.telemetria = f"Ativos Ingeridos: {num_arquivos} | Volume: {len(texto_arquivos)} bytes"
            st.rerun() 
        else:
            st.warning("⚠️ Insira um comando estratégico para iniciar a operação.")

# === PAINEL DIREITO: DOSSIÊ ===
with col_dos:
    st.markdown('<div class="panel-header">DOSSIÊ DE INTELIGÊNCIA</div>', unsafe_allow_html=True)
    
    if st.session_state.res_aether:
        st.markdown(f"<div class='telemetry-badge'>🛰️ TELEMETRIA: {st.session_state.telemetria}</div>", unsafe_allow_html=True)
        st.code(st.session_state.res_aether, language="markdown")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("📄 TXT", data=st.session_state.res_aether, file_name="aether_dossier.txt", mime="text/plain", use_container_width=True)
        with c2:
            st.download_button("📝 MD", data=st.session_state.res_aether, file_name="aether_dossier.md", mime="text/markdown", use_container_width=True)
        with c3:
            if st.button("🔄 RESET", type="secondary", use_container_width=True):
                st.session_state.res_aether = None
                st.session_state.telemetria = None
                st.rerun()
    else:
        st.markdown(f"""
        <div class="nexus-center">
            <h3 style="margin:0; font-weight:900; color:#f8fafc; letter-spacing:1px; font-size: 1.5rem;">⚖️ MOTOR KARV EM ESPERA</h3>
            <p style="color:#64748b; font-size:1rem; margin-top:10px; font-weight: 500;">Aguardando ingestão de matriz de dados e comando tático.</p>
        </div>
        """, unsafe_allow_html=True)
