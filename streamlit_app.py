import streamlit as st
import language_tool_python

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 맞춤법 & 문법 검사기",
    page_icon="✨",
    layout="centered"
)

# 제목 및 상단 꾸미기
st.title('✨ 실시간 영문 맞춤법 & 문법 검사기 📝')
st.markdown("---")
st.write('텍스트를 입력하시면 AI가 잘못된 문법과 철자를 바로잡고 그 **이유**까지 상세히 설명해 드립니다.')

# 텍스트 입력 공간
text = st.text_area("✍️ 검사할 영문 텍스트를 입력하세요:", value='', height=150, placeholder="Example: He go to school yesterday.")

# 버튼 클릭 시 작동
if st.button('🚀 문장 교정하기', use_container_width=True):
    if text.strip() == '':
        st.warning('⚠️ 검사할 문장을 입력해 주세요!') 
    else: 
        with st.spinner('🎯 문법 및 철자 오류를 분석하는 중...'):
            try:
                # LanguageTool 엔진 초기화 (영어 설정)
                tool = language_tool_python.LanguageTool('en-US')
                
                # 분석 실행
                matches = tool.check(text)
                
                # 교정된 문장 생성
                corrected_sentence = tool.correct(text)
                
                # 1. 결과 문장 출력
                st.success('🎉 교정이 완료되었습니다!')
                st.markdown(f"### 📍 **교정된 문장:**")
                st.info(f"**{corrected_sentence}**")
                
                st.markdown("---")
                
                # 2. 틀린 부분 및 이유 제공
                st.markdown("### 🔍 오류 수정 리포트")
                
                if not matches:
                    st.balloons()
                    st.success("✅ 완벽합니다! 문법이나 철자 오류가 발견되지 않았습니다.")
                else:
                    st.write(f"총 **{len(matches)}개**의 오류를 발견하여 수정했습니다.")
                    
                    report_data = []
                    for idx, match in enumerate(matches, 1):
                        # 원래 단어 (텍스트 슬라이싱으로 추출)
                        original_word = text[match.offset:match.offset + match.errorLength]
                        
                        # 추천 단어들 중 첫 번째 선택
                        suggestion = match.replacements[0] if match.replacements else "N/A"
                        
                        # 수정 이유 (한글 번역 및 가독성 개선)
                        reason = match.message
                        
                        report_data.append({
                            "번호": idx,
                            "기존 단어": f"❌ {original_word}",
                            "추천 단어": f"✅ {suggestion}",
                            "수정 이유 (영문)": reason
                        })
                    
                    # 테이블(표) 형태로 가독성 있게 화면에 출력
                    st.table(report_data)
                    
                    # 사용 완료 후 툴 닫기
                    tool.close()
                    
            except Exception as e:
                st.error(f"❌ 분석 중 에러가 발생했습니다: {e}")
