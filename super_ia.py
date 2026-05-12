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
st.set_page_config(page_title="AETHER KARV V107.3 Apex", page_icon="logo.png", layout="wide", initial_sidebar_state="collapsed")

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
dossie_b64 = get_base64_image("dossie.png")

bg_css = f"background-image: url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #020617;"

# --- 🎨 INJEÇÃO DE CSS AVANÇADO ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp {{ {bg_css} color: #f3f4f6; font-family: 'Inter', sans-serif; }}
    .block-container {{ padding-top: 1.5rem !important; padding-bottom: 0rem !important; max-width: 90% !important; margin: 0 auto !important; overflow: hidden !important;}}
    [data-testid="stHeader"], [data-testid="collapsedControl"] {{ display: none !important; }}

    /* MENU CÁPSULAS */
    div[role="radiogroup"] > div > label > div:first-child {{ display: none !important; }}
    div[data-testid="stRadio"] > div {{ justify-content: center !important; gap: 12px !important; background: rgba(15, 23, 42, 0.6) !important; padding: 5px !important; border-radius: 50px !important; border: 1px solid #1e293b !important; width: fit-content !important; margin: 0 auto 15px auto !important; }}
    div[data-testid="stRadio"] label {{ background-color: transparent !important; color: #94a3b8 !important; padding: 10px 25px !important; transition: all 0.4s ease; margin: 0 !important; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; }}
    div[data-testid="stRadio"] label:has(input:checked) {{ background: linear-gradient(90deg, #10b981, #34d399) !important; color: #020617 !important; font-weight: 800 !important; border-radius: 50px !important; box-shadow: 0 0 20px rgba(16, 185, 129, 0.5) !important; }}
    div[data-testid="stRadio"] label p {{ font-size: 1.05rem !important; font-weight: 700 !important; margin: 0; display: flex; align-items: center; color: inherit; }}
    
    /* ÍCONES DOS BOTÕES */
    div[data-testid="stRadio"] label:nth-child(1) p::before {{ content: ''; display: inline-block; width: 20px; height: 20px; margin-right: 8px; background-image: url('data:image/png;base64,{auditoria_b64}'); background-size: contain; background-repeat: no-repeat; background-position: center; }}
    div[data-testid="stRadio"] label:nth-child(2) p::before {{ content: ''; display: inline-block; width: 20px; height: 20px; margin-right: 8px; background-image: url('data:image/png;base64,{forense_b64}'); background-size: contain; background-repeat: no-repeat; background-position: center; }}
    div[data-testid="stRadio"] label:nth-child(3) p::before {{ content: ''; display: inline-block; width: 20px; height: 20px; margin-right: 8px; background-image: url('data:image/png;base64,{engenharia_b64}'); background-size: contain; background-repeat: no-repeat; background-position: center; }}
    
    /* FILTRO DE COR (Preto quando ativo, Verde quando inativo) */
    div[data-testid="stRadio"] label p::before {{ filter: drop-shadow(0px 0px 3px rgba(16, 185, 129, 0.8)); }}
    div[data-testid="stRadio"] label:has(input:checked) p::before {{ filter: brightness(0) drop-shadow(0px 0px 0px transparent) !important; }}

    /* UPLOADER DESTRUIDOR DE LAYOUT NATIVO */
    [data-testid="stFileUploadDropzone"] {{ background-color: transparent !important; border: 2px dashed rgba(16, 185, 129, 0.4) !important; border-radius: 12px !important; transition: 0.3s; min-height: 130px !important; display: flex !important; flex-direction: column; justify-content: center !important; align-items: center !important; color: transparent !important; }}
    [data-testid="stFileUploadDropzone"]:hover {{ border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.1) !important; }}
    
    /* Esconde violentamente os botões e textos nativos do Streamlit */
    [data-testid="stFileUploadDropzone"] button {{ display: none !important; }}
    [data-testid="stFileUploadDropzone"] div[data-testid="stText"] {{ display: none !important; }}
    [data-testid="stFileUploadDropzone"] > div > span {{ display: none !important; }}
    [data-testid="stFileUploadDropzone"] svg {{ display: none !important; }}
    [data-testid="stFileUploadDropzone"] small {{ display: none !important; }}
    
    /* Injeta a Nuvem Personalizada */
    [data-testid="stFileUploadDropzone"]::before {{ content: ''; background-image: url('data:image/png;base64,{upload_b64}'); background-size: contain; background-repeat: no-repeat; background-position: center; width: 55px; height: 55px; display: block; margin: 0 auto 10px auto; pointer-events: none; }}
    [data-testid="stFileUploadDropzone"]::after {{ content: 'ARRASTE ARQUIVOS OU CLIQUE (PDF, DOCX, XLSX, CSV)'; color: #cbd5e1; font-weight: 600; font-size: 0.85rem; font-family: 'Inter', sans-serif; display: block; text-align: center; pointer-events: none; }}

    /* TEXT AREA E BOTOES */
    .stTextArea label {{ font-size: 0.85rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
    .stTextArea textarea {{ background-color: rgba(7, 11, 20, 0.8) !important; border: 1px solid #1e293b !important; color: #cbd5e1 !important; font-size: 0.9rem !important; border-radius: 10px; }}
    .stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2) !important; }}
    .operation-card {{ background: transparent !important; border: none !important; padding: 15px; }}
    
    button[kind="primary"] {{ background: linear-gradient(90deg, #10b981, #34d399) !important; border-radius: 50px !important; font-weight: 900 !important; color: #020617 !important; box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3) !important; text-transform: uppercase; letter-spacing: 1px; padding: 15px !important; margin-top: 15px !important; border: none !important; font-size: 1rem !important; }}
    button[kind="primary"]:hover {{ transform: translateY(-1px); box-shadow: 0 15px 35px rgba(16, 185, 129, 0.5) !important; filter: brightness(1.1); }}

    /* TÍTULO CENTRALIZADO */
    .header-container {{ text-align: center; margin-bottom: 10px; display: flex; flex-direction: column; align-items: center; margin-top: 60px; }}
    .karv-title {{ margin: 0; font-weight: 900; font-size: 2.8rem; color: #ffffff; letter-spacing: -2px; line-height: 1; text-shadow: 0 0 15px rgba(16, 185, 129, 0.3); }}
    .karv-subtitle {{ color: #10b981; font-weight: 700; font-size: 1rem; letter-spacing: 4px; text-transform: uppercase; margin-top: 5px; }}
    
    /* DOSSIÊ */
    .nexus-center {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 320px; text-align: center; }}
    .dossie-icon {{ width: 110px; height: 110px; object-fit: contain; margin-bottom: 15px; filter: drop-shadow(0 0 15px rgba(16, 185, 129, 0.5)); }}
    .download-bar {{ display: flex; justify-content: center; gap: 8px; margin-top: 20px; }}
    .download-pill {{ background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 50px; padding: 6px 14px; color: #cbd5e1; font-size: 0.8rem; cursor: pointer; transition: 0.3s; font-weight: 600; }}
    .download-pill:hover {{ border-color: #10b981; color: #10b981; background: rgba(16, 185, 129, 0.05); }}
    .karv-response {{ background: rgba(15,23,42,0.8); border-left: 4px solid #10b981; padding: 15px; border-radius: 5px; font-family: monospace; white-space: pre-wrap; margin-top: 10px; font-size: 0.95rem; text-align: left; overflow-y: auto; max-height: 350px; }}
    .telemetry-badge {{ display: inline-block; background: #1e293b; color: #34d399; font-size: 0.75rem; padding: 3px 8px; border-radius: 12px; margin-bottom: 10px; border: 1px solid #34d399; text-align: center; width: 100%; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""<div class="header-container"><h1 class="karv-title">AETHER KARV</h1><div class="karv-subtitle">Strategic Intelligence Hub</div></div>""", unsafe_allow_html=True)

# MENU CÁPSULAS
menu = st.radio("", ["AUDITORIA", "FORENSE", "ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)
st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)

# --- GRID ---
col_ing, col_dos = st.columns(2, gap="large")

with col_ing:
    with st.container():
        st.markdown('<div class="operation-card">', unsafe_allow_html=True)
        up = st.file_uploader(" ", accept_multiple_files=True, label_visibility="collapsed")
        st.markdown('<div style="margin-top:20px;"></div>', unsafe_allow_html=True)
        cmd = st.text_area("COMANDO JURÍDICO ESTRATÉGICO:", key="cmd_input", height=130, placeholder="Descreva sua análise jurídica estratégica profunda...")

        if st.button("🚀 PROCESSAR AUDITORIA NEURAL", type="primary", use_container_width=True):
            if cmd:
                with st.status("🧠 Inicializando Motores Neurais AETHER KARV...", expanded=False):
                    texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                    resposta = aether_karv_engine(cmd, texto_arquivos)
                    st.session_state.res_aether = resposta
                    st.session_state.telemetria = f"Ativos Ingeridos: {num_arquivos} | Volume: {len(texto_arquivos)} bytes"
                st.rerun()
            else:
                st.warning("Insira um comando estratégico para iniciar.")
        st.markdown('</div>', unsafe_allow_html=True)

with col_dos:
    with st.container():
        st.markdown('<div class="operation-card">', unsafe_allow_html=True)
        
        if st.session_state.res_aether:
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            if st.session_state.telemetria:
                st.markdown(f"<div class='telemetry-badge'>🛰️ TELEMETRIA: {st.session_state.telemetria}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='karv-response'>{st.session_state.res_aether}</div>", unsafe_allow_html=True)
            if st.button("🔄 NOVA OPERAÇÃO"):
                st.session_state.res_aether, st.session_state.telemetria = None, None
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            dossie_img = f'<img src="data:image/png;base64,{dossie_b64}" class="dossie-icon">' if dossie_b64 else '<div style="font-size:4rem; margin-bottom:15px;">⚖️</div>'
            st.markdown(f"""<div class="nexus-center">{dossie_img}<h3 style="margin:0; font-weight:900; color:white; letter-spacing:1px; font-size: 1.2rem;">MOTOR KARV PRONTO</h3><p style="color:#64748b; font-size:0.9rem; margin-top:5px;">Aguardando ingestão...</p></div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class="download-bar"><div class="download-pill">📄 PDF</div><div class="download-pill">📝 DOCX</div><div class="download-pill">📊 XLSX</div><div class="download-pill">📉 CSV</div></div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
