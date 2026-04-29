import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time
import random

# --- CONFIGURAÇÃO SUPREMA (SOLUÇÃO PARA ERRO 404 NA NUVEM) ---
try:
    # Busca a chave nos Secrets do Streamlit
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Erro: Configure sua GOOGLE_API_KEY nos 'Secrets' do Streamlit.")

# Função para conectar ao modelo sem erro de caminho
def conectar_ia_nuvem():
    # Lista de nomes que o Google aceita na nuvem (sem o prefixo models/ que causa 404)
    modelos_para_testar = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    for nome in modelos_para_testar:
        try:
            # O segredo é usar o parâmetro model_name direto
            m = genai.GenerativeModel(model_name=nome)
            return m
        except:
            continue
    return genai.GenerativeModel('gemini-1.5-flash')

model = conectar_ia_nuvem()

# --- FUNÇÃO PARA GERAR RELATÓRIO WORD ---
def preparar_download(texto_final):
    doc = Document()
    doc.add_heading('AUDITORIA SUPREMA - RELATÓRIO CLOUD', 0)
    for linha in texto_final.split('\n'):
        doc.add_paragraph(linha)
    
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE RESPONSIVA ---
st.set_page_config(page_title="Auditor Supremo Online", layout="wide")
st.title("🛡️ Supremo v16.1 - Cloud Edition")

with st.sidebar:
    st.header("📂 Entrada de Dados")
    arquivo = st.file_uploader("Subir Documento ou Foto", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.divider()
    st.success("✅ Conexão Segura e Ativa")
    st.info("Sistema operando via Google Cloud Brain.")

# LÓGICA DE PROCESSAMENTO DE ARQUIVOS
dados_ia = []
if arquivo:
    if arquivo.type.startswith("image"):
        img = Image.open(arquivo)
        st.image(img, caption="Imagem Carregada", use_column_width=True)
        dados_ia = [img]
    else:
        # Se for texto ou PDF
        try:
            texto_extraido = arquivo.read().decode("utf-8", errors="ignore")
            dados_ia = [f"CONTEÚDO DO DOCUMENTO: {texto_extraido}"]
        except:
            dados_ia = [f"Documento anexado: {arquivo.name}"]

# CAMPO DE PERGUNTA
comando = st.text_area("Instruções para a Auditoria:", 
                       placeholder="Ex: Analise esta imagem/texto e aponte erros...",
                       height=120)

if st.button("🚀 EXECUTAR AUDITORIA"):
    if comando:
        with st.spinner("Consultando rede neural na nuvem..."):
            try:
                # Super Prompt Multi-IA
                prompt_mestre = f"""
                Atue como um Auditor Supremo e Consultor de Elite. 
                Instrução do Usuário: {comando}
                
                FORMATO DE RESPOSTA:
                1. 🔍 ANÁLISE DE FALHAS (Ética e Técnica)
                2. ✍️ VERSÃO CORRIGIDA E SUGESTÕES
                3. ✅ VEREDITO FINAL DO AUDITOR
                """
                
                # Chamada da IA (Texto + Imagem se houver)
                if dados_ia:
                    response = model.generate_content([prompt_mestre, *dados_ia])
                else:
                    response = model.generate_content(prompt_mestre)
                
                resultado_texto = response.text
                
                # Exibição do Resultado
                st.markdown("---")
                st.markdown(resultado_texto)
                
                # Opção de Download
                st.divider()
                st.download_button(
                    label="📥 BAIXAR RELATÓRIO EM WORD (.DOCX)",
                    data=preparar_download(resultado_texto),
                    file_name="Auditoria_Suprema_Nuvem.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                st.balloons()
                
            except Exception as e:
                st.error(f"Erro no processamento: {e}")
    else:
        st.warning("Por favor, digite uma pergunta ou instrução!")

st.sidebar.caption("v16.1 - Edição Global Conectada")
