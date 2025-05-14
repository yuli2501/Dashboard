import streamlit as st
import plotly.express as px
import pandas as pd
from utils.dataAmsterdam import load_data
from utils.dataMexico import load_dataMexico
from utils.dataMilan import load_dataMilan
from utils.dataHongKong import load_dataHongKong

def mostrar_regresion_multiple():
    st.header("Regresión lineal múltiple")
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
        'maximum_nights',
        'host_response_rate',
        'host_acceptance_rate',
        'review_scores_cleanliness',
        'review_scores_checkin',
        'review_scores_location'
    ]

    # Usamos las variables predefinidas en lugar de numeric_cols
    st.sidebar.subheader("Variables")
    
    # Seleccionamos la variable dependiente (y) desde las variables dependientes
    variable_dependiente = st.sidebar.selectbox("Variable dependiente (y)", options=variables_dependientes)

    # Seleccionamos las variables independientes (X) desde las variables independientes
    variables_independientes = st.sidebar.multiselect(
        "Variables independientes (X)",
        options=[col for col in variables_independientes if col != variable_dependiente],
        default=[col for col in variables_independientes if col != variable_dependiente][:3]
    )
 
    # ----------------- SELECTBOX PARA LA VARIABLE A MOSTRAR -----------------
    st.sidebar.subheader("Diagrama comparativo")
    variable_seleccionada = st.sidebar.selectbox(
        "Variable independiente (X)",
        options=variables_independientes
    )

     # Lista de países y sus respectivos datos
    paises = {
        "Ámsterdam": load_data(),
        "México": load_dataMexico(),
        "Milán": load_dataMilan(),
        "Hong Kong": load_dataHongKong()
    }

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

        # --------- FORMULA PARA EL MODELO ---------
        formula = f"{variable_dependiente} ~ {' + '.join(variables_independientes)}"

        from statsmodels.formula.api import ols
        modelo = ols(formula=formula, data=df).fit()

        # --------- GENERAR LAS PREDICCIONES ---------
        df['predicciones'] = modelo.predict(df[variables_independientes])

        # --------- COEFICIENTES Y R², r ---------
        resultados = []
        for var in variables_independientes:
            corr = df[[variable_dependiente, var]].corr().iloc[0, 1]
            coef = modelo.params.get(var, None)
            resultados.append({
                "Variable": var,
                "Coef. Regresión (β)": coef,
                "Correlación (r)": corr
            })

        # ---------------- Tabla ----------------
        resultados_df = pd.DataFrame(resultados)

        # ---------------- Indicadores ----------------
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

        col1, col2, col3, col4 = st.columns(4)

        r_squared = modelo.rsquared
        n_datos = df[[variable_dependiente] + variables_independientes].dropna().shape[0]
        relacion_porcentaje = r_squared * 100  # Relación significativa en %

        with col1:
            kpi_card(icon_r2, "R² (Coef. Determinación)", f"{r_squared:.4f}", "Proporción de la variabilidad", "#C25E4C")
        with col2:
            kpi_card(icon_r, "Promedio r (Correlación)", f"{resultados_df['Correlación (r)'].mean():.4f}", "Grado de variación promedio", "#F28C38")
        with col3:
            kpi_card(icon_significativa, "Relación (%)", f"{relacion_porcentaje:.2f}%", "Porcentaje de relación significativa", "#8DA47E")
        with col4:
            kpi_card(icon_datos, "Datos analizados", n_datos, "Registros utilizados en el modelo", "#E5B25D")

        # ----------------- SCATTERPLOT CON PREDICCIONES -----------------
        st.subheader(f"Diagrama comparativo")

        # Creamos un dataframe largo (long format) para graficar la variable seleccionada y las predicciones
        df_long_predicciones = pd.melt(
            df,
            id_vars=[variable_dependiente],
            value_vars=[variable_seleccionada, 'predicciones'],  # Solo la variable seleccionada y las predicciones
            var_name='Variable',
            value_name='Valor'
        )

        # Ahora sí el scatterplot para los datos reales y las predicciones de la variable seleccionada:
        fig_scatter_predicciones = px.scatter(
            df_long_predicciones,
            x='Valor',
            y=variable_dependiente,
            color='Variable',  # Diferencia entre valores reales y predichos
            labels={'Valor': f'{variable_seleccionada}', variable_dependiente: variable_dependiente},
            color_discrete_sequence=["#C25E4C", "#E5B25D"]  # Usando la paleta personalizada
        )

        fig_scatter_predicciones.update_traces(marker=dict(size=5), selector=dict(mode='markers'))
        fig_scatter_predicciones.update_layout(
            xaxis_title=f"{variable_seleccionada} ",
            yaxis_title=variable_dependiente,
            legend_title="Variable / Predicción",
        )

        st.plotly_chart(fig_scatter_predicciones, use_container_width=True)
        st.markdown("---")

    # -------- HEATMAP DE VARIABLES SELECCIONADAS ---------
    st.sidebar.subheader("Heatmap")
    mostrar_heatmap = st.sidebar.button("Generar heatmap")

    if mostrar_heatmap:
        for pais, (df, numeric_cols, text_cols, unique_categories, numeric_df) in paises.items():
            st.subheader(f"Heatmap {pais}")

            df_heatmap = df[[variable_dependiente] + variables_independientes]
            correlation_matrix = df_heatmap.corr().abs()

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

            st.plotly_chart(fig_heatmap, use_container_width=True)
            st.markdown("---")

        
