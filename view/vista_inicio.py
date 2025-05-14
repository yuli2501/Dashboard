import streamlit as st
from utils.dataAmsterdam import load_data as load_amsterdam_data
from utils.dataMexico import load_dataMexico as load_mexico_data
from utils.dataMilan import load_dataMilan as load_milan_data
from utils.dataHongKong import load_dataHongKong as load_hongKong_data




# Crear tarjetas 
def kpi_card_metric(title, value, delta, title_color):
    st.markdown(f"""
        <div style='
            background-color: #FFFFFF;
            border: 2px solid #E5B25D;
            border-radius: 15px;
            padding: 10px 16px;
            height: 100px;  
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;  
            overflow: hidden;
        '>
            <div style='margin: 0; padding: 0; line-height: 1.1;'>  
                <span style='
                    color: {title_color}; 
                    font-size: 20px; 
                    margin: 0;
                    padding: 0;
                '>{title}</span><br>
                <span style='
                    color: #000000; 
                    font-size: 25px;
                    font-weight: bold;
                    margin: 0;
                    padding: 0;
                '>{value}</span>
            </div>
            <p style='
                margin: 4px 0 0 0; 
                font-size: 13px;
                color: #555555;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            '>{delta}</p>
        </div>
    """, unsafe_allow_html=True)


def show_metrics(df, country_name):
    # Mostrar las métricas del dataset
    st.subheader(f"Métricas del modelo en {country_name}")
    
    col1, col2, col3= st.columns(3)
    with col1:
        kpi_card_metric("Número total de registros", f"{df.shape[0]}", "Registros en el dataset", "#4B8C6A")
    with col2:
        kpi_card_metric("Número de columnas", f"{df.shape[1]}", "Columnas en el dataset", "#F28C38")
    with col3:
        kpi_card_metric("Vecindarios distintos", f"{df['neighbourhood'].nunique()}", "Número de vecindarios", "#8DA47E")
    
    # Si la columna 'price' está presente, agregar métricas relacionadas con el precio
    if 'price' in df.columns:
        col5, col6, col7 = st.columns(3)
        with col5:
            kpi_card_metric("Precio promedio por noche", f"${df['price'].mean():.2f}", "Precio promedio", "#F28C38")
        with col6:
            kpi_card_metric("Alojamiento más caro", f"${df['price'].max():.2f}", "Precio más alto", "#C25E4C")
        with col7:
            kpi_card_metric("Alojamiento más barato", f"${df['price'].min():.2f}", "Precio más bajo", "#8DA47E")


#Mostrar informacion 
def mostrar_informacion_paises():
    st.header("Información general de los países analizados")
    
    # Texto de introducción
    st.write("""
    A continuación presentamos un breve resumen de los cuatro países analizados en este dashboard.
             Los países son: **Milán (Italia)**, **México**, **Ámsterdam (Países Bajos)** y **Hong Kong (China)**.
    """)

    st.markdown("---")

    st.header("Milán, Italia")
    st.write("""
    Milán, la capital financiera y de la moda de Italia, es una de las ciudades más importantes de Europa. 
    Con su rica historia, arquitectura de renombre y una economía sólida, Milán atrae tanto a turistas internacionales 
    como a profesionales. La ciudad es famosa por eventos como la **Semana de la Moda** y la **Exposición Universal**, 
    lo que genera una alta demanda de alojamiento. Además, su infraestructura avanzada, especialmente en el transporte, 
    facilita la movilidad tanto para turistas como para residentes temporales. 
    Analizar Milán en plataformas como Airbnb permite entender cómo la demanda de propiedades varía con los flujos turísticos, 
    las regulaciones locales y el desarrollo económico.
    """)
    
    col1, col2, col3 = st.columns([1, 4, 1])  

    with col2:
        st.image("img/milan.png", width=450)

    df_milan, _, _, _, _ = load_milan_data()  

    tipo_de_cambio = 21.74
    df_milan['price'] = df_milan['price'] * tipo_de_cambio  
        
    show_metrics(df_milan, "Milan")
        

    st.markdown("---")

    st.header("CDMX, México")
    st.write("""
    CDMX es uno de los destinos turísticos más populares del mundo, con una rica diversidad cultural, geográfica y gastronómica. 
    Desde las playas de Cancún hasta la vibrante Ciudad de México, el país atrae a millones de turistas cada año. 
    La creciente clase media y la adopción de plataformas tecnológicas como Airbnb han hecho que los alquileres a corto plazo se conviertan en una opción popular tanto para turistas nacionales como internacionales. 
    Además, las variaciones en el costo de vida y las políticas gubernamentales afectan directamente la oferta y demanda de estos servicios. 
    Analizar México a través de plataformas de alquiler de corto plazo ayuda a comprender las dinámicas del mercado local y cómo los cambios económicos, culturales y turísticos impactan los precios y la disponibilidad.
    """)

    col1, col2, col3 = st.columns([1, 4, 1])  

    with col2:
        st.image("img/cdmx.png", width=450)


    df_mexico, _, _, _, _ = load_mexico_data()  # Carga el dataset de México
    show_metrics(df_mexico, "México")

    st.markdown("---")

    st.header("Ámsterdam, Países Bajos")
    st.write("""
    Ámsterdam, la capital de los Países Bajos, es conocida por su rica historia, su arquitectura pintoresca y sus famosos canales. 
    Como una de las ciudades más visitadas de Europa, Ámsterdam es un destino popular tanto para turistas de todo el mundo como para viajeros de negocios. 
    Con su ambiente cosmopolita, la ciudad ha sido un referente en cuanto a la aceptación de plataformas de alquiler a corto plazo como Airbnb. 
    La demanda de alojamiento fluctúa según los eventos internacionales, la alta temporada turística y las políticas locales que regulan los alquileres. 
    Estudiar Ámsterdam proporciona una visión valiosa sobre cómo las ciudades europeas gestionan el equilibrio entre el turismo, la oferta de propiedades y la regulación del mercado de alquileres.
    """)

    col1, col2, col3 = st.columns([1, 4, 1])  

    with col2:
        st.image("img/amsterdam.png", width=450)

    df_amsterdam, _, _, _, _ = load_amsterdam_data()  

    tipo_de_cambio = 21.74
    df_amsterdam['price'] = df_amsterdam['price'] * tipo_de_cambio  

    show_metrics(df_amsterdam, "Amsterdam")

    st.markdown("---")

    st.header("Hong Kong, China")
    st.write("""
    Hong Kong es un importante centro financiero y comercial global, conocido por su mezcla de culturas orientales y occidentales. 
    Como uno de los destinos más dinámicos del mundo, Hong Kong atrae a turistas, empresarios y residentes temporales. 
    La alta densidad poblacional y la limitada oferta de propiedades hacen que la demanda de alojamiento a corto plazo sea alta, especialmente en áreas cercanas a centros comerciales y financieros. 
    Las políticas gubernamentales, las regulaciones sobre el alquiler de propiedades y los eventos internacionales también juegan un papel crucial en la oferta de alquileres. 
    Analizar Hong Kong permite comprender cómo las ciudades con alta concentración de negocios y turismo manejan las fluctuaciones de precios y la oferta en plataformas como Airbnb.
    """)

    col1, col2, col3 = st.columns([1, 4, 1])  

    with col2:
        st.image("img/china.png", width=450)
    

    df_hongKong, _, _, _, _ = load_hongKong_data() 

    tipo_de_cambio = 2.49
    df_hongKong['price'] = df_hongKong['price'] * tipo_de_cambio  

    show_metrics(df_hongKong, "Hong Kong")

    st.markdown("---")