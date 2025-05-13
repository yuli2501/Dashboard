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
    
    st.image("img/milan.png", width=400)
        

    st.markdown("---")

