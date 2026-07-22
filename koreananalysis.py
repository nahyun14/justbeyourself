import streamlit as st
import re

# Page Config
st.set_page_config(
    page_title="Cognitive AI Care - 인지 스트레스 진단",
    page_icon="🧠",
    layout="centered"
)

# --- 뇌인지 언어학 기반 확장 키워드 사전 (어간/어근 중심) ---
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

    ambiguity_count = sum(len(re.findall(w, full_text)) for w in AMBIGUITY_WORDS)
    causal_count = sum(len(re.findall(w, full_text)) for w in CAUSAL_WORDS)
    pronoun_count = sum(len(re.findall(w, full_text)) for w in PRONOUN_WORDS)

    ambiguity_density = (ambiguity_count / total_words) * 100
    causal_density = (causal_count / total_words) * 100
    pronoun_density = (pronoun_count / total_words) * 100

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

st.info("""
📌 **답변 작성 규칙 안내**
* **문장 수:** 질문 하나당 **딱 2문장**으로 작성해 주세요.
* **문장 길이:** 각 문장은 **5어절 내외**로 길지 않게 작성해 주세요.
* **말투 어조:** 문장 끝은 **'-다'**로 마치되, 혼잣말이나 상황을 털어놓듯 써주세요.
* 💡 **작성 예시:** *"요즘엔 불안한 일들도 많아서 앞으로가 어떨지 잘 모르겠다. 마음을 다잡으려고 해도 생각대로 잘 되지 않는다."*
""")

st.subheader("📋 인지 상태 진단 질문지")

with st.form("cognitive_form"):
    q1 = st.text_area(
        "1. 요즘 들어 이상하게 내 뜻대로 잘 풀리지 않거나 자꾸 손에 안 잡히는 일이 있나요?", 
        height=90, 
        placeholder="예: 요즘엔 공부를 하려고 앉아도 집중이 잘 안되고 자꾸 딴생각이 든다. 마음을 다잡으려고 해도 어떻게 해야 할지 잘 모르겠다."
    )
    q2 = st.text_area(
        "2. 최근 내 기분이나 일상 패턴을 갑자기 흔들어 놓았던 계기나 사건이 있나요?", 
        height=90,
        placeholder="예: 지난주에 친구와 작은 오해가 생기는 바람에 마음이 많이 불편해졌다. 신경을 쓰다 보니 결국 잠도 제대로 못 잤다."
    )
    q3 = st.text_area(
        "3. 최근 있었던 일 중에서 '내가 그때 다르게 행동했다면 어땠을까' 하고 남는 아쉬움이 있나요?", 
        height=90,
        placeholder="예: 그때 내가 조금만 더 참았으면 일이 이렇게 커지지 않았을 텐데 아쉽다. 내 고집 때문에 상황을 망친 것 같아 후회가 된다."
    )
    q4 = st.text_area(
        "4. 조만간 결과를 확인해야 하거나 맞이해야 할 커다란 변화를 앞두고 어떤 생각이 드나요?", 
        height=90,
        placeholder="예: 다가오는 시험 결과를 기다리고 있는데 마음이 편치 않다. 과연 준비한 만큼 결과가 잘 나올지 아직은 확신이 안 선다."
    )
    q5 = st.text_area(
        "5. 최근 에너지를 한꺼번에 쏟아붓고 나중에 긴 피로감이나 잔상이 남았던 순간은 언제인가요?", 
        height=90,
        placeholder="예: 지난 과제를 끝내느라 밤을 새우는 바람에 정신적으로 너무 지쳤다. 쉬고 난 뒤에도 여전히 머리가 멍하고 피곤함이 남아있다."
    )
    
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

        st.write("### 🔍 언어 패턴 지표 분석")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("모호성/불안 어휘 감지", f"{results['ambiguity']}회")
        col_b.metric("인과관계 어휘 감지", f"{results['causal']}회")
        col_c.metric("자아 대명사 감지", f"{results['pronoun']}회")

        st.caption(f"총 작성 어절 수: {results['total_words']}어절")
        st.info("💡 **뇌인지학적 해석:** 불확실성 어휘와 인과 어휘의 비율이 높을수록 뇌의 전두엽이 상황을 제어하려 과도한 에너지를 사용하고 있음을 의미합니다.")
