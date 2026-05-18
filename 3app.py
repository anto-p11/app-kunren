import streamlit as st
import pandas as pd
import datetime
import os

# --- 1. CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="Kunren", page_icon="💪", layout="centered")

DATA_FILE = "historial_habitos.csv"

# --- 2. GESTIÓN DE DATOS (El Motor) ---
def cargar_datos():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Estructura inicial idéntica a tu diseño original
        return pd.DataFrame(columns=[
            "Fecha", "Peso (kg)", "Modo del día", "Rutina Elegida", "Botellas de agua",
            "Hexalectol AM", "Higiene", "Alimentación", "Magnesio PM",
            "Hábitos Cumplidos", "Día Perfecto"
        ])

df_historial = cargar_datos()

# --- 3. INTERFAZ PRINCIPAL ---
st.title("📅 Kunren: Registro Diario")
st.markdown("Registra tu progreso y mantén tu racha intacta.")

with st.container():
    # Fila 1: Fecha y Peso
    col1, col2 = st.columns(2)
    with col1:
        fecha_hoy = st.date_input("Fecha de registro", datetime.date.today())
        fecha_str = fecha_hoy.strftime("%Y-%m-%d")
    with col2:
        peso = st.number_input("Peso actual (kg)", min_value=30.0, max_value=150.0, value=66.0, step=0.1)

    # Fila 2: Jornada y Entrenamiento
    col3, col4 = st.columns(2)
    with col3:
        modo_dia = st.selectbox("Modo del día", ["Universidad", "Fin de semana", "Vacaciones"])
    with col4:
        # Rutinas adaptadas a un split Push/Pull/Legs
        rutina_elegida = st.selectbox(
            "¿Qué entrenamos hoy?", 
            ["Push (Empuje)", "Pull (Tirón)", "Legs (Piernas)", "Descanso Activo", "Cardio"]
        )

    # Fila 3: Registro de Agua
    agua = st.number_input("💧 Botellas de agua", min_value=0, max_value=10, value=0, step=1)

st.write("---")
st.subheader("🎛️ Check de Hábitos")

# Contenedor de hábitos con diseño limpio
with st.container():
    h_hexalectol = st.checkbox("💊 Hexalectol AM")
    h_higiene = st.checkbox("🪥 Higiene Completa")
    h_alimentacion = st.checkbox("🥩 Alimentación Alta en Proteína")
    h_magnesio = st.checkbox("🌙 Magnesio PM")

# --- 4. CÁLCULOS INTELIGENTES ---
# Convierte los booleanos (True/False) a números (1/0) y los suma
habitos_cumplidos = sum([h_hexalectol, h_higiene, h_alimentacion, h_magnesio])
dia_perfecto = 1 if habitos_cumplidos == 4 else 0

st.write("---")
# Panel de métricas en vivo
m1, m2 = st.columns(2)
m1.metric(label="Hábitos Logrados", value=f"{habitos_cumplidos} / 4")
if dia_perfecto == 1:
    m2.success("🏆 ¡DÍA PERFECTO!")
else:
    m2.info("Aún faltan hábitos")

# --- 5. BOTÓN DE GUARDADO SEGURO ---
st.write("") # Espacio
if st.button("💾 Guardar Registro del Día", type="primary", use_container_width=True):
    
    # Preparamos los datos tal cual los ingresaste
    nueva_fila = pd.DataFrame([{
        "Fecha": fecha_str,
        "Peso (kg)": peso,
        "Modo del día": modo_dia,
        "Rutina Elegida": rutina_elegida,
        "Botellas de agua": agua,
        "Hexalectol AM": h_hexalectol,
        "Higiene": h_higiene,
        "Alimentación": h_alimentacion,
        "Magnesio PM": h_magnesio,
        "Hábitos Cumplidos": habitos_cumplidos,
        "Día Perfecto": dia_perfecto
    }])
    
    # Lógica de sobreescritura si el día ya existe, o creación si es nuevo
    if not df_historial.empty and fecha_str in df_historial["Fecha"].values:
        df_historial.loc[df_historial["Fecha"] == fecha_str, nueva_fila.columns] = nueva_fila.values[0]
    else:
        df_historial = pd.concat([df_historial, nueva_fila], ignore_index=True)
        
    # Guardamos en el archivo
    df_historial.to_csv(DATA_FILE, index=False)
    st.success("¡Datos guardados de forma impecable!")

# --- 6. PESTAÑA DE ESTADÍSTICAS ---
if not df_historial.empty:
    with st.expander("📊 Ver Mis Estadísticas y Gráficos"):
        st.subheader("📉 Evolución de Peso")
        df_grafico = df_historial.sort_values("Fecha")
        st.line_chart(data=df_grafico, x="Fecha", y="Peso (kg)")
        
        st.subheader("🏋️‍♂️ Distribución de Entrenamientos")
        rutinas_conteo = df_historial["Rutina Elegida"].value_counts()
        st.bar_chart(rutinas_conteo)