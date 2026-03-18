import streamlit as st
import pandas as pd
import joblib
import sqlite3
import os

# --- CONFIGURACIÓN DE PÁGINA Y CSS ---
st.set_page_config(page_title="EcoTecho Educativo", page_icon="🌱", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #2b303b;
        color: white;
    }
    .sidebar-title {
        color: #4CAF50;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE LA BASE DE DATOS ---
def inicializar_bd():
    """Crea la base de datos SQLite a partir de los archivos .sql si no existe."""
    if not os.path.exists('base_conocimiento.db'):
        conn = sqlite3.connect('base_conocimiento.db')
        cursor = conn.cursor()
        
        # Lista de tus archivos SQL
        archivos_sql = [
            'estructura_techo_verde.sql', 
            'especies_vegetales.sql', 
            'infraestructura_vegetada_2023.sql'
        ]
        
        for archivo in archivos_sql:
            if os.path.exists(archivo):
                with open(archivo, 'r', encoding='utf-8') as f:
                    script_sql = f.read()
                    try:
                        cursor.executescript(script_sql)
                    except Exception as e:
                        print(f"Nota: Hubo un detalle cargando {archivo}: {e}")
        conn.commit()
        conn.close()

# Ejecutar la inicialización silenciosamente
inicializar_bd()

# --- CARGA DE MODELOS ---
@st.cache_resource
def cargar_modelos():
    try:
        rl = joblib.load('modelo_rl_sobrevivencia.pkl')
        rf = joblib.load('modelo_rf_sobrevivencia.pkl')
        return rl, rf
    except Exception:
        return None, None

modelo_rl, modelo_rf = cargar_modelos()

# --- MOTOR DE BÚSQUEDA EN BASE DE DATOS ---
def buscar_en_bd(consulta):
    conn = sqlite3.connect('base_conocimiento.db')
    cursor = conn.cursor()
    consulta = consulta.lower()
    respuesta = ""
    
    try:
        if "norma" in consulta or "requisito" in consulta:
            cursor.execute("SELECT descripcion, aplica_a FROM normativas LIMIT 5")
            resultados = cursor.fetchall()
            if resultados:
                respuesta += "📚 **Normativas y Requisitos aplicables:**\n"
                for desc, aplica in resultados:
                    respuesta += f"- {desc} (Aplica a: {aplica})\n"
                    
        elif "riego" in consulta or "sustrato" in consulta or "especie" in consulta:
            cursor.execute("SELECT nombre_cientifico, riego_requerido, sustrato_recomendado FROM especies_vegetales WHERE nombre_cientifico != '' LIMIT 5")
            resultados = cursor.fetchall()
            if resultados:
                respuesta += "🌿 **Recomendaciones de cuidado (Ejemplos de la BD):**\n"
                for nombre, riego, sustrato in resultados:
                    respuesta += f"**{nombre}**\n- Riego: {riego}\n- Sustrato: {sustrato}\n\n"
                    
        elif "qué es" in consulta or "definición" in consulta or "jardín vertical" in consulta:
            # Busca tanto en terminos como en definiciones
            cursor.execute("SELECT termino, definicion FROM definiciones LIMIT 3")
            resultados = cursor.fetchall()
            if resultados:
                respuesta += "📖 **Glosario Técnico:**\n"
                for termino, definicion in resultados:
                    respuesta += f"- **{termino}:** {definicion}\n"
    except Exception as e:
        pass # Falla silenciosa si una tabla no existe
    finally:
        conn.close()
        
    return respuesta

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">🌱 EcoTecho Educativo</p>', unsafe_allow_html=True)
    st.write("Asistente especializado en sostenibilidad de techos verdes para instituciones educativas.")
    st.divider()
    with st.expander("📚 Consultas disponibles"):
        st.write("- Predicción de supervivencia\n- Información de normativas\n- Fichas de especies")
    with st.expander("💡 Ejemplos de consultas"):
        st.write('*"Predice la supervivencia de la especie 1 en el día 50"*')
        st.write('*"¿Qué normativas aplican?"*')
        st.write('*"¿Cuál es el riego para las especies?"*')

# --- ÁREA DE CHAT ---
st.header("Asistente de Sostenibilidad")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy tu asistente sobre techos verdes. Puedo predecir la supervivencia de especies o consultar normativas y cuidados. ¿En qué te ayudo hoy?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Escribe tu consulta aquí...")

if prompt:
    # 1. Guardar y mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    respuesta_bot = ""

    # 2. Lógica de Enrutamiento Inteligente
    if "predic" in prompt.lower() or "supervivencia" in prompt.lower():
        if modelo_rl is not None and modelo_rf is not None:
            # Simulamos la extracción de especie 1, día 50 (puedes mejorarlo con Regex después)
            especie, dia = 1, 50 
            input_data = pd.DataFrame([[especie, dia]], columns=['especies', 'dia_1'])
            
            if "random forest" in prompt.lower():
                prediccion = modelo_rf.predict(input_data)[0]
                respuesta_bot = f"🌿 **Random Forest:** La supervivencia para la especie {especie} en el día {dia} es de **{prediccion:.2f}**."
            else:
                prediccion = modelo_rl.predict(input_data)[0][0]
                respuesta_bot = f"📈 **Regresión Lineal:** La supervivencia para la especie {especie} en el día {dia} es de **{prediccion:.2f}**."
        else:
            respuesta_bot = "⚠️ Los modelos predictivos no están cargados. Revisa los archivos .pkl."
            
    else:
        # Consulta a las bases de datos SQL
        resultado_sql = buscar_en_bd(prompt)
        if resultado_sql:
            respuesta_bot = resultado_sql
        else:
            respuesta_bot = "No encontré información específica sobre eso. Prueba preguntando por **normativas**, **riego**, **definiciones** o pide una **predicción**."

    # 3. Mostrar y guardar respuesta del bot
    with st.chat_message("assistant"):
        st.markdown(respuesta_bot)
    st.session_state.messages.append({"role": "assistant", "content": respuesta_bot})
