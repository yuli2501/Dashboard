
# ---------------------- LIBRERÍAS ------------------------
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.dataAmsterdam import load_data
from utils.dataMexico import load_dataMexico
from utils.dataMilan import load_dataMilan
from utils.dataHongKong import load_dataHongKong


# ---------------- PALETA DE COLORES ------------------
custom_palette = [
    "#C25E4C",  # Rojo ladrillo
    "#F7C59F",  # Durazno pastel 
    "#E5B25D",  # Mostaza tulipán
    "#F28C38",  # Naranja Holanda
    "#F0E5D8",  # Cremita
]

# ---------------- CONFIGURACIÓN INICIAL ------------------
st.set_page_config(layout="wide", page_title="Dashboard", page_icon="🏡")

# ----------------- ESTILO CSS -----------------
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #F4F0EB;
    }


    .stAppHeader {
        background-color: #F4F0EB;
    }

    /* Sidebar */
    .stSidebar {  
        background-color: #F0E5D8 !important;
        border-right: 3px solid #C25E4C;
    }

    .stTittle{
        text-align: center;
    }

    /* Cambiar el fondo del selectbox */
    div[data-baseweb="select"] > div {
        background-color: #F4F0EB !important;  /* Cremita */
        border: 2px solid #C25E4C !important;  /* Rojo ladrillo */
        border-radius: 10px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-thumb {
        background-color: #C25E4C;
        border-radius: 10px;
    }
    section[data-testid="stSidebar"] button {
        background-color: #F4F0EB !important;    
        border: 2px solid #C25E4C !important;    
        border-radius: 10px !important;         
        font-weight: bold !important;
    }
    </style>

""", unsafe_allow_html=True)
# ---------------- CARGA DE DATOS -------------------------
df, numeric_cols, text_cols, unique_categories, numeric_df = load_data()
dfMexico, numeric_colsMex, text_colsMex, unique_categoriesMex, numericMexico = load_dataMexico()
dfMilan, numeric_colsMilan, text_colsMilan, unique_categoriesMilan, numericMilan = load_dataMilan()
dfHongKong, numeric_colsHongKong, text_colsHongKong, unique_categoriesHongKong, numericHongKong = load_dataHongKong()

# ----------------- SIDEBAR -------------------------------
st.sidebar.title("Dashboard")
View = st.sidebar.selectbox(label="Vistas", options=[
    "Inicio",
    "Análisis univariado",
    "Regresión lineal simple",
    "Regresión lineal múltiple",
    "Regresión logística"
])

# ------------------ VISTA INICIO ------------------------------
if View == "Inicio":
    from view.vista_inicio import mostrar_informacion_paises
    mostrar_informacion_paises()
# ------------------ VISTA 1 ------------------------------
elif View == "Análisis univariado":
    from view.vista_analisis_univariado import mostrar_analisis_univariado
    mostrar_analisis_univariado()

# ------------------ VISTA 2 ------------------------------
elif View == "Regresión lineal simple":
    st.header("Regresión lineal simple")

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

    st.subheader(f"Diagrama de dispersión")

    # Scatterplot con línea de regresión
    fig_scatter = px.scatter(
        df,
        x=variable_independiente,
        y=variable_dependiente,
        trendline="ols",
    )

    fig_scatter.update_traces(marker=dict(color="#D4A037", size=5), selector=dict(mode='markers'))  
    fig_scatter.update_traces(line=dict(color="#C25E4C", width=2), selector=dict(mode='lines'))  

    fig_scatter.update_layout(
        #paper_bgcolor="#F4F0EB",  # Fondo cremita como el de tu dashboard
        #plot_bgcolor="#F4F0EB",
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

    direccion = "incrementa" if coef > 0 else "disminuye"
    st.markdown(f"""
    Por cada unidad que aumenta **{variable_independiente}**, 
    el valor de **{variable_dependiente}** {direccion} en **{abs(coef):.4f} unidades** en promedio.
    """)

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

    # ----------------- HEATMAP SOLO DE Y y X -----------------
    st.subheader("Mapa de calor")

    # Generamos el dataframe solo con las dos variables elegidas
    df_heatmap = df[[variable_dependiente, variable_independiente]]

    # Calculamos la matriz de correlación
    correlation_matrix = df_heatmap.corr().abs()  # Valor absoluto para que siempre sea positivo

    # Creamos el heatmap con Plotly
    fig_heatmap = px.imshow(
        correlation_matrix,
        text_auto=True,
        color_continuous_scale=["#F7C59F", "#E5B25D", "#C25E4C"], 
        labels=dict(color="Correlación"),
        aspect="auto"
    )

    fig_heatmap.update_layout(
        paper_bgcolor="#F4F0EB",  # Fondo cremita
        plot_bgcolor="#F4F0EB",
        xaxis_title="Variables",
        yaxis_title="Variables",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # Mostrar el heatmap
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # ---------------- HEATMAP INTERACTIVO ----------------
    st.sidebar.subheader("Heatmap general")
    mostrar_heatmap = st.sidebar.button("Generar heatmap")

    if mostrar_heatmap:
        st.subheader("Mapa de calor general")
        
        # ----------------- VARIABLES SELECCIONADAS -----------------
        variables_heatmap = [
            'accommodates',
            'bathrooms',
            'bedrooms',
            'beds',
            'price',
            'minimum_nights',
            'maximum_nights',
            'availability_30',
            'availability_90',
            'availability_365',
            'number_of_reviews',
            'review_scores_rating',
            'review_scores_accuracy',
            'review_scores_cleanliness',
            'review_scores_checkin',
            'review_scores_value'
        ]

        # ----------------- FILTRAR DATOS -----------------
        df_heatmap = df[variables_heatmap]

        # ----------------- CALCULAR CORRELACIÓN -----------------
        correlation_matrix = df_heatmap.corr().abs()  # Correlación en valor absoluto, como en tu práctica

        # ----------------- GENERAR EL HEATMAP -----------------
        import plotly.express as px

        fig_heatmap = px.imshow(
            correlation_matrix,
            text_auto=True,
            color_continuous_scale=["#F7C59F", "#E5B25D", "#C25E4C"],  
            labels=dict(color="Correlación"),
            aspect="auto"
        )

        fig_heatmap.update_layout(
            #paper_bgcolor="#F4F0EB",   # Fondo cremita como en tu app
            #plot_bgcolor="#F4F0EB",
            xaxis_title="Variables",
            yaxis_title="Variables",
            margin=dict(l=40, r=40, t=40, b=40)
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

# ------------------ VISTA 3 ------------------------------
elif View == "Regresión lineal múltiple":
    from view.vista_regresion_multiple import mostrar_regresion_multiple
    mostrar_regresion_multiple()

elif View == "Regresión logística":
    st.header("Comparativa de Modelos – Regresión Logística")

    # Selección de datasets para comparar
    selected_datasets = st.sidebar.multiselect(
        "Selecciona datasets para comparar",
        ["México", "Amsterdam", "Milán", "Hong Kong"],
        default=["México", "Milán", "Hong Kong"]
    )
    if not selected_datasets:
        st.warning("Selecciona al menos un dataset para comparar.")
    else:
        # Obtener solo las columnas binarias presentes en todos los datasets
        sets = []
        dfs = {
            "México": dfMexico,
            "Amsterdam": df,
            "Milán": dfMilan,
            "Hong Kong": dfHongKong
        }
        for name, dfi in dfs.items():
            # columnas de texto que tengan exactamente 2 valores únicos
            binary = [c for c in text_cols if c in dfi.columns and dfi[c].nunique() == 2]
            sets.append(set(binary))
        # Intersección: columnas binarias comunes
        binary_cols = sorted(set.intersection(*sets))

        # Construcción de variables X numéricas
        all_nums = set()
        for dfi in dfs.values():
            all_nums |= set([c for c in numeric_cols if c in dfi.columns])
        all_numeric = sorted(all_nums)

        X_vars = st.sidebar.multiselect("Variables independientes (X)", options=all_numeric)
        Y_var = st.sidebar.selectbox("Variable dependiente (Y – binaria)", options=binary_cols)

        if st.sidebar.button("Ejecutar Comparativa"):
            from sklearn.preprocessing import LabelEncoder
            from sklearn.linear_model import LogisticRegression
            from sklearn.metrics import (
                accuracy_score, precision_score, recall_score,
                confusion_matrix, roc_curve, auc
            )
            import plotly.express as px

            metrics = []
            for ds in selected_datasets:
                df_ds = dfs[ds].copy()

                # Validar existencia de Y_var
                if Y_var not in df_ds.columns:
                    st.error(f"La variable '{Y_var}' no está disponible en el dataset de {ds}.")
                    continue

                # Filtrar X_vars existentes en este dataset
                X_sel = [col for col in X_vars if col in df_ds.columns]
                if not X_sel:
                    st.error(f"Ninguna variable X seleccionada está en {ds}.")
                    continue

                # Preprocesado
                X = df_ds[X_sel]
                y = df_ds[Y_var]
                X_enc = pd.get_dummies(X, drop_first=True)
                le = LabelEncoder()
                y_enc = le.fit_transform(y)

                # Entrenamiento
                model = LogisticRegression(max_iter=1000)
                model.fit(X_enc, y_enc)
                y_pred = model.predict(X_enc)
                y_prob = model.predict_proba(X_enc)[:, 1]

                # Métricas
                acc = accuracy_score(y_enc, y_pred)
                prec = precision_score(y_enc, y_pred, zero_division=0)
                rec = recall_score(y_enc, y_pred, zero_division=0)
                cm = confusion_matrix(y_enc, y_pred)
                fpr, tpr, _ = roc_curve(y_enc, y_prob)
                roc_auc = auc(fpr, tpr)

                metrics.append({
                    "Dataset": ds,
                    "Exactitud": acc,
                    "Precisión": prec,
                    "Sensibilidad": rec,
                    "Confusion": cm,
                    "FPR": fpr,
                    "TPR": tpr,
                    "AUC": roc_auc,
                    "Clases": le.classes_
                })

            # Helper de KPI cards
            def kpi_card(title, value, subtitle, color):
                st.markdown(f"""
                    <div style=''
                        background-color: #FFFFFF;
                        border: 2px solid {color};
                        border-radius: 15px;
                        padding: 8px 12px;
                        text-align: center;
                    ''>
                        <h4 style='color:{color}; margin:0;'>{title}</h4>
                        <p style='margin:4px 0; font-size:20px;'>{value}</p>
                        <small style='color:#555'>{subtitle}</small>
                    </div>
                """, unsafe_allow_html=True)

            # Mostrar KPI cards
            cols = st.columns(len(metrics))
            for col, m in zip(cols, metrics):
                with col:
                    kpi_card(
                        title=m["Dataset"],
                        value=f"Acc: {m['Exactitud']:.2%}",
                        subtitle=f"Prec: {m['Precisión']:.2%} | Sen: {m['Sensibilidad']:.2%}",
                        color=custom_palette[0]
                    )

            # Mostrar matriz de confusión y heatmap por dataset
            for m in metrics:
                st.markdown(f"---\n### {m['Dataset']}")

                st.subheader("Matriz de Confusión")
                cm_df = pd.DataFrame(m["Confusion"], index=m["Clases"], columns=m["Clases"])
                st.table(cm_df)

                st.subheader("Heatmap – Matriz de Confusión")
                fig_cm = px.imshow(
                    m["Confusion"],
                    text_auto=True,
                    labels=dict(x="Predicción", y="Real", color="Cantidad"),
                    x=m["Clases"], y=m["Clases"],
                    color_continuous_scale=custom_palette
                )
                fig_cm.update_layout(margin=dict(l=40, r=40, t=40, b=40), paper_bgcolor="#F4F0EB")
                st.plotly_chart(fig_cm, use_container_width=True)

            # Curvas ROC comparadas
            st.markdown("---\n## Curvas ROC comparadas")
            fig_roc = px.line(
                x=[0, 1], y=[0, 1],
                line_dash_sequence=["dash"],
                labels={"x": "FPR", "y": "TPR"},
                title="Línea de azar"
            )
            for m in metrics:
                fig_roc.add_scatter(
                    x=m["FPR"], y=m["TPR"],
                    mode="lines",
                    name=f"{m['Dataset']} (AUC={m['AUC']:.3f})"
                )
            fig_roc.update_layout(xaxis=dict(range=[0, 1]), yaxis=dict(range=[0, 1]), paper_bgcolor="#F4F0EB")
            st.plotly_chart(fig_roc, use_container_width=True)
