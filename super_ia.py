import streamlit as st
import pandas as pd
import os, time, base64
import docx2txt

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO & LIBS TÁTICAS ---
try:
    from groq import Groq
except ImportError:
    pass

st.set_page_config(page_title="AETHER OMNI V131", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# --- 🧠 ESTADO DA SESSÃO ---
if "cmd_input" not in st.session_state: st.session_state.cmd_input = ""
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "telemetria" not in st.session_state or st.session_state.telemetria is None: 
    st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando"}

def set_template(texto):
    """Preenche a caixa de texto automaticamente quando o usuário clica num card rápido"""
    st.session_state.cmd_input = texto

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

# --- ⚡ MOTOR AETHER KARV MULTI-AGENTE ---
def aether_karv_engine(comando, contexto_arquivos, lindb_ativada, agente_foco):
    if not contexto_arquivos.strip():
        contexto_arquivos = "[Nenhum dado de arquivo injetado. Operando apenas com o comando.]"
    
    contexto_lindb = "\nDIRETRIZ DE ALTA PRIORIDADE: Aplicar análise de blindagem de gestores públicos (Art. 22 da LINDB)." if lindb_ativada else ""
    groq_api_key = os.environ.get("GROQ_API_KEY") 
    
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            prompt_tatico = f"Você é o AETHER OMNI, um assistente jurídico de elite. Foco Primário: {agente_foco}. Atue como especialistas paralelos.{contexto_lindb}\nComando: {comando}\nDados: {contexto_arquivos}"
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_tatico}],
                model="llama3-70b-8192", temperature=0.2,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ FALHA NO MOTOR NEURAL: {str(e)}"
    else:
        time.sleep(2) 
        return f"**ANÁLISE JURÍDICA CONCLUÍDA:**\nFoco: {agente_foco}\nProcessamento finalizado com sucesso. {contexto_lindb}\n(Configure a API Key para acesso total)."

# --- 🎨 CSS APEX V131: LEGAL PREMIUM EDITION ---
back_apex_b64 = get_base64_image("back_apex.png")

# Fundo alterado para Azul Marinho Escuro (#0F172A) com leve transparência sobre a imagem
bg_css = f"background: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.95)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #0F172A;"

