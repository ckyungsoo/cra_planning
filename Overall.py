import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.express as px
import datetime


with st.sidebar:
    d = st.date_input("조회일자를 선택하세요", datetime.date(2022,9,30))
    st.write('기준일: ', d.strftime('%Y년 %m월 %d일'))
    
#data table 편집
rsk_assmnt = pd.read_csv('risk_assessment.csv', encoding = 'euc-kr')
fs = pd.read_csv('fs.csv', encoding = 'euc-kr')
corp_list = pd.read_csv('corp_list.csv', encoding = 'euc-kr')
df = rsk_assmnt[rsk_assmnt['date']== d.strftime('%Y-%m-%d')].groupby(['engagement','LoB','rsk_idx_1'])['risk_index'].sum().reset_index()
df_2 = pd.pivot_table(rsk_assmnt[rsk_assmnt['date']==d.strftime('%Y-%m-%d')],
               index = 'engagement', columns = 'rsk_idx_1', values = 'risk_index', aggfunc = 'sum').reset_index()
fs_asset_sep = fs[(fs['주요계정']=='자산총계')&(fs['연결/별도']=='별도')]
df_2 = pd.merge(df_2, fs_asset_sep[fs_asset_sep['결산기준일']==d.strftime('%Y-%m-%d')], how = 'left', left_on = 'engagement', right_on = '회사명')
df_2['당기'] = df_2['당기'].fillna(0)
df_2 = df_2[['engagement', '1 감리위험요소평가', '2 감사인 감리 대상 개별감사업무 선정', '재무제표종류', '재무제표구분',
       '연결/별도', 'Industry', '상장시장', '결산기준일', 'Year',
       '주요계정', '계정코드', '당기']]
df_2 = pd.merge(df_2,corp_list, how = 'left', on = 'engagement')


#Page title
col_a, col_b = st.columns([7,3])
with col_a:
    st.header('Engagement 위험 식별 현황')
with col_b:
    st.write('')
    st.write('')
    st.write(d.strftime('%Y년 %m월 %d일'))

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

st.subheader('위험요소가 식별된 Engagement 수')
col1, col2 = st.columns(2)
with col1 :
    st.metric(label = ':red[감리위험요소]',value = sum_1)

    
with col2:
    st.metric(label = ':red[감사인감리대상]', value = sum_2)

st.write(d.strftime('%Y년 %m월 %d일'),' 현재 법인의 감사 engagement(*)',eng_cnt,'개 중 감리위험요소가 식별된 engagement는', sum_1,'개이며 감사인감리대상위험요소가 식별된 engagement는',sum_2,'개입니다.')
st.caption('(*)  감사대상 engagment중 재무제표를 DART에 공시하는 법인으로 임의감사 등 공시 재무정보를 수집할 수 없는 engagement는 제외하였습니다.')
with st.expander("본부별 감리위험요소가 식별된 Engagement 현황"):
    risky_engs_1 = df_selected_risky_1.groupby(['LoB'])['engagement'].count()
    fig_1 = px.bar(risky_engs_1)
    st.plotly_chart(fig_1, theme = "streamlit", use_contatiner_width = True)

with st.expander("본부별 감사인감리대상위험이 식별된 Engagement 현황"):
    risky_engs_2 = df_selected_risky_2.groupby(['LoB'])['engagement'].count()
    fig_2 = px.bar(risky_engs_2)
    st.plotly_chart(fig_2, theme = "streamlit", use_contatiner_width = True)
    


st.write('')
st.write('')
st.write('')

st.subheader('위험요소가 식별된 Engagement 분포')
st.write('Engagement별로 감리위험요소 위험요소는 평균',df_2['1 감리위험요소평가'].mean(),'개 식별되었으며, 감사인감리대상 위험요소는 평균,',df_2['2 감사인 감리 대상 개별감사업무 선정'].mean(),'개 식별되었습니다.')
st.write('')

col3, col4 = st.columns([2,8])

