import sys 
from pathlib import Path
import streamlit as st
import plotly.express as px

root = Path(__file__).parent.parent
sys.path.append(str(root))

from Utils.funciones import *

path_northwind = mapear_datos('Northwind_small', '.sqlite')

dataframes = cargar_datos(path_northwind)

st.set_page_config(page_title="Temporal",layout="wide")

st.title("Northwind:Análisis temporal")

# Obtener las tablas necesarias
order_table = dataframes['Order']
details_table = dataframes['OrderDetail']


# convertir 'OrderDate' a formato datetime 
order_table['OrderDate'] = pd.to_datetime(order_table['OrderDate'])

# Crear columnas de años y meses
order_table['Year'] = order_table['OrderDate'].dt.year
order_table['Month'] = order_table['OrderDate'].dt.month

# Filtros en la barra lateral
st.sidebar.title("Filtros")

# Crear un filtro para los años disponibles
años_disponibles = sorted(order_table['Year'].unique())

# Widget para seleccionar uno o más años
años_seleccionados = st.sidebar.multiselect(
    "Seleccione el o los años de interés",
    options=años_disponibles,
    default=años_disponibles
)

# Crear un filtro para los meses disponibles
meses_disponibles = sorted(order_table['Month'].unique())

# Widget para seleccionar uno o más meses
meses_seleccionados = st.sidebar.multiselect(
    "Seleccione el o los meses de interés",
    options=meses_disponibles,
    default=meses_disponibles
)

# Crear segundo segmentador por países
paises = order_table['ShipCountry'].unique()

# Crear un selectbox para seleccionar un solo país
país_seleccionado = st.sidebar.selectbox(
    "Seleccione el país de interés",
    options=paises,
    index=0 
)

# Aplicar los filtros
mascara = (
    (order_table['Year'].isin(años_seleccionados)) &
    (order_table['Month'].isin(meses_seleccionados)) &
    (order_table['ShipCountry']==(país_seleccionado))
)

paises_filtrados = order_table[mascara][['Id', 'OrderDate', 'Year', 'Month','ShipCountry']]

# Combinar con la tabla de detalles
info_orden = paises_filtrados.merge(details_table, left_on='Id', right_on='OrderId')

info_orden = info_orden[['OrderId', 'OrderDate', 'ShipCountry', 'Year', 'UnitPrice', 'Quantity', 'Discount']]

# Calcular precio final
info_orden['Precio_Final'] = ((info_orden['Quantity'] * info_orden['UnitPrice'])) * (1 - info_orden['Discount'])

# Agrupar los datos
info_orden_agrupada = info_orden.groupby(['OrderId', 'OrderDate'], as_index=False).agg({'Precio_Final': 'sum'})

# Crear el gráfico de líneas
fig_line = px.line(
    info_orden_agrupada,
    x='OrderDate',
    y='Precio_Final',
    markers=True,
    title='Ventas Totales a lo largo del tiempo',
    labels={
        'OrderDate': 'Fecha del Pedido',
        'Precio_Final': 'Precio Final',
    }
)

# Ajustar las fechas para que se muestren en meses e inclinarlas
fig_line.update_xaxes(dtick="M1", tickangle=45)



st.container( height=None, border=False, key=None)

with st.container():
    st.write("Gráfico de ventas totales a lo largo del tiempo")

    st.plotly_chart(fig_line)

