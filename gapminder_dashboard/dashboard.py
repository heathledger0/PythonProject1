# pip install streamlit plotly pandas
# 실행 방법: streamlit run dashboard.py

import streamlit as st          # 웹 화면(버튼, 탭, 차트 등)을 만드는 도구
import pandas as pd             # 표(엑셀 같은) 데이터를 다루는 도구
import plotly.express as px     # 인터랙티브한 그래프(애니메이션, 지도 등)를 그리는 도구
sdfsdfsdfsdfsdfasdfsdfasdfsdfsafasdfasdf
st.set_page_config(page_title="Gapminder 대시보드", page_icon="🌍", layout="wide")  # 브라우저 탭 제목/아이콘 + 화면을 넓게 사용
st.title("🌍 Gapminder: 세계 발전 데이터 시각화")                                    # 페이지 맨 위 큰 제목
st.caption("Hans Rosling의 TED 강연을 유명하게 만든 데이터 (1952~2007, 142개국)")    # 제목 아래 작은 설명 글씨

df = pd.read_csv("gapminder.csv")  # CSV 파일을 표(데이터프레임)로 불러오기. 이후 모든 탭이 이 df를 함께 사용

tab1, tab2, tab3, tab4 = st.tabs([   # 탭 4개를 한 번에 만들어 각각 tab1~tab4에 담기
    "🫧 애니메이션 버블",            # 첫 번째 탭 이름
    "🗺️ 세계 지도",                  # 두 번째 탭 이름
    "📈 국가 트렌드",                # 세 번째 탭 이름
    "🏆 대륙 비교",                  # 네 번째 탭 이름
])


# --- 탭 1: 애니메이션 버블 차트 ---
with tab1:  # 여기 들여쓰기 안에 적은 내용이 첫 번째 탭 화면에 나옴
    st.header("🫧 GDP vs 기대수명 (시간 흐름)")                                       # 탭 안의 소제목
    st.write("▶ 버튼을 눌러 1952년부터 2007년까지 세계가 어떻게 변했는지 확인해보세요.")  # 안내 문장

    fig = px.scatter(           # 점(버블) 그래프를 만들어 fig에 담기
        df,                     # 사용할 데이터(표)
        x="gdpPercap",          # 가로축 = 1인당 GDP
        y="lifeExp",            # 세로축 = 기대수명
        size="pop",             # 버블 크기 = 인구 (인구 많을수록 큰 원)
        color="continent",      # 버블 색 = 대륙별로 다른 색
        hover_name="country",   # 마우스를 올리면 국가명 표시
        animation_frame="year", # 연도별로 화면을 나눠 ▶ 재생(애니메이션) 가능하게
        animation_group="country",  # 애니메이션 중 같은 나라를 계속 추적(부드럽게 이동)
        log_x=True,             # 가로축을 로그 스케일로(GDP 차이가 너무 커서 안 그러면 한쪽에 몰림)
        size_max=60,            # 가장 큰 버블의 최대 크기 제한
        range_x=[200, 100000],  # 가로축 표시 범위 고정(애니메이션 중 축이 안 흔들리게)
        range_y=[25, 90],       # 세로축 표시 범위 고정
        labels={"gdpPercap": "1인당 GDP (달러)", "lifeExp": "기대수명 (세)", "pop": "인구"},  # 영어 컬럼명 → 화면엔 한글로 표시
        title="1인당 GDP vs 기대수명 (버블 크기 = 인구)",  # 그래프 제목
    )
    fig.update_layout(height=580)                  # 그래프 높이를 580픽셀로 조정
    st.plotly_chart(fig, use_container_width=True) # 완성한 그래프를 화면에 표시(가로 폭에 꽉 채움)


