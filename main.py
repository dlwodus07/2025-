import streamlit as st

# 책 데이터 리스트
books_data = [
    {
        "title": "데미안",
        "author": "헤르만 헤세",
        "description": "한 청년의 자아 찾기 여정을 그린 성장소설.",
        "thumbnail": "https://image.aladin.co.kr/product/22198/22/cover500/k172636398_1.jpg"
    },
    {
        "title": "1984",
        "author": "조지 오웰",
        "description": "전체주의 감시 사회를 그린 디스토피아 고전.",
        "thumbnail": "https://image.aladin.co.kr/product/27143/64/cover500/k622831981_1.jpg"
    },
    {
        "title": "자기 앞의 생",
        "author": "로맹 가리",
        "description": "한 소년과 노파가 함께 살아가는 감동적인 이야기.",
        "thumbnail": "https://image.aladin.co.kr/product/24324/90/cover500/k572632217_1.jpg"
    },
]

# Streamlit 페이지 설정
st.set_page_config(page_title="내장형 책 검색기", page_icon="📚")

st.title("📖 내장 데이터로 책 검색하기")
st.write("제목 또는 저자를 입력해 책을 검색해보세요!")

# 사용자 검색어 입력
query = st.text_input("🔍 검색어 (제목 또는 저자):")

# 검색 로직
if query:
    found_books = []
    for book in books_data:
        if query.lower() in book["title"].lower() or query.lower() in book["author"].lower():
            found_books.append(book)

    # 결과 출력
    if found_books:
        st.success(f"📚 '{query}'에 대한 검색 결과:")
        for book in found_books:
            st.markdown(f"### {book['title']}")
            st.markdown(f"**저자:** {book['author']}")
            st.markdown(f"**내용:** {book['description']}")
            if book.get("thumbnail"):
                st.image(book["thumbnail"], width=120)
            st.markdown("---")
    else:
        st.warning("검색 결과가 없습니다. 다른 키워드를 시도해보세요!")

else:
    st.info("검색어를 입력해주세요.")
