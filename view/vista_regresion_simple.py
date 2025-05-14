import streamlit as st
import plotly.express as px
import pandas as pd
from utils.dataAmsterdam import load_data
from utils.dataMexico import load_dataMexico
from utils.dataMilan import load_dataMilan
from utils.dataHongKong import load_dataHongKong

def mostrar_regresion_simple():
    st.header("Regresión lineal simple")
    st.markdown("---")

    # ----------------- VARIABLES -----------------
    # Dependientes 
    variables_dependientes = [
        'price',
        'number_of_reviews',
        'review_scores_rating',
        'availability_365',
        'review_scores_value'
    ]

    # Independientes 
    variables_independientes = [
        'accommodates',
        'bedrooms',
        'beds',
        'minimum_nights',
        'maximum_nights ',
        'host_response_rate',
        'host_acceptance_rate',
        'review_scores_cleanliness',
        'review_scores_checkin ',
        'review_scores_location'
    ]

    st.sidebar.subheader("Variables")
    variable_dependiente = st.sidebar.selectbox("Variable dependiente (Y)", options=variables_dependientes)
    variable_independiente = st.sidebar.selectbox("Variable independiente (X)", options=variables_independientes)

     # Lista de países y sus respectivos datos
    paises = {
        "Ámsterdam": load_data(),
        "México": load_dataMexico(),
        "Milán": load_dataMilan(),
        "Hong Kong": load_dataHongKong()
    }

    # Mostrar los gráficos y KPIs de cada país
    for pais, (df, numeric_cols, text_cols, unique_categories, numeric_df) in paises.items():
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
                <h3 style="text-align: center;">{pais}</h3>
            """, unsafe_allow_html=True)

        st.subheader("Diagrama de dispersion")
        
        # Diagrama de dispersión con la línea de regresión
        fig_scatter = px.scatter(
            df,
            x=variable_independiente,
            y=variable_dependiente,
            trendline="ols",
        )

        fig_scatter.update_traces(marker=dict(color="#D4A037", size=5), selector=dict(mode='markers'))  
        fig_scatter.update_traces(line=dict(color="#C25E4C", width=2), selector=dict(mode='lines'))  

        fig_scatter.update_layout(
            xaxis_title=variable_independiente,
            yaxis_title=variable_dependiente
        )

        st.plotly_chart(fig_scatter, use_container_width=True)

        # Modelo de regresión
        from statsmodels.formula.api import ols
        model = ols(f"{variable_dependiente} ~ {variable_independiente}", data=df).fit()
        r_squared = model.rsquared
        p_value = model.pvalues[1]  # el p-valor de la variable independiente
        coef = model.params[1]  # pendiente
        correlation = df[[variable_dependiente, variable_independiente]].corr().iloc[0,1]
        n_datos = df[[variable_dependiente, variable_independiente]].dropna().shape[0]
        
        # Interpretación automática
        st.subheader("Indicadores del modelo")
                # ---------------- ÍCONOS SVG ----------------
        icon_r2 = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#E5B25D" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.49 2 2 4.69 2 8V16C2 19.31 6.49 22 12 22C17.51 22 22 19.31 22 16V8C22 4.69 17.51 2 12 2ZM12 4C16.97 4 21 6.13 21 8C21 9.87 16.97 12 12 12C7.03 12 3 9.87 3 8C3 6.13 7.03 4 12 4ZM12 20C7.03 20 3 17.87 3 16V14.15C5.03 15.82 8.36 17 12 17C15.64 17 18.97 15.82 21 14.15V16C21 17.87 16.97 20 12 20Z"/></svg>"""
        icon_r = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#E5B25D" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.49 2 2 4.69 2 8V16C2 19.31 6.49 22 12 22C17.51 22 22 19.31 22 16V8C22 4.69 17.51 2 12 2ZM12 4C16.97 4 21 6.13 21 8C21 9.87 16.97 12 12 12C7.03 12 3 9.87 3 8C3 6.13 7.03 4 12 4ZM12 20C7.03 20 3 17.87 3 16V14.15C5.03 15.82 8.36 17 12 17C15.64 17 18.97 15.82 21 14.15V16C21 17.87 16.97 20 12 20Z"/></svg>"""
        icon_significativa = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#8DA47E" xmlns="http://www.w3.org/2000/svg"><path d="M9 16.2L4.8 12L3.4 13.4L9 19L21 7L19.6 5.6L9 16.2Z"/></svg>"""
        icon_datos = """<svg width="24" height="24" viewBox="0 0 24 24" fill="#E5B25D" xmlns="http://www.w3.org/2000/svg"><path d="M12 2C6.49 2 2 4.69 2 8V16C2 19.31 6.49 22 12 22C17.51 22 22 19.31 22 16V8C22 4.69 17.51 2 12 2ZM12 4C16.97 4 21 6.13 21 8C21 9.87 16.97 12 12 12C7.03 12 3 9.87 3 8C3 6.13 7.03 4 12 4ZM12 20C7.03 20 3 17.87 3 16V14.15C5.03 15.82 8.36 17 12 17C15.64 17 18.97 15.82 21 14.15V16C21 17.87 16.97 20 12 20Z"/></svg>"""

        # ---------------- FUNCIÓN KPI CARD ----------------
        def kpi_card(icon_svg, title, value, delta, title_color):
            st.markdown(f"""
                <div style='
                    background-color: #FFFFFF;
                    border: 2px solid #E5B25D;
                    border-radius: 15px;
                    padding: 8px 12px;
                    height: 120px;  /* Altura fija */
                    box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
                    text-align: center;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;  /* Centramos todo */
                    gap: 6px;  /* Espacio entre título, número e icono */
                    overflow: hidden;
                '>
                    <h3 style='
                        color: {title_color}; 
                        font-size: 15px; 
                        margin: 0;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    '>{title}</h3>
                    <div style='
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        margin: 0;
                        flex-wrap: nowrap;
                        max-height: 40px;  /* Control del bloque del número + ícono */
                    '>
                        {icon_svg}
                        <h1 style='
                            margin: 0 0 0 10px; 
                            color: #000000; 
                            font-size: 26px;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            white-space: nowrap;
                        '>{value}</h1>
                    </div>
                    <p style='
                        margin: 0; 
                        font-size: 13px;
                        overflow: hidden;
                        text-overflow: ellipsis;
                        white-space: nowrap;
                    '>{delta}</p>
                </div>
            """, unsafe_allow_html=True)

        # ---------------- KPIs ----------------
        col1, col2, col3, col4 = st.columns(4)

        relacion_porcentaje = r_squared * 100  # % basado en R²

        with col1:
            kpi_card(icon_r2, "R² (Coef. Determinación)", f"{r_squared:.4f}", "Proporción de la variabilidad", "#C25E4C")
        with col2:
            kpi_card(icon_r, "r (Coef. Correlación)", f"{correlation:.4f}", "Grado de variación", "#F28C38")
        with col3:
            kpi_card(icon_significativa, "Relación (%)", f"{relacion_porcentaje:.2f}%", "Porcentaje de relación", "#8DA47E")
        with col4:
            kpi_card(icon_datos, "Datos analizados", n_datos, "Registros en el modelo", "#E5B25D")

        st.markdown("---")

    # ---------------- HEATMAP INTERACTIVO ----------------
    st.sidebar.subheader("Heatmap general")
    mostrar_heatmap = st.sidebar.button("Generar heatmap")

    if mostrar_heatmap:

        # ----------------- VARIABLES SELECCIONADAS -----------------
        variables_heatmap = [
            'accommodates', 'bathrooms', 'bedrooms', 'beds', 'price', 'minimum_nights', 
            'maximum_nights', 'availability_30', 'availability_90', 'availability_365',
            'number_of_reviews', 'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
            'review_scores_checkin', 'review_scores_value'
        ]

        # ----------------- MUESTRO EL HEATMAP PARA CADA PAÍS -----------------
        for pais, (df, numeric_cols, text_cols, unique_categories, numeric_df) in paises.items():
            st.subheader(f"Heatmap {pais}")

            # ----------------- FILTRAR DATOS -----------------
            # Filtramos el DataFrame solo con las variables del heatmap
            df_heatmap = df[variables_heatmap]

            # ----------------- CALCULAR CORRELACIÓN -----------------
            correlation_matrix = df_heatmap.corr().abs()  # Correlación en valor absoluto

            # ----------------- GENERAR EL HEATMAP -----------------
            fig_heatmap = px.imshow(
                correlation_matrix,
                text_auto=True,
                color_continuous_scale=["#F7C59F", "#E5B25D", "#C25E4C"],  
                labels=dict(color="Correlación"),
                aspect="auto"
            )

            fig_heatmap.update_layout(
                xaxis_title="Variables",
                yaxis_title="Variables",
                margin=dict(l=40, r=40, t=40, b=40)
            )

            # Mostrar el heatmap para el país actual
            st.plotly_chart(fig_heatmap, use_container_width=True)
            st.markdown("---")