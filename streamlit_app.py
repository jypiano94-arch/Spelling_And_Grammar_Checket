import streamlit as st
import urllib.request
import urllib.parse
import json

# 페이지 기본 설정
st.set_page_config(
    page_title="Grammar & Spelling Checker",
    page_icon="✨",
    layout="centered"
)

# 제목 및 상단 꾸미기
st.title('✨ 실시간 영문 문법 & 맞춤법 검사기 📝')
st.markdown("---")
st.write('**문맥상의 문법 오류와 철자**를 실시간으로 교정합니다.')

# 텍스트 입력 공간
text = st.text_area("✍️ 검사할 영문 텍스트를 입력하세요:", value='', height=150, placeholder="Example: I wants to do something excited.")

# 버튼 클릭 시 작동
if st.button('🚀 문장 교정하기', use_container_width=True):
    if text.strip() == '':
        st.warning('⚠️ 검사할 문장을 입력해 주세요!') 
    else: 
        with st.spinner('🎯 문장을 정밀 분석하는 중...'):
            try:
                # 외부 라이브러리 없이 무료 오픈소스 LanguageTool API 직접 호출 (자바 에러 우회)
                api_url = "https://api.languagetoolplus.com/v2/check"
                data = urllib.parse.urlencode({
                    'text': text,
                    'language': 'en-US'
                }).encode('utf-8')
                
                req = urllib.request.Request(api_url, data=data, headers={'User-Agent': 'Mozilla/5.0'})
                
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                
                matches = res_data.get('matches', [])
                
                # 1. 결과 출력 및 문장 교정 진행
                st.success('🎉 분석이 완료되었습니다!')
                
                corrected_text = text
                # 뒤에서부터 교정해야 문자열 인덱스가 뒤틀리지 않음
                for match in sorted(matches, key=lambda x: x['offset'], reverse=True):
                    if match['replacements']:
                        offset = match['offset']
                        length = match['length']
                        replacement = match['replacements'][0]['value']
                        corrected_text = corrected_text[:offset] + replacement + corrected_text[offset+length:]
                
                st.markdown(f"### 📍 **교정된 문장:**")
                st.info(f"**{corrected_text}**")
                
                st.markdown("---")
                
                # 2. 오류 수정 리포트 표 출력
                st.markdown("### 🔍 오류 수정 리포트")
                
                if not matches:
                    st.balloons()
                    st.success("✅ 완벽합니다! 문맥이나 문법상 오류가 발견되지 않았습니다.")
                else:
                    st.write(f"총 **{len(matches)}개**의 어색한 부분을 발견하여 수정했습니다.")
                    
                    report_data = []
                    for idx, match in enumerate(matches, 1):
                        offset = match['offset']
                        length = match['length']
                        bad_word = text[offset:offset+length]
                        good_word = match['replacements'][0]['value'] if match['replacements'] else "N/A"
                        
                        report_data.append({
                            "번호": idx,
                            "기존 표현": f"❌ {bad_word}",
                            "추천 표현": f"✅ {good_word}",
                            "수정 이유": match['message']
                        })
                    
                    st.table(report_data)
                    
            except Exception as e:
                st.error("❌ 분석 서버와 통신 중 에러가 발생했습니다. 잠시 후 다시 시도해 주세요.")
