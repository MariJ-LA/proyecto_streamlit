import sys 
from pathlib import Path
import streamlit as st
import plotly.express as px
import pandas as pd

# Cargar datos desde archivo SQLite
root = Path(__file__).parent.parent
sys.path.append(str(root))
from Utils.funciones import *

path_northwind = mapear_datos('Northwind_small', '.sqlite')
dataframes = cargar_datos(path_northwind)

st.set_page_config(page_title="Clientes", layout="wide")
st.title("Northwind: Ventas por clientes")

# Obtener las tablas necesarias
order_table = dataframes['Order']
details_table = dataframes['OrderDetail']
products_table = dataframes['Product']
category_table = dataframes['Category']
customer_table = dataframes['Customer']

# Convertir 'OrderDate' a formato datetime 
order_table['OrderDate'] = pd.to_datetime(order_table['OrderDate'])

# Crear columnas de años y meses
order_table['Year'] = order_table['OrderDate'].dt.year

# Filtros en la barra lateral
st.sidebar.title("Filtros")

# Crear un filtro para los años disponibles
años_disponibles = sorted(order_table['Year'].unique())

# Widget para seleccionar un solo año
año_seleccionado = st.sidebar.selectbox(
    "Seleccione el año de interés",
    options=años_disponibles,
    index=0  
)

# Crear segmentador por cliente
Clientes = order_table['CustomerId'].unique()

cliente_seleccionado = st.sidebar.multiselect(
    "Seleccione el o los Clientes de interés",
    options=Clientes,
    default=Clientes
)

# Crear la máscara de filtrado
mascara = (
    (order_table['CustomerId'].isin(cliente_seleccionado)) &
    (order_table['Year'] == año_seleccionado)
)

clientes_filtrados = order_table[mascara][['Id', 'CustomerId']]

# Combinar con la tabla de detalles
info_clientes = clientes_filtrados.merge(details_table, left_on='Id', right_on='OrderId')

# Seleccionar las columnas necesarias
info_clientes = info_clientes[['CustomerId', 'UnitPrice', 'Quantity', 'Discount']]

# Calcular el precio final
info_clientes['Precio_Final'] = ((info_clientes['Quantity'] * info_clientes['UnitPrice'])) * (1 - info_clientes['Discount'])

# Agrupar por cliente y calcular la suma del precio final
info_clientes_agrupada = info_clientes.groupby(['CustomerId'], as_index=False).agg({'Precio_Final': 'sum'})

# Crear el gráfico de barras
fig_bar = px.bar(
    info_clientes_agrupada,
    x='CustomerId',
    y='Precio_Final',
    title='Ventas totales por cliente',
    labels={
        'CustomerId': 'Cliente', 
        'Precio_Final': 'Precio Final'  
    }
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig_bar)
