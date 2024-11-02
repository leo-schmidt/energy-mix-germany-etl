import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from energy_mix_germany.smard_api.get_s3_data import get_s3_data
from energy_mix_germany.params import *

st.set_page_config(
    page_title="Energy mix Germany ETL", page_icon=":high_voltage:", layout="wide"
)

st.title("Energy mix in Germany")

st.write("Work in progress")

# read data from test csv
df = get_s3_data("test_data.csv")
df.set_index("Datetime", inplace=True)

# plots for production, consumption and price
fig_production = go.Figure(layout_title_text="Production")

for column in df.columns[:-4]:
    fig_production.add_trace(
        go.Scatter(
            x=df.index,
            y=df[column],
            hoverinfo="x+y",
            mode="lines",
            line=dict(
                width=0.5,
            ),  # color='rgb(131, 90, 241)'),
            name=column,
            stackgroup="one",  # define stack group
        )
    )

fig_consumption = go.Figure(layout_title_text="Consumption")

for column in df.columns[-4:-1]:
    fig_consumption.add_trace(
        go.Scatter(
            x=df.index,
            y=df[column],
            hoverinfo="x+y",
            mode="lines",
            line=dict(
                width=0.5,
            ),  # color='rgb(131, 90, 241)'),
            name=column,
            # stackgroup='one' # define stack group
        )
    )

fig_price = go.Figure(layout_title_text="Price")

fig_price.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Market price: Germany/Luxembourg"],
        hoverinfo="x+y",
        mode="lines",
        line=dict(
            width=0.5,
        ),  # color='rgb(131, 90, 241)'),
        name=column,
        stackgroup="one",  # define stack group
    )
)

# draw plots

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_production)
    st.plotly_chart(fig_price)

with col2:
    st.plotly_chart(fig_consumption)
