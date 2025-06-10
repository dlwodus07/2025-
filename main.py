import streamlit as st
import pandas as pd

# 스택 클래스 정의
class BookViewStack:
    """
    도서 조회 기록을 관리하는 스택 자료구조
    LIFO(Last In First Out) 방식 - 마지막에 본 도서가 가장 먼저 나옴
    """
    def __init__(self, max_size=10):
        self.stack = []  # 스택을 리스트로 구현
        self.max_size = max_size  # 최대 저장 개수
    
    def push(self, book_info):
        """
        스택에 도서 정보 추가 (Push 연산)
        - 같은 순위의 도서가 이미 있으면 제거 후 맨 위에 추가
        - 최대 크기를 초과하면 가장 오래된 항목 제거
        """
        # 중복 제거: 같은 순위번호의 도서가 있으면 제거
        self.stack = [book for book in self.stack if book['순위번호'] != book_info['순위번호']]
        
        # 새 도서를 스택 맨 위에 추가
        self.stack.append(book_info)
        
        # 최대 크기 초과시 가장 아래(오래된) 항목 제거
        if len(self.stack) > self.max_size:
            self.stack.pop(0)  # 첫 번째 요소 제거 (가장 오래된 것)
    
    def pop(self):
        """
        스택에서 맨 위 도서 제거하고 반환 (Pop 연산)
        스택이 비어있으면 None 반환
        """
        if not self.is_empty():
            return self.stack.pop()
        return None
    
    def peek(self):
        """
        스택 맨 위 도서 확인 (제거하지 않음)
        """
        if not self.is_empty():
            return self.stack[-1]
        return None
    
    def is_empty(self):
        """스택이 비어있는지 확인"""
        return len(self.stack) == 0
    
    def size(self):
        """스택 크기 반환"""
        return len(self.stack)
    
    def get_history(self):
        """조회 기록 반환 (최신순으로 정렬)"""
        return list(reversed(self.stack))

# 세션 상태 초기화 (스택 객체 생성)
if 'book_stack' not in st.session_state:
    st.session_state.book_stack = BookViewStack()

# CSV 파일 읽기 (CP949 인코딩)
@st.cache_data
def load_book_data():
    """데이터 로딩 함수 - 캐싱으로 성능 최적화"""
    return pd.read_csv("people_book.csv", encoding="cp949")

# 데이터 로드
df = load_book_data()

# 메인 제목
st.title("📚 인기 도서 순위 조회")
st.markdown("### 스택(Stack) 자료구조로 조회 기록 관리")

# 레이아웃: 메인 영역과 사이드바로 구분
col_main, col_history = st.columns([2.5, 1.5])

with col_main:
    # 순위 선택 (중복 제거 및 정렬)
    unique_ranks = sorted(df["순위번호"].unique())
    selected_rank = st.selectbox("순위를 선택하세요 📊", unique_ranks)
    
    # 선택된 순위의 도서 정보 필터링
    book_info = df[df["순위번호"] == selected_rank].iloc[0]
    
    # 스택에 현재 조회한 도서 정보 추가 (자동으로 Push)
    book_dict = {
        '순위번호': book_info['순위번호'],
        '도서명정보': book_info['도서명정보'],
        '저자명정보': book_info['저자명정보'],
        '출판사명': book_info['출판사명'],
        '출판년도': book_info['출판년도'],
        '도서이미지URL': book_info['도서이미지URL']
    }
    st.session_state.book_stack.push(book_dict)
    
    # 도서 정보 표시
    st.subheader(f"📖 {book_info['도서명정보']}")
    
    # 상세 정보를 두 컬럼으로 나누어 표시
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown(f"**👤 저자:** {book_info['저자명정보']}")
        st.markdown(f"**🏢 출판사:** {book_info['출판사명']}")
    
    with info_col2:
        year = int(book_info['출판년도']) if not pd.isna(book_info['출판년도']) else '정보 없음'
        st.markdown(f"**📅 출판년도:** {year}")
        st.markdown(f"**🏆 현재 순위:** {book_info['순위번호']}위")
    
    # 도서 이미지 출력
    st.image(book_info["도서이미지URL"], use_column_width=True)