with col3:
    lob = st.selectbox('조회대상',('All','CM1','CM2','ICE1','ICE2','ICE3','IGH','IM1','IM2','IM3','IM4'))
    
with col4:
    st.write('')
    
#engagement 위험 식별 현황 scatterplot    
if lob == 'All':
    fig_5 = px.scatter(df_2, x='1 감리위험요소평가', y='2 감사인 감리 대상 개별감사업무 선정',size = '당기', color = 'engagement',log_x = False, size_max = 60)
    fig_5.add_hline(y = df_2['2 감사인 감리 대상 개별감사업무 선정'].mean(),line_width = 0.5, line_dash = 'dash', line_color = 'red', annotation_text = df_2['2 감사인 감리 대상 개별감사업무 선정'].mean())
    fig_5.add_vline(x = df_2['1 감리위험요소평가'].mean(), line_width = 0.5, line_dash = 'dash', line_color = 'red', annotation_text = df_2['1 감리위험요소평가'].mean())
    st.plotly_chart(fig_5, theme = "streamlit", use_container_width = True)
    df_2_sorted = df_2[['engagement', '1 감리위험요소평가', '2 감사인 감리 대상 개별감사업무 선정','당기']].rename(columns ={'당기':'자산(별도,억원)'})
    df_2_sorted['자산(별도,억원)'] = (df_2_sorted['자산(별도,억원)']/100000000).round()
    with st.expander("세부내역"):
        st.table(df_2_sorted.style.highlight_max(subset=['1 감리위험요소평가', '2 감사인 감리 대상 개별감사업무 선정']))
else :
    fig_5 = px.scatter(df_2[df_2['LoB']==lob], x='1 감리위험요소평가', y='2 감사인 감리 대상 개별감사업무 선정',size = '당기', color = 'engagement',log_x = False, size_max = 60)
    fig_5.add_hline(y = df_2['2 감사인 감리 대상 개별감사업무 선정'].mean(),line_width = 0.5, line_dash = 'dash', line_color = 'red', annotation_text = df_2['2 감사인 감리 대상 개별감사업무 선정'].mean())
    fig_5.add_vline(x = df_2['1 감리위험요소평가'].mean(), line_width = 0.5, line_dash = 'dash', line_color = 'red', annotation_text = df_2['1 감리위험요소평가'].mean())
    st.plotly_chart(fig_5, theme = "streamlit", use_container_width = True)
    df_2_sorted = df_2[df_2['LoB']==lob][['engagement', '1 감리위험요소평가', '2 감사인 감리 대상 개별감사업무 선정','당기']].rename(columns ={'당기':'자산(별도,억원)'})
    df_2_sorted['자산(별도,억원)'] = (df_2_sorted['자산(별도,억원)']/100000000).round()
    with st.expander("세부내역"):
        st.table(df_2_sorted.style.highlight_max(subset=['1 감리위험요소평가', '2 감사인 감리 대상 개별감사업무 선정']))

    
st.write('')
st.write('')
st.write('')

    
#본부별 인게이지먼트별 감리위험요소평가 식별 개수
st.subheader('감리위험요소 식별 현황')
fig_3 = px.box(df[df['rsk_idx_1']=='1 감리위험요소평가'] , x = 'LoB', y = 'risk_index')
st.plotly_chart(fig_3, theme = "streamlit", use_contatiner_width = True)
st.write('감리위험요소가 유의적(*)으로 식별된 Engaement는 다음과 같습니다.')
st.caption(':blue[(*)감리위험요소 식별 개수 분포의 3분위수(75%)(법인 전체 Engagment기준)를 초과하는 Engagement를 유의적이라 판단하였습니다.]')
st.table(df_selected_1[df_selected_1['risk_index'] > df_selected_1['risk_index'].quantile(q=0.75)].rename(columns = {'risk_index':'감리위험요소'}))
with st.expander("전체내역"):
    st.table(df_selected_1.sort_values(by = ['risk_index'], ascending = False).style.hide_index())

