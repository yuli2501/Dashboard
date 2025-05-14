import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

from utils.dataAmsterdam import load_data as load_amsterdam_data
from utils.dataMexico import load_dataMexico as load_mexico_data
from utils.dataMilan import load_dataMilan as load_milan_data

# Función para crear las categorías de variables numéricas
def create_categoricals(df):
    df["accommodates_cat"] = pd.cut(df["accommodates"],
                                    bins=[0, 1, 2, 4, np.inf],
                                    labels=["1 persona", "2 personas", "3-4 personas", "5 o más"])

    df["bedrooms_cat"] = pd.cut(df["bedrooms"],
                                bins=[-1, 0, 1, 2, 3, np.inf],
                                labels=["Sin habitación", "1", "2", "3", "4 o más"])

    df["beds_cat"] = pd.cut(df["beds"],
                            bins=[-1, 0, 1, 2, 3, np.inf],
                            labels=["Sin cama", "1", "2", "3", "4 o más"])

    df["minimum_nights_cat"] = pd.cut(df["minimum_nights"],
                                      bins=[0, 1, 3, 7, np.inf],
                                      labels=["1 noche", "2-3 noches", "4-7 noches", "Más de 7 noches"])

    df["maximum_nights_cat"] = pd.cut(df["maximum_nights"],
                                      bins=[0, 7, 30, 90, np.inf],
                                      labels=["1-7 noches", "8-30 noches", "31-90 noches", "Más de 90 noches"])

    df["availability_365_cat"] = pd.cut(df["availability_365"],
                                        bins=[-1, 0, 30, 90, 180, 365],
                                        labels=["Sin disponibilidad", "1-30 días", "31-90 días", "91-180 días", "181-365 días"])

    return df

# Función para mostrar el análisis univariado de los 4 países
def mostrar_analisis_univariado():
    st.header("Análisis Univariado")
    
    st.markdown("---")

    # Variables categóricas directas
    categoricas_directas = [
        "host_is_superhost",
        "host_identity_verified",
        "neighbourhood_cleansed",
        "property_type",
        "room_type",
        "instant_bookable",
        "host_response_time",
        "has_availability"
    ]

    # Opciones de variables para el análisis
    opciones_variables = categoricas_directas + ["accommodates_cat", "bedrooms_cat", "beds_cat", "minimum_nights_cat", "maximum_nights_cat", "availability_365_cat"]

    # Variable objetivo y tipo de gráfica
    variable_objetivo = st.sidebar.selectbox("Variable objetivo", opciones_variables)
    tipo_grafica = st.sidebar.selectbox("Tipo de gráfica", ["Gráfica de pastel", "Gráfica de barras"])
    st.sidebar.markdown("---")
    show_info = st.sidebar.checkbox("Mostrar información sobre el análisis univariado")


    if show_info:
        st.write("""
        El análisis univariado de frecuencia nos permite conocer cuántas veces aparece cada valor o categoría dentro de una variable. 
        Esto es muy útil para entender la distribución de los datos, identificar valores atípicos o poco comunes, 
        y asegurarnos de que la información esté bien representada antes de continuar con otros análisis.
        """)
        st.markdown("---")
    # Cargar los datasets para los 4 países
    df_amsterdam, _, _, _, _ = load_amsterdam_data()  # Carga los datos de Ámsterdam
    df_mexico, _, _, _, _ = load_mexico_data()  # Carga los datos de México
    df_milan, _, _, _, _ = load_milan_data()  # Carga los datos de Milán

    # Crear variables categóricas para cada país
    df_amsterdam = create_categoricals(df_amsterdam)
    df_mexico = create_categoricals(df_mexico)
    df_milan = create_categoricals(df_milan)

    # Paleta de colores personalizada
    custom_palette = [
        "#C25E4C",  # Rojo ladrillo
        "#F7C59F",  # Durazno pastel 
        "#E5B25D",  # Mostaza tulipán
        "#F28C38",  # Naranja Holanda
        "#F0E5D8",  # Cremita
    ]
    
    # Mostrar la gráfica comparativa para cada país de manera independiente
    for country_name, df in [("Ámsterdam", df_amsterdam), 
                             ("CDMX", df_mexico), 
                             ("Milán", df_milan)]:
        
        # Crear un contenedor de tarjeta para el país y la gráfica
        with st.container():
            # Estilo de la tarjeta (solo el contorno y el nombre)
            st.markdown(f"""
                <div style="
                    background-color: #FFFFFF;
                    border: 2px solid #E5B25D;
                    border-radius: 10px;
                    padding: 1px;
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                    margin-bottom: 10px;
                ">
                <h3 style="text-align: center; color: #F28C38;">{country_name}</h3>
            """, unsafe_allow_html=True)

            # Filtrar los datos de la variable objetivo seleccionada
            conteo = df[[variable_objetivo]].value_counts().reset_index(name='Frecuencia')
            conteo.columns = [variable_objetivo, 'Frecuencia']

            # Mostrar gráfica según el tipo
            if tipo_grafica == "Gráfica de barras":
                fig = px.bar(conteo,
                             x=variable_objetivo,
                             y='Frecuencia',
                             text='Frecuencia',
                             color=variable_objetivo,
                             title=f"Frecuencia de {variable_objetivo} en {country_name}",
                             color_discrete_sequence=custom_palette)
            elif tipo_grafica == "Gráfica de pastel":
                fig = px.pie(conteo,
                             names=variable_objetivo,
                             values='Frecuencia',
                             title=f"Distribución de {variable_objetivo} en {country_name}",
                             color_discrete_sequence=custom_palette)

            fig.update_layout(
                title_x=0.3,  # Centra el título
                title_y=0.95,  # Ajusta la posición vertical del título
            )
            # Mostrar la gráfica dentro del contenedor de la tarjeta
            st.plotly_chart(fig, use_container_width=True)

            # Cerrar el contenedor de la tarjeta
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
