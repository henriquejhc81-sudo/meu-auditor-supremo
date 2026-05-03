import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN STEALTH GLOBAL & UI CLEANING ---
st.set_page_config(page_title="AETHER OMNI | Intelligence", layout="wide", page_icon="🛡️")

if 'historico' not in st.session_state:
    st.session_state['historico'] = []
if 'show_history' not in st.session_state:
    st.session_state['show_history'] = False

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Esconder Menu Streamlit (Direita) e Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .main { background-color: #0b0d11; color: #e1e1e1; }
    
    /* Botões Estilo Enterprise */
    .stButton>button { 
        width: 100%; 
        background: #1e2128; 
        color: #00c6ff; 
        border: 1px solid #2d323d;
        border-radius: 8px; 
        font-weight: 600; 
        height: 3.2em;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background: #00c6ff; 
        color: #0b0d11;
        border: 1px solid #00c6ff;
    }

    /* Cartões de Relatório */
    .report-card { 
        padding: 30px; 
        border-radius: 12px; 
        background: #161920; 
        border: 1px solid #252a34; 
        color: #cfd2d9; 
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .history-card { 
        background: #1c2028; 
        padding: 12px; 
        border-radius: 6px; 
        border-left: 2px solid #00c6ff; 
        margin-bottom: 8px; 
        font-size: 0.85em; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (LÓGICA DE OURO) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model = genai.GenerativeModel(modelos if modelos else 'gemini-1.5-flash')
except:
    st.error("📡 Erro de sincronização com o núcleo de inteligência.")

def preparar_docx(lista_resultados, unico=True):
    doc = Document()
    if unico:
        doc.add_heading('PARECER TÉCNICO AETHER', 0)
        texto = lista_resultados[-1]['texto'] if isinstance(lista_resultados, list) else lista_resultados
        doc.add_paragraph(texto)
    else:
        doc.add_heading('CONSOLIDADO DE AUDITORIA', 0)
        for res in lista_resultados:
            doc.add_heading(f"Sessão: {res['titulo']}", level=1)
            doc.add_paragraph(res['texto'])
            doc.add_page_break()
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- PAINEL LATERAL ---
with st.sidebar:
    st.title("🛡️ AETHER OMNI")
    st.caption("v51.2 Master Compliance")
    
    if st.button("📜 Histórico de Missões"):
        st.session_state['show_history'] = not st.session_state['show_history']

    if st.session_state['show_history']:
        if st.session_state['historico']:
            for item in st.session_state['historico']:
                st.markdown(f"<div class='history-card'><b>{item['fonte']}</b><br>{item['titulo']}</div>", unsafe_allow_html=True)
            st.download_button("📥 Exportar Histórico", preparar_docx(st.session_state['historico'], unico=False), "omni_history.docx")
        else:
            st.caption("Sem registros ativos.")

    st.divider()
    st.subheader("Parâmetros Sniper")
    st.toggle("OCR Inteligente", value=True)
    st.toggle("Risco Provisório", value=True)
    st.toggle("Análise Forense", value=True)
    
    st.divider()
    acao_filtro = st.selectbox("Comportamento Neural:", [
        "Auditoria Técnica",
        "Geração de Contrato Corrigido",
        "Geração de Petição Corrigida"
    ])

    st.divider()
    with st.expander("Sistemas"):
        if st.button("Reiniciar Motor"):
            st.session_state['historico'] = []
            st.rerun()

# --- CENTRAL OMNI ---
st.title("🛡️ AETHER OMNI")
st.markdown("<p style='color:#7b818f;'>SISTEMA DE ALTA FREQUÊNCIA PARA AUDITORIA E COMPLIANCE GLOBAL</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("Entrada de Dados")
    arquivos = st.file_uploader("Upload de Ativos (PDF, PNG, XLSX)", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("O sistema processa evidências multimodais com cruzamento automático de dados.")

with col2:
    st.subheader("Centro de Comando")
    tipo_missao = st.selectbox("Estratégia:", [
        "Auditoria Forense (Padrão)", 
        "Auditar e Corrigir Processo Judicial", 
        "Auditar e Corrigir Contrato",
        "Análise Grafotécnica",
        "Geração Documental"
    ])
    
    pergunta = st.text_area("Instruções Diretas:", placeholder="Defina os parâmetros ou anexe arquivos para análise...", height=150)
    
    if st.button("EXECUTAR VARREDURA OMNI"):
        if pergunta or arquivos:
            with st.spinner("Processando..."):
                try:
                    conteudo_extra = ""
                    imagens = []
                    nome_fonte = "Consulta Manual"
                    
                    if arquivos:
                        nome_fonte = arquivos[0].name if isinstance(arquivos, list) else arquivos.name
                        for arq in arquivos:
                            if arq.type.startswith("image"):
                                imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                conteudo_extra += f"\n\nDATASET {arq.name}:\n{df.to_string()}"

                    # PROMPT BLINDADO E LEGALMENTE SEGURO
                    prompt_final = f"""
                    Atue como o sistema AETHER OMNI (Auditor Forense e Consultor de Compliance Sênior).
                    MISSÃO: {tipo_missao}. 
                    AÇÃO: {acao_filtro}.
                    DADOS: {pergunta} {conteudo_extra}
                    
                    DIRETRIZES DE RESPOSTA:
                    1. NÃO use o termo 'Advogado'. Use 'Consultor Técnico' ou 'Auditor'.
                    2. Responda com autoridade executiva e rigor técnico.
                    3. Se o objetivo for CORREÇÃO, entregue o texto revisado com base nas normas e leis vigentes.
                    4. Estrutura: Diagnóstico de Inconsistências -> Parecer Técnico -> Veredito.
                    5. AO FINAL DE TUDO, adicione EXATAMENTE esta frase em destaque: 
                       'NOTA: Este relatório é um parecer técnico gerado por inteligência artificial para auxílio na tomada de decisão, não substituindo a consultoria jurídica ou contábil individualizada.'
                    """
                    
                    response = model.generate_content([prompt_final, *imagens]) if imagens else model.generate_content(prompt_final)
                    
                    st.session_state['historico'].insert(0, {
                        "titulo": tipo_missao,
                        "fonte": nome_fonte,
                        "texto": response.text
                    })
                    
                    st.success("Operação Finalizada.")
                    tab1, tab2 = st.tabs(["📄 Resultado", "💾 Exportação"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 Baixar Parecer (.DOCX)", preparar_docx(response.text, unico=True), f"AETHER_{nome_fonte}.docx")
                except Exception as e:
                    st.error(f"Falha na rede: {e}")
        else:
            st.warning("Aguardando entrada de dados.")
