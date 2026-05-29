import streamlit as st
from spellchecker import SpellChecker
import re

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 영문 맞춤법 검사기",
    page_icon="✨",
    layout="centered"
)

# 제목 및 상단 꾸미기
st.title('✨ 실시간 영문 맞춤법 & 철자 검사기 📝')
st.markdown("---")
st.write('텍스트를 입력하시면 AI가 잘못된 철자를 찾아내고 올바른 추천 단어와 함께 분석 리포트를 제공합니다.')

# 텍스트 입력 공간
text = st.text_area("✍️ 검사할 영문 텍스트를 입력하세요:", value='', height=150, placeholder="Example: He went to scool yesterday with his freinds.")

# 버튼 클릭 시 작동
if st.button('🚀 문장 교정하기', use_container_width=True):
    if text.strip() == '':
        st.warning('⚠️ 검사할 문장을 입력해 주세요!') 
    else: 
        with st.spinner('🎯 철자 오류를 분석하는 중...'):
            # 영어 철자 검사기 초기화
            spell = SpellChecker(language='en')
            
            # 특수문자를 제외하고 단어만 분리
            words = re.findall(r'\b\w+\b', text)
            
            # 틀린 단어 찾기
            misspelled = spell.unknown(words)
            
            # 1. 결과 출력 준비
            st.success('🎉 분석이 완료되었습니다!')
            
            # 교정된 문장 만들기
            corrected_text = text
            report_data = []
            
            if not misspelled:
                st.balloons()
                st.markdown(f"### 📍 **교정된 문장:**")
                st.info(f"**{text}**")
                st.markdown("---")
                st.success("✅ 완벽합니다! 철자 오류가 발견되지 않았습니다.")
            else:
                # 틀린 단어들을 돌면서 문장 수정 및 리포트 작성
                for idx, word in enumerate(misspelled, 1):
                    # 가장 확률이 높은 추천 단어 가져오기
                    correction = spell.correction(word)
                    if correction is None:
                        correction = word
                    
                    # 문장 내에서 틀린 단어를 새 단어로 교체 (대소문자 구분을 위해 패턴 사용)
                    corrected_text = re.sub(r'\b' + word + r'\b', correction, corrected_text, flags=re.IGNORECASE)
                    
                    report_data.append({
                        "번호": idx,
                        "기존 단어": f"❌ {word}",
                        "추천 단어": f"✅ {correction}",
                        "수정 이유": "철자(Spelling)가 올바르지 않습니다. 추천 단어를 확인하세요."
                    })
                
                # 교정된 최종 문장 출력
                st.markdown(f"### 📍 **교정된 문장:**")
                st.info(f"**{corrected_text}**")
                
                st.markdown("---")
                
                # 오류 수정 리포트 표 출력
                st.markdown("### 🔍 오류 수정 리포트")
                st.write(f"총 **{len(misspelled)}개**의 오류를 발견하여 수정했습니다.")
                st.table(report_data)
