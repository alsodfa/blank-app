import streamlit as st
import pandas as pd
from PIL import Image

# --- 사이드바 구성 ---
st.sidebar.title("분석 조건 설정")

# 투수/타자 선택 (필수)
position = st.sidebar.radio("선택", ["투수", "타자"], index=0)

# 세부사항 단일 선택 (옵션)
detail_options = ["세부사항없음", "주자 있음", "주자 없음", "이닝별", "월별"]
detail = st.sidebar.radio("세부사항 (하나만 선택)", detail_options, index=0)

# 월별 또는 이닝별 선택 시 슬라이더 등장
month_range = None
inning_range = None

if detail == "월별":
    month_range = st.sidebar.slider("월 선택", 3, 9, (3, 4))  # 3~4월, 5~6월 등
elif detail == "이닝별":
    inning_range = st.sidebar.slider("이닝 선택", 1, 9, (1, 3))

# --- 메인 화면 ---
st.title("2025시즌 삼성라이온즈 결산")

# 선수 검색창 (자동완성)
all_players = ["최원태", "원태인", "정우영", "김현수"]  # 예시 리스트
selected_player = st.text_input("선수 이름 검색", "")

# 필터된 선수 리스트 보여주기
if selected_player:
    filtered_players = [p for p in all_players if selected_player in p]
    if filtered_players:
        selected_player = st.selectbox("선수 선택", filtered_players)
    else:
        st.warning("해당 이름을 포함하는 선수가 없습니다.")

# 선수 사진 띄우기 (예시)
if selected_player:
    image = Image.open("/mnt/data/39ebc047-b5d6-4b73-8e9a-ec52d898639e.png")  # 사용자 업로드 사진 사용
    st.image(image, caption=f"{selected_player} 선수", width=200)

# --- 시각화 영역 (임시) ---
st.subheader("스탯 시각화")
st.info("선수와 조건을 선택하면 여기에 그래프가 나타납니다.")

# TODO: 선택한 조건(position, detail, 월/이닝 범위 등)에 따라 데이터 필터링 및 시각화
# 예: df[(df["선수"] == selected_player) & (df["이닝"] >= inning_range[0])] 등

# Streamlit 실행 예시:
# streamlit run streamlit_baseball_dashboard.py
