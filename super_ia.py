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
# Layout "wide" garante o uso de toda a tela horizontalmente
st.set_page_config(page_title="AETHER KARV V118", page_icon="logo.png", layout="wide", initial_sidebar_state="collapsed")

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

# Fundo Global Seguro
bg_css = f"background-image: url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center top; background-repeat: no-repeat; background-attachment: fixed;" if back_apex_b64 else "background-color: #0e1117;"

# --- 🎨 CSS APEX V118: MODERNO E NATIVO ---
# Aqui usamos CSS não-destrutivo. Ele embeleza o Streamlit sem tentar esconder o núcleo dele.
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    .stApp {{ {bg_css} color: #f3f4f6; font-family: 'Inter', sans-serif; }}
    
    /* Centraliza e dá respiro ao conteúdo */
    .block-container {{ padding-top: 3rem !important; padding-bottom: 3rem !important; max-width: 1200px !important; }}
    
    /* Esconde o cabeçalho padrão do Streamlit */
    [data-testid="stHeader"] {{ display: none !important; }}

    /* HEADER CUSTOMIZADO */
    .header-container {{ text-align: center; margin-bottom: 2rem; }}
    .karv-title {{ margin: 0; font-weight: 900; font-size: 3rem; color: #ffffff; letter-spacing: -1px; text-shadow: 0 0 20px rgba(16, 185, 129, 0.4); line-height: 1.1; }}
    .karv-subtitle {{ color: #10b981; font-weight: 700; font-size: 1rem; letter-spacing: 4px; text-transform: uppercase; margin-top: 5px; }}

    /* ESTILIZAÇÃO DE CONTAINERS (Efeito Vidro/Glassmorphism Seguro) */
    [data-testid="stVerticalBlock"] > div > div > div > div > div[data-testid="stVerticalBlock"] {{
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 15px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        height: 100%;
    }}

    /* TÍTULOS DOS PAINÉIS */
    h3 {{ color: #ffffff !important; font-weight: 800 !important; font-size: 1.2rem !important; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 1.5rem !important; border-bottom: 1px solid rgba(16, 185, 129, 0.3); padding-bottom: 0.5rem; }}

    /* EMBELEZAMENTO DO UPLOADER NATIVO (Sem quebrá-lo) */
    [data-testid="stFileUploadDropzone"] {{
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 2px dashed rgba(16, 185, 129, 0.5) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }}
    [data-testid="stFileUploadDropzone"]:hover {{
        background-color: rgba(16, 185, 129, 0.1) !important;
        border-color: #10b981 !important;
    }}
    
    /* BOTÃO PRINCIPAL (Primary) */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        color: #020617 !important;
        font-weight: 800 !important;
        border-radius: 50px !important;
        padding: 0.75rem 2rem !important;
        border: none !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
        transition: all 0.3s ease;
    }}
    .stButton > button[kind="primary"]:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5) !important; }}

    /* BOTÃO SECUNDÁRIO (Nova Operação) */
    .stButton > button[kind="secondary"] {{
        background: rgba(30, 41, 59, 0.6) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(16, 185, 129, 0.4) !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s ease;
    }}
    .stButton > button[kind="secondary"]:hover {{ border-color: #10b981 !important; color: #10b981 !important; background: rgba(16, 185, 129, 0.1) !important; }}

    /* TEXT AREA (COMANDO) */
    .stTextArea label {{ color: #ffffff !important; font-weight: 700 !important; font-size: 0.9rem !important; letter-spacing: 0.5px; text-transform: uppercase; }}
    .stTextArea textarea {{
        background-color: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }}
    .stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2) !important; }}

    /* BADGE DE TELEMETRIA E DOSSIÊ */
    .telemetry-badge {{ background: rgba(16, 185, 129, 0.1); color: #34d399; font-size: 0.85rem; padding: 0.5rem 1rem; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.3); font-weight: 600; text-align: center; margin-bottom: 1rem; display: block; }}
    .empty-state {{ text-align: center; padding: 3rem 1rem; opacity: 0.6; }}
</style>
""", unsafe_allow_html=True)

# --- INÍCIO DA INTERFACE ---

# 1. CABEÇALHO
st.markdown("""
<div class="header-container">
    <h1 class="karv-title">AETHER KARV</h1>
    <div class="karv-subtitle">Strategic Intelligence Hub</div>
</div>
""", unsafe_allow_html=True)

# 2. NAVEGAÇÃO SEGURA (Native Streamlit Tabs para estabilidade máxima)
# Tabs são nativos, lindos e nunca quebram o layout
aba1, aba2, aba3 = st.tabs(["🛡️ AUDITORIA", "🔍 FORENSE", "⚙️ ENGENHARIA"])

with aba1:
    st.markdown("<br>", unsafe_allow_html=True) # Respiro
    
    # 3. COLUNAS SIMÉTRICAS
    col_ing, col_dos = st.columns(2, gap="large")

    # --- PAINEL ESQUERDO: INGESTÃO ---
    with col_ing:
        with st.container():
            st.markdown("### INGESTÃO ESTRATÉGICA")
            
            up = st.file_uploader("Arquivos Base (PDF, DOCX, XLSX, CSV)", accept_multiple_files=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            cmd = st.text_area("COMANDO JURÍDICO:", key="cmd_input", height=150, placeholder="Ex: Analise os documentos e aponte inconsistências jurídicas contratuais...")

            if st.button("🚀 PROCESSAR AUDITORIA NEURAL", type="primary"):
                if cmd:
                    with st.status("🧠 Inicializando Motores AETHER KARV...", expanded=False):
                        texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                        resposta = aether_karv_engine(cmd, texto_arquivos)
                        st.session_state.res_aether = resposta
                        st.session_state.telemetria = f"Ativos Ingeridos: {num_arquivos} | Volume Processado: {len(texto_arquivos)} bytes"
                    st.rerun()
                else:
                    st.warning("⚠️ Insira um comando estratégico para iniciar a operação.")

    # --- PAINEL DIREITO: DOSSIÊ ---
    with col_dos:
        with st.container():
            st.markdown("### DOSSIÊ DE INTELIGÊNCIA")
            
            if st.session_state.res_aether:
                # Dossiê Preenchido
                st.markdown(f"<div class='telemetry-badge'>🛰️ TELEMETRIA: {st.session_state.telemetria}</div>", unsafe_allow_html=True)
                
                # st.code fornece uma caixa preta de código com o botão de "Copiar" nativo
                st.code(st.session_state.res_aether, language="markdown")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Controles Finais
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.download_button("📄 TXT", data=st.session_state.res_aether, file_name="dossie_aether.txt", mime="text/plain", use_container_width=True)
                with c2:
                    st.download_button("📝 MD", data=st.session_state.res_aether, file_name="dossie_aether.md", mime="text/markdown", use_container_width=True)
                with c3:
                    if st.button("🔄 RESET", type="secondary", use_container_width=True):
                        st.session_state.res_aether = None
                        st.session_state.telemetria = None
                        st.rerun()
            else:
                # Estado Vazio (Aguardando)
                st.markdown("""
                <div class="empty-state">
                    <h1 style="font-size: 4rem; margin-bottom: 0;">⚖️</h1>
                    <h4 style="color: #f8fafc; font-weight: 800; letter-spacing: 1px; margin-top: 1rem;">MOTOR KARV EM ESPERA</h4>
                    <p style="color: #64748b; font-size: 0.9rem;">Aguardando ingestão de dados e comando tático.</p>
                </div>
                """, unsafe_allow_html=True)

with aba2:
    st.info("Módulo Forense em desenvolvimento.")

with aba3:
    st.info("Módulo de Engenharia em desenvolvimento.")
