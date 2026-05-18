import streamlit as st
import pandas as pd
import datetime
import os

# --- 1. CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="Kunren", page_icon="💪", layout="centered")

DATA_FILE = "historial_habitos.csv"

# --- 2. GESTIÓN DE DATOS (El Motor Seguro) ---
def cargar_datos():
    # Estructura con las nuevas columnas de medidas
    columnas_base = [
        "Fecha", "Peso (kg)", "Cintura (cm)", "Cadera (cm)", "Brazos (cm)", "Piernas (cm)",
        "Modo del día", "Rutina Elegida", "Botellas de agua",
        "Hexalectol AM", "Higiene", "Alimentación", "Magnesio PM",
        "Hábitos Cumplidos", "Día Perfecto"
    ]
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # Añade columnas nuevas automáticamente si no existían antes
        for col in columnas_base:
            if col not in df.columns:
                df[col] = 0.0
        return df
    else:
        return pd.DataFrame(columns=columnas_base)

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

    # Fila 2: Jornada y Entrenamiento (Actualizado)
    col3, col4 = st.columns(2)
    with col3:
        modo_dia = st.selectbox("Modo del día", ["Universidad", "Fin de semana", "Vacaciones"])
    with col4:
        rutina_elegida = st.selectbox(
            "¿Qué entrenamos hoy?", 
            ["Push (Empuje)", "Pull (Tirón)", "Legs (Piernas)", "Upper Body", "Lower Body", "Descanso Activo", "Cardio"]
        )

    # Fila 3: Registro de Agua
    agua = st.number_input("💧 Botellas de agua", min_value=0, max_value=10, value=0, step=1)

st.write("---")
st.subheader("📏 Medidas Corporales (Opcional)")
# Sección nueva de medidas
m_col1, m_col2 = st.columns(2)
with m_col1:
    cintura = st.number_input("Cintura (cm)", min_value=0.0, value=0.0, step=0.1)
    brazos = st.number_input("Brazos (cm)", min_value=0.0, value=0.0, step=0.1)
with m_col2:
    cadera = st.number_input("Cadera (cm)", min_value=0.0, value=0.0, step=0.1)
    piernas = st.number_input("Piernas (cm)", min_value=0.0, value=0.0, step=0.1)

st.write("---")
st.subheader("🎛️ Check de Hábitos")

with st.container():
    h_hexalectol = st.checkbox("💊 Hexalectol AM")
    h_higiene = st.checkbox("🪥 Higiene Completa")
    h_alimentacion = st.checkbox("🥩 Alimentación Alta en Proteína")
    h_magnesio = st.checkbox("🌙 Magnesio PM")

# --- 4. CÁLCULOS INTELIGENTES ---
habitos_cumplidos = sum([h_hexalectol, h_higiene, h_alimentacion, h_magnesio])
dia_perfecto = 1 if habitos_cumplidos == 4 else 0

st.write("---")
m1, m2 = st.columns(2)
m1.metric(label="Hábitos Logrados", value=f"{habitos_cumplidos} / 4")
if dia_perfecto == 1:
    m2.success("🏆 ¡DÍA PERFECTO!")
else:
    m2.info("Aún faltan hábitos")

# --- 5. BOTÓN DE GUARDADO SEGURO ---
st.write("") 
if st.button("💾 Guardar Registro del Día", type="primary", use_container_width=True):
    
    nueva_fila = pd.DataFrame([{
        "Fecha": fecha_str, "Peso (kg)": peso, 
        "Cintura (cm)": cintura, "Cadera (cm)": cadera, "Brazos (cm)": brazos, "Piernas (cm)": piernas,
        "Modo del día": modo_dia, "Rutina Elegida": rutina_elegida, "Botellas de agua": agua,
        "Hexalectol AM": h_hexalectol, "Higiene": h_higiene, "Alimentación": h_alimentacion, "Magnesio PM": h_magnesio,
        "Hábitos Cumplidos": habitos_cumplidos, "Día Perfecto": dia_perfecto
    }])
    
    if not df_historial.empty and fecha_str in df_historial["Fecha"].values:
        df_historial.loc[df_historial["Fecha"] == fecha_str, nueva_fila.columns] = nueva_fila.values[0]
    else:
        df_historial = pd.concat([df_historial, nueva_fila], ignore_index=True)
        
    df_historial.to_csv(DATA_FILE, index=False)
    st.success("¡Datos y medidas guardados impecablemente!")

# --- 6. PESTAÑA DE ESTADÍSTICAS Y GRÁFICOS ---
if not df_historial.empty:
    st.write("---")
    st.header("📊 Tus Estadísticas y Avances")
    
    df_grafico = df_historial.sort_values("Fecha")
    
    # Gráfico de Peso
    st.subheader("📉 Evolución de Peso")
    st.line_chart(data=df_grafico, x="Fecha", y="Peso (kg)")
    
    # Nuevo Gráfico de Medidas
    st.subheader("📏 Avance de Medidas")
    st.markdown("Selecciona las medidas que quieres comparar en el gráfico:")
    metricas_elegidas = st.multiselect(
        "Filtro de medidas:", 
        ["Cintura (cm)", "Cadera (cm)", "Brazos (cm)", "Piernas (cm)"],
        default=["Cintura (cm)", "Cadera (cm)"]
    )
    
    if metricas_elegidas:
        # Filtramos para que el gráfico no se caiga a cero en los días que no te mediste
        df_medidas = df_grafico[["Fecha"] + metricas_elegidas].replace(0.0, pd.NA).dropna()
        if not df_medidas.empty:
            st.line_chart(data=df_medidas, x="Fecha", y=metricas_elegidas)
        else:
            st.info("Guarda medidas mayores a 0 para generar tu gráfico de evolución.")
    
    # Gráfico de Rutinas
    st.subheader("🏋️‍♂️ Frecuencia de Entrenamientos")
    rutinas_conteo = df_historial["Rutina Elegida"].value_counts()
    st.bar_chart(rutinas_conteo)
