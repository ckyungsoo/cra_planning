import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.express as px
import datetime

with st.sidebar:
    d = st.date_input("조회일자를 선택하세요", datetime.date(2022,9,30))
    st.write('기준일: ', d.strftime('%Y년 %m월 %d일'))
    lob = st.selectbox('조회대상 본부를 선택하세요.'('All','CM1','CM2','ICE1','ICE2','ICE3','IGH','IM1','IM2','IM3','IM4'))

rsk_assmnt = pd.read_csv('risk_assessment.csv', encoding = 'euc-kr')
df = rsk_assmnt[rsk_assmnt['date']== d.strftime('%Y-%m-%d')].groupby(['engagement','LoB','rsk_idx_1'])['risk_index'].sum().reset_index()

#Page title
st.header('본부별 Engagement의 위험 식별 현황')
st.subheader(d.strftime('%Y년 %m월 %d일'))
st.write('')
st.write('')
st.write('')
#법인전체 위험지표가 식별된 인게이지먼트
#sorting 기준일 : 선택한 기준일, 위험평가지표 구분 : rsk_idx_1, 집계기준 : LoB,인게이지먼트별 risk_index의 합계
df_selected_1 = rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['rsk_idx_1']=='1 감리위험요소평가')].groupby(['LoB','engagement'])['risk_index'].sum().reset_index()
df_selected_2 = rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['rsk_idx_1']=='2 감사인 감리 대상 개별감사업무 선정')].groupby(['LoB','engagement'])['risk_index'].sum().reset_index()

#risk_index가 식별된 인게이지먼트만 sorting
df_selected_risky_1 = df_selected_1[~(df_selected_1['risk_index']==0)]
df_selected_risky_2 = df_selected_2[~(df_selected_2['risk_index']==0)]

#감리위험표소평가 식별한 engagement 합계와 LoB별 소계
sum_1 = df_selected_risky_1.groupby(['LoB'])['engagement'].count().reset_index()['engagement'].sum()
sum_1_t = df_selected_risky_1.groupby(['LoB'])['engagement'].count().reset_index().transpose()

#감사인감리대상 식별한 engagement 합계와 LoB별 소계
sum_2 = df_selected_risky_2.groupby(['LoB'])['engagement'].count().reset_index()['engagement'].sum()
sum_2_t = df_selected_risky_2.groupby(['LoB'])['engagement'].count().reset_index().transpose()

#전체 Enagement 개수
eng_cnt = len(set(rsk_assmnt['engagement']))

st.subheader('위험요소가 식별된 Engagement')
col1, col2 = st.columns(2)
with col1 :
    st.metric(label = '감리위험요소',value = sum_1)

    
with col2:
    st.metric(label = '감사인감리대상', value = sum_2)


with st.expander("본부별 감리위험요소 식별된 engagement 개수"):
    risky_engs_1 = df_selected_risky_1.groupby(['LoB'])['engagement'].count()
    fig_1 = px.bar(risky_engs_1)
    st.plotly_chart(fig_1, theme = "streamlit", use_contatiner_width = True)

with st.expander("본부별 감사인감리대상 식별된 engagment 개수"):
    risky_engs_2 = df_selected_risky_2.groupby(['LoB'])['engagement'].count()
    fig_2 = px.bar(risky_engs_2)
    st.plotly_chart(fig_2, theme = "streamlit", use_contatiner_width = True)
    
st.write(d.strftime('%Y년 %m월 %d일'),' 현재 법인의 감사 engagement(*)',eng_cnt,'개 중 감리위험요소가 식별된 engagement는', sum_1,'개이며 감사인감리대상위험요소가 식별된 engagement는',sum_2,'개입니다.')
st.caption('(*)  감사대상 engagment중 재무제표를 DART에 공시하는 법인으로 임의감사 등 공시 재무정보를 수집할 수 없는 engagement는 제외하였습니다.')

st.write('')
st.write('')
st.write('')
#본부별 인게이지먼트별 감리위험요소평가 식별 개수
st.subheader(':blue[Engagement별로 식별한 감리위험요소 개수의 분포]')
fig_3 = px.box(df[df['rsk_idx_1']=='1 감리위험요소평가'] , x = 'LoB', y = 'risk_index')
st.plotly_chart(fig_3, theme = "streamlit", use_contatiner_width = True)
with st.expander("세부내역"):
    st.table(df_selected_1.sort_values(by = ['risk_index'], ascending = False).style.hide_index())

st.write('')
st.write('')

#본부별 인게이지먼트별 감사인감리대상 식별 개수
st.subheader(':blue[Engagement별로 식별한 감사인감리대상위험 개수의 분포]')
fig_4 = px.box(df[df['rsk_idx_1']=='2 감사인 감리 대상 개별감사업무 선정'] , x = 'LoB', y = 'risk_index')
st.plotly_chart(fig_4, theme = "streamlit", use_contatiner_width = True)
with st.expander("세부내역"):
    st.table(df_selected_2.sort_values(by = ['risk_index'], ascending = False).style.hide_index())
