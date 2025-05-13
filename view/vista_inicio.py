import streamlit as st

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
        st.image("img/milan.png", width=400)
        

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
        st.image("img/cdmx.png", width=400)

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
        st.image("img/amsterdam.png", width=400)

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
        st.image("img/china.png", width=400)


    st.markdown("---")