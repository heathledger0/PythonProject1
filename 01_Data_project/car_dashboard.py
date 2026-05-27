import streamlit as st
import pandas as pd
import plotly.express as px


# 1. 페이지 설정
st.set_page_config(page_title="자동차 통계 애니메이션 시각화", layout="wide")

st.title("🚗 시간에 따라 움직이는 자동차 판매 버블 차트")
st.markdown("하단의 **재생(▶) 버튼**을 누르면 2023년부터 2025년까지 세단 시장의 전동화 및 가격·판매량 변화 추이가 애니메이션으로 재생됩니다.")

# 2. 데이터 불러오기
@st.cache_data
def load_bubble_data():
    # 위에서 다운로드한 CSV 파일 이름을 적어줍니다.
    return pd.read_csv("bubble_car_sales.csv")

df = load_bubble_data()

# 3. 애니메이션 버블 차트 생성
fig = px.scatter(
    df,
    x="평균가격(만원)",
    y="분기판매량(대)",
    animation_frame="시점",         # 애니메이션을 구동할 시간 축 (2023 Q1 ~ 2025 Q4)
    animation_group="모델명",       # 애니메이션 흐름 속에서 추적할 그룹
    size="누적매출액(억원)",         # 버블의 크기
    color="모델명",                 # 버블의 색상
    hover_name="모델명",            # 마우스를 올렸을 때 표시할 이름
    text="모델명",                  # 버블 위에 텍스트 라벨 표시
    size_max=70,                    # 버블 최대 크기 제한
    range_x=[2000, 5200],           # X축 범위 고정 (애니메이션 시 화면 흔들림 방지)
    range_y=[5000, 35000],          # Y축 범위 고정
    title="분기별 차량 가격 대비 판매량 및 매출 규모 변동 추이",
    labels={"평균가격(만원)": "차량 평균 판매 가격 (만 원)", "분기판매량(대)": "분기별 판매 실적 (대)"}
)

# 텍스트 라벨 위치 조정 및 차트 레이아웃 깔끔하게 정리
fig.update_traces(textposition='top center')
fig.update_layout(
    height=650,
    margin=dict(l=40, r=40, t=60, b=40),
    font=dict(size=13)
)

# 4. 스트림릿 화면에 차트 뿌리기
st.plotly_chart(fig, use_container_width=True)

# 5. 데이터 구조 확인용 테이블
if st.checkbox("버블 차트 원본 데이터 보기"):
    st.dataframe(df, use_container_width=True)