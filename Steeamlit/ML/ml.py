import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# 아이리스 데이터셋 불러오기
iris = datasets.load_iris()
st.write("# Iris Flower 예측 ")

# 사이드바 이름
st.sidebar.header('입력값 조절')

# 사이드바 설정
# st.sidebar([이름], min, max, default)
def sidebar_feature():
    sepal_length = st.sidebar.slider('꽃밭침 길이', 4.3, 7.9, 5.1)
    sepal_width = st.sidebar.slider('꽃밭침 넓이', 2.0, 4.4, 3.5)
    petal_length = st.sidebar.slider('꽃밭침 길이', 1.0, 6.9, 1.4)
    petal_width = st.sidebar.slider('꽃밭침 넓이', 0.1, 2.5, 0.2)
    # json 파일
    data = {'sepal_length' : sepal_length,
            'sepal_width' : sepal_width,
            'petal_length': petal_length,
            'petal_width' : petal_width }
    features = pd.DataFrame(data, index=[0])
    return features

df = sidebar_feature()


# 그래프 이름
st.subheader('사용자 입력 파라미터')
# 사용자가 사이드바로 입력한 데이터셋 보여주기
st.write(df)


iris = datasets.load_iris()
# 입력값
X = iris.data
# 예측값
Y = iris.target


# 붓꽃 종류 보여주기
# 1: setosa, 2: virsicolor, 3: virginica
st.subheader('예측')
st.write(iris.target_names)


# 사용할 머신러닝 모델 불러오기
knn_clf = KNeighborsClassifier()
# 트레이닝
knn_clf.fit(X,Y)


# 예측하기
prediction = knn_clf.predict(df)
# 예측 확률
prediction_proba = knn_clf.predict_proba(df)

st.write("# KNeighborsClassifier")

# 예측 데이터프레임
st.subheader('KNeighborsClassifier 예측')
st.write(iris.target_names[prediction])


# 예측 확률 데이터프레임
# 어떤 타입일 확률이 가장 높은지 보여줌 (1에 가까울수록 확률이 높음)
st.subheader('KNeighborsClassifier 예측 확률')
st.write(prediction_proba)

#################### 다른 모델 적용해보기 ################################

# 사용할 머신러닝 모델 불러오기
clf = RandomForestClassifier()
# 트레이닝
clf.fit(X,Y)

st.write("# RandomForestClassifier")

# 예측하기
prediction2 = clf.predict(df)
# 예측 확률
prediction_proba2 = clf.predict_proba(df)


# 예측 데이터프레임
st.subheader('RandomForestClassifier 예측')
st.write(iris.target_names[prediction2])


# 예측 확률 데이터프레임
# 어떤 타입일 확률이 가장 높은지 보여줌 (1에 가까울수록 확률이 높음)
st.subheader('RandomForestClassifßier 예측 확률')
st.write(prediction_proba2)