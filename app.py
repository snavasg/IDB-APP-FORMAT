import streamlit as st
import hashlib, time, io, zipfile
from pipeline import run_pipeline   # ← tu función existente

# ╔══════════════════════════ 1. LOGIN ═════════════════════════╗
def login() -> bool:
    """Autenticación mínima con hashes SHA-256 guardados en st.secrets"""
    if st.session_state.get("auth_ok"):
        return True

    st.set_page_config(page_title="Generador de Plantillas BID", page_icon="📑")
    st.title("🔒 Inicio de sesión")

    user = st.text_input("Usuario")
    pwd  = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        creds = st.secrets["credentials"]
        if user in creds and hashlib.sha256(pwd.encode()).hexdigest() == creds[user]:
            st.session_state["auth_ok"] = True
            return True
        st.error("Credenciales incorrectas")
        time.sleep(1)
    st.stop()

# Ejecutar control de acceso
if not login():
    st.stop()
# ╚═════════════════════════════════════════════════════════════╝


# ╔══════════════════════ 2. CONFIG & HEADER ═══════════════════╗
st.set_page_config(page_title="Generador de Plantillas BID", page_icon="📑")
st.title("📑 Generador de Plantillas BID")

with st.expander("ℹ️ Cómo usar esta herramienta", expanded=True):
    st.markdown(
        """
        1. **Sube** uno o varios archivos **.xlsx** que contengan las hojas  
           *SDO & Result Indicators* y *Solutions & Outputs*.
        2. Pulsa **Procesar** y espera unos segundos por cada archivo.  
        3. Aparecerán botones para **descargar** cada resultado o todo en un **ZIP**.
        """
    )
# ╚═════════════════════════════════════════════════════════════╝


# ╔══════════════════════ 3. UPLOAD & PROCESO ══════════════════╗
uploaded_files = st.file_uploader(
    "📂 Arrastra aquí tus archivos .xlsx",
    type=["xlsx"], accept_multiple_files=True, key="uploader"
)

if st.button("🚀 Procesar") and uploaded_files:
    resultados = []
    for f in uploaded_files:
        with st.spinner(f"Procesando **{f.name}** …"):
            nombre, contenido = run_pipeline(f.read())
            nombre_final = f"{f.name.rsplit('.',1)[0]}_{nombre}"
            resultados.append((nombre_final, contenido))
    st.session_state["resultados"] = resultados
# ╚═════════════════════════════════════════════════════════════╝


# ╔══════════════════════ 4. DESCARGAS UI ══════════════════════╗
if "resultados" in st.session_state:
    st.subheader("⬇️ Descargas")

    # Botón ZIP si hay más de un archivo
    if len(st.session_state["resultados"]) > 1:
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for fname, fbytes in st.session_state["resultados"]:
                zf.writestr(fname, fbytes)
        buffer.seek(0)
        st.download_button(
            "📦 Descargar TODO (.zip)",
            data=buffer,
            file_name="bid_templates.zip",
            mime="application/zip"
        )

    # Botones individuales
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
        st.session_state.pop("resultados", None)  # elimina solo los outputs
        st.rerun()  

