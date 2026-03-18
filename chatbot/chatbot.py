import streamlit as st
import pandas as pd
import joblib

# --- CONFIGURACIÓN DE PÁGINA ---
# Esto debe ir al principio. Configura el título de la pestaña y el layout.
st.set_page_config(page_title="EcoTecho Educativo", page_icon="🌱", layout="wide")

# --- CSS PERSONALIZADO ---
# Inyectamos un poco de CSS para intentar igualar tu paleta de colores
st.markdown("""
    <style>
    /* Color de fondo de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #2b303b;
        color: white;
    }
    /* Estilo del título de la barra lateral */
    .sidebar-title {
        color: #4CAF50; /* Verde EcoTecho */
        font-size: 24px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- CARGA DE MODELOS ---
# Carga los modelos que exportaste desde tu notebook
try:
    modelo_rl_supervivencia = joblib.load('modelo_rl_sobrevivencia.pkl')
    modelo_rf_consumo = joblib.load('modelo_rf_consumo.pkl')
except FileNotFoundError:
    st.error("No se encontraron los modelos. Asegúrate de haber ejecutado joblib.dump() en tu notebook y que los archivos .pkl estén en la misma carpeta.")

# --- BARRA LATERAL (Sidebar) ---
with st.sidebar:
    st.markdown('<p class="sidebar-title">🌱 EcoTecho Educativo</p>', unsafe_allow_html=True)
    st.write("Asistente especializado en sostenibilidad de techos verdes para instituciones educativas. Base de datos con 381 especies vegetales.")
    
    st.divider()
    
    # Acordeones para replicar tu menú izquierdo
    with st.expander("📚 Consultas disponibles"):
        st.write("- Predicción de supervivencia\n- Consumo de agua\n- Información de especies")
        
    with st.expander("💡 Ejemplos de consultas"):
        st.write('Prueba preguntar: *"Predice la supervivencia de la especie 1 en el día 50 usando Random Forest."*')
        
    with st.expander("🌿 Especies destacadas"):
        st.write("1. Ajuga reptans\n2. Sendum\n3. Greenovia\n4. Ramilletes")
        
    with st.expander("❓ Preguntas frecuentes"):
        st.write("**¿De dónde provienen los datos?**\nDe estudios de adaptación de especies en Bogotá.")

# --- ÁREA PRINCIPAL (Chat) ---
st.header("Asistente de Sostenibilidad")
st.caption("Pregúntame sobre especies vegetales, sistemas de techos verdes y jardines verticales")

# Inicializar historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! Soy tu asistente especializado en techos verdes sostenibles para entornos educativos. Tengo información detallada sobre 381 especies vegetales, sistemas de techos verdes, jardines verticales y requisitos técnicos según normativa colombiana. ¿En qué puedo ayudarte hoy?"}
    ]

# Mostrar historial del chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
prompt = st.chat_input("Ejemplo: ¿Qué especies son resistentes a sequía?")

if prompt:
    # 1. Mostrar y guardar el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Lógica MUY BÁSICA para detectar qué quiere el usuario
    # Idealmente, aquí conectarías con un LLM o usarías expresiones regulares (Regex) para extraer los números.
    # Por ahora, haremos una prueba con palabras clave.
    respuesta = "No entendí muy bien tu consulta. Intenta preguntar por la predicción de la especie 1 en el día 50."
    
    if "supervivencia" in prompt.lower() and "especie 1" in prompt.lower():
        especie = 1
        dia = 50 # Valor por defecto para la prueba
        
        # Preparar datos para el modelo (igual que en tu notebook)
        input_data = pd.DataFrame([[especie, dia]], columns=['especies', 'dia_1'])
        
        if "random forest" in prompt.lower():
            prediccion = modelo_rf_supervivencia.predict(input_data)[0]
            respuesta = f"🌿 **Predicción Random Forest:** La supervivencia para la especie {especie} en el día {dia} es de **{prediccion:.2f}**."
        else:
            prediccion = modelo_rl_supervivencia.predict(input_data)[0][0]
            respuesta = f"📈 **Predicción Regresión Lineal:** La supervivencia para la especie {especie} en el día {dia} es de **{prediccion:.2f}**."

    # 3. Mostrar y guardar la respuesta del asistente
    with st.chat_message("assistant"):
        st.markdown(respuesta)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})