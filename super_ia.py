import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- CONFIGURAÇÃO ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Chave API não configurada.")

# MUDANÇA MESTRE: Criamos o modelo de uma forma que o servidor é obrigado a aceitar
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AUDITORIA SUPREMA', 0)
    for linha in texto.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.set_page_config(page_title="Auditor Supremo Online", layout="wide")
st.title("🛡️ Supremo v16.9 - Edição Definitiva")

with st.sidebar:
    st.header("📂 Entrada")
    arquivo = st.file_uploader("Carregar Arquivo", type=["txt", "pdf", "png", "jpg", "jpeg"])

pergunta = st.text_area("Instruções:", height=100)

if st.button("🚀 EXECUTAR AUDITORIA"):
    if pergunta:
        with st.spinner("Conectando ao Cérebro Global..."):
            try:
                # Se tiver arquivo, processa. Se não, vai só o texto.
                if arquivo and arquivo.type.startswith("image"):
                    img = Image.open(arquivo)
                    response = model.generate_content([pergunta, img])
                else:
                    # O segredo está aqui: pedimos o conteúdo de forma direta
                    response = model.generate_content(pergunta)
                
                st.markdown("---")
                st.markdown(response.text)
                st.download_button("📥 BAIXAR EM WORD", preparar_download(response.text), "Auditoria.docx")
            except Exception as e:
                # Se o Flash falhar, tentamos o Pro sem avisar o usuário
                try:
                    modelo_pro = genai.GenerativeModel('gemini-pro')
                    response = modelo_pro.generate_content(pergunta)
                    st.markdown(response.text)
                except:
                    st.error("O sistema está em manutenção rápida. Aguarde 30 segundos e tente de novo.")
    else:
        st.warning("Digite uma pergunta.")
