import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (맑은 고딕 등 시스템에 따라 조정 필요)
plt.rcParams['font.family'] = 'Malgun Gothic'

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

# 시각화
fig, ax = plt.subplots(figsize=(8, 10))

ax.barh(ages, male_values, color='steelblue', label='남성')
ax.barh(ages, -female_values, color='pink', label='여성')

ax.set_yticks(ages)
ax.set_yticklabels([f"{age}세" for age in ages])
ax.set_xlabel("인구수")
ax.set_title(f"{selected_region} 인구 피라미드 ({age_range[0]}~{age_range[1]}세)")

# x축 숫자 양쪽으로 출력
xticks = ax.get_xticks()
ax.set_xticklabels([abs(int(x)) for x in xticks])
ax.legend()

st.pyplot(fig)
