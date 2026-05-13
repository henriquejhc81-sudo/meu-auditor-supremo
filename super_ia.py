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
st.set_page_config(page_title="AETHER KARV V112 Apex", page_icon="logo.png", layout="wide", initial_sidebar_state="collapsed")

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

# --- 🎨 CSS APEX V112: ANIQUILAÇÃO DE ARTEFATOS DO STREAMLIT ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    /* RESET E BACKGROUND */
    .stApp {{ {bg_css} color: #f3f4f6; font-family: 'Inter', sans-serif; overflow: hidden; }}
    .block-container {{ padding-top: 1rem !important; padding-bottom: 0rem !important; max-width: 65rem !important; margin: 0 auto !important; height: 100vh; display: flex; flex-direction: column; justify-content: center; }}
    [data-testid="stHeader"] {{ display: none !important; }}

    /* TÍTULO REINSERIDO E CENTRALIZADO */
    .header-container {{ text-align: center; margin-bottom: 15px; margin-top: 40px; }}
    .karv-title {{ margin: 0; font-weight: 900; font-size: 2.2rem; color: #ffffff; letter-spacing: -1px; text-shadow: 0 0 15px rgba(16, 185, 129, 0.4); line-height: 1; }}
    .karv-subtitle {{ color: #10b981; font-weight: 700; font-size: 0.85rem; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px; }}

    /* MENU CÁPSULAS (SEM BOLINHAS) */
    div[role="radiogroup"] {{ display: flex !important; flex-direction: row !important; justify-content: center !important; gap: 5px !important; background: rgba(10, 18, 27, 0.7) !important; border-radius: 50px !important; padding: 5px !important; border: 1px solid rgba(16,185,129,0.3) !important; width: fit-content !important; margin: 0 auto 15px auto !important; }}
    
    /* Ataque profundo às bolinhas de seleção */
    div[data-testid="stRadio"] div[role="radio"] div:first-of-type {{ display: none !important; }}
    .stRadio [data-baseweb="radio"] > div:first-child {{ display: none !important; }}
    
    div[data-testid="stRadio"] label {{ background-color: transparent !important; color: #94a3b8 !important; padding: 8px 25px !important; margin: 0 !important; cursor: pointer; border-radius: 50px; display: flex; align-items: center; justify-content: center; }}
    div[data-testid="stRadio"] label:has(input:checked) {{ background: linear-gradient(90deg, #10b981, #34d399) !important; color: #020617 !important; font-weight: 800 !important; box-shadow: 0 0 15px rgba(16, 185, 129, 0.5) !important; }}
    div[data-testid="stRadio"] label p {{ font-size: 0.9rem !important; font-weight: 700 !important; margin: 0 !important; display: flex !important; align-items: center !important; }}

    /* ÍCONES DO MENU */
    div[data-testid="stRadio"] label:nth-child(1) p::before {{ content: ''; display: inline-block; width: 16px; height: 16px; margin-right: 6px; background-image: url('data:image/png;base64,{auditoria_b64}'); background-size: contain; background-repeat: no-repeat; }}
    div[data-testid="stRadio"] label:nth-child(2) p::before {{ content: ''; display: inline-block; width: 16px; height: 16px; margin-right: 6px; background-image: url('data:image/png;base64,{forense_b64}'); background-size: contain; background-repeat: no-repeat; }}
    div[data-testid="stRadio"] label:nth-child(3) p::before {{ content: ''; display: inline-block; width: 16px; height: 16px; margin-right: 6px; background-image: url('data:image/png;base64,{engenharia_b64}'); background-size: contain; background-repeat: no-repeat; }}
    div[data-testid="stRadio"] label p::before {{ filter: drop-shadow(0px 0px 3px rgba(16, 185, 129, 0.8)); }}
    div[data-testid="stRadio"] label:has(input:checked) p::before {{ filter: brightness(0) !important; }}

    /* PAINÉIS DE VIDRO TÁTICO */
    [data-testid="column"] {{ background: rgba(10, 18, 27, 0.6) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; border-radius: 12px !important; padding: 15px !important; backdrop-filter: blur(10px); }}
    .panel-header {{ color: #ffffff; font-weight: 800; font-size: 0.95rem; letter-spacing: 1px; margin-bottom: 10px; text-transform: uppercase; border-bottom: 1px solid rgba(16,185,129,0.3); padding-bottom: 5px; }}

    /* UPLOADER: ATAQUE ABSOLUTO À UI NATIVA */
    .stFileUploader {{ min-height: 90px !important; }}
    [data-testid="stFileUploadDropzone"] {{ 
        background-color: transparent !important; border: 2px dashed rgba(16, 185, 129, 0.4) !important; 
        border-radius: 10px !important; position: relative; overflow: hidden; height: 90px !important; min-height: 90px !important; padding: 0 !important;
    }}
    [data-testid="stFileUploadDropzone"]:hover {{ border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.05) !important; }}
    
    /* Força brutal para ocultar o botão, ícone e texto originais */
    .stFileUploader section > button, 
    .stFileUploader section > span, 
    .stFileUploader section > small, 
    .stFileUploader section > svg, 
    .stFileUploader div[data-testid="stText"] {{ display: none !important; opacity: 0 !important; }}
    
    /* Desenhando nossa UI de Upload Compacta */
    [data-testid="stFileUploadDropzone"]::before {{
        content: ''; position: absolute; top: 15px; left: 50%; transform: translateX(-50%);
        background-image: url('data:image/png;base64,{upload_b64}'); background-size: contain; background-repeat: no-repeat; background-position: center; width: 30px; height: 30px; z-index: 1; pointer-events: none;
    }}
    [data-testid="stFileUploadDropzone"]::after {{
        content: 'ARRASTE ARQUIVOS OU CLIQUE (PDF, DOCX, XLSX, CSV)';
        position: absolute; bottom: 15px; left: 0; right: 0; text-align: center; white-space: pre-wrap; color: #8b9eb3; font-size: 0.75rem; font-weight: 600; z-index: 1; pointer-events: none;
    }}

    /* CAIXA DE COMANDO (TEXT AREA) COMPACTA */
    .stTextArea label {{ font-size: 0.75rem !important; margin-bottom: 5px !important; margin-top: 10px !important; }}
    .stTextArea textarea {{ background-color: rgba(7, 11, 20, 0.8) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; color: #ffffff !important; font-size: 0.85rem !important; border-radius: 8px !important; padding: 10px !important; height: 80px !important; min-height: 80px !important; }}
    .stTextArea textarea:focus {{
