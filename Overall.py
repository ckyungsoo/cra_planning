import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.express as px

rsk_assmnt = pd.read_csv('risk_assessment.csv', encoding = 'euc-kr')
df = rsk_assmnt[rsk_assmnt['date']=='2022-09-30'].groupby(['engagement','LoB','rsk_idx_1'])['risk_index'].sum().reset_index()

co11, co12 = st.columns(2)

with col1:
  #본부별 인게이지먼트별 감리위험요소평가 식별 개수
  st.write('본부별 감리위험요소가 식별된 인게이지먼트 개수')
  fig_1 = px.box(df[df['rsk_idx_1']=='1 감리위험요소평가'] , x = 'LoB', y = 'risk_index')
  st.plotly_chart(fig_1, theme = "streamlit", use_contatiner_width = True)

with col2:
  #본부별 인게이지먼트별 감사인감리대상 식별 개수
  st.write('본부별 감사인감리대상위험이 식별된 인게이지먼트 개수')
  fig_2 = px.box(df[df['rsk_idx_1']=='2 감사인 감리 대상 개별감사업무 선정'] , x = 'LoB', y = 'risk_index')
  st.plotly_chart(fig_2, theme = "streamlit", use_contatiner_width = True)
