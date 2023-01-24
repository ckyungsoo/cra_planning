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

col1.metric('표본심사',rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_2']=='1 표본심사')]['risk_index'].sum())

col2.metric('직권지정',rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_2']=='2 직권지정')]['risk_index'].sum())

col3.metric('관리종목',rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_2']=='3 관리종목')]['risk_index'].sum())

col4.metric('한계기업',rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_2']=='4 한계기업')]['risk_index'].sum())

col5.metric('기타',rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_2']=='5 기타')]['risk_index'].sum())

st.table(pd.DataFrame(rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_1']=='1 감리위험요소평가')&(rsk_assmnt['risk_index']>0)]['rsk_idx_3']).rename(columns = {'rsk_idx_3':'위험지표'}))

st.subheader('감사인감리대상위험')
col6, col7 = st.columns([1,4])
col6.metric('개별감사업무선정', rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_2']=='1 개별감사업무 선정')]['risk_index'].sum())
col7.metric('','')
st.table(pd.DataFrame(rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['engagement']==eng)&(rsk_assmnt['rsk_idx_1']=='2 감사인 감리 대상 개별감사업무 선정')&(rsk_assmnt['risk_index']>0)]['rsk_idx_3']).rename(columns = {'rsk_idx_3':'위험지표'}))
