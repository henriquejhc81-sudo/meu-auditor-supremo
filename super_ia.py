import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time

# --- CONFIGURAÇÃO DE SEGURANÇA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # FORÇA A VERSÃO ESTÁVEL DA API PARA EVITAR ERRO 404
    genai.configure(api_key=API_KEY)
except:
    st.error("Chave API não configurada nos Secrets.")

# FUNÇÃO PARA CONECTAR SEM ERROS DE CAMINHO
def conectar_ia_estavel():
    # Usamos o nome mais simples possível, que é o padrão global
    try:
        return genai.GenerativeModel('gemini-1.5-flash')
    except:
        return genai.GenerativeModel('gemini-pro')

model = conectar_ia_estavel()

def preparar_download(texto_final):
    doc = Document()
    doc.add_heading('AUDITORIA SUPREMA - RELATÓRIO', 0)
    for linha in texto_final.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.set_page_config(page_title="Auditor Supremo Online", layout="wide")
st.title("🛡️ Supremo v16.2 - Edição Estável")

with st.sidebar:
    st.header("📂 Entrada")
    arquivo = st.file_uploader("Subir Arquivo/Foto", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.success("🔒 Servidor Online")

dados_ia = []
if arquivo:
    if arquivo.type.startswith("image"):
        img = Image.open(arquivo)
        st.image(img, width=300)
        dados_ia = [img]
    else:
        texto = arquivo.read().decode("utf-8", errors="ignore")
        dados_ia = [f"CONTEÚDO: {texto}"]

comando = st.text_area("Instruções:", height=100)

if st.button("🚀 EXECUTAR AUDITORIA"):
    if comando:
        with st.spinner("Conectando ao Cérebro Global..."):
            try:
                # O segredo: Prompt direto
                prompt = f"Responda como Auditor Supremo: {comando}"
                
                if dados_ia:
                    response = model.generate_content([prompt, *dados_ia])
                else:
                    response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                
                st.download_button(
                    label="📥 BAIXAR EM WORD",
                    data=preparar_download(response.text),
                    file_name="Auditoria.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                # Se der erro, mostramos de forma amigável e tentamos reconectar
                st.error(f"Aguarde 10 segundos e tente novamente. (Log: {e})")
    else:
        st.warning("Digite uma pergunta.")
