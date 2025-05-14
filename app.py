
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
    from view.vista_regresion_simple import mostrar_regresion_simple
    mostrar_regresion_simple()

# ------------------ VISTA 3 ------------------------------
elif View == "Regresión lineal múltiple":
    from view.vista_regresion_multiple import mostrar_regresion_multiple
    mostrar_regresion_multiple()

# ------------------ VISTA 4 ------------------------------
elif View == "Regresión logística":
    st.header("Regresión logística")

    # ------------ VARIABLES DEPENDIENTES (BINARIAS) ------------
    variables_dependientes_log = [
        'host_is_superhost',
        'instant_bookable',
        'host_identity_verified',
        'has_availability'
    ]

    # ------------ VARIABLES INDEPENDIENTES -------------------
    variables_independientes_log = [
        'number_of_reviews', 'review_scores_rating',
        'review_scores_accuracy', 'review_scores_cleanliness',
        'review_scores_checkin', 'review_scores_communication',
        'review_scores_location', 'review_scores_value',
        'host_response_rate', 'host_acceptance_rate',
        'availability_365', 'availability_30', 'availability_90',
        'host_listings_count', 'minimum_nights', 'accommodates',
        'price', 'beds'
    ]

    # ------------ SIDEBAR -----------------
    st.sidebar.subheader("Variables")
    variable_dependiente = st.sidebar.selectbox("Variable dependiente (Y)", options=variables_dependientes_log)
    variables_independientes = st.sidebar.multiselect("Variables independientes (X)", options=variables_independientes_log,  default=variables_independientes_log[:3] ) 

    if not variables_independientes:
        st.warning("⚠️ Selecciona al menos una variable independiente para continuar.")
    else:
        # ----------------- PREPARAR DATOS -----------------
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, roc_auc_score, roc_curve
        import numpy as np

        # Limpieza de datos: eliminamos NaN
        data = df[[variable_dependiente] + variables_independientes].dropna()

        # Transformar la variable dependiente (Sí/No a 1/0 si es texto)
        if data[variable_dependiente].dtype == 'object':
            data[variable_dependiente] = data[variable_dependiente].apply(lambda x: 1 if x in ['Yes', 't', 'Sí', 'si', 'TRUE', 'True'] else 0)

        X = data[variables_independientes]
        y = data[variable_dependiente]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        # ----------------- MATRIZ DE CONFUSIÓN -----------------
        cm = confusion_matrix(y_test, y_pred)
        st.subheader("Matriz de confusión")
        st.write(pd.DataFrame(cm, columns=["Pred. Negativo", "Pred. Positivo"], index=["Real Negativo", "Real Positivo"]))

        st.subheader("Heatmap de la matriz de confusión")
        import plotly.express as px
        fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale=["#F7C59F", "#E5B25D", "#C25E4C"])
        fig_cm.update_layout(xaxis_title="Predicción", yaxis_title="Real")
        st.plotly_chart(fig_cm, use_container_width=True)

        # ----------------- MÉTRICAS -----------------
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)

        # ----------------- FUNCIÓN MÉTRICAS-----------------
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
                    <div style='margin: 0; padding: 0; line-height: 1.1;'>  <!-- Aquí se hace el truco -->
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

        # ----------------- MÉTRICAS COMO KPIs -----------------
        st.subheader("Métricas del modelo")

        col1, col2, col3 = st.columns(3)

        with col1:
            kpi_card_metric("Precisión", f"{precision:.2%}", "Relación positivos predichos correctamente", "#C25E4C")
        with col2:
            kpi_card_metric("Exactitud", f"{accuracy:.2%}", "Proporción total de aciertos", "#F28C38")
        with col3:
            kpi_card_metric("Sensibilidad", f"{recall:.2%}", "Capacidad de encontrar positivos reales", "#8DA47E")

        # ----------------- LINEPLOT DE MEJORA DEL MODELO -----------------
        if len(variables_independientes) > 1:  # Solo si hay más de una variable
            st.subheader("Evolución del modelo")

            metrics_data = []

            for i in range(1, len(variables_independientes) + 1):
                selected_vars = variables_independientes[:i]

                X = data[selected_vars]
                y = data[variable_dependiente]

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

                model = LogisticRegression(max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                acc = accuracy_score(y_test, y_pred)
                prec = precision_score(y_test, y_pred)
                rec = recall_score(y_test, y_pred)

                metrics_data.append({
                    'Variables usadas': ', '.join(selected_vars),
                    'Número de variables': i,
                    'Precisión': prec,
                    'Exactitud': acc,
                    'Sensibilidad': rec
                })

            metrics_df = pd.DataFrame(metrics_data)

            # Lineplot de las métricas
            fig_metrics = px.line(
                metrics_df,
                x='Número de variables',
                y=['Precisión', 'Exactitud', 'Sensibilidad'],
                markers=True,
                labels={"value": "Métrica", "variable": "Tipo de métrica", "Número de variables": "Número de variables"},
                color_discrete_sequence=custom_palette
            )

            fig_metrics.update_layout(
                legend_title="Métrica",
                xaxis=dict(tickmode='linear', dtick=1)
            )

            st.plotly_chart(fig_metrics, use_container_width=True)

        # ----------------- TABLA DE MÉTRICAS POR VARIABLES -----------------
        st.subheader("Tabla de la evolución del modelo")

        # Quitamos la columna 'Número de variables'
        metrics_df_tabla = metrics_df[['Variables usadas', 'Precisión', 'Exactitud', 'Sensibilidad']]

        # Mostramos la tabla
        st.dataframe(metrics_df_tabla)
