import streamlit as st
import plotly.express as px
import pandas as pd

# ---------------- PALETA DE COLORES ------------------
custom_palette = [
    "#C25E4C",  # Rojo ladrillo
    "#F7C59F",  # Durazno pastel (suavecito y cálido)
    "#E5B25D",  # Mostaza tulipán
    "#F28C38",  # Naranja Holanda
    "#F0E5D8",  # Cremita (deja este al final)
]

def show_AnalisisUnivariado(df, numeric_cols, text_cols, unique_categories):

    st.header("Análisis univariado")
     
    # ----------------- GRÁFICAS -----------------
    st.sidebar.subheader("Variables")

    # Variables categóricas para las gráficas
    opciones_bar = [
        'room_type', 'property_type', 'neighbourhood', 
        'host_response_time', 'host_response_rate', 'host_acceptance_rate'
    ]

    opciones_pie = [
        'room_type', 'host_is_superhost', 'instant_bookable', 'host_identity_verified',
        'has_availability', 'license', 'host_response_time'
    ]

    opciones_area = [
        'price', 'number_of_reviews', 'availability_365',
        'host_total_listings_count', 'accommodates', 'minimum_nights',
        'maximum_nights', 'review_scores_rating', 'review_scores_cleanliness'
    ]

    variable_cat_bar = st.sidebar.selectbox("Gráfica de frecuencias", options=opciones_bar)
    variable_cat_pie = st.sidebar.selectbox("Gráfica de categorías", options=opciones_pie)
    variable_cat_area = st.sidebar.selectbox("Gráfica de distribución", options=opciones_area)

    # ----------- GRÁFICA DE BARRAS -----------------
    count_data_bar = df[variable_cat_bar].value_counts().reset_index()
    count_data_bar.columns = [variable_cat_bar, 'Frecuencia']
    st.subheader(f"Frecuencia de {variable_cat_bar}")
    fig_bar = px.bar(count_data_bar, x=variable_cat_bar, y='Frecuencia', color_discrete_sequence=["#D4A037"])
    #fig_bar.update_layout(paper_bgcolor="#F4F0EB", plot_bgcolor="#F4F0EB")
    st.plotly_chart(fig_bar, use_container_width=True)

    # ----------- GRÁFICA DE PASTEL -----------------
    count_data_pie = df[variable_cat_pie].value_counts().reset_index()
    count_data_pie.columns = [variable_cat_pie, 'Cantidad']
    st.subheader(f"Categorías de {variable_cat_pie}")
    fig_pie = px.pie(count_data_pie, names=variable_cat_pie, values='Cantidad', color_discrete_sequence=custom_palette)
    #fig_pie.update_layout(paper_bgcolor="#F4F0EB", plot_bgcolor="#F4F0EB")
    st.plotly_chart(fig_pie, use_container_width=True)

    # ----------- GRÁFICA DE ÁREA  -----------------
    # Definir bins y labels
    if variable_cat_area == 'price':
        bins = [0, 50, 100, 200, 300, df['price'].max()]
        labels = ['Económico', 'Accesible', 'Medio', 'Alto', 'Premium']
    elif variable_cat_area == 'number_of_reviews':
        bins = [0, 30, 60, df['number_of_reviews'].max()]
        labels = ['Muy pocas', 'Pocas', 'Muchas']
    elif variable_cat_area == 'availability_365':
        bins = [0, 90, 180, 270, 365]
        labels = ['Menos de 3 meses', '3-6 meses', '6-9 meses', 'Todo el año']
    elif variable_cat_area == 'host_total_listings_count':
        bins = [0, 1, 2, 3, df['host_total_listings_count'].max()]
        labels = ['Muy pocos', 'Pocos', 'Muchos', 'Demasiados']
    elif variable_cat_area == 'accommodates':
        bins = [1, 2, 4, 5, df['accommodates'].max()]
        labels = ['Muy pocos huépedes', 'Pocos huéspedes', 'Muchos huéspedes', 'Demasiados huéspedes']
    elif variable_cat_area == 'minimum_nights':
        bins = [1, 2, 4, 5, df['minimum_nights'].max()]
        labels = ['1-2  noches', '2-4 noches', '4-5 noches', '1 semana']
    elif variable_cat_area == 'maximum_nights':
        bins = [1, 30, 90, 180, 365, df['maximum_nights'].max()]
        labels = ['Menos de 1 mes', '1-3 meses', '3-6 meses', '6-10 meses', '1 año']
    elif variable_cat_area == 'review_scores_rating':
        bins = [0, 2, 3, 4, 4.5, 5]
        labels = ['Muy bajo', 'Bajo', 'Aceptable', 'Bueno', 'Excelente']
    elif variable_cat_area == 'review_scores_cleanliness':
        bins = [0, 2, 3, 4, 4.5, 5]
        labels = ['Muy bajo', 'Bajo', 'Aceptable', 'Bueno', 'Excelente']
    else:
        st.warning("Selecciona una variable válida para la gráfica de área.")
        bins = None
        labels = None

    # Gráfica de área corregida
    df['Categorías'] = pd.cut(df[variable_cat_area], bins=bins, labels=labels, include_lowest=True)
    count_data_area = df.groupby('Categorías').size().reset_index(name='Cantidad')

    st.subheader(f"Distribución de {variable_cat_area}")
    fig_area = px.area(count_data_area, x='Categorías', y='Cantidad', color_discrete_sequence=["#8DA47E"])
    #fig_area.update_layout(paper_bgcolor="#F4F0EB", plot_bgcolor="#F4F0EB")
    st.plotly_chart(fig_area, use_container_width=True)

    # ----------- MAPA -------------------------------
    st.subheader("Ubicación de alojamientos")
    fig_map = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="name",
        color="price",  # O la variable que prefieras
        color_continuous_scale="YlOrRd",
        mapbox_style="carto-positron",  # Cambia a otro si quieres
        zoom=11,
        height=500
    )

    fig_map.update_layout(
        paper_bgcolor="#F4F0EB",  # Fondo igual al de tu página
        margin={"r":0, "t":30, "l":0, "b":0}
    )

    fig_map.update_traces(marker=dict(size=6, opacity=0.9))
    st.plotly_chart(fig_map, use_container_width=True)

    # ----------- SIDEBAR OPCIONES -------------
    st.sidebar.subheader("Dataset")
    show_data = st.sidebar.checkbox(label="Mostrar dataset")

    if show_data:
        st.subheader("Dataset completo")
        st.write(df)

        # Lista de las columnas numéricas
        important_cols = [
            'price', 'availability_365', 'number_of_reviews',
            'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
            'review_scores_checkin', 'review_scores_communication',
            'review_scores_location', 'review_scores_value'
        ]

        stats = df[important_cols].describe()
        stats = stats.loc[['mean', 'std', 'min', 'max']]
        stats.index = ['Promedio', 'Desviación estándar', 'Mínimo', 'Máximo']

        # Mostrar la tabla
        st.subheader("Resumen estadístico")
        st.write(stats)