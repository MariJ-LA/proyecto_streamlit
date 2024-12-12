import sys
from pathlib import Path
import streamlit as st
import plotly.express as px

root = Path(__file__).parent.parent
sys.path.append(str(root))

from Utils.funciones import *

path_northwind = mapear_datos('Northwind_small','.sqlite')

dataframes = cargar_datos(path_northwind)

st.set_page_config(page_title="Categorias", layout="wide")

st.title("Northwind: Ventas por categoría")

# Obtener las tablas necesarias
order_table = dataframes['Order']
details_table = dataframes['OrderDetail']
products_table = dataframes['Product']
category_table = dataframes['Category']

# Convertir 'OrderDate' a formato datetime
order_table['OrderDate'] = pd.to_datetime(order_table['OrderDate'])
order_table['Year'] = order_table['OrderDate'].dt.year
order_table['Month'] = order_table['OrderDate'].dt.month

# Crear las listas de filtros
años_disponibles = sorted(order_table['Year'].unique())
meses_disponibles = sorted(order_table['Month'].unique())

# Filtros en la barra lateral
st.sidebar.title("Filtros")

# Filtro para seleccionar año
años_seleccionados = st.sidebar.multiselect(
    "Seleccione el o los años de interés",
    options=años_disponibles,
    default=años_disponibles
)

# Filtro para seleccionar mes
meses_seleccionados = st.sidebar.multiselect(
    "Seleccione el o los meses de interés",
    options=meses_disponibles,
    default=meses_disponibles
)

# Aplicar los filtros dentro de la máscara 
mascara = (
    (order_table['Year'].isin(años_seleccionados)) & 
    (order_table['Month'].isin(meses_seleccionados))
)

# Filtrar la tabla de pedidos según los filtros seleccionados
ventas_filtradas = order_table[mascara][['Id', 'Year', 'Month']]

# Unir la tabla de detalles con la de productos para obtener el id del producto relacionado al pedido
info_orden = ventas_filtradas.merge(details_table[['OrderId', 'ProductId', 'UnitPrice', 'Quantity', 'Discount']], left_on='Id', right_on='OrderId')

info_orden = info_orden.merge(products_table[['Id', 'CategoryId']], left_on='ProductId', right_on='Id')

info_orden = info_orden.merge(category_table[['Id', 'CategoryName']], left_on='CategoryId', right_on='Id')

info_orden = info_orden[['Year', 'Month', 'CategoryName', 'Quantity', 'UnitPrice', 'Discount']]

# Calcular el precio final de cada venta
info_orden['Precio_Final'] = (info_orden['Quantity'] * info_orden['UnitPrice']) * (1 - info_orden['Discount'])

# Agrupar por categoría y calcular las ventas totales
ventas_por_categoria = info_orden.groupby('CategoryName')['Precio_Final'].sum().reset_index()

# Crear el gráfico de barras para ventas por categoría
fig_bar_categoria = px.bar(
    ventas_por_categoria,
    x='CategoryName',
    y='Precio_Final',
    title='Ventas Totales por Categoría',
    labels={'CategoryName': 'Categoría', 'Precio_Final': 'Ventas Totales'}
)

# Mostrar el gráfico
st.plotly_chart(fig_bar_categoria)



