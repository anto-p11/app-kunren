import streamlit as st
import pandas as pd
import datetime
import os

# --- 1. CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="Kunren", page_icon="💪", layout="centered")

DATA_FILE = "historial_habitos.csv"
META_PESO = 55.0

# --- 2. CÁLCULOS INTELIGENTES ---
def calcular_racha_actual(df):
    if df.empty or "Día Perfecto" not in df.columns:
        return 0
    df_ordenado = df.sort_values("Fecha", ascending=False)
    racha = 0
    for perfecto in df_ordenado["Día Perfecto"]:
        if perfecto == 1 or perfecto == 1.0:
            racha += 1
        else:
            break
    return racha

def mostrar_progreso_peso(df, peso_actual):
    if df.empty:
        st.info("Registra tu primer peso para activar la barra de progreso.")
        return
    
    peso_inicial = df.sort_values("Fecha").iloc[0]["Peso (kg)"]
    
    if peso_inicial <= META_PESO:
        st.success(f"¡Ya estás en tu meta o por debajo! 🎉 ({peso_actual} kg)")
        return

    progreso = (peso_inicial - peso_actual) / (peso_inicial - META_PESO)
    progreso = max(0.0, min(1.0, progreso))
    
    faltan = round(peso_actual - META_PESO, 1)
    
    st.markdown(f"**🎯 Meta: {META_PESO} kg** (Faltan {faltan} kg)")
    st.progress(progreso)
    st.caption(f"Has avanzado un {int(progreso*100)}% hacia tu objetivo desde que empezaste ({peso_inicial} kg).")

# --- 3. GESTIÓN DE DATOS ---
def cargar_datos():
    columnas_base = [
        "Fecha", "Peso (kg)", "Busto (cm)", "Cintura (cm)", "Cadera (cm)", "Brazos (cm)", "Piernas (cm)",
        "Modo del día", "Rutina Elegida", "Botellas de agua",
        "Hexalectol AM", "Higiene", "Alimentación", "Magnesio PM",
        "Hábitos Cumplidos", "Día Perfecto"
    ]
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        for col in columnas_base:
            if col not in df.columns:
                df[col] = 0.0
        return df
    else:
        return pd.DataFrame(columns=columnas_base)

df_historial = cargar_datos()
racha_actual = calcular_racha_actual(df_historial)

# --- 4. INTERFAZ PRINCIPAL ---
st.title("📅 Kunren: Registro Diario")

col_racha1, col_racha2 = st.columns(2)
with col_racha1:
    st.metric(label="Racha Actual 🔥", value=f"{racha_actual} días")
with col_racha2:
    st.markdown("**Calendario de Logros:**")
    if not df_historial.empty:
        mini_df = df_historial.sort_values("Fecha", ascending=False).head(3)
        for idx, row in mini_df.iterrows():
            icono = "🏆" if row["Día Perfecto"] == 1 else "❌"
            st.markdown(f"`{row['Fecha']}` {icono}")

st.write("")
if not df_historial.empty:
    ultimo_peso = df_historial.sort_values("Fecha").iloc[-1]["Peso (kg)"]
    mostrar_progreso_peso(df_historial, ultimo_peso)

st.write("---")

fecha_hoy = st.date_input("Fecha de registro", datetime.date.today())
fecha_str = fecha_hoy.strftime("%Y-%m-%d")

# --- CARGA DE DATOS PREVIOS DEL DÍA ---
val_peso = 66.0
val_modo = "Universidad"
val_rutina = "Push (Empuje)"
val_agua = 0
val_busto = 0.0
val_brazos = 0.0
val_cintura = 0.0
val_cadera = 0.0
val_piernas = 0.0
val_hexalectol = False
val_higiene = False
val_alimentacion = False
val_magnesio = False

