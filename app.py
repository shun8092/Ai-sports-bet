
import streamlit as st

st.set_page_config(page_title="AI 運彩預測", layout="centered")
st.title("🤖 AI 運彩預測工具")
st.markdown("---")

sport = st.selectbox("選擇運動類型", ["⚽ 足球", "🏀 籃球"])

st.subheader("請輸入賠率（歐賠格式）")
col1, col2, col3 = st.columns(3)

with col1:
    odd_home = st.number_input("主勝賠率", min_value=1.0, step=0.01, value=1.85)
with col2:
    odd_draw = st.number_input("和局賠率", min_value=1.0, step=0.01, value=3.40)
with col3:
    odd_away = st.number_input("客勝賠率", min_value=1.0, step=0.01, value=4.20)

st.markdown("---")

def implied_prob(odd):
    return 1 / odd if odd > 0 else 0

total_inverse = implied_prob(odd_home) + implied_prob(odd_draw) + implied_prob(odd_away)
h_prob = implied_prob(odd_home) / total_inverse
d_prob = implied_prob(odd_draw) / total_inverse
a_prob = implied_prob(odd_away) / total_inverse

def expected_value(prob, odd):
    return round(prob * odd - 1, 2)

st.subheader("AI 分析結果：")
st.write(f"🔹 主勝預測勝率：約 {h_prob*100:.1f}% ，期望值 EV = {expected_value(h_prob, odd_home)}")
st.write(f"🔹 和局預測勝率：約 {d_prob*100:.1f}% ，期望值 EV = {expected_value(d_prob, odd_draw)}")
st.write(f"🔹 客勝預測勝率：約 {a_prob*100:.1f}% ，期望值 EV = {expected_value(a_prob, odd_away)}")

best_option = max([
    ("主勝", expected_value(h_prob, odd_home)),
    ("和局", expected_value(d_prob, odd_draw)),
    ("客勝", expected_value(a_prob, odd_away))
], key=lambda x: x[1])

if best_option[1] > 0:
    st.success(f"✅ 建議下注：{best_option[0]}（期望值 {best_option[1]}）")
else:
    st.warning("⚠️ 所有選項期望值為負，建議跳過此場比賽")

st.markdown("---")
st.caption("本工具為輔助預測，請搭配理性判斷與資金控管。")
