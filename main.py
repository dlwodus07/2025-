import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ 데이터 로드 함수
@st.cache_data
def load_data():
    df_gender = pd.read_csv("people_gender.csv", encoding="cp949")
    return df_gender

df = load_data()

# ✅ 지역 선택
regions = df['행정구역'].unique()
selected_region = st.selectbox("지역을 선택하세요:", regions)

# ✅ 선택한 지역 필터링
region_data = df[df['행정구역'] == selected_region]

# ✅ 연령 슬라이더
age_range = st.slider("연령대를 선택하세요:", 0, 100, (0, 100))

# ✅ 연령대 컬럼 이름 생성
ages = list(range(age_range[0], age_range[1] + 1))
male_cols = [f"2025년05월_남_{age}세" for age in ages]
female_cols = [f"2025년05월_여_{age}세" for age in ages]

# ✅ 데이터 처리
male_values = region_data[male_cols].iloc[0].astype(str).str.replace(",", "").astype(int)
female_values = region_data[female_cols].iloc[0].astype(str).str.replace(",", "").astype(int)

# ✅ 인구 피라미드용 데이터프레임 생성
pyramid_df = pd.DataFrame({
    "연령": ages * 2,
    "성별": ["남"] * len(ages) + ["여"] * len(ages),
    "인구수": list(male_values) + list(female_values * -1)
})

# ✅ 시각화
fig = px.bar(
    pyramid_df,
    x="인구수",
    y="연령",
    color="성별",
    orientation="h",
    title=f"{selected_region} 인구 피라미드 (연령 {age_range[0]}~{age_range[1]}세)",
    color_discrete_map={"남": "#1f77b4", "여": "#e377c2"},
)

fig.update_layout(
    xaxis_title="인구수",
    yaxis_title="연령",
    font=dict(family="Malgun Gothic"),
    bargap=0.1
)

st.plotly_chart(fig)