# --- 탭 2: 세계 지도 ---
with tab2:  # 두 번째 탭 화면
    st.header("🗺️ 세계 지도로 보기")  # 소제목
    화면을
    col1, col2 = st.columns(2)  #  좌우 2칸으로 나누기
    with col1:                  # 왼쪽 칸
        metric = st.selectbox(                      # 드롭다운에서 한 개 선택 → 고른 값이 metric에 담김
            "표시할 지표",                            # 드롭다운 위 라벨
            ["gdpPercap", "lifeExp", "pop"],         # 선택지(실제 컬럼명)
            format_func=lambda x: {"gdpPercap": "1인당 GDP", "lifeExp": "기대수명", "pop": "인구"}[x],  # 화면엔 한글로 보이게 변환
        )
    with col2:                  # 오른쪽 칸
        animate = st.checkbox("연도별 애니메이션", value=True)  # 체크박스(기본은 켜짐) → True/False가 animate에 담김

    label_map = {"gdpPercap": "1인당 GDP (달러)", "lifeExp": "기대수명 (세)", "pop": "인구"}  # 컬럼명 → 한글 라벨 사전

    # px.choropleth: iso_alpha(국가 코드)로 세계 지도를 자동 생성
    fig = px.choropleth(        # 나라별로 색칠하는 세계 지도 그래프
        df,                     # 사용할 데이터
        locations="iso_alpha",  # 나라를 알아보는 기준 = 국가 코드 컬럼(예: KOR, JPN)
        color=metric,           # 색칠 기준 = 위에서 고른 지표
        hover_name="country",   # 마우스 올리면 국가명 표시
        animation_frame="year" if animate else None,  # 체크박스 켜졌으면 연도 애니메이션, 아니면 정지
        color_continuous_scale="Viridis",  # 색 팔레트(낮음→높음 그라데이션)
        labels={metric: label_map[metric]},  # 범례 라벨을 한글로
        title=f"세계 {label_map[metric]} 분포",  # 고른 지표에 맞춰 제목 자동 변경
    )
    fig.update_layout(height=520)                  # 지도 높이 조정
    st.plotly_chart(fig, use_container_width=True) # 화면에 표시


# --- 탭 3: 국가 트렌드 ---
with tab3:  # 세 번째 탭 화면
    st.header("📈 국가별 시간 흐름")  # 소제목

    default_countries = ["Korea, Rep.", "Japan", "China", "United States", "Germany"]  # 처음에 미리 골라둘 나라들
    all_countries = sorted(df["country"].unique())  # 데이터에 있는 모든 나라 목록(가나다/알파벳 순 정렬)
    selected = st.multiselect(   # 여러 개를 고를 수 있는 위젯 → 고른 나라들이 리스트로 selected에 담김
        "국가 선택 (여러 개 가능)",  # 라벨
        all_countries,            # 선택지(전체 나라)
        default=[c for c in default_countries if c in all_countries],  # 기본 선택값(데이터에 실제 있는 것만)
    )

    if not selected:                       # 아무 나라도 안 골랐다면
        st.info("국가를 하나 이상 선택하세요.")  # 안내 메시지를 보여주고
        st.stop()                          # 여기서 멈춤(그릴 데이터가 없으니 에러 방지)

    metric2 = st.radio(          # 라디오 버튼(한 개만 선택) → 고른 값이 metric2에 담김
        "지표 선택",              # 라벨
        ["lifeExp", "gdpPercap", "pop"],  # 선택지(실제 컬럼명)
        format_func=lambda x: {"lifeExp": "기대수명", "gdpPercap": "1인당 GDP", "pop": "인구"}[x],  # 화면엔 한글로
        horizontal=True,         # 버튼을 가로로 나란히 배치
    )

    filtered = df[df["country"].isin(selected)]  # 전체 표에서 '고른 나라들'에 해당하는 행만 골라내기
    label_map2 = {"lifeExp": "기대수명 (세)", "gdpPercap": "1인당 GDP (달러)", "pop": "인구"}  # 한글 라벨 사전

    fig = px.line(               # 선 그래프(시간에 따른 변화 보기에 좋음)
        filtered,                # 골라낸 데이터만 사용
        x="year", y=metric2,     # 가로축=연도, 세로축=고른 지표
        color="country",         # 나라별로 다른 색 선
        markers=True,            # 선 위에 점도 함께 표시
        labels={"year": "연도", metric2: label_map2[metric2]},  # 축 라벨을 한글로
        title=f"선택 국가 {label_map2[metric2]} 변화 (1952~2007)",  # 제목 자동 변경
    )
    fig.update_layout(height=480)                  # 높이 조정
    st.plotly_chart(fig, use_container_width=True) # 화면에 표시


