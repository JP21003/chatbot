import streamlit as st
import pandas as pd
import joblib
import sqlite3
import os
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA Y CSS ---
st.set_page_config(page_title="EcoTecho Educativo", page_icon="🌱", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #2b303b; color: white; }
    .sidebar-title { color: #4CAF50; font-size: 24px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DEL MODELO DE LENGUAJE (GEMINI) ---
# Intentamos cargar la API Key desde los secretos de Streamlit
llm_activado = False
try:
    # Configura la API Key. En Streamlit Cloud se configura en la sección "Secrets"
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    llm_model = genai.GenerativeModel('gemini-1.5-flash')
    llm_activado = True
except Exception:
    st.sidebar.warning("⚠️ Modelo de lenguaje (Gemini) no configurado. Faltan las API Keys. Se usarán respuestas básicas.")

# --- INICIALIZACIÓN DE LA BASE DE DATOS ---
def inicializar_bd():
    if not os.path.exists('base_conocimiento.db'):
        conn = sqlite3.connect('base_conocimiento.db')
        cursor = conn.cursor()
        archivos_sql = ['estructura_techo_verde.sql', 'especies_vegetales.sql', 'infraestructura_vegetada_2023.sql']
        for archivo in archivos_sql:
            if os.path.exists(archivo):
                with open(archivo, 'r', encoding='utf-8') as f:
                    try:
                        cursor.executescript(f.read())
                    except Exception:
                        pass
        conn.commit()
        conn.close()

inicializar_bd()

# --- CARGA DE MODELOS PREDICTIVOS CON DETECCIÓN DE ERRORES ---
@st.cache_resource
def cargar_modelos():
    try:
        # Verificamos si los archivos realmente existen en la carpeta
        if not os.path.exists('modelo_rl_sobrevivencia.pkl'):
            st.error("❌ No se encuentra el archivo 'modelo_rl_sobrevivencia.pkl' en el directorio.")
            return None, None
            
        rl = joblib.load('modelo_rl_sobrevivencia.pkl')
        rf = joblib.load('modelo_rf_sobrevivencia.pkl')
        return rl, rf
    except Exception as e:
        # Si falla por versiones de librerías, mostrará el error exacto aquí:
        st.error(f"❌ Error interno al cargar los modelos .pkl: {e}")
        return None, None

modelo_rl, modelo_rf = cargar_modelos()

# --- MOTOR DE BÚSQUEDA EN BASE DE DATOS ---
def buscar_en_bd(consulta):
    conn = sqlite3.connect('base_conocimiento.db')
    cursor = conn.cursor()
    consulta = consulta.lower()
    contexto_crudo = ""
    
    try:
        if "norma" in consulta or "requisito" in consulta:
            cursor.execute("SELECT descripcion, aplica_a FROM normativas LIMIT 5")
            for desc, aplica in cursor.fetchall():
                contexto_crudo += f"Normativa: {desc} (Aplica a: {aplica})\n"
                    
        elif "riego" in consulta or "sustrato" in consulta or "especie" in consulta:
            cursor.execute("SELECT nombre_cientifico, riego_requerido, sustrato_recomendado FROM especies_vegetales WHERE nombre_cientifico != '' LIMIT 5")
            for nombre, riego, sustrato in cursor.fetchall():
                contexto_crudo += f"Especie: {nombre}, Riego: {riego}, Sustrato: {sustrato}\n"
                    
        elif "qué es" in consulta or "definición" in consulta or "jardín" in consulta:
            cursor.execute("SELECT termino, definicion FROM definiciones LIMIT 3")
            for termino, definicion in cursor.fetchall():
                contexto_crudo += f"Definición de {termino}: {definicion}\n"
    except Exception:
        pass
    finally:
        conn.close()
        
    return contexto_crudo

# --- FUNCIÓN PARA GENERAR RESPUESTA CON LLM ---
def generar_respuesta_natural(pregunta_usuario, contexto_datos):
    if not llm_activado:
        return f"Aquí tienes la información cruda:\n{contexto_datos}"
    
    prompt = f"""
    Eres 'EcoTecho Educativo', un asistente experto en sostenibilidad de techos verdes y jardines verticales en Colombia.
    El usuario te ha preguntado: "{pregunta_usuario}"
    
    Basado ÚNICAMENTE en la siguiente información de tu base de datos o modelos predictivos, redacta una respuesta natural, conversacional y fácil de entender. 
    No inventes datos que no estén en el contexto. Si el contexto está vacío, dile al usuario que no tienes información exacta pero invítalo a preguntar sobre normativas, riego o supervivencia.
    
    CONTEXTO PROVISTO:
    {contexto_datos}
    """
    
    try:
        respuesta = llm_model.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        return f"Error en el modelo de lenguaje: {e}\n\nDatos crudos: {contexto_datos}"

# --- BARRA LATERAL ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">🌱 EcoTecho Educativo</p>', unsafe_allow_html=True)
    st.write("Asistente especializado en sostenibilidad de techos verdes para instituciones educativas.")
    st.divider()
    with st.expander("📚 Consultas disponibles"):
        st.write("- Predicción de supervivencia\n- Información de normativas\n- Fichas de especies")

# --- ÁREA DE CHAT ---
st.header("Asistente de Sostenibilidad")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! Soy tu asistente sobre techos verdes. Puedo predecir la supervivencia de especies o consultar normativas y cuidados. ¿En qué te ayudo hoy?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Escribe tu consulta aquí...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    contexto_para_llm = ""

    # 1. Obtener datos (De ML o de SQL)
    if "predic" in prompt.lower() or "supervivencia" in prompt.lower():
        if modelo_rl is not None and modelo_rf is not None:
            especie, dia = 1, 50 
            input_data = pd.DataFrame([[especie, dia]], columns=['especies', 'dia_1'])
            
            if "random forest" in prompt.lower():
                prediccion = modelo_rf.predict(input_data)[0]
                contexto_para_llm = f"El modelo de Random Forest predice una supervivencia de {prediccion:.2f} para la especie {especie} en el día {dia}."
            else:
                prediccion = modelo_rl.predict(input_data)[0][0]
                contexto_para_llm = f"El modelo de Regresión Lineal predice una supervivencia de {prediccion:.2f} para la especie {especie} en el día {dia}."
        else:
            contexto_para_llm = "No se pudieron realizar las predicciones porque los modelos .pkl no están cargados correctamente. Revisa los mensajes de error en la parte superior."
            
    else:
        # Buscar en base de datos
        resultado_sql = buscar_en_bd(prompt)
        if resultado_sql:
            contexto_para_llm = resultado_sql
        else:
            contexto_para_llm = "No se encontró información en la base de datos sobre la consulta del usuario."

    # 2. Pasar los datos al LLM para que los ponga bonitos
    with st.spinner("Generando respuesta..."):
        respuesta_bot = generar_respuesta_natural(prompt, contexto_para_llm)

    with st.chat_message("assistant"):
        st.markdown(respuesta_bot)
    st.session_state.messages.append({"role": "assistant", "content": respuesta_bot})
