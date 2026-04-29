import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- CONFIGURAÇÃO DE SEGURANÇA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Chave API não configurada nos Secrets.")

# FUNÇÃO DE AUTO-DETECÇÃO (MATA O ERRO 404)
def carregar_modelo_disponivel():
    try:
        # Pergunta ao Google: "Quais modelos eu posso usar agora?"
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Escolhe o primeiro da lista (geralmente o gemini-1.5-flash ou pro)
        return genai.GenerativeModel(modelos)
    except:
        # Se não conseguir listar, tenta o nome padrão simplificado
        return genai.GenerativeModel('gemini-pro')

model = carregar_modelo_disponivel()

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
st.title("🛡️ Supremo v16.3 - Edição Inteligente")

with st.sidebar:
    st.header("📂 Entrada")
    arquivo = st.file_uploader("Subir Arquivo/Foto", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.success("🔒 Servidor Conectado")

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
        with st.spinner("Buscando resposta..."):
            try:
                if dados_ia:
                    response = model.generate_content([comando, *dados_ia])
                else:
                    response = model.generate_content(comando)
                
                st.markdown("---")
                st.markdown(response.text)
                
                st.download_button(
                    label="📥 BAIXAR EM WORD",
                    data=preparar_download(response.text),
                    file_name="Auditoria.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"Erro técnico: {e}. Tente novamente em 10 segundos.")
    else:
        st.warning("Digite uma pergunta.")