if not df_historial.empty and fecha_str in df_historial["Fecha"].values:
    fila_hoy = df_historial[df_historial["Fecha"] == fecha_str].iloc[0]
    val_peso = float(fila_hoy.get("Peso (kg)", 66.0))
    val_modo = str(fila_hoy.get("Modo del día", "Universidad"))
    val_rutina = str(fila_hoy.get("Rutina Elegida", "Push (Empuje)"))
    val_agua = int(fila_hoy.get("Botellas de agua", 0))
    val_busto = float(fila_hoy.get("Busto (cm)", 0.0))
    val_brazos = float(fila_hoy.get("Brazos (cm)", 0.0))
    val_cintura = float(fila_hoy.get("Cintura (cm)", 0.0))
    val_cadera = float(fila_hoy.get("Cadera (cm)", 0.0))
    val_piernas = float(fila_hoy.get("Piernas (cm)", 0.0))
    val_hexalectol = bool(fila_hoy.get("Hexalectol AM", False))
    val_higiene = bool(fila_hoy.get("Higiene", False))
    val_alimentacion = bool(fila_hoy.get("Alimentación", False))
    val_magnesio = bool(fila_hoy.get("Magnesio PM", False))

lista_modos = ["Universidad", "Fin de semana", "Vacaciones"]
idx_modo = lista_modos.index(val_modo) if val_modo in lista_modos else 0
lista_rutinas = ["Push (Empuje)", "Pull (Tirón)", "Legs (Piernas)", "Upper Body", "Lower Body", "Descanso Activo", "Cardio"]
idx_rutina = lista_rutinas.index(val_rutina) if val_rutina in lista_rutinas else 0

# --- 5. BLOQUE DE REGISTRO VISUAL ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        peso_input = st.number_input("Peso actual (kg)", min_value=30.0, max_value=150.0, value=val_peso, step=0.1)
    with col2:
        agua = st.number_input("💧 Botellas de agua", min_value=0, max_value=10, value=val_agua, step=1)

    col3, col4 = st.columns(2)
    with col3:
        modo_dia = st.selectbox("Modo del día", lista_modos, index=idx_modo)
    with col4:
        rutina_elegida = st.selectbox("¿Qué entrenamos hoy?", lista_rutinas, index=idx_rutina)

# --- 6. MEDIDAS SEPARADAS ---
st.write("---")
with st.expander("📏 Dimensiones Corporales", expanded=False):
    st.markdown("#### 📐 Tren Superior")
    col_sup1, col_sup2 = st.columns(2)
    with col_sup1:
        busto = st.number_input("Busto (cm)", min_value=0.0, value=val_busto, step=0.1)
    with col_sup2:
        brazos = st.number_input("Brazos (cm)", min_value=0.0, value=val_brazos, step=0.1)
        
    st.markdown("#### 📐 Zona Media e Inferior")
    col_inf1, col_inf2, col_inf3 = st.columns(3)
    with col_inf1:
        cintura = st.number_input("Cintura (cm)", min_value=0.0, value=val_cintura, step=0.1)
    with col_inf2:
        cadera = st.number_input("Cadera (cm)", min_value=0.0, value=val_cadera, step=0.1)
    with col_inf3:
        piernas = st.number_input("Piernas (cm)", min_value=0.0, value=val_piernas, step=0.1)

# --- 7. CHECK DE HÁBITOS ---
st.write("---")
st.subheader("🎛️ Check de Hábitos")
with st.container():
    h_hexalectol = st.checkbox("💊 Hexalectol AM", value=val_hexalectol)
    h_higiene = st.checkbox("🪥 Higiene Completa", value=val_higiene)
    h_alimentacion = st.checkbox("🥩 Alimentación Alta en Proteína", value=val_alimentacion)
    h_magnesio = st.checkbox("🌙 Magnesio PM", value=val_magnesio)

habitos_cumplidos = sum([h_hexalectol, h_higiene, h_alimentacion, h_magnesio])
dia_perfecto = 1 if habitos_cumplidos == 4 else 0

