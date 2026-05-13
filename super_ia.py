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
st.set_page_config(page_title="AETHER KARV V115 Apex", page_icon="logo.png", layout="wide", initial_sidebar_state="collapsed")

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
dossie_b64 = get_base64_image("dossie.png")

# Fundo Global
bg_css = f"background-image: url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center center; background-repeat: no-repeat; background-attachment: fixed;" if back_apex_b64 else "background-color: #020617;"

# --- 🎨 CSS APEX V115: NATIVO, ESTÁVEL E FLUIDO ---
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

/* O Básico de Tela */
.stApp {{ {bg_css} color: #f3f4f6; font-family: 'Inter', sans-serif; }}
.block-container {{ padding-top: 2rem !important; max-width: 1200px !important; margin: 0 auto; }}
[data-testid="stHeader"] {{ display: none !important; }}

/* Título */
.header-container {{ text-align: center; margin-bottom: 2rem; margin-top: 1rem; }}
.karv-title {{ margin: 0; font-weight: 900; font-size: 2.5rem; color: #ffffff; letter-spacing: -1px; text-shadow: 0 0 20px rgba(16, 185, 129, 0.5); }}
.karv-subtitle {{ color: #10b981; font-weight: 700; font-size: 0.9rem; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px; }}

/* Customização do Menu Nativo do Streamlit */
div[data-testid="stRadio"] > div {{
    display: flex; flex-direction: row; justify-content: center; gap: 15px;
    background: rgba(10, 18, 27, 0.8); border: 1px solid rgba(16,185,129,0.3);
    padding: 10px 20px; border-radius: 50px; margin: 0 auto 30px auto; width: fit-content;
    box-shadow: 0 5px 15px rgba(0,0,0,0.5);
}}
div[data-testid="stRadio"] label {{ color: #94a3b8 !important; font-weight: bold; padding: 0 10px; cursor: pointer; }}
div[data-testid="stRadio"] label[data-checked="true"] {{ color: #10b981 !important; text-shadow: 0 0 10px rgba(16,185,129,0.5); }}

/* Estilização Geral de Caixas e Textos */
[data-testid="stVerticalBlock"] > div > div > div > div > div[data-testid="stVerticalBlock"] {{
    background: rgba(10, 18, 27, 0.7);
    border: 1px solid rgba(16, 185, 129, 0.2);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    box-shadow: inset 0 0 20px rgba(16,185,129,0.05);
}}

/* Estilização do Uploader Nativo */
[data-testid="stFileUploadDropzone"] {{
    background-color: rgba(10, 18, 27, 0.5) !important;
    border: 1px dashed rgba(16, 185, 129, 0.5) !important;
    border-radius: 10px !important;
    color: #10b981 !important;
}}
[data-testid="stFileUploadDropzone"]:hover {{
    border-color: #10b981 !important;
    background-color: rgba(16, 185, 129, 0.1) !important;
}}
[data-testid="stFileUploadDropzone"] button {{
    background-color: #10b981 !important; color: #020617 !important; border: none !important; font-weight: bold !important;
}}

/* Text Area (Comando) */
.stTextArea label {{ font-size: 0.85rem !important; font-weight: 800 !important; color: #fff !important; text-transform: uppercase !important; letter-spacing: 1px; margin-bottom: 5px !important; }}
.stTextArea textarea {{ background-color: rgba(0, 0, 0, 0.5) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; color: #ffffff !important; border-radius: 8px !important; padding: 15px !important; }}
.stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.3) !important; outline: none !important; }}

/* Botão Principal Verde */
.stButton > button {{
    background: linear-gradient(90deg, #10b981, #34d399) !important; border-radius: 50px !important; font-weight: 900 !important; color: #020617 !important;
    text-transform: uppercase !important; letter-spacing: 1px !important; padding: 15px !important; border: none !important; width: 100% !important; margin-top: 15px !important; transition: all 0.3s ease;
}}
.stButton > button:hover {{ transform: translateY(-2px); filter: brightness(1.1); box-shadow: 0 10px 20px rgba(16, 185, 129, 0.4) !important; }}

/* Elementos do Dossiê */
.nexus-center {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 250px; text-align: center; }}
.dossie-icon {{ width: 90px; height: 90px; object-fit: contain; margin-bottom: 15px; filter: drop-shadow(0 0 20px rgba(16, 185, 129, 0.6)); }}
.karv-response {{ background: rgba(0, 0, 0, 0.6); border-left: 3px solid #10b981; padding: 15px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; margin-top: 10px; font-size: 0.85rem; text-align: left; overflow-y: auto; max-height: 300px; color: #cbd5e1; }}
.telemetry-badge {{ display: inline-block; background: rgba(16, 185, 129, 0.1); color: #34d399; font-size: 0.8rem; padding: 5px 15px; border-radius: 12px; margin-bottom: 10px; border: 1px solid rgba(16, 185, 129, 0.3); font-weight: bold; }}

/* Cabeçalhos Nativos das Colunas */
h3 {{ color: #ffffff !important; font-weight: 800 !important; font-size: 1.1rem !important; letter-spacing: 1px; text-transform: uppercase; border-bottom: 1px solid rgba(16,185,129,0.3); padding-bottom: 8px; margin-bottom: 20px !important; }}
</style>
""", unsafe_allow_html=True)

# --- INÍCIO DA INTERFACE ---
st.markdown("""
<div class="header-container">
    <h1 class="karv-title">AETHER KARV</h1>
    <div class="karv-subtitle">Strategic Intelligence Hub</div>
</div>
""", unsafe_allow_html=True)

menu = st.radio("Navegação Tática", ["🛡️ AUDITORIA", "🔍 FORENSE", "⚙️ ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)

col_ing, col_dos = st.columns(2, gap="large")

with col_ing:
    with st.container():
        st.markdown("### INGESTÃO")
        up = st.file_uploader("Arquivos Base (PDF, DOCX, XLSX, CSV)", accept_multiple_files=True, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        cmd = st.text_area("COMANDO JURÍDICO ESTRATÉGICO:", key="cmd_input", placeholder="Descreva sua análise jurídica profunda...")

        if st.button("🚀 PROCESSAR AUDITORIA NEURAL"):
            if cmd:
                with st.status("🧠 Inicializando Motores AETHER KARV...", expanded=False):
                    texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                    resposta = aether_karv_engine(cmd, texto_arquivos)
                    st.session_state.res_aether = resposta
                    st.session_state.telemetria = f"Ativos Ingeridos: {num_arquivos} | Volume: {len(texto_arquivos)} bytes"
                st.rerun()
            else:
                st.warning("Insira um comando estratégico para iniciar.")

with col_dos:
    with st.container():
        st.markdown("### DOSSIÊ")
        
        if st.session_state.res_aether:
            st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
            if st.session_state.telemetria:
                st.markdown(f"<div class='telemetry-badge'>🛰️ TELEMETRIA: {st.session_state.telemetria}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='karv-response'>{st.session_state.res_aether}</div>", unsafe_allow_html=True)
            if st.button("🔄 NOVA OPERAÇÃO", key="btn_nova"):
                st.session_state.res_aether, st.session_state.telemetria = None, None
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            dossie_img = f'<img src="data:image/png;base64,{dossie_b64}" class="dossie-icon">' if dossie_b64 else '<div style="font-size:4rem; margin-bottom:15px;">⚖️</div>'
            st.markdown(f"""
            <div class="nexus-center">
                {dossie_img}
                <h4 style="margin:0; font-weight:900; color:#f8fafc; letter-spacing:1px;">MOTOR KARV PRONTO</h4>
                <p style="color:#64748b; font-size:0.9rem; margin-top:5px;">Aguardando ingestão e comando...</p>
            </div>
            """, unsafe_allow_html=True)
