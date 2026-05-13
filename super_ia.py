import streamlit as st
import os, base64

# --- ⚙️ CONFIGURAÇÃO DE AMBIENTE ---
# Layout "wide" é obrigatório para UI Fusion
st.set_page_config(page_title="AETHER KARV V120 Apex", page_icon="logo.png", layout="wide", initial_sidebar_state="collapsed")

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO & LIBS (Feature Lock History) ---
# Garante que as funções históricas não foram perdidas
try:
    from groq import Groq
except ImportError:
    st.error("Engine Groq não encontrada.")
import pandas as pd
import time, docx2txt

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Carrega sua imagem ideal como referência e o fundo limpo
back_apex_clean_b64 = get_base64_image("back_apex_clean.png")

# Ícones e Imagens Táticas (Histórico V100-V117)
# auditoria_b64 = get_base64_image("auditoria_link.png") # Not used in V120 Apex
# forense_b64 = get_base64_image("forense_link.png") # Not used in V120 Apex
# engenharia_b64 = get_base64_image("engenharia_link.png") # Not used in V120 Apex
# upload_b64 = get_base64_image("upload.png") # Not used in V120 Apex
# dossie_b64 = get_base64_image("dossie.png") # Not used in V120 Apex

# --- 🧠 ESTADO DA SESSÃO (Memória Tática) ---
if "cmd_input" not in st.session_state: st.session_state.cmd_input = ""
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "telemetria" not in st.session_state: st.session_state.telemetria = None

# --- 🎨 CSS APEX V120: UI FUSION - GEOMETRIA SINCRONIZADA ---
# Usamos positioning absoluta para criar 'div' invisíveis sobre o seu desenho ideal
css_fusion = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

