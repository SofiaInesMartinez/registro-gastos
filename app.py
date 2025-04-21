import streamlit as st
import pandas as pd
import os

# Archivo CSV donde se guardan los gastos
ARCHIVO_GASTOS = "gastos.csv"

# Cargar los datos existentes (si el archivo existe)
def cargar_gastos():
    if os.path.exists(ARCHIVO_GASTOS):
        return pd.read_csv(ARCHIVO_GASTOS)
    else:
        return pd.DataFrame(columns=["Nombre", "Monto"])

# Guardar un nuevo gasto en el archivo CSV
def guardar_gasto(nombre, monto):
    nuevo_gasto = pd.DataFrame([[nombre, monto]], columns=["Nombre", "Monto"])
    gastos = cargar_gastos()
    gastos = pd.concat([gastos, nuevo_gasto], ignore_index=True)
    gastos.to_csv(ARCHIVO_GASTOS, index=False)

# --- Interfaz con Streamlit ---

st.set_page_config(page_title="Registro de Gastos", page_icon="💸")

st.title("💸 Registro de Gastos Personales")

with st.form(key="formulario_gasto"):
    nombre = st.text_input("Nombre del gasto")
    monto = st.number_input("Monto ($)", min_value=0.0, step=0.5)
    submitted = st.form_submit_button("Agregar gasto")

    if submitted:
        if nombre.strip() == "":
            st.warning("Por favor, ingresá un nombre para el gasto.")
        else:
            guardar_gasto(nombre, monto)
            st.success(f"Gasto '{nombre}' de ${monto:.2f} agregado.")

# Mostrar tabla de gastos
st.subheader("📋 Historial de gastos")

gastos = cargar_gastos()
if gastos.empty:
    st.info("Aún no se registraron gastos.")
else:
    st.dataframe(gastos, use_container_width=True)

    total = gastos["Monto"].sum()
    st.markdown(f"### 💰 Total gastado: ${total:.2f}")
