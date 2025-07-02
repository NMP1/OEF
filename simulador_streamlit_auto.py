import streamlit as st
from PIL import Image
import os
import time

from trabalhos_dict import trabalhos

# Lista de fases
fases = ['0', '0A', '0B', '0C', '0D', '0E', '1', '1A', '1B', '1C', '1D', '1E', '1F', '2']

# Estado inicial
if "fase_index" not in st.session_state:
    st.session_state.fase_index = 0
if "auto" not in st.session_state:
    st.session_state.auto = False
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# Configuração da página
#st.set_page_config(layout="wide")
import os

icon_path = os.path.join("images", "icon.png")

st.set_page_config(
    page_title="OEF - G2",
    page_icon=icon_path,
    layout="wide"
)

# === Cabeçalho ===
header_path = os.path.join("images", "Header.png")
if os.path.exists(header_path):
    st.image(header_path, use_container_width=True)

st.markdown(
    """
    <h1 style='text-align: center; font-size: 2.5em;'>
        Simulador Visual de Faseamento Ferroviário
    </h1>
    """,
    unsafe_allow_html=True,
)


#st.title("Simulador Visual de Faseamento Ferroviário")

# === Controlo de Apresentação ===
col_btn = st.columns([1, 1, 8])
if col_btn[0].button("▶ Iniciar Apresentação"):
    st.session_state.auto = True
    st.session_state.fase_index = 0
    st.session_state.last_update = time.time()

if col_btn[1].button("⏹ Parar"):
    st.session_state.auto = False

# Navegação manual por setas
col_setas = st.columns([1, 10, 1])
with col_setas[0]:
    if st.button("⬅ Anterior", key="prev") and st.session_state.fase_index > 0:
        st.session_state.fase_index -= 1
        st.session_state.auto = False

with col_setas[2]:
    if st.button("Seguinte ➡", key="next") and st.session_state.fase_index < len(fases) - 1:
        st.session_state.fase_index += 1
        st.session_state.auto = False

# Avanço automático entre fases
if st.session_state.auto:
    tempo_entre_fases = 5  # segundos
    tempo_passado = time.time() - st.session_state.last_update
    if tempo_passado >= tempo_entre_fases:
        st.session_state.fase_index += 1
        st.session_state.last_update = time.time()
    if st.session_state.fase_index >= len(fases):
        st.session_state.auto = False
        st.session_state.fase_index = len(fases) - 1

# === Conteúdo da Fase ===
fase_escolhida = fases[st.session_state.fase_index]

#st.subheader(f"Fase {fase_escolhida} – Layout")
st.markdown(
    f"<h3 style='text-align: center;'>Fase {fase_escolhida} – Layout</h3>",
    unsafe_allow_html=True
)

img_path = os.path.join("Layout", f"{fase_escolhida}.png")
if os.path.exists(img_path):
    st.image(img_path, use_container_width=True)

    with st.expander("🛈 Legenda do layout", expanded=False):
        legenda_img = os.path.join("images", "legenda.png")
        if os.path.exists(legenda_img):
            st.image(legenda_img, use_column_width=True)
        else:
            st.warning("Legenda não encontrada.")
else:
    st.warning("Imagem de layout não disponível.")
    
# Trabalhos e Gantt
col1, col2 = st.columns(2)

with col1:
    st.subheader("Descrição")
    st.text(trabalhos.get(fase_escolhida, "Sem informação de trabalhos."))

with col2:
    st.subheader("Planeamento")
    gantt_path = os.path.join("Planeamento", f"{fase_escolhida}.png")
    if os.path.exists(gantt_path):
        st.image(gantt_path, use_container_width=True)
    else:
        st.info(" ")

# === Rodapé ===
footer_path = os.path.join("images", "Footer.png")
if os.path.exists(footer_path):
    st.image(footer_path, use_container_width=True)

# Re-executar se estiver em modo automático
if st.session_state.auto:
    st.rerun()
