import streamlit as st
import pandas as pd
import os, time, base64
import docx2txt

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO & LIBS (Inferred History) ---
try:
    from groq import Groq
except ImportError:
    pass

# --- ⚙️ CONFIGURAÇÃO DE AMBIENTE ---
# Layout "wide" é obrigatório para UI Fusion
st.set_page_config(page_title="AETHER KARV V110 Apex", page_icon="logo.png", layout="wide", initial_sidebar_state="collapsed")

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

# --- ⚡ EXTRATOR NEXUS (Data Ingest History) ---
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

# --- ⚡ MOTOR AETHER KARV (Groq History) ---
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
        # Fallback offline para testes
        time.sleep(2.5) 
        return f"**AUDITORIA SINTÉTICA (MODO OFFLINE):**\nO sistema processou o comando `{comando[:20]}...` com sucesso."

# --- 🎨 CARREGAMENTO VISUAL ---
back_apex_b64 = get_base64_image("back_apex.png")
upload_b64 = get_base64_image("upload.png")
dossie_b64 = get_base64_image("dossie.png")

bg_css = f"background-image: url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;" if back_apex_b64 else "background-color: #020617;"

# --- 🎨 CSS APEX V110 FUSION ---
# Este CSS é agressivo. Ele remove todo o padding padrão do Streamlit
# e força a interface a ser o cockpit tático.
css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

