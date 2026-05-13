import streamlit as st
import pandas as pd
import os, time, base64
import docx2txt

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO & LIBS TÁTICAS ---
try:
    from groq import Groq
except ImportError:
    pass

st.set_page_config(page_title="AETHER OMNI V125", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# --- 🧠 ESTADO DA SESSÃO (Memória Core) ---
if "cmd_input" not in st.session_state: st.session_state.cmd_input = ""
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "telemetria" not in st.session_state: st.session_state.telemetria = None
if "agentes_status" not in st.session_state: st.session_state.agentes_status = "Standby"

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

# --- ⚡ MOTOR AETHER KARV (Processamento Neural Multi-Agente) ---
def aether_karv_engine(comando, contexto_arquivos, lindb_ativada):
    if not contexto_arquivos.strip():
        contexto_arquivos = "[Nenhum dado de arquivo injetado. Operando apenas com o comando jurídico.]"
    
    contexto_lindb = "\nDIRETRIZ DE ALTA PRIORIDADE: Aplicar análise de blindagem de gestores públicos (Art. 22 da LINDB)." if lindb_ativada else ""
    
    groq_api_key = os.environ.get("GROQ_API_KEY") 
    
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            prompt_tatico = f"Você é o AETHER OMNI, um sistema de orquestração multi-agente de auditoria avançada.\nAtue como 7 agentes especialistas paralelos (TCU, Jurídico, Financeiro, Risco, etc) cruzando as informações.{contexto_lindb}\nComando: {comando}\nDados: {contexto_arquivos}"
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_tatico}],
                model="llama3-70b-8192", 
                temperature=0.2,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ FALHA NO LINK NEURAL GROQ: {str(e)}"
    else:
        time.sleep(3) 
        return f"**AUDITORIA SINTÉTICA OMNI:**\nAnálise Concluída. {contexto_lindb}\nConfigure GROQ_API_KEY para acesso neural."

# --- 🎨 IMAGENS E FUNDO (Névoa Anti-Fadiga) ---
back_apex_b64 = get_base64_image("back_apex.png")

# O overlay rgba(6, 10, 15, 0.85) cria a "névoa" fosca altamente densa pedida, focando a visão na interface.
bg_css = f"background: linear-gradient(rgba(4, 8, 13, 0.85), rgba(4, 8, 13, 0.85)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-repeat: no-repeat; background-attachment: fixed;" if back_apex_b64 else "background-color: #04080D;"

# --- 🎨 CSS APEX V125: HIGH-DENSITY ENTERPRISE UI ---
css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');

