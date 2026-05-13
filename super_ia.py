import streamlit as st
import pandas as pd
import os, time, base64
import docx2txt

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO ---
try:
    from groq import Groq
except ImportError:
    pass

st.set_page_config(page_title="AETHER KARV V119", page_icon="logo.png", layout="wide", initial_sidebar_state="collapsed")

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

if "cmd_input" not in st.session_state: st.session_state.cmd_input = ""
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "telemetria" not in st.session_state: st.session_state.telemetria = None

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
                model="llama3-70b-8192", temperature=0.2,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ FALHA NO LINK NEURAL GROQ: {str(e)}"
    else:
        time.sleep(2.5) 
        return f"**AUDITORIA SINTÉTICA (MODO OFFLINE):**\nO sistema processou o comando `{comando[:20]}...` com sucesso."

# --- 🎨 IMAGENS ---
back_apex_b64 = get_base64_image("back_apex.png")
dossie_b64 = get_base64_image("dossie.png")

bg_css = f"background-image: url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center top; background-repeat: no-repeat; background-attachment: fixed;" if back_apex_b64 else "background-color: #020617;"

# --- 🎨 CSS APEX V119: ALINHAMENTO FANTASMA ---
css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

.stApp {{ {bg_css} color: #f3f4f6; font-family: 'Inter', sans-serif; overflow-x: hidden; }}

/* ⚠️ ATENÇÃO COMANDANTE: AJUSTE O NUMERO ABAIXO PARA SUBIR OU DESCER TUDO NA TELA */
.block-container {{ padding-top: 11rem !important; max-width: 1200px !important; margin: 0 auto; padding-bottom: 0 !important; }}

[data-testid="stHeader"] {{ display: none !important; }}

/* ESCONDE A PALAVRA "Seletor" DO MENU */
div[data-testid="stRadio"] > label {{ display: none !important; }}

/* MENU CÁPSULAS (Sem fundo, para encaixar na cápsula do seu desenho) */
div[role="radiogroup"] {{ 
    display: flex !important; flex-direction: row !important; justify-content: center !important; gap: 20px !important; 
    background: transparent !important; border: none !important; box-shadow: none !important; 
    width: fit-content !important; margin: 0 auto 60px auto !important; /* 60px empurra os painéis para baixo */
}}
div[role="radiogroup"] label div[dir="auto"]:first-child, div[role="radio"] div:first-child, span[data-baseweb="radio"] {{ display: none !important; }}

/* BOTÕES DO MENU (Verde sutil quando clicado) */
div[data-testid="stRadio"] label {{ background-color: transparent !important; color: #8b9eb3 !important; padding: 8px 30px !important; margin: 0 !important; cursor: pointer; border-radius: 50px; display: flex; align-items: center; justify-content: center; transition: 0.3s; }}
div[data-testid="stRadio"] label:has(input:checked) {{ background: rgba(16, 185, 129, 0.15) !important; border: 1px solid #10b981 !important; color: #10b981 !important; font-weight: 800 !important; box-shadow: 0 0 15px rgba(16, 185, 129, 0.3) !important; }}
div[data-testid="stRadio"] label p {{ font-size: 1rem !important; font-weight: 700 !important; margin: 0 !important; display: flex !important; align-items: center !important; text-transform: uppercase; letter-spacing: 1px; }}

/* ⚠️ A MÁGICA: COLUNAS INVISÍVEIS PARA NÃO SOBREPOR SEU DESENHO ⚠️ */
[data-testid="column"] {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    backdrop-filter: none !important;
    padding: 20px 45px !important; /* Espaço para o conteúdo não vazar das bordas do seu desenho */
}}

/* UPLOADER LIMPO (Encaixa na sua área desenhada) */
[data-testid="stFileUploadDropzone"] {{
    background-color: rgba(7, 11, 20, 0.6) !important;
    border: 1px dashed rgba(16, 185, 129, 0.4) !important;
    border-radius: 8px !important;
    padding: 20px !important;
}}
[data-testid="stFileUploadDropzone"]:hover {{ border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.1) !important; }}

/* TEXT AREA */
.stTextArea label {{ font-size: 0.8rem !important; margin-bottom: 5px !important; margin-top: 10px !important; font-weight: 800 !important; letter-spacing: 1px; color: #fff !important; text-transform: uppercase; }}
.stTextArea textarea {{ background-color: rgba(7, 11, 20, 0.8) !important; border: 1px solid rgba(16, 185, 129, 0.3) !important; color: #ffffff !important; font-size: 0.9rem !important; border-radius: 8px !important; padding: 15px !important; height: 100px !important; min-height: 100px !important; resize: none; }}
.stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2) !important; outline: none !important; }}

/* BOTÃO DE PROCESSAR */
.stButton > button {{
    background: linear-gradient(90deg, #10b981, #34d399) !important; border-radius: 50px !important; font-weight: 900 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 1px !important; padding: 12px !important; border: none !important; font-size: 0.95rem !important; width: 100% !important; margin-top: 15px !important; box-shadow: 0 5px 15px rgba(16, 185, 129, 0.2) !important; transition: all 0.3s ease;
}}
.stButton > button:hover {{ transform: translateY(-2px); filter: brightness(1.1); box-shadow: 0 10px 20px rgba(16, 185, 129, 0.4) !important; }}

/* TÍTULOS E ELEMENTOS INTERNOS */
.panel-header {{ color: #ffffff; font-weight: 800; font-size: 1rem; letter-spacing: 1px; margin-bottom: 15px; text-transform: uppercase; border-bottom: 1px solid rgba(16,185,129,0.3); padding-bottom: 5px; }}
.telemetry-badge {{ display: inline-block; background: rgba(16, 185, 129, 0.1); color: #34d399; font-size: 0.8rem; padding: 6px 15px; border-radius: 12px; margin-bottom: 15px; border: 1px solid rgba(16, 185, 129, 0.3); font-weight: bold; width: 100%; text-align: center; }}
[data-testid="stCodeBlock"] {{ background: rgba(0, 0, 0, 0.6) !important; border: 1px solid rgba(16,185,129,0.5) !important; border-radius: 8px !important; margin-bottom: 20px; }}
.nexus-center {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 250px; text-align: center; }}
</style>
"""

st.markdown(css_code, unsafe_allow_html=True)

# --- INTERFACE TÁTICA ---
# Como o logo já está no fundo, não precisamos desenhá-lo.

menu = st.radio("Seletor", ["AUDITORIA", "FORENSE", "ENGENHARIA"], index=0, horizontal=True)

col_ing, col_dos = st.columns(2, gap="large")

with col_ing:
    st.markdown('<div class="panel-header">INGESTÃO NEXUS</div>', unsafe_allow_html=True)
    up = st.file_uploader("Arquivos Base", accept_multiple_files=True, label_visibility="collapsed")
    cmd = st.text_area("COMANDO JURÍDICO ESTRATÉGICO:", key="cmd_input", placeholder="Descreva sua análise jurídica profunda...")

    if st.button("🚀 PROCESSAR AUDITORIA"):
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
    st.markdown('<div class="panel-header">DOSSIÊ CONCLUÍDO</div>', unsafe_allow_html=True)
    
    if st.session_state.res_aether:
        st.markdown(f"<div class='telemetry-badge'>🛰️ TELEMETRIA: {st.session_state.telemetria}</div>", unsafe_allow_html=True)
        st.code(st.session_state.res_aether, language="markdown")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button("📄 TXT", data=st.session_state.res_aether, file_name="dossie.txt", mime="text/plain")
        with c2:
            st.download_button("📝 MD", data=st.session_state.res_aether, file_name="dossie.md", mime="text/markdown")
        with c3:
            if st.button("🔄 RESET", use_container_width=True):
                st.session_state.res_aether, st.session_state.telemetria = None, None
                st.rerun()
    else:
        st.markdown(f"""
        <div class="nexus-center">
            <h3 style="margin:0; font-weight:900; color:#f8fafc; letter-spacing:1px; font-size: 1.1rem;">⚖️ MOTOR KARV PRONTO</h3>
            <p style="color:#64748b; font-size:0.9rem; margin-top:5px; font-weight: 500;">Aguardando ingestão e comando...</p>
        </div>
        """, unsafe_allow_html=True)
