import streamlit as st
import google.generativeai as genai
import streamlit_option_menu as option_menu

# Configuración de la API de Gemini
try:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)

    # Modelo Gemini (usar uno de los modelos disponibles)
    model = genai.GenerativeModel('gemini-1.5-flash')
except KeyError:
    st.error("La clave de API de Gemini no se ha encontrado. Asegúrate de que esté configurada en st.secrets.")
    model = None  # Establecer el modelo a None si la clave de API no está disponible

def generar_plan_entrenamiento(edad, altura, peso, genero, experiencia_trail, experiencia_mtb):
    """
    Genera un plan de entrenamiento personalizado utilizando la API de Gemini.
    """
    prompt = f"""
    Genera un plan de entrenamiento personalizado para una persona de {edad} años,
    {altura} cm de altura, {peso} kg de peso y género {genero}.
    El usuario tiene experiencia en trail running de nivel {experiencia_trail} y en MTB de nivel {experiencia_mtb}.
    El plan debe incluir recomendaciones diarias y niveles de intensidad.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error al generar el plan de entrenamiento: {e}")
        return None

# Interfaz de Streamlit
st.markdown("""
    <style>
    body {
        background-color: #333;
        color: #fff;
    }
    .big-font {
        font-size:36px !important;
        font-weight: bold;
        color: #007bff;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #222;
        color: #fff;
        text-align: center;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar menu
with st.sidebar:
    selected = option_menu.option_menu(
        menu_title="Main Menu",
        options=["Generar Plan", "Acerca de"],
        icons=["activity", "question-circle"],
        menu_icon="cast",
        default_index=0,
    )

st.markdown('<p class="big-font">Tu entrenador inteligente</p>', unsafe_allow_html=True)

if selected == "Generar Plan":
    # Formulario de entrada de datos
    edad = st.number_input("Edad", min_value=10, max_value=100, value=30)
    altura = st.number_input("Altura (cm)", min_value=100, max_value=250, value=170)
    peso = st.number_input("Peso (kg)", min_value=30, max_value=150, value=70)
    genero = st.selectbox("Género", ["Masculino", "Femenino"])
    experiencia_trail = st.selectbox("Experiencia en Trail Running", ["Principiante", "Intermedio", "Avanzado"])
    experiencia_mtb = st.selectbox("Experiencia en MTB", ["Principiante", "Intermedio", "Avanzado"])

    # Validar la entrada
    if edad <= 0:
        st.error("La edad debe ser un número positivo.")
    elif altura <= 0:
        st.error("La altura debe ser un número positivo.")
    elif peso <= 0:
        st.error("El peso debe ser un número positivo.")
    else:
        # Generar plan de entrenamiento
        if st.button("Generar Plan") and model is not None: # Verificar si el modelo está inicializado
            plan = generar_plan_entrenamiento(edad, altura, peso, genero, experiencia_trail, experiencia_mtb)
            if plan:
                st.subheader("Plan de Entrenamiento Generado:")
                # Parsear el plan en una lista de diccionarios
                plan_data = []
                semanas = plan.split("Semana ")
                for semana in semanas[1:]:
                    semana_num = semana[0]
                    dias = semana.split("Lunes:")
                    if len(dias) > 1:
                        lunes = dias[1].split("Martes:")[0].strip()
                        martes = semana.split("Martes:")[1].split("Miércoles:")[0].strip()
                        miercoles = semana.split("Miércoles:")[1].split("Jueves:")[0].strip()
                        jueves = semana.split("Jueves:")[1].split("Viernes:")[0].strip()
                        viernes = semana.split("Viernes:")[1].split("Sábado:")[0].strip()
                        sabado = semana.split("Sábado:")[1].split("Domingo:")[0].strip()
                        domingo = semana.split("Domingo:")[1].split("Semana")[0].strip()

                        plan_data.append({"Semana": semana_num, "Día": "Lunes", "Actividad": lunes})
                        plan_data.append({"Semana": semana_num, "Día": "Martes", "Actividad": martes})
                        plan_data.append({"Semana": semana_num, "Día": "Miércoles", "Actividad": miercoles})
                        plan_data.append({"Semana": semana_num, "Día": "Jueves", "Actividad": jueves})
                        plan_data.append({"Semana": semana_num, "Día": "Viernes", "Actividad": viernes})
                        plan_data.append({"Semana": semana_num, "Día": "Sábado", "Actividad": sabado})
                        plan_data.append({"Semana": semana_num, "Día": "Domingo", "Actividad": domingo})
                
                # Mostrar el plan como una tabla
                st.dataframe(plan_data)

elif selected == "Acerca de":
    st.write("Esta aplicación genera planes de entrenamiento personalizados para trail running y MTB.")

st.markdown('<div class="footer">Esta aplicación genera planes de entrenamiento personalizados para trail running y MTB. ¡Sigue adelante, tú puedes!</div>', unsafe_allow_html=True)