st.write('')
st.write('')

#본부별 인게이지먼트별 감사인감리대상 식별 개수
st.subheader('감사인감리대상위험 식별 현황')
fig_4 = px.box(df[df['rsk_idx_1']=='2 감사인 감리 대상 개별감사업무 선정'] , x = 'LoB', y = 'risk_index')
st.plotly_chart(fig_4, theme = "streamlit", use_contatiner_width = True)
st.write('감사인감리대상위험요소가 유의적(*)으로 식별된 Engaement는 다음과 같습니다.')
st.caption(':blue[(*)감사인감리위험요소 식별 개수 분포의 3분위수(75%)(법인 전체 Engagment기준)를 초과하는 Engagement를 유의적이라 판단하였습니다.]')
st.table(df_selected_2[df_selected_2['risk_index'] > df_selected_2['risk_index'].quantile(q=0.75)].rename(columns = {'risk_index':'감사인감리대상'}))
with st.expander("전체내역"):
    st.table(df_selected_2.sort_values(by = ['risk_index'], ascending = False).style.hide_index())

#본부 engaement 별 위험지표 식별현황
st.subheader('위험요소 항목별 세부 내역')
st.write('본부 Engagement별로 식별한 위험요소의 세부내역은 다음과 같습니다.')
col5, col6 = st.columns([2,8])
with col5:
    lob_2 = st.selectbox('조회본부선택',('CM1','CM2','ICE1','ICE2','ICE3','IGH','IM1','IM2','IM3','IM4'))
    
with col6:
    st.write('')
#감리위험요소평가
st.write(lob_2,' Engagement가 식별한 감리위험요소의 항목별 내역은 아래와 같습니다.')
rsk = '1 감리위험요소평가'
rsk_table_lob_1 = rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['LoB']==lob_2)&(rsk_assmnt['rsk_idx_1']==rsk)].groupby(['engagement','rsk_idx_2'])['risk_index'].sum().unstack()
st.table(rsk_table_lob_1)
engmnt = st.selectbox('Engagement 선택',tuple(set(rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['LoB']==lob_2)].engagement)))
rsk_assmnt_sorted = rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['LoB']==lob_2)&(rsk_assmnt['rsk_idx_1']==rsk)&(rsk_assmnt['engagement']==engmnt)&(rsk_assmnt['risk_index']>0)][['rsk_idx_2','rsk_idx_3']]
st.write(engmnt,'가 식별한 위험요소의 세부내역은 아래와 같습니다.')
st.table(rsk_assmnt_sorted.rename(columns={'rsk_idx_2':'구분','rsk_idx_3':'내용'}))
                      
#감사인 감리대상
st.write(lob_2,' Engagement가 식별한 감사인감리대상위험요소의 항목별 내역은 아래와 같습니다.')
rsk_2 = '2 감사인 감리 대상 개별감사업무 선정'
rsk_table_lob_2 = rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['LoB']==lob_2)&(rsk_assmnt['rsk_idx_1']==rsk_2)].groupby(['engagement','rsk_idx_2'])['risk_index'].sum().unstack()
st.table(rsk_table_lob_2)   
engmnt_2 = st.selectbox('Engagement 선택.',tuple(set(rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['LoB']==lob_2)].engagement)))
rsk_assmnt_sorted = rsk_assmnt[(rsk_assmnt['date']==d.strftime('%Y-%m-%d'))&(rsk_assmnt['LoB']==lob_2)&(rsk_assmnt['rsk_idx_1']==rsk_2)&(rsk_assmnt['engagement']==engmnt_2)&(rsk_assmnt['risk_index']>0)][['rsk_idx_2','rsk_idx_3']]
st.write(engmnt_2,'가 식별한 위험요소의 세부내역은 아래와 같습니다.')
st.table(rsk_assmnt_sorted.rename(columns={'rsk_idx_2':'구분','rsk_idx_3':'내용'}))
