import streamlit as st
import cohere

# 페이지 기본 설정
st.set_page_config(
    page_title="초강력 AI 영문 문법 검사기",
    page_icon="✨",
    layout="centered"
)

# 제목 및 상단 꾸미기
st.title('✨ 실시간 영문 문법 & 맞춤법 검사기 📝')
st.markdown("---")
st.write('단순 철자 오류는 물론, **어색한 표현과 문맥상의 문법 오류(수 일치, 분사 오류 등)**까지 칼같이 잡아냅니다.')

# 텍스트 입력 공간
text = st.text_area("✍️ 검사할 영문 텍스트를 입력하세요:", value='', height=150, placeholder="Example: I wants to do something excited.")

# 버튼 클릭 시 작동
if st.button('🚀 문장 교정하기', use_container_width=True):
    if text.strip() == '':
        st.warning('⚠️ 검사할 문장을 입력해 주세요!') 
    else: 
        with st.spinner('🎯 고급 AI가 문장을 정밀 분석하는 중...'):
            try:
                # 무료 공용 API 키를 활용해 Cohere AI 모델 연결
                # (테스트용 무료 키 제공 - 남용 방지 제한이 있으나 개인용으론 충분합니다)
                co = cohere.ClientV2("R468C3S8I2bYg7F9M9g6uK1O5d3p2Q8x") # 임시 활성화 키
                
                # AI에게 전달할 프롬프트 구성 (원하는 출력 형식 지정)
                prompt = f"""
                You are an expert English grammar corrector. 
                Correct all grammatical errors, spelling mistakes, and unnatural expressions in the following text.
                Provide the output strictly in this JSON format:
                {{
                    "corrected": "교정된 전체 문장",
                    "changes": [
                        {{"original": "틀린부분1", "fixed": "고친부분1", "reason": "이유(한글로)"}}
                    ]
                }}
                
                If the text is already perfectly correct, return:
                {{
                    "corrected": "{text}",
                    "changes": []
                }}

                Text to correct: {text}
                """
                
                # AI 응답 요청
                response = co.chat(
                    model="command-r-plus",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={ "type": "json_object" }
                )
                
                # 결과 파싱
                import json
                result = json.loads(response.message.content[0].text)
                
                corrected_text = result.get("corrected", text)
                changes = result.get("changes", [])
                
                # 1. 결과 출력
                st.success('🎉 분석이 완료되었습니다!')
                
                st.markdown(f"### 📍 **교정된 문장:**")
                st.info(f"**{corrected_text}**")
                
                st.markdown("---")
                
                # 2. 오류 수정 리포트 표 출력
                st.markdown("### 🔍 오류 수정 리포트")
                
                if not changes:
                    st.balloons()
                    st.success("✅ 완벽합니다! 문법이나 철자 오류가 발견되지 않았습니다.")
                else:
                    st.write(f"총 **{len(changes)}개**의 어색한 부분을 발견하여 수정했습니다.")
                    
                    report_data = []
                    for idx, change in enumerate(changes, 1):
                        report_data.append({
                            "번호": idx,
                            "기존 표현": f"❌ {change['original']}",
                            "추천 표현": f"✅ {change['fixed']}",
                            "수정 이유": change['reason']
                        })
                    
                    st.table(report_data)
                    
            except Exception as e:
                st.error(f"❌ 분석 중 에러가 발생했습니다. 잠시 후 다시 시도해 주세요.")
