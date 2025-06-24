import streamlit as st
import hashlib, time, io, zipfile
from pipeline import run_pipeline   # ← tu función existente

# --------------------------- Inicio de sesión ---------------------------
def login():
    """Devuelve True si el usuario ya está autenticado."""
    if st.session_state.get("auth_ok"):
        return True

    st.title("🔒 Inicio de sesión")
    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        creds = st.secrets["credentials"]
        if u in creds and hashlib.sha256(p.encode()).hexdigest() == creds[u]:
            st.session_state["auth_ok"] = True
            return True
        st.error("Credenciales incorrectas")
        time.sleep(1)
    st.stop()


# ---------- Ejecutar control de acceso ----------
if not login():  # detiene la app si no pasa el login
    st.stop()
# ------------------------------------------------------------------------


# --------------------------- Interfaz principal -------------------------
st.set_page_config(page_title="BID Template Generator", page_icon="📑")
st.title("📑 Generador de Plantillas BID")

uploaded = st.file_uploader(
    "Arrastra aquí uno o varios archivos .xlsx",
    type=["xlsx"],
    accept_multiple_files=True,
    key="uploader"
)

if st.button("Procesar") and uploaded:
    resultados = []
    for f in uploaded:
        with st.spinner(f"Procesando {f.name}…"):
            nombre, bytes_xlsx = run_pipeline(f.read())
            nombre_final = f"{f.name.rsplit('.',1)[0]}_{nombre}"
            resultados.append((nombre_final, bytes_xlsx))
    st.session_state["resultados"] = resultados


# --------------------------- Zona de descargas --------------------------
if "resultados" in st.session_state:
    st.subheader("Descargas disponibles")

    # 1️⃣ Descargar todo en .ZIP
    if len(st.session_state["resultados"]) > 1:
        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as z:
            for fname, fbytes in st.session_state["resultados"]:
                z.writestr(fname, fbytes)
        zip_buf.seek(0)
        st.download_button(
            "⬇️ Descargar TODO (.zip)",
            data=zip_buf,
            file_name="bid_templates.zip",
            mime="application/zip"
        )

    # 2️⃣ Descargar archivos individuales
    for fname, fbytes in st.session_state["resultados"]:
        st.download_button(
            f"⬇️ {fname}",
            data=fbytes,
            file_name=fname,
            mime=("application/vnd.openxmlformats-officedocument."
                  "spreadsheetml.sheet")
        )

    st.divider()

    # 3️⃣ Reiniciar proceso
    if st.button("🔄 Reiniciar"):
        st.session_state.clear()
        st.experimental_rerun()
