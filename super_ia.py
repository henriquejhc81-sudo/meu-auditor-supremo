import streamlit as st
import pandas as pd
import os, time, base64
import docx2txt

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO & LIBS ---
try:
    from groq import Groq
except ImportError:
    pass

# --- ⚙️ CONFIGURAÇÃO DE AMBIENTE ---
st.set_page_config(page_title="AETHER KARV V116 Apex", page_icon="logo.png", layout="wide", initial_sidebar_state="collapsed")

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# --- 🧠 ESTADO DA SESSÃO ---
if "cmd_input" not in st.session_state:
    st.session_state.cmd_input = ""
if "res_aether" not in st.session_state:
    st.session_state.res_aether = None
if "telemetria" not in st.session_state:
    st.session_state.telemetria = None

# --- ⚡ EXTRATOR NEXUS ---
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

# --- ⚡ MOTOR AETHER KARV ---
def aether_karv_engine(comando, contexto_arquivos):
    if not contexto_arquivos.strip():
        contexto_arquivos = "[Nenhum dado de arquivo injetado. Operando apenas com o comando.]"
    
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
        return f"**AUDITORIA SINTÉTICA (MODO OFFLINE):**\nO sistema processou o comando `{comando[:20]}...` com sucesso."

# --- 🎨 CARREGAMENTO VISUAL ---
back_apex_b64 = get_base64_image("back_apex.png")
auditoria_b64 = get_base64_image("auditoria_link.png")
forense_b64 = get_base64_image("forense_link.png")
engenharia_b64 = get_base64_image("engenharia_link.png")
upload_b64 = get_base64_image("upload.png")

bg_css = f"background-image: url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center top; background-repeat: no-repeat; background-attachment: fixed;" if back_apex_b64 else "background-color: #020617;"

# --- CSS BASE GLOBAL ---
css_base = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

