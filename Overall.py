import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.express as px

with st.sidebar:
    d = st.date_input("조회일자를 선택하세요", datetime.date(2022,9,30))
    st.write('기준일: ', d.strftime('%Y년 %m월 %d일'))

rsk_assmnt = pd.read_csv('risk_assessment.csv', encoding = 'euc-kr')
df = rsk_assmnt[rsk_assmnt['date']== d.strftime('%Y-%m-%d'].groupby(['engagement','LoB','rsk_idx_1'])['risk_index'].sum().reset_index()

#본부별 인게이지먼트별 감리위험요소평가 식별 개수
st.subheader(':blue[감리위험요소가 식별된 인게이지먼트 분포]')
fig_1 = px.box(df[df['rsk_idx_1']=='1 감리위험요소평가'] , x = 'LoB', y = 'risk_index')
st.plotly_chart(fig_1, theme = "streamlit", use_contatiner_width = True)


#본부별 인게이지먼트별 감사인감리대상 식별 개수
st.subheader(':blue[감사인감리대상위험이 식별된 인게이지먼트 분포]')
fig_2 = px.box(df[df['rsk_idx_1']=='2 감사인 감리 대상 개별감사업무 선정'] , x = 'LoB', y = 'risk_index')
st.plotly_chart(fig_2, theme = "streamlit", use_contatiner_width = True)
