import streamlit as st
import pandas as pd

df = pd.read_csv('data/MERGED/joueurs_lnh.csv')


df['saison'].groupby([df.saison, df.ligue]).agg('count')

st.area_chart(chart_data)