.stApp {{ {bg_css} color: #f3f4f6; font-family: 'Inter', sans-serif; overflow-x: hidden; }}
.block-container {{ padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 75rem !important; margin: 0 auto !important; display: flex; flex-direction: column; justify-content: center; min-height: 100vh; }}
[data-testid="stHeader"] {{ display: none !important; }}

/* HEADER CENTRALIZADO */
.header-container {{ text-align: center; margin-bottom: 20px; }}
.karv-title {{ margin: 0; font-weight: 900; font-size: 2.5rem; color: #ffffff; letter-spacing: -1px; text-shadow: 0 0 15px rgba(16, 185, 129, 0.4); line-height: 1; }}
.karv-subtitle {{ color: #10b981; font-weight: 700; font-size: 0.85rem; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px; }}

/* MENU CÁPSULAS */
div[role="radiogroup"] {{ display: flex !important; flex-direction: row !important; justify-content: center !important; gap: 5px !important; background: rgba(10, 18, 27, 0.7) !important; border-radius: 50px !important; padding: 5px !important; border: 1px solid rgba(16,185,129,0.3) !important; width: fit-content !important; margin: 0 auto 20px auto !important; box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important; }}
div[data-testid="stRadio"] div[role="radio"] div:first-of-type, .stRadio [data-baseweb="radio"] > div:first-child {{ display: none !important; }}
div[data-testid="stRadio"] label {{ background-color: transparent !important; color: #94a3b8 !important; padding: 8px 25px !important; margin: 0 !important; cursor: pointer; border-radius: 50px; display: flex; align-items: center; justify-content: center; transition: 0.3s; }}
div[data-testid="stRadio"] label:has(input:checked) {{ background: linear-gradient(90deg, #10b981, #34d399) !important; color: #020617 !important; font-weight: 800 !important; box-shadow: 0 0 15px rgba(16, 185, 129, 0.5) !important; }}
div[data-testid="stRadio"] label p {{ font-size: 0.9rem !important; font-weight: 700 !important; margin: 0 !important; display: flex !important; align-items: center !important; }}
div[data-testid="stRadio"] label:nth-child(1) p::before {{ content: ''; display: inline-block; width: 16px; height: 16px; margin-right: 6px; background-image: url('data:image/png;base64,{auditoria_b64}'); background-size: contain; background-repeat: no-repeat; }}
div[data-testid="stRadio"] label:nth-child(2) p::before {{ content: ''; display: inline-block; width: 16px; height: 16px; margin-right: 6px; background-image: url('data:image/png;base64,{forense_b64}'); background-size: contain; background-repeat: no-repeat; }}
div[data-testid="stRadio"] label:nth-child(3) p::before {{ content: ''; display: inline-block; width: 16px; height: 16px; margin-right: 6px; background-image: url('data:image/png;base64,{engenharia_b64}'); background-size: contain; background-repeat: no-repeat; }}
div[data-testid="stRadio"] label p::before {{ filter: drop-shadow(0px 0px 3px rgba(16, 185, 129, 0.8)); }}
div[data-testid="stRadio"] label:has(input:checked) p::before {{ filter: brightness(0) !important; }}

/* ELEMENTOS INTERNOS DOS PAINÉIS */
.panel-header {{ color: #ffffff; font-weight: 800; font-size: 1rem; letter-spacing: 1px; margin-bottom: 15px; text-transform: uppercase; border-bottom: 1px solid rgba(16,185,129,0.3); padding-bottom: 5px; }}
.stFileUploader {{ min-height: 90px !important; }}
[data-testid="stFileUploadDropzone"] {{ background-color: transparent !important; border: 2px dashed rgba(16, 185, 129, 0.4) !important; border-radius: 10px !important; position: relative; overflow: hidden; height: 90px !important; min-height: 90px !important; padding: 0 !important; }}
[data-testid="stFileUploadDropzone"]:hover {{ border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.05) !important; }}
.stFileUploader section > button, .stFileUploader section > span, .stFileUploader section > small, .stFileUploader section > svg, .stFileUploader div[data-testid="stText"] {{ display: none !important; opacity: 0 !important; }}
[data-testid="stFileUploadDropzone"]::before {{ content: ''; position: absolute; top: 15px; left: 50%; transform: translateX(-50%); background-image: url('data:image/png;base64,{upload_b64}'); background-size: contain; background-repeat: no-repeat; background-position: center; width: 30px; height: 30px; z-index: 1; pointer-events: none; }}
[data-testid="stFileUploadDropzone"]::after {{ content: 'ARRASTE ARQUIVOS OU CLIQUE PARA UPLOAD'; position: absolute; bottom: 20px; left: 0; right: 0; text-align: center; color: #8b9eb3; font-size: 0.75rem; font-weight: 600; z-index: 1; pointer-events: none; }}
.stTextArea label {{ font-size: 0.75rem !important; margin-bottom: 5px !important; margin-top: 10px !important; font-weight: 800 !important; letter-spacing: 1px; color: #fff !important; }}
.stTextArea textarea {{ background-color: rgba(7, 11, 20, 0.8) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; color: #ffffff !important; font-size: 0.85rem !important; border-radius: 8px !important; padding: 10px !important; height: 90px !important; min-height: 90px !important; resize: none; }}
.stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2) !important; outline: none !important; }}

/* BOTÃO PROCESSAR */
.stButton > button {{ background: linear-gradient(90deg, #10b981, #34d399) !important; border-radius: 50px !important; font-weight: 900 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 1px !important; padding: 10px !important; border: none !important; font-size: 0.9rem !important; width: 100% !important; margin-top: 10px !important; box-shadow: 0 5px 15px rgba(16, 185, 129, 0.2) !important; transition: all 0.3s ease; }}
.stButton > button:hover {{ transform: translateY(-2px); filter: brightness(1.1); box-shadow: 0 10px 20px rgba(16, 185, 129, 0.4) !important; }}

/* DOSSIÊ ESPECÍFICOS */
.telemetry-badge {{ display: inline-block; background: rgba(16, 185, 129, 0.1); color: #34d399; font-size: 0.75rem; padding: 5px 15px; border-radius: 12px; margin-bottom: 15px; border: 1px solid rgba(16, 185, 129, 0.3); font-weight: bold; width: 100%; text-align: center; }}
[data-testid="stCodeBlock"] {{ background: rgba(0, 0, 0, 0.6) !important; border: 1px solid #10b981 !important; border-radius: 8px !important; margin-bottom: 15px; }}

/* BOTÕES DE DOWNLOAD TIPO PILL */
[data-testid="stDownloadButton"] button {{
    background: rgba(30, 41, 59, 0.6) !important; border: 1px solid rgba(16,185,129,0.4) !important; border-radius: 50px !important; padding: 5px 15px !important; color: #cbd5e1 !important; font-size: 0.8rem !important; font-weight: 600 !important; transition: 0.3s !important; box-shadow: none !important; width: 100% !important; margin: 0 !important; text-transform: none !important;
}}
[data-testid="stDownloadButton"] button:hover {{ border-color: #10b981 !important; color: #10b981 !important; background: rgba(16, 185, 129, 0.1) !important; transform: translateY(-1px) !important; }}
</style>
"""
st.markdown(css_base, unsafe_allow_html=True)

# --- CSS CONDICIONAL (MÁGICA DA REVELAÇÃO PROGRESSIVA) ---
if not st.session_state.res_aether:
    # MODO ZEN: Apenas a coluna central aparece com o Ingestor
    st.markdown("""
    <style>
    [data-testid="column"]:nth-child(1), [data-testid="column"]:nth-child(3) { display: none !important; }
    [data-testid="column"]:nth-child(2) { background: rgba(10, 18, 27, 0.75) !important; border: 1px solid rgba(16, 185, 129, 0.4) !important; border-radius: 15px !important; padding: 30px !important; backdrop-filter: blur(15px); box-shadow: 0 10px 40px rgba(0,0,0,0.5), inset 0 0 20px rgba(16, 185, 129, 0.05); }
    </style>
    """, unsafe_allow_html=True)
else:
    # MODO DUAL: Tela dividida para mostrar o Dossiê
    st.markdown("""
    <style>
    [data-testid="column"] { background: rgba(10, 18, 27, 0.65) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; border-radius: 12px !important; padding: 25px !important; backdrop-filter: blur(12px); box-shadow: inset 0 0 20px rgba(16, 185, 129, 0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown("""
<div class="header-container">
    <h1 class="karv-title">AETHER KARV</h1>
    <div class="karv-subtitle">Strategic Intelligence Hub</div>
</div>
""", unsafe_allow_html=True)

menu = st.radio("", ["AUDITORIA", "FORENSE", "ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)

# --- LÓGICA DE INTERFACE DINÂMICA ---
def renderizar_painel_ingestao():
    st.markdown('<div class="panel-header">INGESTÃO ESTRATÉGICA</div>', unsafe_allow_html=True)
    up = st.file_uploader(" ", accept_multiple_files=True, label_visibility="collapsed")
    cmd = st.text_area("COMANDO JURÍDICO ESTRATÉGICO:", key="cmd_input", placeholder="Ex: Faça uma análise cruzada dos contratos e aponte cláusulas de rescisão abusivas...")

    if st.button("🚀 PROCESSAR AUDITORIA NEURAL"):
        if cmd:
            with st.status("🧠 Inicializando Motores Neurais AETHER KARV...", expanded=False):
                texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                resposta = aether_karv_engine(cmd, texto_arquivos)
                st.session_state.res_aether = resposta
                st.session_state.telemetria = f"Ativos Ingeridos: {num_arquivos} | Volume Processado: {len(texto_arquivos)} bytes"
            st.rerun()
        else:
            st.warning("Insira um comando estratégico para iniciar a operação.")

if not st.session_state.res_aether:
    # MODO ZEN: 3 Colunas invisíveis, usamos a do meio para centralizar
    col_vazia1, col_centro, col_vazia2 = st.columns([1, 2, 1], gap="large")
    with col_centro:
        renderizar_painel_ingestao()
else:
    # MODO DUAL: Resultados Prontos
    col_ing, col_dos = st.columns(2, gap="large")
    
    with col_ing:
        renderizar_painel_ingestao()
        
    with col_dos:
        st.markdown('<div class="panel-header">DOSSIÊ CONCLUÍDO</div>', unsafe_allow_html=True)
        
        if st.session_state.telemetria:
            st.markdown(f"<div class='telemetry-badge'>🛰️ TELEMETRIA: {st.session_state.telemetria}</div>", unsafe_allow_html=True)
        
        # St.code gera o botão de "Copy" perfeitamente funcional!
        st.code(st.session_state.res_aether, language="markdown")
        
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        # Botões funcionais de Download
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("📄 BAIXAR TXT", data=st.session_state.res_aether, file_name="auditoria_aether.txt", mime="text/plain")
        with c2:
            st.download_button("📝 BAIXAR MD", data=st.session_state.res_aether, file_name="auditoria_aether.md", mime="text/markdown")
        with c3:
            if st.button("🔄 NOVA OPERAÇÃO", use_container_width=True):
                st.session_state.res_aether, st.session_state.telemetria = None, None
                st.rerun()
