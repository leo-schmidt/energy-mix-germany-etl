import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(page_title="Energy mix Germany", page_icon=":high_voltage:", layout="wide")

st.write("Work in progress")

df = pd.read_csv("test_data.csv", index_col=0)

fig = go.Figure()

for column in df.columns[:-4]:
    fig.add_trace(go.Scatter(
        x=df.index, y=df[column],
        hoverinfo='x+y',
        mode='lines',
        line=dict(width=0.5, ), #color='rgb(131, 90, 241)'),
        name=column,
        stackgroup='one' # define stack group
    ))

st.plotly_chart(fig)