with col_history:
    # 조회 기록 표시 (스택 활용)
    st.subheader("🕒 최근 조회 기록")
    st.caption(f"스택 크기: {st.session_state.book_stack.size()}개")
    
    # 스택에서 조회 기록 가져오기
    history = st.session_state.book_stack.get_history()
    
    if history:
        # 최근 조회한 도서들을 카드 형태로 표시
        for i, book in enumerate(history[:8]):  # 최근 8개만 표시
            with st.expander(
                f"{i+1}. {book['도서명정보'][:15]}{'...' if len(book['도서명정보']) > 15 else ''}", 
                expanded=(i == 0)  # 첫 번째만 펼쳐서 표시
            ):
                st.write(f"**순위:** {book['순위번호']}위")
                st.write(f"**저자:** {book['저자명정보']}")
                year = int(book['출판년도']) if not pd.isna(book['출판년도']) else '정보 없음'
                st.write(f"**출판년도:** {year}")
                
                # 이 도서로 바로가기 버튼
                if st.button(f"📖 다시 보기", key=f"view_{book['순위번호']}_{i}"):
                    # 세션에서 선택된 순위 변경하고 페이지 새로고침
                    st.query_params.from_dict({"rank": str(book['순위번호'])})
                    st.rerun()
    else:
        st.info("아직 조회한 도서가 없습니다.")
    
    # 스택 관리 버튼들
    st.markdown("---")
    st.subheader("🔧 기록 관리")
    
    # Pop 버튼 (가장 최근 조회 기록 제거)
    if st.button("🗑️ 최근 기록 삭제", help="스택에서 Pop 연산 수행"):
        removed_book = st.session_state.book_stack.pop()
        if removed_book:
            st.success(f"'{removed_book['도서명정보']}' 기록이 삭제되었습니다!")
            st.rerun()
        else:
            st.warning("삭제할 기록이 없습니다!")
    
    # 전체 기록 삭제
    if st.button("🧹 전체 기록 삭제", help="스택 전체 초기화"):
        st.session_state.book_stack = BookViewStack()
        st.success("모든 조회 기록이 삭제되었습니다!")
        st.rerun()

# 하단 정보 섹션
st.markdown("---")

# 스택 자료구조 설명
with st.expander("🧠 스택(Stack) 자료구조란?"):
    st.markdown("""
    **스택의 특징:**
    - **LIFO 구조**: Last In First Out (후입선출) - 마지막에 들어간 것이 먼저 나옴
    - **Push 연산**: 스택 맨 위에 새로운 데이터 추가
    - **Pop 연산**: 스택 맨 위의 데이터를 제거하고 반환
    - **Peek 연산**: 스택 맨 위의 데이터를 확인 (제거하지 않음)
    
    **이 앱에서의 활용:**
    - 사용자가 조회한 도서를 순서대로 스택에 저장
    - 가장 최근에 본 도서가 맨 위에 표시됨
    - 같은 도서를 다시 보면 기존 기록을 제거하고 맨 위로 이동
    - 최대 10개까지만 저장하여 메모리 효율성 확보
    """)

# 디버깅 정보
with st.expander("🔧 디버깅 과정 및 문제 해결"):
    st.markdown("""
    **발생한 문제들과 해결 과정:**
    
    **1. 세션 상태 관리 문제**
    - **문제**: Streamlit에서 selectbox 변경시 스택 데이터가 초기화됨
    - **해결**: `st.session_state`를 사용하여 스택 객체를 영구 보존
    - **코드**: `if 'book_stack' not in st.session_state:` 조건으로 초기화 방지
    
    **2. 중복 데이터 처리**
    - **문제**: 같은 도서를 여러 번 선택하면 스택에 중복 저장됨
    - **해결**: Push 메서드에서 같은 순위번호 도서를 먼저 제거 후 추가
    - **논리**: 리스트 컴프리헨션으로 `[book for book in self.stack if book['순위번호'] != book_info['순위번호']]`
    
    **3. 메모리 관리**
    - **문제**: 계속 사용하면 스택 크기가 무한정 증가할 수 있음
    - **해결**: `max_size=10`으로 최대 크기 제한, 초과시 가장 오래된 항목 자동 제거
    - **효과**: 메모리 사용량 제한으로 안정적인 앱 운영
    
    **4. 사용자 경험 개선**
    - **문제**: 기록에서 도서 선택시 어떻게 해당 도서로 이동할지 고민
    - **해결**: 버튼 클릭시 `st.rerun()`으로 페이지 새로고침하여 최신 상태 반영
    """)

# 현재 스택 상태 정보
st.subheader("📊 현재 스택 상태")
stack_col1, stack_col2, stack_col3 = st.columns(3)

with stack_col1:
    st.metric("저장된 도서 수", st.session_state.book_stack.size())

with stack_col2:
    st.metric("최대 저장 가능", "10개")

with stack_col3:
    is_empty = st.session_state.book_stack.is_empty()
    st.metric("스택 상태", "비어있음" if is_empty else "데이터 있음")

# 맨 아래 정보
st.markdown("---")
st.caption("💡 **스택의 LIFO 특성을 활용한 도서 조회 기록 관리 시스템**")
st.caption("📚 CP949 인코딩으로 한글 도서 데이터 처리 | 🔄 자동 중복 제거 | 📝 최대 10개 기록 저장")
