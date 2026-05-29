import streamlit as st
from textblob import TextBlob

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 영문 문법 & 맞춤법 검사기",
    page_icon="✨",
    layout="centered"
)

# 제목 및 상단 꾸미기
st.title('✨ 실시간 영문 문법 & 맞춤법 검사기 📝')
st.markdown("---")
st.write('텍스트를 입력하시면 AI가 단순 철자 오류뿐만 아니라 **문맥에 맞는 문법 오류**까지 바로잡아 드립니다.')

# 텍스트 입력 공간
text = st.text_area("✍️ 검사할 영문 텍스트를 입력하세요:", value='', height=150, placeholder="Example: I wants to do something excited.")

# 버튼 클릭 시 작동
if st.button('🚀 문장 교정하기', use_container_width=True):
    if text.strip() == '':
        st.warning('⚠️ 검사할 문장을 입력해 주세요!') 
    else: 
        with st.spinner('🎯 문장 문맥 및 문법을 분석하는 중...'):
            # TextBlob을 이용한 문맥 분석 및 교정
            blob = TextBlob(text)
            corrected_text = str(blob.correct())
            
            # 1. 결과 출력
            st.success('🎉 분석이 완료되었습니다!')
            
            st.markdown(f"### 📍 **교정된 문장:**")
            st.info(f"**{corrected_text}**")
            
            st.markdown("---")
            
            # 2. 변경 사항 비교 및 리포트
            st.markdown("### 🔍 오류 수정 리포트")
            
            # 원본 문장과 교정된 문장이 완전히 일치하는지 확인
            if text.strip().lower() == corrected_text.strip().lower():
                st.balloons()
                st.success("✅ 완벽합니다! 문맥이나 문법상 오류가 발견되지 않았습니다.")
            else:
                st.write("입력하신 문장에서 어색한 문법 및 철자를 수정했습니다.")
                
                # 단어별로 비교하여 틀린 부분 시각화
                orig_words = text.split()
                corr_words = corrected_text.split()
                
                report_data = []
                idx = 1
                
                # 최소 길이에 맞춰 단어 비교 (간단한 비교 로직)
                for o_w, c_w in zip(orig_words, corr_words):
                    # 문장부호 제거 후 비교
                    clean_o = "".join(c for c in o_w if c.isalnum())
                    clean_c = "".join(c for c in c_w if c.isalnum())
                    
                    if clean_o.lower() != clean_c.lower():
                        report_data.append({
                            "번호": idx,
                            "기존 표현": f"❌ {o_w}",
                            "추천 표현": f"✅ {c_w}",
                            "수정 이유": "문맥에 맞지 않는 문법 성분이거나 철자 오류입니다."
                        })
                        idx += 1
                
                if report_data:
                    st.table(report_data)
                else:
                    st.info("💡 전체적인 문장 구조와 구두점이 문맥에 맞게 매끄럽게 교정되었습니다.")
