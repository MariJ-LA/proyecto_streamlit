import sys
from pathlib import Path
import streamlit as st
import plotly.express as px

# Configurar la página 
st.set_page_config(layout="wide")

# Portada personalizada
st.markdown("""
    <style>
        .portada {
            text-align: center;
            font-family: 'Arial', sans-serif;
            background-color: #2E3B55;
            color: white;
            padding: 50px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .portada h1 {
            font-size: 40px;
            margin-bottom: 10px;
        }
        .portada h2 {
            font-size: 30px;
            margin-bottom: 15px;
        }
        .portada p {
            font-size: 18px;
            margin-bottom: 10px;
        }
        .card {
            background-color: #807CDE; 
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
            font-size: 18px;
            color: #000A55; 
        }
        .card h3 {
            font-size: 24px;
            margin-bottom: 15px;
        }
        .card p {
            font-size: 28px;
            font-weight: bold;
            color: white; 
        }
    </style>

    <div class="portada">
        <h1>Northwind: Visualizando el Comportamiento de las Ventas</h1>
        <h2>Proyecto final</h2>
        <p>Base de datos utilizada: Northwind</p>
        <p>Estudiante: María José Leiva Abarca</p>
    </div>
""", unsafe_allow_html=True)

root = Path(__file__).parent.parent
sys.path.append(str(root))

from Utils.funciones import *

# Mapear los datos y cargarlos
path_northwind = mapear_datos('Northwind_small', '.sqlite')
dataframes = cargar_datos(path_northwind)

# Obtener las tablas necesarias
details_table = dataframes['OrderDetail']

# Pasar el 'OrderId' a tipo cadena
details_table['OrderId'] = details_table['OrderId'].astype(str)

# Calcular el precio final de cada venta
details_table['Precio_Final'] = (details_table['Quantity'] * details_table['UnitPrice']) * (1 - details_table['Discount'])

# Contar las órdenes únicas
cantidad_ordenes = details_table['OrderId'].nunique()

# Calcular el total de ventas
total_ventas = details_table['Precio_Final'].sum()

# Subtitulo
st.subheader("Metricas importantes")

# Crear dos columnas para las tarjetas
col1, col2 = st.columns(2)

# Mostrar el total de órdenes en la primera tarjeta
with col1:
    st.markdown(f"""
    <div class="card">
        <h3>Cantidad de Órdenes Registradas</h3>
        <p>{cantidad_ordenes}</p>
    </div>
    """, unsafe_allow_html=True)

# Mostrar el total de ventas en la segunda tarjeta
with col2:
    st.markdown(f"""
    <div class="card">
        <h3>Total de Ventas</h3>
        <p>${total_ventas:,.2f}</p>
    </div>
    """, unsafe_allow_html=True)






