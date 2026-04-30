import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- DESIGN AETHER ---
st.set_page_config(page_title="AETHER AUDIT", layout="wide")

# --- CONEXÃO BLINDADA (FORÇANDO v1 ESTÁVEL) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # Forçamos a configuração sem o sufixo que causa o erro v1beta
    genai.configure(api_key=API_KEY)
    # O SEGREDO: Usamos o nome puro para evitar o erro 404 na nuvem
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("📡 Sincronizando conexão...")

def gerar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO', 0)
    for linha in texto.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
with st.sidebar:
    if st.button("🔄 Reiniciar Sistema"):
        st.rerun()
    st.caption("v26.7 | Cloud Secured")

st.title("🛡️ AETHER AUDIT")
col1, col2 = st.columns(2)

with col1:
    arquivo = st.file_uploader("Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.toggle("Modo Profundo", value=True)

with col2:
    pergunta = st.text_area("O que devo analisar?", placeholder="Ex: Analise e veja se tem erros", height=150)
    if st.button("🚀 INICIAR VARREDURA"):
        if pergunta:
            with st.spinner("Varrendo..."):
                try:
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([pergunta, img])
                    else:
                        # Processamento seguro de arquivos de texto
                        conteudo = arquivo.read().decode("utf-8", errors="ignore") if arquivo else ""
                        response = model.generate_content(f"{pergunta}\n\nDocumento: {conteudo}")
                    
                    st.success("Concluído!")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR WORD", gerar_docx(response.text), "aether_report.docx")
                except Exception as e:
                    st.error(f"Erro: {e}. Tente clicar no botão Reiniciar na lateral.")
        else:
            st.warning("Digite uma instrução.")