/* RESET E BACKGROUND GLOBAL */
.stApp {{ {bg_css} color: #f3f4f6; font-family: 'Inter', sans-serif; overflow-x: hidden; }}
.reportview-container .main .block-container {{ padding: 0 !important; max-width: 100% !important; }}
[data-testid="stHeader"] {{ display: none !important; }}

/* TÍTULOS (Hardcoded na imagem, então só precisamos remover o padding do topo) */
.block-container {{ padding-top: 13rem !important; }}

/* ENGANHARIA DE BOTOES E INPUTS TÁTICOS (Fusão com a imagem) */

/* 1. SELETOR DE MÓDULOS TÁTICOS (Top Tabs invisíveis, native stylized) */
div[role="radiogroup"] {{ display: flex !important; flex-direction: row !important; justify-content: center !important; gap: 15px !important; background: rgba(10, 18, 27, 0.7) !important; border-radius: 50px !important; padding: 10px 20px !important; border: 1px solid rgba(16,185,129,0.3) !important; width: fit-content !important; margin: 0 auto 30px auto !important; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
div[role="radiogroup"] label div[dir="auto"]:first-child, div[role="radio"] div:first-child, span[data-baseweb="radio"] {{ display: none !important; }}
div[data-testid="stRadio"] label {{ background-color: transparent !important; color: #94a3b8 !important; padding: 8px 25px !important; margin: 0 !important; cursor: pointer; border-radius: 50px; display: flex; align-items: center; justify-content: center; transition: 0.3s; }}
div[data-testid="stRadio"] label:has(input:checked) {{ background: linear-gradient(90deg, #10b981, #34d399) !important; color: #020617 !important; font-weight: 800 !important; box-shadow: 0 0 15px rgba(16, 185, 129, 0.4) !important; }}
div[data-testid="stRadio"] label p {{ font-size: 1rem !important; font-weight: 700 !important; margin: 0 !important; }}

/* 2. PAINÉIS LATERAIS DE DADOS (Glassmorphism Fusion) */
[data-testid="column"] {{
    background: rgba(10, 18, 27, 0.7) !important;
    border: 1px solid rgba(16, 185, 129, 0.2) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    backdrop-filter: blur(10px);
    height: 100%;
}}

/* 3. UPLOADER TÁTICO (Nexus Ingest) */
[data-testid="stFileUploadDropzone"] {{
    background-color: transparent !important;
    border: 2px dashed rgba(16, 185, 129, 0.4) !important;
    border-radius: 10px !important;
    color: #10b981 !important;
}}
[data-testid="stFileUploadDropzone"] svg {{ fill: #10b981 !important; }}
[data-testid="stFileUploadDropzone"] div[data-testid="stText"] {{ color: #94a3b8 !important; font-weight: 600; }}

/* 4. TEXT AREA (Comando Tático) */
.stTextArea label {{ font-size: 0.85rem !important; font-weight: 800 !important; color: #fff !important; text-transform: uppercase !important; letter-spacing: 1px; margin-bottom: 5px !important; }}
.stTextArea textarea {{ background-color: rgba(7, 11, 20, 0.8) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; color: #ffffff !important; border-radius: 8px !important; padding: 15px !important; height: 120px !important; }}
.stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.3) !important; outline: none !important; }}

/* 5. BOTÕES DE AÇÃO (Apex Neon Style) */
.stButton > button {{
    background: linear-gradient(90deg, #10b981, #34d399) !important;
    border-radius: 50px !important; font-weight: 900 !important; color: #020617 !important;
    text-transform: uppercase !important; letter-spacing: 1px !important; padding: 12px !important; border: none !important; width: 100% !important; margin-top: 15px !important; transition: all 0.3s ease;
}}
.stButton > button:hover {{ transform: translateY(-2px); filter: brightness(1.1); box-shadow: 0 10px 20px rgba(16, 185, 129, 0.4) !important; }}

/* 6. RESULTADOS E DOSSIÊ (Output) */
.karv-response {{ background: rgba(7, 11, 20, 0.8); border-left: 3px solid #10b981; padding: 15px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; margin-top: 10px; font-size: 0.9rem; text-align: left; overflow-y: auto; max-height: 350px; }}
.telemetry-badge {{ display: inline-block; background: rgba(16, 185, 129, 0.1); color: #34d399; font-size: 0.8rem; padding: 5px 15px; border-radius: 12px; margin-bottom: 10px; border: 1px solid rgba(16, 185, 129, 0.3); font-weight: bold; }}

/* 7. CUSTOM HEADER FOR COLUMNS */
.panel-header {{ color: #ffffff; font-weight: 800; font-size: 1rem; letter-spacing: 1px; margin-bottom: 10px; text-transform: uppercase; border-bottom: 1px solid rgba(16,185,129,0.3); padding-bottom: 5px; }}

</style>
"""

# Injetando o CSS com segurança
st.markdown(css_code, unsafe_allow_html=True)

# --- INÍCIO DA INTERFACE TÁTICA ---
# Como a logo e nome já estão no fundo, pulamos direto para os controles

# 1. SELETOR DE MÓDULOS TÁTICOS (Top Bar)
# Alinhado sobre a área de scanner central
menu = st.radio("Seletor", ["🛡️ AUDITORIA", "🔍 FORENSE", "⚙️ ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)

st.markdown("<br>", unsafe_allow_html=True) # Respiro visual

# 2. COLUNAS TÁTICAS (Simetria perfeita)
col_ing, col_dos = st.columns(2, gap="large")

# --- COLUNA ESQUERDA: INGESTÃO E COMANDO ---
with col_ing:
    st.markdown('<div class="panel-header">INGESTÃO NEXUS</div>', unsafe_allow_html=True)
    # st.markdown("### INGESTÃO NEXUS")
    # File Uploader Tático (Sincronizado visualmente)
    up = st.file_uploader("Arquivos Base", accept_multiple_files=True, label_visibility="collapsed")
    
    st.markdown('<div class="panel-header">COMANDO JURÍDICO</div>', unsafe_allow_html=True)
    # st.markdown("### COMANDO JURÍDICO")
    # Text Area
    cmd = st.text_area("Descreva sua análise jurídica estratégica profunda...", key="cmd_input", label_visibility="collapsed")

    # Botão de Ação
    if st.button("🚀 PROCESSAR AUDITORIA NEURAL"):
        if cmd:
            with st.status("🧠 Inicializando Motores AETHER KARV...", expanded=False):
                # Executando funcionalidade histórica Nexus
                texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                # Executando funcionalidade histórica Groq
                resposta = aether_karv_engine(cmd, texto_arquivos)
                # Salvando Estado
                st.session_state.res_aether = resposta
                st.session_state.telemetria = f"Ativos Ingeridos: {num_arquivos} | Volume: {len(texto_arquivos)} bytes"
            st.rerun() # Refresh tático
        else:
            st.warning("⚠️ Insira um comando estratégico para iniciar a operação.")

# --- COLUNA DIREITA: DOSSIÊ E TELEMETRIA ---
with col_dos:
    st.markdown('<div class="panel-header">DOSSIÊ CONCLUÍDO</div>', unsafe_allow_html=True)
    # st.markdown("### DOSSIÊ CONCLUÍDO")
    
    if st.session_state.res_aether:
        st.markdown(f"<div class='telemetry-badge'>🛰️ TELEMETRIA: {st.session_state.telemetria}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='karv-response'>{st.session_state.res_aether}</div>", unsafe_allow_html=True)
        # st.code(st.session_state.res_aether, language="markdown")
        if st.button("🔄 NOVA OPERAÇÃO"):
            st.session_state.res_aether, st.session_state.telemetria = None, None
            st.rerun()
    else:
        # Estado Vazio (Aguardando) com ícone tático
        st.markdown("<div style='text-align:center; padding-top: 50px; opacity: 0.5;'>", unsafe_allow_html=True)
        st.markdown(f"<img src='data:image/png;base64,{dossie_b64}' style='width: 100px; margin-bottom: 20px;' >" if dossie_b64 else "⚖️", unsafe_allow_html=True)
        st.markdown("<h4>MOTOR KARV EM ESPERA</h4>", unsafe_allow_html=True)
        st.markdown("<p>Aguardando ingestão e comando...</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
