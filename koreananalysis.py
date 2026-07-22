import streamlit as st
import re

# Page Config
st.set_page_config(
    page_title="Cognitive AI Care - 인지 스트레스 진단",
    page_icon="🧠",
    layout="centered"
)

# --- 뇌인지 언어학 기반 키워드 사전 ---
AMBIGUITY_WORDS = ['어떻게', '모르겠다', '막막', '아마도', '글쎄', '어쩌지', '혼란', '불안', '답답', '어렵다']
CAUSAL_WORDS = ['왜냐하면', '때문에', '인해서', '이유는', '결국', '바람에', '그래서', '탓']
PRONOUN_WORDS = ['나', '내가', '내', '나를', '나의', '나에게', '혼자']

def analyze_cognitive_state(text_list):
    full_text = " ".join(text_list)
    words = full_text.split()
    total_words = max(len(words), 1)

    # 1. 어휘 카운팅
    ambiguity_count = sum(len(re.findall(w, full_text)) for w in AMBIGUITY_WORDS)
    causal_count = sum(len(re.findall(w, full_text)) for w in CAUSAL_WORDS)
    pronoun_count = sum(len(re.findall(w, full_text)) for w in PRONOUN_WORDS)

    # 2. 비율 및 가중치 점수 계산
    ambiguity_score = (ambiguity_count / total_words) * 300
    causal_score = (causal_count / total_words) * 200
    pronoun_score = (pronoun_count / total_words) * 150
    length_penalty = min(20, len(full_text) * 0.05)  # 글이 길수록 세밀한 표출

    # 3. 종합 인지 스트레스 점수 (0~100점)
    raw_score = ambiguity_score * 0.45 + causal_score * 0.35 + pronoun_score * 0.20 + length_penalty
    final_score = round(min(100.0, max(10.0, raw_score)), 1)

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

st.subheader("📋 인지 상태 진단 질문지")
st.write("아래 5가지 질문에 대해 떠오르는 대로 편안하게 답을 적어주세요.")

with st.form("cognitive_form"):
    q1 = st.text_area("1. 최근 가장 어떻게 해결해야 할지 몰라 막막했던 상황은 무엇인가요?", height=100)
    q2 = st.text_area("2. 나를 힘들게 한 고민이 있다면, 그 일이 '왜' 일어났다고 생각하시나요?", height=100)
    q3 = st.text_area("3. 요즘 나 자신에 대해 가장 자주 하는 생각이나 혼잣말은 무엇인가요?", height=100)
    q4 = st.text_area("4. 다가오는 일정이나 미래를 생각할 때 드는 느낌을 적어주세요.", height=100)
    q5 = st.text_area("5. 지난 일주일 동안 머리가 가장 피곤하다고 느꼈던 순간은 언제인가요?", height=100)
    
    submit_button = st.form_submit_button("진단 결과 확인하기 🚀")

if submit_button:
    responses = [q1, q2, q3, q4, q5]
    if sum(len(r.strip()) for r in responses) < 20:
        st.warning("⚠️ 정확한 분석을 위해 각 질문에 최소 한 문장 이상 작성해 주세요!")
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
                st.write("현재 불확실한 상황에 대한 인지적 에너지 소모가 큽니다. 원인 분석을 잠시 내려놓고 뇌에 휴식을 제공해야 합니다.")
            elif score >= 40:
                st.warning("🟡 **주의 (인지적 피로 누적)**")
                st.write("상황을 통제하려는 경향과 인지적 스트레스가 점차 누적되고 있습니다.")
            else:
                st.success("🟢 **양호 (안정적인 인지 상태)**")
                st.write("현재 상황을 객관적이고 안정적으로 다스리고 있습니다.")

        # 지표별 수치 출력
        st.write("### 🔍 언어 패턴 지표 분석")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("모호성/불안 어휘", f"{results['ambiguity']}회")
        col_b.metric("인과관계 어휘", f"{results['causal']}회")
        col_c.metric("자아 대명사(나/내)", f"{results['pronoun']}회")

        st.info("💡 **뇌인지학적 해석:** 불확실성 어휘와 인과 어휘의 비율이 높을수록 뇌의 전두엽이 상황을 제어하려 과도한 에너지를 사용하고 있음을 의미합니다.")
