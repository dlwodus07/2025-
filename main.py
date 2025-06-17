import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import seaborn as sns

# 한글 폰트 설정 (matplotlib에서 한글 표시를 위해)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(
    page_title="문해력 현황 분석 및 교육 지원",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 메인 제목 및 설명
st.title("📚 문해력 현황 분석 및 교육 지원 시스템")
st.markdown("### 사서 및 교사를 위한 데이터 기반 문해력 교육 도구")

# 사이드바
st.sidebar.title("🔧 분석 도구")
st.sidebar.markdown("---")

# CSV 데이터 로드 함수
@st.cache_data
def load_data():
    """
    CSV 데이터를 로드하고 전처리하는 함수
    캐시를 사용하여 성능 최적화
    """
    # 실제 데이터 (제공된 CSV 파일 내용)
    data = {
        'Year': [2017, 2017, 2017, 2014, 2014, 2014, 2020, 2020, 2020],
        'Gender': ['전체', '남성', '여성', '전체', '남성', '여성', '전체', '남성', '여성'],
        'Value': [77.6, 81.9, 73.4, 71.5, 77.0, 66.0, 79.8, 83.7, 76.0]
    }
    df = pd.DataFrame(data)
    return df

# 데이터 로드
df = load_data()

# 사이드바 필터 옵션
st.sidebar.subheader("📊 데이터 필터")
selected_years = st.sidebar.multiselect(
    "연도 선택:",
    options=df['Year'].unique(),
    default=df['Year'].unique()
)