st.write("---")
m1, m2 = st.columns(2)
m1.metric(label="Hábitos Logrados", value=f"{habitos_cumplidos} / 4")
if dia_perfecto == 1:
    m2.success("🏆 ¡DÍA PERFECTO!")
else:
    m2.info("Aún faltan hábitos")

st.write("---")

# --- 8. SISTEMA DE DOBLE BOTÓN DE GUARDADO ---
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    btn_guardar_avance = st.button("💾 Guardar Avance", use_container_width=True)
with col_btn2:
    btn_finalizar_dia = st.button("🏁 Finalizar Día", type="primary", use_container_width=True)

if btn_guardar_avance or btn_finalizar_dia:
    nueva_fila = pd.DataFrame([{
        "Fecha": fecha_str, "Peso (kg)": peso_input, 
        "Busto (cm)": busto, "Cintura (cm)": cintura, "Cadera (cm)": cadera, "Brazos (cm)": brazos, "Piernas (cm)": piernas,
        "Modo del día": modo_dia, "Rutina Elegida": rutina_elegida, "Botellas de agua": agua,
        "Hexalectol AM": h_hexalectol, "Higiene": h_higiene, "Alimentación": h_alimentacion, "Magnesio PM": h_magnesio,
        "Hábitos Cumplidos": habitos_cumplidos, "Día Perfecto": dia_perfecto
    }])
    
    if not df_historial.empty and fecha_str in df_historial["Fecha"].values:
        df_historial.loc[df_historial["Fecha"] == fecha_str, nueva_fila.columns] = nueva_fila.values[0]
    else:
        df_historial = pd.concat([df_historial, nueva_fila], ignore_index=True)
        
    df_historial.to_csv(DATA_FILE, index=False)
    
    if btn_finalizar_dia:
        st.balloons()
        st.success("¡Jornada finalizada y guardada con éxito! 🏆")
    else:
        # Mensaje sutil que desaparece solo, ideal para no molestar
        st.toast('Avance guardado 💾', icon='✅')

# --- 9. HISTORIAL GRÁFICO ---
if not df_historial.empty:
    with st.expander("📊 Ver Mis Estadísticas y Avances"):
        df_grafico = df_historial.sort_values("Fecha")
        
        st.subheader("📉 Evolución de Peso")
        st.line_chart(data=df_grafico, x="Fecha", y="Peso (kg)")
        
        st.subheader("📏 Avance de Medidas")
        metricas_elegidas = st.multiselect(
            "Selecciona qué medidas comparar:", 
            ["Busto (cm)", "Cintura (cm)", "Cadera (cm)", "Brazos (cm)", "Piernas (cm)"],
            default=["Busto (cm)", "Cintura (cm)"]
        )
        if metricas_elegidas:
            df_medidas = df_grafico[["Fecha"] + metricas_elegidas].replace(0.0, pd.NA).dropna()
            if not df_medidas.empty:
                st.line_chart(data=df_medidas, x="Fecha", y=metricas_elegidas)
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.subheader("📊 Jornadas")
            st.bar_chart(df_historial["Modo del día"].value_counts())
        with col_g2:
            st.subheader("🏋️‍♂️ Rutinas")
            st.bar_chart(df_historial["Rutina Elegida"].value_counts())

# --- 10. ZONA DE PELIGRO ---
if not df_historial.empty:
    st.write("---")
    with st.expander("⚙️ Zona de Peligro"):
        fechas_disponibles = sorted(df_historial["Fecha"].unique(), reverse=True)
        fecha_a_borrar = st.selectbox("Selecciona fecha para borrar:", fechas_disponibles)
        if st.button("🗑️ Eliminar día seleccionado", use_container_width=True):
            df_historial = df_historial[df_historial["Fecha"] != fecha_a_borrar]
            df_historial.to_csv(DATA_FILE, index=False)
            st.success(f"Día {fecha_a_borrar} eliminado.")
            st.rerun()
