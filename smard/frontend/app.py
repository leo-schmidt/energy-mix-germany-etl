import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Energy mix Germany ETL", page_icon=":high_voltage:", layout="wide")

st.title("Energy mix in Germany")

df = pd.read_csv("test_data.csv", index_col=0)

fig_production = go.Figure()

for column in df.columns[:-4]:
    fig_production.add_trace(go.Scatter(
        x=df.index, y=df[column],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, ), #color='rgb(131, 90, 241)'),
        name=column,
        stackgroup='one' # define stack group
    ))

fig_consumption = go.Figure()

for column in df.columns[-4:-1]:
    fig_consumption.add_trace(go.Scatter(
        x=df.index, y=df[column],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, ), #color='rgb(131, 90, 241)'),
        name=column,
        #stackgroup='one' # define stack group
    ))

fig_price = go.Figure()

fig_price.add_trace(go.Scatter(
        x=df.index, y=df['Market price: Germany/Luxembourg'],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, ), #color='rgb(131, 90, 241)'),
        name=column,
        stackgroup='one' # define stack group
    ))

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_production)
    st.plotly_chart(fig_price)

with col2:
    st.plotly_chart(fig_consumption)

st.write("Work in progress")