selected_gender = st.sidebar.multiselect(
    "성별 선택:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

# 필터링된 데이터
filtered_df = df[(df['Year'].isin(selected_years)) & (df['Gender'].isin(selected_gender))]

# 메인 대시보드 레이아웃
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 문해력 변화 추이")
    
    # matplotlib을 사용한 선형 그래프
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 성별별로 그래프 그리기
    for gender in filtered_df['Gender'].unique():
        gender_data = filtered_df[filtered_df['Gender'] == gender]
        ax.plot(gender_data['Year'], gender_data['Value'], 
                marker='o', linewidth=2, label=gender, markersize=8)
    
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Literacy Rate (%)', fontsize=12)
    ax.set_title('Literacy Rate Trends by Year', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(60, 90)
    
    # Streamlit에 그래프 표시
    st.pyplot(fig)
    
    # 성별 비교 막대 그래프
    st.subheader("🔍 성별 비교 분석")
    
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    # 막대 그래프를 위한 데이터 준비
    years = filtered_df['Year'].unique()
    x = np.arange(len(years))
    width = 0.25
    
    # 각 성별별로 막대 그래프 생성
    genders = ['전체', '남성', '여성']
    colors = ['#3498db', '#e74c3c', '#f39c12']
    
    for i, gender in enumerate(genders):
        if gender in filtered_df['Gender'].values:
            values = []
            for year in years:
                year_gender_data = filtered_df[(filtered_df['Year'] == year) & 
                                             (filtered_df['Gender'] == gender)]
                if not year_gender_data.empty:
                    values.append(year_gender_data['Value'].iloc[0])
                else:
                    values.append(0)
            
            ax2.bar(x + i * width, values, width, label=gender, 
                   color=colors[i], alpha=0.8)
    
    ax2.set_xlabel('Year', fontsize=12)
    ax2.set_ylabel('Literacy Rate (%)', fontsize=12)
    ax2.set_title('Literacy Rate Comparison by Gender', fontsize=14, fontweight='bold')
    ax2.set_xticks(x + width)
    ax2.set_xticklabels(years)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    st.pyplot(fig2)

with col2:
    st.subheader("📊 주요 통계")
    
    # 최신 데이터 (2020년) 추출
    latest_data = df[df['Year'] == 2020]
    
    # 통계 정보를 메트릭으로 표시
    for _, row in latest_data.iterrows():
        st.metric(
            label=f"{row['Gender']} (2020년)",
            value=f"{row['Value']}%"
        )
    
    st.markdown("---")
    
    # 성별 격차 분석
    st.subheader("⚖️ 성별 격차 분석")
    
    # 각 연도별 성별 격차 계산
    gap_data = []
    for year in df['Year'].unique():
        year_data = df[df['Year'] == year]
        male_score = year_data[year_data['Gender'] == '남성']['Value'].iloc[0]
        female_score = year_data[year_data['Gender'] == '여성']['Value'].iloc[0]
        gap = male_score - female_score
        gap_data.append({'Year': year, 'Gap': gap})
    
    gap_df = pd.DataFrame(gap_data)
    
    # 격차 트렌드 그래프
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.plot(gap_df['Year'], gap_df['Gap'], marker='o', 
             linewidth=3, color='#e74c3c', markersize=8)
    ax3.set_xlabel('Year', fontsize=10)
    ax3.set_ylabel('Gap (Male - Female, %p)', fontsize=10)
    ax3.set_title('Gender Gap Trend', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    st.pyplot(fig3)

# 전체 폭 섹션들
st.markdown("---")

# 상세 데이터 테이블
st.subheader("📋 상세 데이터")
col1, col2 = st.columns([3, 1])

with col1:
    st.dataframe(filtered_df, use_container_width=True)

with col2:
    # 데이터 다운로드 버튼
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 CSV 다운로드",
        data=csv,
        file_name='literacy_data.csv',
        mime='text/csv'
    )

# 교육 권장사항 섹션
st.markdown("---")
st.subheader("🎯 교육 권장사항 및 활용 방안")

# 탭으로 구분된 권장사항
tab1, tab2, tab3, tab4 = st.tabs(["📚 일반 권장사항", "👨‍🏫 교사용 가이드", "📖 사서용 가이드", "📈 개선 전략"])

with tab1:
    st.markdown("""
    ### 🔍 데이터 분석 결과 기반 권장사항
    
    **주요 발견사항:**
    - 전반적으로 문해력이 향상되고 있음 (2014년 71.5% → 2020년 79.8%)
    - 성별 격차가 지속적으로 존재함 (남성이 여성보다 높음)
    - 2020년 기준 남녀 격차는 7.7%p
    
    **개선 필요 영역:**
    1. 여성 학습자 대상 맞춤형 프로그램 개발
    2. 성별 격차 해소를 위한 교육 방법 연구
    3. 지속적인 문해력 향상을 위한 종합적 접근
    """)

with tab2:
    st.markdown("""
    ### 👨‍🏫 교사를 위한 활용 가이드
    
    **수업 계획 수립:**
    - 성별별 학습 특성을 고려한 차별화된 교육 방법 적용
    - 문해력 부족 학생 조기 발견 및 집중 지원
    - 동료 교육(Peer Teaching) 활용으로 학습 효과 극대화
    
    **평가 및 피드백:**
    - 정기적인 문해력 진단 평가 실시
    - 개별 학습자 진도 추적 및 맞춤형 피드백 제공
    - 다양한 텍스트 유형을 활용한 종합적 평가
    """)

with tab3:
    st.markdown("""
    ### 📖 사서를 위한 활용 가이드
    
    **장서 개발:**
    - 성별, 연령별 선호도를 고려한 도서 선정
    - 문해력 수준별 맞춤형 도서 분류 및 추천
    - 다양한 장르와 형태의 자료 확충
    
    **독서 프로그램 운영:**
    - 성별 맞춤형 독서 동아리 운영
    - 문해력 향상을 위한 체계적 독서 교육 프로그램 개발
    - 지역사회와 연계한 문해력 증진 활동 기획
    """)

with tab4:
    st.markdown("""
    ### 📈 문해력 개선 전략
    
    **단기 전략 (1년 이내):**
    - 성별 격차 해소를 위한 특별 프로그램 운영
    - 교사 및 사서 대상 문해력 교육 연수 강화
    - 가정과 연계한 독서 환경 조성
    
    **중장기 전략 (2-5년):**
    - 체계적인 문해력 교육 커리큘럼 개발
    - 디지털 문해력 교육 통합
    - 지역사회 전체의 문해력 향상을 위한 네트워크 구축
    """)

# 추가 분석 도구
st.markdown("---")
st.subheader("🔧 추가 분석 도구")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 예측 모델")
    
    # 간단한 선형 회귀를 통한 예측
    if len(df['Year'].unique()) >= 2:
        # 전체 데이터로 예측 (선형 회귀)
        overall_data = df[df['Gender'] == '전체'].copy()
        
        if len(overall_data) >= 2:
            # numpy를 사용한 선형 회귀
            x = overall_data['Year'].values
            y = overall_data['Value'].values
            
            # 최소제곱법으로 기울기와 절편 계산
            slope = np.sum((x - np.mean(x)) * (y - np.mean(y))) / np.sum((x - np.mean(x))**2)
            intercept = np.mean(y) - slope * np.mean(x)
            
            # 2025년 예측값
            prediction_2025 = slope * 2025 + intercept
            
            st.metric(
                label="2025년 예상 문해력 (전체)",
                value=f"{prediction_2025:.1f}%",
                delta=f"{prediction_2025 - overall_data['Value'].iloc[-1]:.1f}%p"
            )

with col2:
    st.markdown("### 🎯 목표 설정")
    
    target_year = st.selectbox("목표 연도", [2025, 2026, 2027, 2028, 2030])
    target_value = st.slider("목표 문해력 (%)", 80, 95, 85)
    
    current_value = df[df['Gender'] == '전체']['Value'].iloc[-1]
    required_improvement = target_value - current_value
    years_remaining = target_year - 2020
    annual_improvement = required_improvement / years_remaining if years_remaining > 0 else 0
    
    st.metric(
        label=f"{target_year}년 목표 달성을 위한 연간 개선율",
        value=f"{annual_improvement:.2f}%p/년"
    )

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📚 문해력 현황 분석 및 교육 지원 시스템 | 사서 및 교사를 위한 데이터 기반 교육 도구</p>
    <p>데이터 기반으로 더 나은 교육 환경을 만들어갑니다.</p>
</div>
""", unsafe_allow_html=True)
