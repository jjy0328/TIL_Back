import streamlit as st
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from PIL import Image

st.write("# 빙어, 도미 이진분류")
# 사이드바 이름
st.sidebar.header('입력값 조절')

# 사이드바 설정
# st.sidebar([이름], min, max, default)
def sidebar_feature():
    length = st.sidebar.slider('생선 길이', 9.3, 41.0, 30.0)
    weight = st.sidebar.slider('생선 무게', 6.7, 1000.0, 390.0)

    # json 파일
    data = {'생선 길이' : length,
            '생선 무게' : weight,}
    features = pd.DataFrame(data, index=[0])
    return features

df = sidebar_feature()

# 그래프 이름
st.subheader('사용자 입력 파라미터')
# 사용자가 사이드바로 입력한 데이터셋 보여주기
st.write(df)

#######################################
# 도미 데이터

bream_length = [25.4, 26.3, 26.5, 29.0, 29.0, 29.7, 29.7, 30.0, 30.0, 30.7, 31.0, 31.0, 
                31.5, 32.0, 32.0, 32.0, 33.0, 33.0, 33.5, 33.5, 34.0, 34.0, 34.5, 35.0, 
                35.0, 35.0, 35.0, 36.0, 36.0, 37.0, 38.5, 38.5, 39.5, 41.0, 41.0]
bream_weight = [242.0, 290.0, 340.0, 363.0, 430.0, 450.0, 500.0, 390.0, 450.0, 500.0, 475.0, 500.0, 
                500.0, 340.0, 600.0, 600.0, 700.0, 700.0, 610.0, 650.0, 575.0, 685.0, 620.0, 680.0, 
                700.0, 725.0, 720.0, 714.0, 850.0, 1000.0, 920.0, 955.0, 925.0, 975.0, 950.0]


# 빙어 데이터

# 빙어 특성
smelt_length = [9.8, 10.5, 10.6, 11.0, 11.2, 11.3, 11.8, 11.8, 12.0, 12.2, 12.4, 13.0, 14.3, 15.0]
smelt_weight = [6.7, 7.5, 7.0, 9.7, 9.8, 8.7, 10.0, 9.9, 9.8, 12.2, 13.4, 12.2, 19.7, 19.9]


# 도미, 빙어 합치기

length = bream_length + smelt_length
weight = bream_weight + smelt_weight

# weight와 length 2차원 리스트로 만들어보기 

fish = [[l,w] for l,w in zip(length,weight)]

# 정답 데이터 만들기 : 머신러닝에서는 정답값이 1, 아닌 것을 0으로 봄 
# 정답 데이터를 만드는 이유 : 예측에 관한 답이 있어야 정확하게 예측했는지를 알 수 있기 때문

fish_target = [1] * 35 + [0] * 14

###############################################

# scatter plot -> 지원하지 않아 사진으로 대체

image = Image.open('output.png')

st.image(image, caption='Scatter plot of Bream & Smelt')

################################################
target_names=['도미', '빙어']


# 최근접이웃 학습
kn = KNeighborsClassifier()

kn.fit(fish, fish_target)

# 예측하기
prediction = kn.predict(df)
# 예측 확률
prediction_proba = kn.predict_proba(df)

st.write("# KNeighborsClassifier")


# 예측 확률 데이터프레임
# 어떤 타입일 확률이 가장 높은지 보여줌 (1에 가까울수록 확률이 높음)

st.write("0: 빙어")
st.write("1: 도미")

st.subheader('KNeighborsClassifier 예측 확률')
st.write(prediction_proba)