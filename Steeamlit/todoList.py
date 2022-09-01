import streamlit as st
import datetime

# 날짜 선택
today = st.date_input("날짜를 선택하세요.", datetime.datetime.now())
the_time = st.time_input("시간을 입력하세요.", datetime.time())


status = st.radio("오늘의 할 일", ("순한 맛", "매운 맛"))
if status == "순한 맛":
    st.success("순한 맛 가동")
else:
    st.warning("매운 맛 가동")


## 체크박스
if st.checkbox("끝내주게 숨 쉬기"):
# 체크 표시를 하면 완료 메세지가 뜹니다 
    st.write("완료")

if st.checkbox(" 맛있는거 먹기 "):
    st.write("완료")

if st.checkbox(" 꿀잠 자기 "):
    st.write("완료")

