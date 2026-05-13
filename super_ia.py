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
st.set_page_config(page_title="AETHER KARV V117 Apex", page_icon="logo.png", layout="wide", initial_sidebar_state="collapsed")

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

bg_css = f"background-image: url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center top; background-repeat: no-repeat; background-attachment: fixed;" if back_apex_b64 else "background-color: #020617;"

# --- 🎨 CSS APEX V117: ESTABILIDADE ESTRUTURAL ---
css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

/* RESET E BACKGROUND GLOBAL */
.stApp {{ {bg_css} color: #f3f4f6; font-family: 'Inter', sans-serif; }}
.block-container {{ padding-top: 2rem !important; padding-bottom: 2rem !important; max-width: 1100px !important; margin: 0 auto !important; }}
[data-testid="stHeader"] {{ display: none !important; }}

/* HEADER CENTRALIZADO (Distante das bordas) */
.header-container {{ text-align: center; margin-bottom: 30px; margin-top: 20px; }}
.karv-title {{ margin: 0; font-weight: 900; font-size: 2.8rem; color: #ffffff; letter-spacing: -1px; text-shadow: 0 0 15px rgba(16, 185, 129, 0.4); line-height: 1; }}
.karv-subtitle {{ color: #10b981; font-weight: 700; font-size: 0.95rem; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px; }}

/* MENU CÁPSULAS ALINHADO E ESTÁVEL */
div[role="radiogroup"] {{ display: flex !important; flex-direction: row !important; justify-content: center !important; gap: 10px !important; background: rgba(10, 18, 27, 0.7) !important; border-radius: 50px !important; padding: 6px !important; border: 1px solid rgba(16,185,129,0.3) !important; width: fit-content !important; margin: 0 auto 30px auto !important; box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important; }}
div[data-testid="stRadio"] div[role="radio"] div:first-of-type, .stRadio [data-baseweb="radio"] > div:first-child {{ display: none !important; }}
div[data-testid="stRadio"] label {{ background-color: transparent !important; color: #94a3b8 !important; padding: 10px 25px !important; margin: 0 !important; cursor: pointer; border-radius: 50px; display: flex; align-items: center; justify-content: center; transition: 0.3s; }}
div[data-testid="stRadio"] label:has(input:checked) {{ background: linear-gradient(90deg, #10b981, #34d399) !important; color: #020617 !important; font-weight: 800 !important; box-shadow: 0 0 15px rgba(16, 185, 129, 0.5) !important; }}
div[data-testid="stRadio"] label p {{ font-size: 0.95rem !important; font-weight: 700 !important; margin: 0 !important; display: flex !important; align-items: center !important; }}

/* ÍCONES DO MENU */
div[data-testid="stRadio"] label:nth-child(1) p::before {{ content: ''; display: inline-block; width: 18px; height: 18px; margin-right: 8px; background-image: url('data:image/png;base64,{auditoria_b64}'); background-size: contain; background-repeat: no-repeat; }}
div[data-testid="stRadio"] label:nth-child(2) p::before {{ content: ''; display: inline-block; width: 18px; height: 18px; margin-right: 8px; background-image: url('data:image/png;base64,{forense_b64}'); background-size: contain; background-repeat: no-repeat; }}
div[data-testid="stRadio"] label:nth-child(3) p::before {{ content: ''; display: inline-block; width: 18px; height: 18px; margin-right: 8px; background-image: url('data:image/png;base64,{engenharia_b64}'); background-size: contain; background-repeat: no-repeat; }}
div[data-testid="stRadio"] label p::before {{ filter: drop-shadow(0px 0px 3px rgba(16, 185, 129, 0.8)); }}
div[data-testid="stRadio"] label:has(input:checked) p::before {{ filter: brightness(0) !important; }}

/* OS 2 PAINÉIS LATERAIS (INGESTÃO E DOSSIÊ) */
[data-testid="column"] {{
    background: rgba(10, 18, 27, 0.65) !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
    border-radius: 12px !important;
    padding: 25px !important;
    backdrop-filter: blur(12px);
    box-shadow: inset 0 0 20px rgba(16, 185, 129, 0.05);
    height: 100%; /* Força a mesma altura */
}}
.panel-header {{ color: #ffffff; font-weight: 800; font-size: 1rem; letter-spacing: 1px; margin-bottom: 20px; text-transform: uppercase; border-bottom: 1px solid rgba(16,185,129,0.3); padding-bottom: 8px; }}

/* UPLOADER SÓLIDO E SEGURO */
[data-testid="stFileUploadDropzone"] {{ 
    background-color: rgba(7, 11, 20, 0.5) !important; 
    border: 1px dashed rgba(16, 185, 129, 0.5) !important; 
    border-radius: 10px !important; padding: 25px 15px !important; text-align: center !important;
}}
[data-testid="stFileUploadDropzone"]:hover {{ border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.1) !important; }}

/* Esconde o botão e textos feios, e injeta nossa arte */
[data-testid="stFileUploadDropzone"] button, [data-testid="stFileUploadDropzone"] span, [data-testid="stFileUploadDropzone"] small, [data-testid="stFileUploadDropzone"] svg, [data-testid="stFileUploadDropzone"] div[data-testid="stText"] {{ display: none !important; opacity: 0 !important; }}

[data-testid="stFileUploadDropzone"]::before {{
    content: ''; display: block; margin: 0 auto 10px auto;
    background-image: url('data:image/png;base64,{upload_b64}'); background-size: contain; background-repeat: no-repeat; background-position: center; width: 40px; height: 40px; pointer-events: none;
}}
[data-testid="stFileUploadDropzone"]::after {{
    content: 'ARRASTE ARQUIVOS OU CLIQUE PARA UPLOAD\\A(PDF, DOCX, XLSX, CSV)';
    display: block; color: #8b9eb3; font-size: 0.8rem; font-weight: 600; white-space: pre-wrap; pointer-events: none; line-height: 1.4;
}}

/* TEXT AREA (COMANDO JURÍDICO) */
.stTextArea label {{ font-size: 0.8rem !important; margin-bottom: 8px !important; margin-top: 15px !important; font-weight: 800 !important; letter-spacing: 1px; color: #fff !important; text-transform: uppercase; }}
.stTextArea textarea {{ background-color: rgba(7, 11, 20, 0.8) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; color: #ffffff !important; font-size: 0.9rem !important; border-radius: 8px !important; padding: 15px !important; height: 120px !important; min-height: 120px !important; resize: none; }}
.stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2) !important; outline: none !important; }}

/* BOTÃO DE PROCESSAR */
.stButton > button {{
    background: linear-gradient(90deg, #10b981, #34d399) !important; border-radius: 50px !important; font-weight: 900 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 1px !important; padding: 12px !important; border: none !important; font-size: 0.95rem !important; width: 100% !important; margin-top: 15px !important; box-shadow: 0 5px 15px rgba(16, 185, 129, 0.2) !important; transition: all 0.3s ease;
}}
.stButton > button:hover {{ transform: translateY(-2px); filter: brightness(1.1); box-shadow: 0 10px 20px rgba(16, 185, 129, 0.4) !important; }}

/* ELEMENTOS DO DOSSIÊ */
.nexus-center {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 300px; text-align: center; }}
.dossie-icon {{ width: 90px; height: 90px; object-fit: contain; margin-bottom: 15px; filter: drop-shadow(0 0 15px rgba(16, 185, 129, 0.6)); }}
.telemetry-badge {{ display: inline-block; background: rgba(16, 185, 129, 0.1); color: #34d399; font-size: 0.8rem; padding: 6px 15px; border-radius: 12px; margin-bottom: 15px; border: 1px solid rgba(16, 185, 129, 0.3); font-weight: bold; width: 100%; text-align: center; }}

/* CAIXA PRETA DE CÓDIGO/RESULTADO (st.code) */
[data-testid="stCodeBlock"] {{ background: rgba(0, 0, 0, 0.6) !important; border: 1px solid #10b981 !important; border-radius: 8px !important; margin-bottom: 20px; }}

/* BARRA DE DOWNLOADS TIPO PILLS */
.download-bar {{ display: flex; justify-content: center; gap: 10px; margin-top: 10px; border-top: 1px solid rgba(16,185,129,0.2); padding-top: 15px; }}
[data-testid="stDownloadButton"] button, .download-pill {{
    background: rgba(30, 41, 59, 0.6) !important; border: 1px solid rgba(16,185,129,0.4) !important; border-radius: 50px !important; padding: 6px 18px !important; color: #cbd5e1 !important; font-size: 0.8rem !important; font-weight: 600 !important; transition: 0.3s !important; box-shadow: none !important; margin: 0 !important; line-height: 1.5 !important; height: auto !important; width: 100%;
}}
[data-testid="stDownloadButton"] button:hover, .download-pill:hover {{ border-color: #10b981 !important; color: #10b981 !important; background: rgba(16, 185, 129, 0.1) !important; transform: translateY(-1px) !important; }}
</style>
"""

# Injetando o CSS com segurança
st.markdown(css_code, unsafe_allow_html=True)

# --- CABEÇALHO ---
st.markdown("""
<div class="header-container">
    <h1 class="karv-title">AETHER KARV</h1>
    <div class="karv-subtitle">Strategic Intelligence Hub</div>
</div>
""", unsafe_allow_html=True)

menu = st.radio("", ["AUDITORIA", "FORENSE", "ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)

# AS DUAS COLUNAS PRINCIPAIS SEMPRE ATIVAS E LADO A LADO
col_ing, col_dos = st.columns(2, gap="large")

with col_ing:
    st.markdown('<div class="panel-header">INGESTÃO</div>', unsafe_allow_html=True)
    up = st.file_uploader(" ", accept_multiple_files=True, label_visibility="collapsed")
    cmd = st.text_area("COMANDO JURÍDICO ESTRATÉGICO:", key="cmd_input", placeholder="Descreva sua análise jurídica estratégica profunda...")

    if st.button("🚀 PROCESSAR AUDITORIA NEURAL"):
        if cmd:
            with st.status("🧠 Inicializando Motores Neurais AETHER KARV...", expanded=False):
                texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                resposta = aether_karv_engine(cmd, texto_arquivos)
                st.session_state.res_aether = resposta
                st.session_state.telemetria = f"Ativos Ingeridos: {num_arquivos} | Volume: {len(texto_arquivos)} bytes"
            st.rerun()
        else:
            st.warning("Insira um comando estratégico para iniciar.")

with col_dos:
    st.markdown('<div class="panel-header">DOSSIÊ</div>', unsafe_allow_html=True)
    
    if st.session_state.res_aether:
        st.markdown(f"<div class='telemetry-badge'>🛰️ TELEMETRIA: {st.session_state.telemetria}</div>", unsafe_allow_html=True)
        
        # St.code gera a caixa com o botão de "Copy" nativo
        st.code(st.session_state.res_aether, language="markdown")
        
        # Colunas menores para alinhar os botões de download e reset
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("📄 BAIXAR TXT", data=st.session_state.res_aether, file_name="auditoria_aether.txt", mime="text/plain")
        with c2:
            st.download_button("📝 BAIXAR MD", data=st.session_state.res_aether, file_name="auditoria_aether.md", mime="text/markdown")
        with c3:
            if st.button("🔄 NOVA OPERAÇÃO", use_container_width=True):
                st.session_state.res_aether, st.session_state.telemetria = None, None
                st.rerun()
                
    else:
        # TELA DE ESPERA COM A BALANÇA (Igual à imagem ideal)
        dossie_img = f'<img src="data:image/png;base64,{dossie_b64}" class="dossie-icon">' if dossie_b64 else '<div style="font-size:4rem; margin-bottom:15px;">⚖️</div>'
        st.markdown(f"""
        <div class="nexus-center">
            {dossie_img}
            <h3 style="margin:0; font-weight:900; color:#f8fafc; letter-spacing:1px; font-size: 1.1rem;">MOTOR KARV PRONTO</h3>
            <p style="color:#64748b; font-size:0.9rem; margin-top:5px; font-weight: 500;">Aguardando ingestão e comando estratégico...</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botões de enfeite desabilitados aguardando arquivo
        st.markdown("""
        <div class="download-bar">
            <div class="download-pill" style="opacity: 0.5;">📄 PDF</div>
            <div class="download-pill" style="opacity: 0.5;">📝 DOCX</div>
            <div class="download-pill" style="opacity: 0.5;">📊 XLSX</div>
            <div class="download-pill" style="opacity: 0.5;">📉 CSV</div>
        </div>
        """, unsafe_allow_html=True)