.stApp {{ background-color: #020617; color: #f3f4f6; font-family: 'Inter', sans-serif; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
[data-testid="stHeader"] {{ display: none !important; }}

/* CONTÊINER MESTRE DO COCKPIT */
.cockpit-fusion-master {{
    position: relative;
    width: 100vw;
    height: 100vh;
    background-image: url('data:image/png;base64,{back_apex_clean_b64}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    overflow: hidden;
}}

/* 1. CABEÇALHO EM CÁPSULA (Simetria Sincronizada) */
.capsule-header-overlay {{
    position: absolute;
    top: 5vh;
    left: 10vw;
    right: 10vw;
    height: 10vh;
    background: rgba(10, 18, 27, 0.6) !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
    border-radius: 50px;
    backdrop-filter: blur(12px);
    display: flex;
    align-items: center;
    justify-content: space-around; /* Sincroniza com as cápsulas do menu */
    padding: 0 5vw;
    z-index: 10;
}}

.karv-title {{ margin: 0; font-weight: 900; font-size: 2.2rem; color: #ffffff; letter-spacing: -1px; text-shadow: 0 0 15px rgba(16, 185, 129, 0.4); line-height: 1; }}
.karv-subtitle {{ color: #10b981; font-weight: 700; font-size: 0.8rem; letter-spacing: 3px; text-transform: uppercase; margin-top: 2px; }}

/* MENU CÁPSULAS (Sincronizado com o desenho ideal) */
div[role="radiogroup"] {{ display: flex !important; flex-direction: row !important; justify-content: center !important; gap: 0px !important; background: transparent !important; border: none !important; padding: 0 !important; border-radius: 0 !important; width: fit-content !important; margin: 0 !important; box-shadow: none; }}
div[role="radiogroup"] label div[dir="auto"]:first-child, div[role="radio"] div:first-child, span[data-baseweb="radio"] {{ display: none !important; }}
div[data-testid="stRadio"] label {{ background-color: transparent !important; color: #94a3b8 !important; padding: 6px 18px !important; margin: 0 !important; cursor: pointer; border-radius: 50px; display: flex; align-items: center; justify-content: center; transition: 0.3s; }}
div[data-testid="stRadio"] label:has(input:checked) {{ background: linear-gradient(90deg, #10b981, #34d399) !important; color: #020617 !important; font-weight: 800 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.4) !important; }}
div[data-testid="stRadio"] label p {{ font-size: 0.8rem !important; font-weight: 700 !important; margin: 0 !important; display: flex !important; align-items: center !important; }}

/* 2. PAINÉIS DE VIDRO TÁTICO (NEXUS INGESTER & DOSSIÊ TÁTICO) */
/* Os painéis são contêineres nativos posicionados milimetricamente */
[data-testid="column"] {{
    background: rgba(10, 18, 27, 0.6) !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
    border-radius: 12px;
    backdrop-filter: blur(12px);
    padding: 2.5vh 2.5vw;
    height: 60vh;
}}

/* POSICIONAMENTO DINÂMICO DOS PAINÉIS */
.ingestao-panel-pos {{ position: absolute; top: 20vh; left: 10vw; width: 35vw; }}
.dossie-panel-pos {{ position: absolute; top: 20vh; right: 10vw; width: 35vw; }}

/* TÍTULOS DOS PAINÉIS */
.panel-header {{ color: #ffffff; font-weight: 800; font-size: 1rem; letter-spacing: 1px; margin-bottom: 2vh; text-transform: uppercase; border-bottom: 1px solid rgba(16,185,129,0.3); padding-bottom: 0.5vh; }}

/* 3. NEXUS INGESTER (Painel Esquerdo - Ingestão) */
/* Área de Upload Tática SINCRONIZADA */
.nexus-upload-overlay {{
    position: absolute;
    top: 6vh;
    left: 2.5vw;
    width: 30vw;
    height: 25vh;
    border: 2px dashed rgba(16, 185, 129, 0.4) !important;
    border-radius: 8px !important;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 5;
    pointer-events: auto; /* Permite cliques */
}}

/* Força bruta contra textos nativos do FileUploader nativo */
.stFileUploader {{ min-height: 25vh !important; margin-bottom: 0 !important; }}
[data-testid="stFileUploadDropzone"] {{ background-color: transparent !important; border: none !important; overflow: hidden; height: 100% !important; padding: 0 !important; }}
[data-testid="stFileUploadDropzone"] svg {{ fill: #10b981 !important; }}
[data-testid="stFileUploadDropzone"] div[data-testid="stText"] {{ color: #94a3b8 !important; font-weight: 600; font-size: 0.8rem; }}

/* Esconde o botão e textos feios */
[data-testid="stFileUploadDropzone"] button, [data-testid="stFileUploadDropzone"] small {{ display: none !important; }}

/* COMANDO JURÍDICO SINCRONIZADO */
.nexus-cmd-overlay {{
    position: absolute;
    top: 33vh;
    left: 2.5vw;
    width: 30vw;
    height: 15vh;
    z-index: 5;
    pointer-events: auto; /* Permite cliques */
}}

/* st.text_area SINCRONIZADA */
.stTextArea label {{ font-size: 0.8rem !important; margin-bottom: 5px !important; font-weight: 800 !important; letter-spacing: 1px; color: #fff !important; text-transform: uppercase; }}
.stTextArea textarea {{ background-color: rgba(7, 11, 20, 0.8) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; color: #ffffff !important; font-size: 0.85rem !important; border-radius: 8px !important; padding: 10px !important; height: 10vh !important; min-height: 10vh !important; resize: none; }}
.stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2) !important; outline: none !important; }}

/* BOTÃO DE PROCESSAR SINCRONIZADO */
.stButton > button {{
    background: linear-gradient(90deg, #10b981, #34d399) !important; border-radius: 50px !important; font-weight: 900 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 1px !important; padding: 10px !important; border: none !important; font-size: 0.9rem !important; width: 100% !important; margin-top: 15vh !important; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.2) !important;
}}
.stButton > button:hover {{ transform: translateY(-1px); filter: brightness(1.1); box-shadow: 0 6px 15px rgba(16, 185, 129, 0.4) !important; }}

/* ÍCONES DE FORMATO (PDF, DOCX, XLSX, CSV) Estáticos */
.format-pill-overlay {{
    position: absolute;
    top: 25vh;
    left: 3.5vw;
    width: 28vw;
    display: flex;
    justify-content: center;
    gap: 15px;
    opacity: 0.6;
    pointer-events: none; /* Sincroniza com o desenho ideal */
}}
.format-pill {{ background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(16,185,129,0.3); border-radius: 50px; padding: 4px 12px; color: #cbd5e1; font-size: 0.75rem; font-weight: 600; }}

/* 4. DOSSIÊ TÁTICO (Painel Direito - Resultado) */
/* st.code fornece uma caixa preta de código com o botão de "Copiar" nativo */
[data-testid="stCodeBlock"] {{ background: rgba(0, 0, 0, 0.6) !important; border: 1px solid rgba(16,185,129,0.5) !important; border-radius: 8px !important; margin-bottom: 2vh; height: 35vh; }}

/* TELEMETRIA */
.telemetry-badge {{ display: inline-block; background: rgba(16, 185, 129, 0.1); color: #34d399; font-size: 0.75rem; padding: 4px 12px; border-radius: 10px; margin-bottom: 1vh; border: 1px solid rgba(16, 185, 129, 0.3); font-weight: bold; width: 100%; text-align: center; }}

/* BARRA DE DOWNLOADS TIPO PILLS (Download Pills) */
/* st.download_button SINCRONIZADA */
[data-testid="stDownloadButton"] button, .stButton > button[key="btn_reset"] {{
    background: rgba(30, 41, 59, 0.4) !important; border: 1px solid rgba(16,185,129,0.3) !important; border-radius: 50px !important; padding: 4px 12px !important; color: #cbd5e1 !important; font-size: 0.75rem !important; font-weight: 600 !important; transition: 0.3s !important; box-shadow: none !important; margin: 0 !important; height: auto !important; width: auto !important;
}}
[data-testid="stDownloadButton"] button:hover, .stButton > button[key="btn_reset"]:hover {{ border-color: #10b981 !important; color: #10b981 !important; background: rgba(16, 185, 129, 0.1) !important; }}

/* ESTADO VAZIO SINCRONIZADO */
.empty-dossie-overlay {{
    position: absolute;
    top: 10vh;
    left: 2.5vw;
    width: 30vw;
    text-align: center;
    opacity: 0.6;
    pointer-events: none; /* Sincroniza com o desenho ideal */
}}
.empty-icon {{ font-size: 4rem; margin-bottom: 2vh; }}

/* 5. EMBLEMA CENTRAL Estático */
.central-emblem-overlay {{
    position: absolute;
    top: 40vh;
    left: 45vw;
    width: 10vw;
    height: 20vh;
    z-index: 1;
    opacity: 0.8;
    pointer-events: none; /* Sincroniza com o desenho ideal */
}}
.central-emblem-img {{ width: 100%; height: 100%; object-fit: contain; filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.6)); }}
</style>
"""

# Injeta a Camada de Fusão Apex
st.markdown(css_fusion, unsafe_allow_html=True)

# --- INÍCIO DO COCKPIT TÁTICO APEX ---
st.markdown('<div class="cockpit-fusion-master">', unsafe_allow_html=True)

# 1. CABEÇALHO EM CÁPSULA (Simetria Sincronizada)
st.markdown("""
<div class="capsule-header-overlay">
    <div style="text-align: left;">
        <h1 class="karv-title">AETHER KARV</h1>
        <div class="karv-subtitle">Strategic Intelligence Hub</div>
    </div>
""", unsafe_allow_html=True)

# Menu de Rádio (Native Streamlit Radio sincronizado)
menu = st.radio("", ["AUDITORIA", "FORENSE", "ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)

st.markdown("</div>", unsafe_allow_html=True) # Fecha capsule-header-overlay

# 2. PAINÉIS DE VIDRO TÁTICO (NEXUS INGESTER & DOSSIÊ TÁTICO)
col_ing, col_dos = st.columns(2, gap="large")

with col_ing:
    st.markdown('<div class="panel-header ingestao-panel-pos">NEXUS INGESTER</div>', unsafe_allow_html=True)
    
    # 3. NEXUS INGESTER (Painel Esquerdo - Ingestão)
    # Área de Upload SINCRONIZADA (File Uploader Nativo)
    st.markdown('<div class="nexus-upload-overlay">', unsafe_allow_html=True)
    up = st.file_uploader("ARRASTE ARQUIVOS OU CLIQUE PARA UPLOAD", accept_multiple_files=True, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Ícones de Formato (PDF, DOCX, XLSX, CSV) Estáticos
    st.markdown("""
    <div class="format-pill-overlay">
        <div class="format-pill">📄 PDF</div>
        <div class="format-pill">📝 DOCX</div>
        <div class="format-pill">📊 XLSX</div>
        <div class="format-pill">📉 CSV</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Área de Comando Jurídico SINCRONIZADA (st.text_area Nativa)
    st.markdown('<div class="nexus-cmd-overlay">', unsafe_allow_html=True)
    cmd = st.text_area("COMANDO JURÍDICO ESTRATÉGICO:", key="cmd_input", height=120, placeholder="Ex: Analise os documentos e aponte inconsistências jurídicas...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botão de Processar SINCRONIZADO
    if st.button("🚀 PROCESSAR AUDITORIA", key="btn_auditoria"):
        if cmd:
            with st.status("🧠 Inicializando Motores Táticos AETHER KARV...", expanded=False):
                texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                resposta = aether_karv_engine(cmd, texto_arquivos)
                st.session_state.res_aether = resposta
                st.session_state.telemetria = f"Ativos Ingeridos: {num_arquivos} | Volume Tático Processado: {len(texto_arquivos)} bytes"
            st.rerun()
        else:
            st.warning("⚠️ Insira um comando estratégico para iniciar a operação.")

with col_dos:
    st.markdown('<div class="panel-header dossie-panel-pos">DOSSIÊ TÁTICO</div>', unsafe_allow_html=True)
    
    # 4. DOSSIÊ TÁTICO (Painel Direito - Resultado)
    if st.session_state.res_aether:
        # Dossiê Preenchido
        # Mostra Telemetria
        st.markdown(f"<div class='telemetry-badge'>🛰️ TELEMETRIA: {st.session_state.telemetria}</div>", unsafe_allow_html=True)
        
        # st.code fornece uma caixa preta de código com o botão de "Copiar" nativo
        st.code(st.session_state.res_aether, language="markdown")
        
        # downloads pills SINCRONIZADA
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1.5, 1.5, 1])
        with c1:
            st.download_button("📄 TXT", data=st.session_state.res_aether, file_name="aether_dossier.txt", mime="text/plain", use_container_width=True)
        with c2:
            st.download_button("📝 MD", data=st.session_state.res_aether, file_name="aether_dossier.md", mime="text/markdown", use_container_width=True)
        with c3:
            if st.button("🔄 RESET", key="btn_reset", use_container_width=True):
                st.session_state.res_aether = None
                st.session_state.telemetria = None
                st.rerun()
                
    else:
        # Estado Vazio (Aguardando) SINCRONIZADO
        st.markdown('<div class="empty-dossie-overlay">', unsafe_allow_html=True)
        st.markdown("""
            <div class="empty-icon">⚖️</div>
            <h4 style="margin:0; font-weight:900; color:#f8fafc; letter-spacing:1px; font-size: 1.1rem;">MOTOR KARV EM ESPERA</h4>
            <p style="color:#64748b; font-size:0.9rem; margin-top:5px; font-weight: 500;">Aguardando ingestão tática e comando...</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 5. EMBLEMA CENTRAL Estático
# st.markdown('<div class="central-emblem-overlay">', unsafe_allow_html=True)
# central_emblem_img_b64 = back_apex_clean_b64 # Placeholder for emblem
# st.markdown(f'<img src="data:image/png;base64,{central_emblem_img_b64}" class="central-emblem-img">', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# Fecha o Cockpit Master
st.markdown('</div>', unsafe_allow_html=True)
