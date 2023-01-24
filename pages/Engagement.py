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
