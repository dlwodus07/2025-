import streamlit as st
import pandas as pd
import altair as alt

@st.cache_data
def load_data():
    df_gender = pd.read_csv("people_gender.csv", encoding="cp949")
    return df_gender

df = load_data()

regions = df['행정구역'].unique()
selected_region = st.selectbox("지역을 선택하세요:", regions)
region_data = df[df['행정구역'] == selected_region]

age_range = st.slider("연령대를 선택하세요:", 0, 100, (0, 100))
ages = list(range(age_range[0], age_range[1] + 1))

male_cols = [f"2025년05월_남_{age}세" for age in ages]
female_cols = [f"2025년05월_여_{age}세" for age in ages]

male_values = region_data[male_cols].iloc[0].astype(str).str.replace(",", "").astype(int)
female_values = region_data[female_cols].iloc[0].astype(str).str.replace(",", "").astype(int)

pyramid_df = pd.DataFrame({
    "연령": ages * 2,
    "성별": ["남"] * len(ages) + ["여"] * len(ages),
    "인구수": list(male_values) + list(female_values * -1)
})

chart = alt.Chart(pyramid_df).mark_bar().encode(
    x=alt.X('인구수:Q', title='인구수', axis=alt.Axis(format='.0f')),
    y=alt.Y('연령:O', title='연령', sort='descending'),
    color=alt.Color('성별:N', scale=alt.Scale(domain=["남", "여"], range=["steelblue", "pink"]))
).properties(
    width=600,
    height=800,
    title=f"{selected_region} 인구 피라미드 ({age_range[0]}~{age_range[1]}세)"
)

st.altair_chart(chart)
