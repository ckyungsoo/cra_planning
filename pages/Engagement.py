import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.express as px
import datetime

rsk_assmnt = pd.read_csv('risk_assessment.csv', encoding = 'euc-kr')

with st.sidebar:
    d = st.date_input("조회일자를 선택하세요", datetime.date(2022,9,30))
    st.write('기준일: ', d.strftime('%Y년 %m월 %d일'))
    eng = st.selectbox("Engagment를 입력하세요", list(set(rsk_assmnt['engagement'])))

st.subheader('감리위험요소평가')
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric('표본심사',rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_2']=='1 표본심사')]['risk_index'].sum()
with col2:
    st.metric('직권지정',rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_2']=='2 직권지정')]['risk_index'].sum()
with col3:
    st.metric('관리종목',rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_2']=='3 관리종목')]['risk_index'].sum()
with col4:
    st.metric('한계기업',rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_2']=='4 한계기업')]['risk_index'].sum()
with col5:
    st.metric('기타',rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_2']=='5 ')]['risk_index'].sum()



st.subheader('감사인감리대상위험')
