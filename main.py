pip install streamlit requests
import streamlit as st
import requests

st.set_page_config(page_title="책 검색기", page_icon="📚")

st.title("📖 책을 찾아드립니다!")
st.write("검색어를 입력하면 관련 책들을 보여드릴게요!")

# 사용자 입력
query = st.text_input("책 제목 또는 저자 이름을 입력하세요:")

# 검색 함수
def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        return []

# 결과 출력
if query:
    books = search_books(query)
    if books:
        st.subheader(f"🔍 '{query}' 검색 결과")
        for book in books[:5]:  # 최대 5권만 출력
            volume_info = book["volumeInfo"]
            title = volume_info.get("title", "제목 없음")
            authors = ", ".join(volume_info.get("authors", ["저자 정보 없음"]))
            description = volume_info.get("description", "설명 없음")[:200] + "..."
            thumbnail = volume_info.get("imageLinks", {}).get("thumbnail")

            st.markdown(f"### {title}")
            st.markdown(f"**저자:** {authors}")
            st.markdown(f"**내용 요약:** {description}")
            if thumbnail:
                st.image(thumbnail, width=120)
            st.markdown("---")
    else:
        st.warning("책을 찾을 수 없습니다. 다른 키워드를 시도해보세요!")
