import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# --- 설정 ---
st.set_page_config(page_title="Titanic Data Dashboard", layout="wide")
st.title("🚢 Titanic 생존자 분석 대시보드")

# --- 데이터 로딩 ---
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")
    df['Age'].fillna(df['Age'].median(), inplace=True)
    df['Fare'].fillna(df['Fare'].median(), inplace=True)
    df['Embarked'].fillna('S', inplace=True)
    return df

df = load_data()

# --- 사이드바 필터 ---
st.sidebar.header("🔍 데이터 필터")
sex_filter = st.sidebar.multiselect("성별 선택", options=df['Sex'].unique(), default=df['Sex'].unique())
pclass_filter = st.sidebar.multiselect("등급 선택", options=sorted(df['Pclass'].unique()), default=sorted(df['Pclass'].unique()))
embarked_filter = st.sidebar.multiselect("탑승 항구 선택", options=df['Embarked'].unique(), default=df['Embarked'].unique())

# 클러스터 수 설정
k_clusters = st.sidebar.slider("클러스터 수 (KMeans)", min_value=1, max_value=5, value=1)

# 필터링 적용
filtered_df = df[
    (df['Sex'].isin(sex_filter)) &
    (df['Pclass'].isin(pclass_filter)) &
    (df['Embarked'].isin(embarked_filter))
]

st.subheader("🎯 필터링된 생존자 통계")

# --- 생존율 파이 차트 ---
survived_counts = filtered_df['Survived'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(survived_counts, labels=['사망', '생존'], autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
ax1.axis('equal')
st.pyplot(fig1)

# --- 성별 및 등급별 생존율 ---
st.subheader("📊 성별 및 등급별 생존율")
grouped = filtered_df.groupby(['Sex', 'Pclass'])['Survived'].mean().unstack()
st.bar_chart(grouped)

# --- 나이 히스토그램 ---
st.subheader("📈 나이 분포")
fig2, ax2 = plt.subplots()
sns.histplot(filtered_df['Age'], bins=20, kde=True, ax=ax2)
st.pyplot(fig2)

# --- 산점도 (Fare vs Age + 클러스터링) ---
st.subheader("💡 요금 vs 나이 (클러스터링 포함)")
if k_clusters > 1:
    km = KMeans(n_clusters=k_clusters, n_init=10, random_state=42)
    filtered_df['cluster'] = km.fit_predict(filtered_df[['Fare', 'Age']])
    fig3, ax3 = plt.subplots()
    sns.scatterplot(
        data=filtered_df, x='Fare', y='Age', hue='cluster', palette='Set2', ax=ax3
    )
    st.pyplot(fig3)
else:
    fig3, ax3 = plt.subplots()
    sns.scatterplot(data=filtered_df, x='Fare', y='Age', ax=ax3)
    st.pyplot(fig3)

# --- 원본 데이터 보기 ---
with st.expander("🧾 원본 데이터 보기"):
    st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
st.markdown("🧠 더 많은 AI 대시보드를 쉽게 만들고 싶다면 👉 [GPTOnline](https://gptonline.ai/ko/)")
