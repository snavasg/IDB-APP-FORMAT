# app.py ─ Generador de Plantillas BID
# -----------------------------------
# • Login con usuario/contraseña guardados en st.secrets
# • Procesamiento de múltiples archivos .xlsx
# • Descarga individual o ZIP
# • Reinicio de proceso
# • Botón “Cerrar sesión” sin romper la app

import streamlit as st
import hashlib, time, io, zipfile
from pipeline import run_pipeline  # ← tu función existente

# ╔═══════════════ 0. CONFIG GLOBAL ═══════════════╗
st.set_page_config(page_title="Generador de Plantillas BID", page_icon="📑")

# ╔═══════════════ 1. LOGIN SIMPLE ════════════════╗
def login() -> bool:
    """Devuelve True cuando el usuario está autenticado."""
    if st.session_state.get("auth_ok"):
        return True

    st.title("🔒 Inicio de sesión")
    user = st.text_input("Usuario")
    pwd  = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        creds = st.secrets["credentials"]
        if user in creds and hashlib.sha256(pwd.encode()).hexdigest() == creds[user]:
            st.session_state["auth_ok"] = True
            st.experimental_rerun()  # refresca para mostrar la app
        else:
            st.error("Credenciales incorrectas")
            time.sleep(1)
    st.stop()

# Ejecutar control de acceso
login()
# ╚════════════════════════════════════════════════╝


# ╔═══════════════ 2. HEADER & AYUDA ══════════════╗
st.title("📑 Generador de Plantillas BID")
with st.expander("ℹ️ Cómo usar esta herramienta", expanded=True):
    st.markdown(
        """
        1. **Sube** uno o varios archivos **.xlsx** que contengan las hojas  
           *SDO & Result Indicators* y *Solutions & Outputs*.  
        2. Pulsa **Procesar** y espera unos segundos.  
        3. Descarga cada resultado o todos juntos en un **ZIP**.  
        """
    )
# ╚════════════════════════════════════════════════╝


# ╔═══════════════ 3. SUBIDA Y PROCESO ════════════╗
uploaded_files = st.file_uploader(
    "📂 Arrastra aquí tus archivos .xlsx",
    type=["xlsx"], accept_multiple_files=True, key="uploader"
)

if st.button("🚀 Procesar") and uploaded_files:
    resultados = []
    for f in uploaded_files:
        with st.spinner(f"Procesando **{f.name}** …"):
            out_name, out_bytes = run_pipeline(f.read())
            final_name = f"{f.name.rsplit('.',1)[0]}_{out_name}"
            resultados.append((final_name, out_bytes))
    st.session_state["resultados"] = resultados
# ╚════════════════════════════════════════════════╝


# ╔═══════════════ 4. DESCARGAS ═══════════════════╗
if "resultados" in st.session_state:
    st.subheader("⬇️ Descargas")

    # ZIP si hay >1 archivo
    if len(st.session_state["resultados"]) > 1:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for fname, fbytes in st.session_state["resultados"]:
                zf.writestr(fname, fbytes)
        zip_buffer.seek(0)
        st.download_button(
            "📦 Descargar TODO (.zip)",
            data=zip_buffer,
            file_name="bid_templates.zip",
            mime="application/zip"
        )

    # Individuales
    for fname, fbytes in st.session_state["resultados"]:
        st.download_button(
            f"💾 {fname}",
            data=fbytes,
            file_name=fname,
            mime=("application/vnd.openxmlformats-officedocument."
                  "spreadsheetml.sheet")
        )

    st.divider()

    # Reiniciar resultados (no cierra sesión)
    if st.button("🔄 Reiniciar proceso"):
        st.session_state.pop("resultados", None)
        st.experimental_rerun()
# ╚════════════════════════════════════════════════╝


# ╔═══════════════ 5. SIDEBAR (LOGOUT) ════════════╗
with st.sidebar:
    st.header("Opciones")
    if st.button("🔓 Cerrar sesión"):
        # Desloguear y limpiar artefactos relevantes
        st.session_state["auth_ok"] = False
        st.session_state.pop("resultados", None)
        st.session_state.pop("uploader",  None)
        st.experimental_rerun()
# ╚════════════════════════════════════════════════╝