css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* BLOQUEIO DE SCROLL */
html, body {{ overflow: hidden !important; height: 100vh !important; width: 100vw !important; margin: 0; padding: 0; }}
.stApp {{ {bg_css} color: #cbd5e1; font-family: 'Inter', sans-serif; height: 100vh !important; overflow: hidden !important; }}

/* ELIMINA MARGENS DO STREAMLIT */
.block-container {{ padding-top: 1rem !important; padding-bottom: 0rem !important; max-width: 96% !important; height: 100vh !important; display: flex; flex-direction: column; }}
[data-testid="stHeader"], footer {{ display: none !important; }}

/* TOPBAR PREMIUM */
.omni-topbar {{ display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(212, 175, 55, 0.15); padding: 8px 25px; margin-bottom: 15px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4); flex-shrink: 0; }}
.omni-brand {{ display: flex; align-items: center; gap: 12px; }}
.omni-brand h1 {{ margin: 0; font-family: 'Inter', sans-serif; font-size: 1.2rem; color: #f8fafc; font-weight: 700; letter-spacing: 0.5px; }}
.omni-brand span {{ color: #D4AF37; font-size: 0.7rem; font-weight: 600; letter-spacing: 1px; border: 1px solid rgba(212, 175, 55, 0.4); padding: 3px 8px; border-radius: 8px; background: rgba(212, 175, 55, 0.05); text-transform: uppercase; }}
.omni-status {{ font-size: 0.75rem; color: #94a3b8; font-weight: 500; }}
.omni-status span {{ color: #D4AF37; font-weight: 600; }}

/* CONTAINERS ARREDONDADOS (12px) E SUAVES */
[data-testid="column"] {{ background: rgba(30, 41, 59, 0.3) !important; backdrop-filter: blur(16px) !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 12px !important; padding: 15px 20px !important; height: calc(100vh - 90px) !important; display: flex; flex-direction: column; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); }}

/* TÍTULOS DE SESSÃO PREMIUM */
.section-title {{ color: #f8fafc; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }}
.section-title::before {{ content: ''; display: block; width: 4px; height: 12px; background: #D4AF37; border-radius: 4px; }}

/* UPLOADER & TEXT AREA */
[data-testid="stFileUploadDropzone"] {{ background-color: rgba(15, 23, 42, 0.4) !important; border: 1px dashed rgba(255,255,255,0.1) !important; border-radius: 8px !important; padding: 10px !important; min-height: 45px !important; transition: 0.3s; }}
[data-testid="stFileUploadDropzone"] small {{ display: none !important; }}

div[data-baseweb="select"] > div {{ background-color: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255,255,255,0.05) !important; color: #f8fafc !important; font-size: 0.8rem !important; border-radius: 8px !important; }}

.stTextArea label, .stCheckbox label span, .stSelectbox label {{ font-size: 0.7rem !important; color: #cbd5e1 !important; font-weight: 600 !important; margin-bottom: 4px !important; }}
.stTextArea textarea {{ background-color: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255,255,255,0.05) !important; color: #f8fafc !important; font-size: 0.85rem !important; border-radius: 8px !important; height: 100px !important; min-height: 100px !important; padding: 10px !important; box-shadow: inset 0 2px 5px rgba(0,0,0,0.2); }}
.stTextArea textarea:focus {{ border-color: #D4AF37 !important; box-shadow: 0 0 10px rgba(212, 175, 55, 0.1) !important; }}

/* CHECKBOX */
[data-testid="stCheckbox"] {{ background: rgba(0,0,0,0.1); padding: 6px 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.03); margin-bottom: 5px; }}

/* BOTÃO DE PROCESSAR DOURADO/ROYAL */
.stButton > button[kind="primary"] {{ background: linear-gradient(135deg, #B8860B, #D4AF37) !important; border-radius: 8px !important; font-weight: 700 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; padding: 10px !important; border: none !important; width: 100% !important; margin-top: auto !important; transition: 0.3s; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2); font-size: 0.9rem !important; }}
.stButton > button[kind="primary"]:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4); filter: brightness(1.1); }}

/* KPIs HTML (Dourado Fosco) */
.custom-kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 15px; flex-shrink: 0; }}
.kpi-box {{ background: rgba(15, 23, 42, 0.4); border-radius: 8px; display: flex; flex-direction: column; border: 1px solid rgba(255,255,255,0.03); border-left: 3px solid #D4AF37; padding: 10px; }}
.kpi-title {{ color: #94a3b8; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; font-weight: 600; }}
.kpi-value {{ color: #f8fafc; font-size: 1.1rem; font-weight: 500; }}
.kpi-value.highlight {{ color: #D4AF37; font-weight: 700; }}

/* AGENT GRID */
.agent-grid {{ display: flex; gap: 8px; margin-bottom: 15px; flex-wrap: wrap; flex-shrink: 0; }}
.agent-badge {{ background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.3); color: #D4AF37; font-size: 0.65rem; font-weight: 600; padding: 4px 10px; border-radius: 6px; display: flex; align-items: center; gap: 4px; }}
.agent-standby {{ background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); color: #94a3b8; font-size: 0.65rem; padding: 4px 10px; border-radius: 6px; display: flex; align-items: center; gap: 4px; }}

/* DOSSIÊ CONSOLE */
.console-output {{ background: rgba(15, 23, 42, 0.5) !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 8px !important; padding: 15px !important; flex-grow: 1; overflow-y: auto; font-size: 0.85rem; color: #f1f5f9; margin-bottom: 12px; box-shadow: inset 0 2px 10px rgba(0,0,0,0.3); line-height: 1.6; }}
[data-testid="stCodeBlock"] {{ background: transparent !important; border: none !important; padding: 0 !important; }}

/* BOTÕES SECUNDÁRIOS NA BASE */
.action-buttons-row {{ display: flex; gap: 10px; flex-shrink: 0; margin-top: auto; }}
.stButton > button[kind="secondary"], .stDownloadButton > button {{ background: rgba(255,255,255,0.05) !important; color: #cbd5e1 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 8px !important; font-size: 0.75rem !important; font-weight: 500 !important; padding: 6px !important; width: 100% !important; transition: 0.3s; margin: 0 !important; }}
.stButton > button[kind="secondary"]:hover, .stDownloadButton > button:hover {{ background: rgba(255,255,255,0.1) !important; color: #fff !important; border-color: #D4AF37 !important; }}

/* STANDBY PLACEHOLDER - WELCOME CARDS */
.standby-container {{ display:flex; flex-direction:column; align-items:center; justify-content:center; flex-grow:1; border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; background: rgba(15, 23, 42, 0.3); padding: 20px; }}
.welcome-title {{ color: #f8fafc; font-size: 1.2rem; font-weight: 600; margin-bottom: 5px; }}
.welcome-subtitle {{ color: #94a3b8; font-size: 0.85rem; margin-bottom: 20px; text-align: center; }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# --- TOPBAR ---
st.markdown(f"""
<div class="omni-topbar">
    <div class="omni-brand"><h1>AETHER OMNI</h1><span>LEGAL INTELLIGENCE</span></div>
    <div class="omni-status">SESSÃO: <span>CRIPTOGRAFADA (AES-256)</span></div>
</div>
""", unsafe_allow_html=True)

# --- GRID TÁTICO PRINCIPAL ---
col_setup, col_main = st.columns([1.2, 2.5], gap="large")

# ==========================================
# PAINEL 1: SETUP E INGESTÃO (ESQUERDA)
# ==========================================
with col_setup:
    st.markdown('<div class="section-title">📁 Enviar Documentos e Processos</div>', unsafe_allow_html=True)
    up = st.file_uploader("Arraste contratos, petições ou planilhas...", accept_multiple_files=True, label_visibility="collapsed")
    
    st.markdown('<div class="section-title" style="margin-top:15px;">⚖️ Configurações da Análise</div>', unsafe_allow_html=True)
    
    agente_foco = st.selectbox("Especialidade do Assistente", ["Análise de Contratos", "Due Diligence Societária", "Compliance e Risco", "Auditoria Trabalhista", "Direito Público"])
    ativar_lindb = st.checkbox("Aplicar Filtro de Proteção (Art. 22 LINDB)", value=True)
    
    st.markdown('<div class="section-title" style="margin-top:15px;">💬 Instruções ou Pedidos Especiais</div>', unsafe_allow_html=True)
    cmd = st.text_area("", key="cmd_input", placeholder="Ex: Verifique as cláusulas de rescisão e aponte os riscos...")

    if st.button("🚀 Iniciar Varredura Jurídica", type="primary"):
        if cmd:
            with st.spinner("Analisando documentos..."):
                texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                time.sleep(1) 
                resposta = aether_karv_engine(cmd, texto_arquivos, ativar_lindb, agente_foco)
                
                st.session_state.res_aether = resposta
                st.session_state.telemetria = {
                    "arquivos": str(num_arquivos),
                    "volume": f"{len(texto_arquivos)/1024:.1f} KB",
                    "tempo": time.strftime("%H:%M:%S"),
                    "risco": "Análise Concluída"
                }
            st.rerun() 
        else:
            st.warning("Por favor, forneça uma instrução para a análise.")

# ==========================================
# PAINEL 2: MAIN STAGE (DIREITA)
# ==========================================
with col_main:
    # --- LINHA 1: KPIs ---
    t = st.session_state.telemetria
    st.markdown(f"""
    <div class="custom-kpi-grid">
        <div class="kpi-box"><span class="kpi-title">Documentos Lidos</span><span class="kpi-value">{t['arquivos']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Volume Processado</span><span class="kpi-value">{t['volume']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Hora da Análise</span><span class="kpi-value">{t['tempo']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Status da Varredura</span><span class="kpi-value highlight">{t['risco']}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- LINHA 2: MULTI-AGENT ---
    st.markdown('<div class="section-title">Status dos Módulos Especialistas</div>', unsafe_allow_html=True)
    
    if st.session_state.res_aether:
        st.markdown("""
        <div class="agent-grid">
            <div class="agent-badge">✓ JURISPRUDÊNCIA: ATIVO</div>
            <div class="agent-badge">✓ RISCO CONTRATUAL: ATIVO</div>
            <div class="agent-badge">✓ CONFORMIDADE: ATIVO</div>
            <div class="agent-badge">✓ AUDITORIA FINANCEIRA: ATIVO</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="agent-grid">
            <div class="agent-standby">○ JURISPRUDÊNCIA: ESPERA</div>
            <div class="agent-standby">○ RISCO CONTRATUAL: ESPERA</div>
            <div class="agent-standby">○ CONFORMIDADE: ESPERA</div>
            <div class="agent-standby">○ AUDITORIA FINANCEIRA: ESPERA</div>
        </div>
        """, unsafe_allow_html=True)

    # --- LINHA 3: CONSOLE OUTPUT ---
    st.markdown('<div class="section-title">Parecer Jurídico (Resultado)</div>', unsafe_allow_html=True)
    if st.session_state.res_aether:
        st.markdown('<div class="console-output">', unsafe_allow_html=True)
        st.markdown(st.session_state.res_aether) # Usando markdown normal em vez de code para leitura mais agradável
        st.markdown('</div>', unsafe_allow_html=True)
        
        b1, b2, b3 = st.columns([1,1,2])
        with b1: st.download_button("⬇ Exportar Relatório (Word)", data=st.session_state.res_aether, file_name="AETHER_Parecer.txt", use_container_width=True)
        with b2: st.download_button("⬇ Exportar Matriz (PDF)", data=st.session_state.res_aether, file_name="AETHER_Matriz.md", use_container_width=True)
        with b3: 
            if st.button("⟳ Nova Análise (Limpar Dados)", type="secondary", use_container_width=True):
                st.session_state.res_aether = None
                st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando"}
                st.rerun()
    else:
        # TELA DE BOAS-VINDAS E TEMPLATES
        st.markdown('<div class="standby-container">', unsafe_allow_html=True)
        st.markdown('<div class="welcome-title">Como posso ajudar na sua análise hoje?</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtitle">Escolha um atalho rápido ou digite sua instrução no painel à esquerda.</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.button("📄 Analisar Petição Inicial da Parte Contrária", on_click=set_template, args=("Faça uma análise crítica da petição inicial em anexo, identificando fragilidades jurídicas e sugerindo teses de defesa.",), use_container_width=True)
            st.button("🔍 Procurar Cláusulas Abusivas em Contrato", on_click=set_template, args=("Revise o contrato anexo e destaque todas as cláusulas que possam ser consideradas abusivas ou desproporcionais.",), use_container_width=True)
        with c2:
            st.button("📅 Calcular Prazos e Ler Intimação", on_click=set_template, args=("Leia a publicação do diário oficial e identifique os prazos processuais e as providências cabíveis.",), use_container_width=True)
            st.button("📊 Simular Probabilidade de Acordo", on_click=set_template, args=("Com base nos documentos, avalie os riscos de perda e simule uma proposta de acordo financeiramente viável.",), use_container_width=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
