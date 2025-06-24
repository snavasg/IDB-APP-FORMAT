# app.py
import streamlit as st
from pipeline import run_pipeline

import streamlit as st
import hashlib, time

# ---------- Login ----------
def login():
    if st.session_state.get("auth_ok"):
        return True

    st.title("🔒 Inicia sesión")
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

# Llama al login antes de mostrar la app
login()
# ---------- Fin Login ----------


st.set_page_config(page_title="Generador de Plantillas BID", page_icon="📑")
st.title("📑 Generador de Plantillas BID")

st.markdown(
"""
1. Carga uno o varios archivos **.xlsx** que contengan las hojas  
   *SDO & Result Indicators* y *Solutions & Outputs*.
2. Haz clic en **Procesar**.  
3. Descarga el archivo enriquecido que se genera automáticamente.
"""
)

uploaded_files = st.file_uploader(
    "Arrastra o selecciona tus proyectos (.xlsx)", type=["xlsx"], accept_multiple_files=True
)

if st.button("Procesar") and uploaded_files:
    for f in uploaded_files:
        with st.spinner(f"Procesando {f.name} ..."):
            out_name, out_bytes = run_pipeline(f.read())
            st.success(f"✅ {f.name} procesado")
            st.download_button(
                label="Descargar resultado",
                data=out_bytes,
                file_name=f"{f.name.rsplit('.',1)[0]}_{out_name}",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
else:
    st.info("Carga al menos un archivo para habilitar el botón.")
