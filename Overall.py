import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.express as px

rsk_assmnt = pd.read_csv('risk_assessment.csv', encoding = 'euc-kr')
df = rsk_assmnt.groupby(['engagement','LoB','rsk_idx_1'])['risk_index'].sum().reset_index()
fig = px.box(df , x = 'LoB', y = 'risk_index', color = 'rsk_idx_1')
st.plotly_chart(fig, theme = "streamlit", use_contatiner_width = True)