import streamlit as st
import re

# Page Config
st.set_page_config(
    page_title="Cognitive AI Care - 인지 스트레스 진단",
    page_icon="🧠",
    layout="centered"
)

# --- 뇌인지 언어학 기반 확장 키워드 사전 (어간/어근 중심) ---
# 어미 변화(활용)에 상관없이 감지할 수 있도록 어간 패턴으로 확장
AMBIGUITY_WORDS = [
    '모르', '불안', '막막', '어떻', '어쩌', '혼란', '글쎄', '답답', '아마', 
    '망설', '확신', '의문', '걱정', '아득', '막연', '복잡', '혹시', '모호', 
    '어렴풋', '두렵', '주저', '겁나', '위태', '초조', '지침', '피곤'
]

CAUSAL_WORDS = [
    '때문', '왜냐', '인해', '이유', '바람에', '결국', '그래서', '탓', 
    '원인', '비롯', '계기', '의해', '덕분', '이로', '따라', '근거', '자초'
]

PRONOUN_WORDS = ['나', '내', '혼자', '스스로', '저', '자신']

def analyze_cognitive_state(text_list):
    full_text = " ".join(text_list)
    words = full_text.split()
    total_words = max(len(words), 1)

    # 1. 어간/키워드 패턴 매칭
    ambiguity_count = sum(len(re.findall(w, full_text)) for w in AMBIGUITY_WORDS)
    causal_count = sum(len(re.findall(w, full_text)) for w in CAUSAL_WORDS)
    pronoun_count = sum(len(re.findall(w, full_text)) for w in PRONOUN_WORDS)

    # 2. 어휘 밀도(Density) 기반 점수 산출 (전체 어절 대비 비중)
    ambiguity_density = (ambiguity_count / total_words) * 100
    causal_density = (causal_count / total_words) * 100
    pronoun_density = (pronoun_count / total_words) * 100

    # 3. 종합 인지 스트레스 점수 계산 (0~100점 보정)
    raw_score = (ambiguity_density * 40) + (causal_density * 35) + (pronoun_density * 25)
    final_score = round(min(100.0, max(10.0, raw_score * 1.5)), 1)

    return {
        'score': final_score,
        'ambiguity': ambiguity_count,
        'causal': causal_count,
        'pronoun': pronoun_count,
        'total_words': total_words
    }

# --- UI 레이아웃 ---
st.title("🧠 인지 언어 기반 스트레스 진단")
st.caption("뇌인지과학과 자연어 처리(NLP) 기술을 결합하여, 당신의 언어 패턴 속에 숨겨진 인지적 피로도를 분석합니다.")
st.markdown("---")

# 📝 작성 가이드 박스 추가
st.info("""
📌 **답변 작성 규칙 안내**
* **문장 수:** 질문 하나당 **딱 2문장**으로 작성해 주세요.
* **문장 길이:** 각 문장은 **5어절 내외**로 길지 않게 작성해 주세요.
* **말투 어조:** 문장 끝은 **'-다'**로 마치되, 혼잣말이나 상황을 털어놓듯 써주세요.
* 💡 **작성 예시:** *"요즘엔 불안한 일들도 많아서 앞으로가 어떨지 잘 모르겠다. 마음을 다잡으려고 해도 생각대로 잘 되지 않는다."*
""")

st.subheader("📋 인지 상태 진단 질문지")

with st.form("cognitive_form"):
    q1 = st.text_area("1. 최근 가장 어떻게 해결해야 할지 몰라 막막했던 상황은 무엇인가요?", height=90, placeholder="예시 말투를 참고하여 2문장으로 적어주세요.")
    q2 = st.text_area("2. 나를 힘들게 한 고민이 있다면, 그 일이 '왜' 일어났다고 생각하시나요?", height=90)
    q3 = st.text_area("3. 요즘 나 자신에 대해 가장 자주 하는 생각이나 혼잣말은 무엇인가요?", height=90)
    q4 = st.text_area("4. 다가오는 일정이나 미래를 생각할 때 드는 느낌을 적어주세요.", height=90)
    q5 = st.text_area("5. 지난 일주일 동안 머리가 가장 피곤하다고 느꼈던 순간은 언제인가요?", height=90)
    
    submit_button = st.form_submit_button("진단 결과 확인하기 🚀")

if submit_button:
    responses = [q1, q2, q3, q4, q5]
    total_length = sum(len(r.strip()) for r in responses)
    
    if total_length < 15:
        st.warning("⚠️ 정확한 분석을 위해 각 질문에 규칙에 맞는 문장을 입력해 주세요!")
    else:
        results = analyze_cognitive_state(responses)
        score = results['score']

        st.markdown("---")
        st.subheader("📊 인지 스트레스 진단 결과")

        # 점수 카드 및 상태 표시
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric(label="종합 인지 스트레스 지수", value=f"{score}점")
        
        with col2:
            if score >= 70:
                st.error("🔴 **고위험 (인지적 과부하 상태)**")
                st.write("현재 불확실한 상황에 대한 인지적 에너지 소모가 매우 큽니다. 원인 분석을 잠시 내려놓고 휴식을 취하세요.")
            elif score >= 40:
                st.warning("🟡 **주의 (인지적 피로 누적)**")
                st.write("상황을 통제하려는 경향과 인지적 스트레스가 점차 누적되고 있습니다.")
            else:
                st.success("🟢 **양호 (안정적인 인지 상태)**")
                st.write("현재 상황을 객관적이고 안정적으로 다스리고 있습니다.")

        # 지표별 수치 출력
        st.write("### 🔍 언어 패턴 지표 분석")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("모호성/불안 어휘 감지", f"{results['ambiguity']}회")
        col_b.metric("인과관계 어휘 감지", f"{results['causal']}회")
        col_c.metric("자아 대명사 감지", f"{results['pronoun']}회")

        st.caption(f"총 작성 어절 수: {results['total_words']}어절")
        st.info("💡 **뇌인지학적 해석:** 불확실성 어휘와 인과 어휘의 비율이 높을수록 뇌의 전두엽이 상황을 제어하려 과도한 에너지를 사용하고 있음을 의미합니다.")