# --- 탭 4: 대륙 비교 ---
with tab4:  # 네 번째 탭 화면
    st.header("🏆 대륙별 비교")  # 소제목

    year = st.slider("연도 선택", 1952, 2007, 2007, step=5)  # 슬라이더: 최소1952, 최대2007, 기본2007, 5년 간격
    df_year = df[df["year"] == year]                         # 전체 표에서 고른 연도의 행만 골라내기

    col1, col2 = st.columns(2)  # 화면을 좌우 2칸으로 나누기

    with col1:                  # 왼쪽 칸
        st.subheader("대륙별 평균 기대수명")  # 작은 제목
        bar_df = df_year.groupby("continent", as_index=False)["lifeExp"].mean().sort_values("lifeExp", ascending=False)  # 대륙별 평균 기대수명 계산 후 높은 순 정렬
        fig = px.bar(            # 막대그래프
            bar_df, x="continent", y="lifeExp",  # 가로축=대륙, 세로축=평균 기대수명
            color="continent",   # 대륙별 다른 색
            labels={"lifeExp": "평균 기대수명 (세)", "continent": "대륙"},  # 한글 라벨
            title=f"{year}년 대륙별 평균 기대수명",  # 고른 연도를 제목에 표시
        )
        fig.update_layout(showlegend=False, height=380)  # 범례 숨기고(색만 봐도 충분) 높이 조정
        st.plotly_chart(fig, use_container_width=True)   # 화면에 표시

    with col2:                  # 오른쪽 칸
        st.subheader("대륙별 GDP 분포 (박스 플롯)")  # 작은 제목
        fig = px.box(           # 박스플롯(평균이 아니라 분포 전체: 최소~최대, 중앙값 등을 보여줌)
            df_year, x="continent", y="gdpPercap",  # 가로축=대륙, 세로축=1인당 GDP
            color="continent",  # 대륙별 다른 색
            labels={"gdpPercap": "1인당 GDP (달러)", "continent": "대륙"},  # 한글 라벨
            title=f"{year}년 대륙별 GDP 분포",  # 고른 연도를 제목에 표시
        )
        fig.update_layout(showlegend=False, height=380)  # 범례 숨기고 높이 조정
        st.plotly_chart(fig, use_container_width=True)   # 화면에 표시

    st.subheader(f"{year}년 상위 10개국 (1인당 GDP 기준)")  # 표 위 제목
    top10 = df_year.nlargest(10, "gdpPercap")[["country", "continent", "gdpPercap", "lifeExp", "pop"]]  # GDP 상위 10개국 행 + 보여줄 컬럼만 추리기
    top10.columns = ["국가", "대륙", "1인당 GDP", "기대수명", "인구"]  # 컬럼 이름을 한글로 바꾸기
    top10 = top10.reset_index(drop=True)  # 행 번호를 0부터 새로 매기기(기존 번호 버림)
    top10.index += 1                      # 행 번호를 1부터 시작하게(1위, 2위처럼 보이게)
    st.dataframe(top10.style.background_gradient(subset=["1인당 GDP"], cmap="YlGn"), use_container_width=True)  # 표를 화면에 표시(GDP 칸은 값이 클수록 진한 초록으로)