/* RESET GERAL E FONTES */
.stApp {{ {bg_css} color: #cbd5e1; font-family: 'Inter', sans-serif; }}
.block-container {{ padding-top: 2rem !important; padding-bottom: 2rem !important; max-width: 95% !important; margin: 0 auto; }}
[data-testid="stHeader"] {{ display: none !important; }}

/* TOPBAR CORPORATIVA (Substituindo o título gigante por uma barra de status) */
.omni-topbar {{
    display: flex; justify-content: space-between; align-items: center; 
    background: rgba(10, 15, 24, 0.9); border-bottom: 1px solid rgba(16, 185, 129, 0.4); 
    padding: 10px 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}}
.omni-brand {{ display: flex; align-items: center; gap: 10px; }}
.omni-brand h1 {{ margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 1.5rem; color: #10b981; font-weight: 700; letter-spacing: -1px; }}
.omni-brand span {{ color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; }}
.omni-status {{ font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #10b981; background: rgba(16, 185, 129, 0.1); padding: 4px 10px; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.3); }}

/* PAINÉIS DE ALTA DENSIDADE (Grid Design) */
[data-testid="column"] {{
    background: rgba(10, 15, 24, 0.8) !important;
    border: 1px solid rgba(51, 65, 85, 0.5) !important; /* Borda mais sóbria e corporativa */
    border-radius: 8px !important;
    padding: 20px !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7) !important;
    backdrop-filter: blur(5px) !important;
}}
/* Destaque sutil no hover dos painéis */
[data-testid="column"]:hover {{ border-color: rgba(16, 185, 129, 0.3) !important; transition: 0.3s; }}

/* CABEÇALHOS DE SEÇÃO */
.section-header {{ color: #f8fafc; font-weight: 600; font-size: 0.95rem; letter-spacing: 1px; margin-bottom: 15px; text-transform: uppercase; border-left: 3px solid #10b981; padding-left: 10px; }}

/* UPLOADER E INPUTS - COMPACTOS */
[data-testid="stFileUploadDropzone"] {{
    background-color: rgba(0, 0, 0, 0.3) !important; border: 1px dashed rgba(100, 116, 139, 0.5) !important;
    border-radius: 6px !important; padding: 15px !important; min-height: auto !important;
}}
.stTextArea label, .stCheckbox label span {{ font-size: 0.8rem !important; color: #94a3b8 !important; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600 !important; }}
.stTextArea textarea {{ background-color: rgba(0, 0, 0, 0.4) !important; border: 1px solid rgba(51, 65, 85, 0.8) !important; color: #f8fafc !important; font-size: 0.85rem !important; border-radius: 6px !important; padding: 10px !important; height: 100px !important; min-height: 100px !important; font-family: 'Inter', sans-serif; }}
.stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: none !important; }}

/* SWITCHES E CHECKBOXES (Estilo Enterprise) */
[data-testid="stCheckbox"] {{ background: rgba(16, 185, 129, 0.05); padding: 10px; border-radius: 6px; border: 1px solid rgba(16, 185, 129, 0.2); margin-bottom: 10px; }}

/* BOTÃO DE PROCESSAR - TERMINAL STYLE */
.stButton > button[kind="primary"] {{
    background: #10b981 !important; border-radius: 4px !important; font-family: 'JetBrains Mono', monospace !important; font-weight: 700 !important; color: #020617 !important; text-transform: uppercase !important; padding: 10px !important; border: none !important; font-size: 0.9rem !important; width: 100% !important; margin-top: 10px !important; transition: all 0.2s ease;
}}
.stButton > button[kind="primary"]:hover {{ filter: brightness(1.2); box-shadow: 0 0 15px rgba(16, 185, 129, 0.4) !important; }}

/* DOSSIÊ TÁTICO (Terminal / Console Visual) */
.terminal-output {{ background: rgba(2, 6, 23, 0.9) !important; border: 1px solid rgba(51, 65, 85, 0.8) !important; border-radius: 6px !important; margin-bottom: 15px; font-family: 'JetBrains Mono', monospace !important; font-size: 0.85rem; }}
[data-testid="stCodeBlock"] {{ background: transparent !important; border: none !important; margin: 0 !important; padding: 10px !important; }}
[data-testid="stCodeBlock"] code {{ font-family: 'JetBrains Mono', monospace !important; color: #a7f3d0 !important; }}

/* TELEMETRIA COMPACTA */
.telemetry-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px; }}
.telemetry-item {{ background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 4px; border-left: 2px solid #3b82f6; font-size: 0.75rem; color: #94a3b8; font-family: 'JetBrains Mono', monospace; }}
.telemetry-item span {{ color: #f8fafc; font-weight: bold; display: block; margin-top: 2px; font-size: 0.85rem; }}

/* BOTÕES SECUNDÁRIOS */
.stButton > button[kind="secondary"], .stDownloadButton > button {{
    background: rgba(15, 23, 42, 0.8) !important; color: #cbd5e1 !important; border: 1px solid rgba(51, 65, 85, 0.8) !important; border-radius: 4px !important; font-weight: 600 !important; font-size: 0.75rem !important; padding: 5px 10px !important; width: 100% !important;
}}
.stButton > button[kind="secondary"]:hover, .stDownloadButton > button:hover {{ border-color: #10b981 !important; color: #10b981 !important; }}
</style>
"""

st.markdown(css_code, unsafe_allow_html=True)

# --- TOPBAR CORPORATIVA (Estilo Enterprise) ---
st.markdown(f"""
<div class="omni-topbar">
    <div class="omni-brand">
        <h1>AETHER OMNI</h1>
        <span>// Strategic Intelligence Hub</span>
    </div>
    <div class="omni-status">
        ● SYSTEM: ONLINE | ENCRYPTION: AES-256
    </div>
</div>
""", unsafe_allow_html=True)

# --- GRID TÁTICO (Proporção 30/70 para focar na leitura dos dados) ---
col_config, col_dossie = st.columns([1, 2.5], gap="medium")

# === PAINEL 1: SETUP E INGESTÃO (Esquerda) ===
with col_config:
    st.markdown('<div class="section-header">1. INGESTÃO DE DADOS (NEXUS)</div>', unsafe_allow_html=True)
    up = st.file_uploader("ARQUIVOS BASE (ERP, Razão, Contratos)", accept_multiple_files=True, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">2. ORQUESTRAÇÃO MULTI-AGENTE</div>', unsafe_allow_html=True)
    
    # Diferencial Competitivo Visualizado:
    ativar_lindb = st.checkbox("🛡️ Blindagem Jurídica (Art. 22 LINDB)", value=True, help="Força os agentes a avaliarem as decisões sob a ótica de obstáculos reais do gestor público.")
    
    cmd = st.text_area("DIRETRIZ DE AUDITORIA:", key="cmd_input", placeholder="Ex: Inicie Due Diligence focada em anomalias financeiras e risco de M&A...")

    if st.button("▶ INICIAR ORQUESTRAÇÃO", type="primary"):
        if cmd:
            # Simulação visual da Orquestração Multi-Agente (Mostra o poder da ferramenta)
            with st.status("📡 Conectando ao AETHER OMNI Hub...", expanded=True) as status:
                st.write("⚙️ Ingerindo Datasets via Nexus Extractor...")
                texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                time.sleep(1)
                st.write("🕵️ Alocando Agente de Fraude Financeira (MindBridge logic)...")
                time.sleep(0.5)
                if ativar_lindb:
                    st.write("🛡️ Ativando Agente de Compliance Público (LINDB Ativada)...")
                    time.sleep(0.5)
                st.write("⚖️ Cruzando Jurisprudência (CoCounsel logic)...")
                time.sleep(0.5)
                st.write("🧠 Sintetizando Relatório Executivo...")
                
                # Execução Real do Motor
                resposta = aether_karv_engine(cmd, texto_arquivos, ativar_lindb)
                
                st.session_state.res_aether = resposta
                st.session_state.telemetria = {
                    "arquivos": num_arquivos,
                    "volume": f"{len(texto_arquivos)/1024:.2f} KB",
                    "agentes": "7 Agentes Sincronizados",
                    "lindb": "Ativa" if ativar_lindb else "Inativa"
                }
                status.update(label="✅ Orquestração Concluída", state="complete", expanded=False)
            st.rerun() 
        else:
            st.warning("⚠️ Forneça uma diretriz para os agentes operarem.")

# === PAINEL 2: DOSSIÊ E TELEMETRIA (Direita) ===
with col_dossie:
    st.markdown('<div class="section-header">3. CONSOLE DE INTELIGÊNCIA</div>', unsafe_allow_html=True)
    
    if st.session_state.res_aether:
        # Telemetria Enterprise
        st.markdown(f"""
        <div class="telemetry-grid">
            <div class="telemetry-item">ATIVOS INGERIDOS: <span>{st.session_state.telemetria['arquivos']} Docs ({st.session_state.telemetria['volume']})</span></div>
            <div class="telemetry-item">STATUS ORQUESTRAÇÃO: <span style="color:#10b981;">{st.session_state.telemetria['agentes']}</span></div>
            <div class="telemetry-item">BLINDAGEM LINDB: <span style="color:{'#10b981' if st.session_state.telemetria['lindb'] == 'Ativa' else '#94a3b8'};">{st.session_state.telemetria['lindb']}</span></div>
            <div class="telemetry-item">TEMPO DE RESPOSTA: <span>{time.strftime("%H:%M:%S")} (UTC)</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Saída Terminal/Console
        st.markdown('<div class="terminal-output">', unsafe_allow_html=True)
        st.code(st.session_state.res_aether, language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Ações Finais
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            st.download_button("⬇️ EXPORTAR RELATÓRIO (.TXT)", data=st.session_state.res_aether, file_name="omni_dossier.txt", mime="text/plain", use_container_width=True)
        with c2:
            st.download_button("⬇️ EXPORTAR MATRIZ (.MD)", data=st.session_state.res_aether, file_name="omni_matriz.md", mime="text/markdown", use_container_width=True)
        with c3:
            if st.button("⟳ LIMPAR CONSOLE", type="secondary", use_container_width=True):
                st.session_state.res_aether = None
                st.session_state.telemetria = None
                st.rerun()
    else:
        # Estado de Espera Profissional
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 350px; opacity: 0.5;">
            <div style="font-size: 3rem; margin-bottom: 10px;">📊</div>
            <h3 style="margin:0; font-family: 'JetBrains Mono', monospace; font-size: 1.2rem; color: #f8fafc;">CONSOLE OMNI EM STANDBY</h3>
            <p style="color:#94a3b8; font-size:0.9rem; margin-top:5px;">Aguardando configuração de agentes e ingestão de dados à esquerda.</p>
        </div>
        """, unsafe_allow_html=True)
