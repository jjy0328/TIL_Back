import streamlit as st
import pandas as pd


view = [40,60,20]
st.write('# Age')
st.write('## raw')
view
st.write('## bar chart')
st.bar_chart(view)

# Series로 변환하기
sview = pd.Series(view)
sview