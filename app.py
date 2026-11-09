import streamlit as st
from detector import analyse_text, analyse_url

st.set_page_config(page_title="ShieldAI | Scam Detector", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.main {max-width: 1050px; padding-top: 2rem;}
.hero {padding: 1.4rem 1.6rem; border: 1px solid rgba(128,128,128,.25); border-radius: 18px; margin-bottom: 1.2rem;}
.small-muted {color: #8b949e; font-size: .92rem;}
.result {padding: 1rem 1.2rem; border-radius: 14px; border: 1px solid rgba(128,128,128,.25);}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🛡️ ShieldAI</h1><h3>AI-assisted phishing & scam detector</h3><p class="small-muted">An educational prototype that checks suspicious messages and URLs, explains warning signs, and gives a risk estimate.</p></div>', unsafe_allow_html=True)

tab_msg, tab_url, tab_about = st.tabs(["✉️ Check a message", "🔗 Check a URL", "ℹ️ About the project"])

with tab_msg:
    st.subheader("Paste an email, SMS, or chat message")
    message = st.text_area("Message to analyse", height=190, placeholder="Example: Your account is suspended. Verify immediately at ...")
    if st.button("Analyse message", type="primary", key="msg"):
        if not message.strip():
            st.warning("Paste a message first.")
        else:
            result = analyse_text(message)
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("Estimated risk", f"{result['score']}/100")
                st.progress(result["score"] / 100)
                st.error("High risk") if result["score"] >= 65 else st.warning("Use caution") if result["score"] >= 35 else st.success("Lower risk")
            with c2:
                st.markdown("**Assessment**")
                st.write(result["summary"])
                st.markdown("**Signals found**")
                if result["signals"]:
                    for signal in result["signals"]:
                        st.write("• " + signal)
                else:
                    st.write("No obvious warning signs were detected by this prototype.")
            st.caption("This is a heuristic estimate, not proof that a message is safe or fraudulent.")

with tab_url:
    st.subheader("Inspect a website address")
    url = st.text_input("Website URL", placeholder="https://example.com")
    if st.button("Check URL", type="primary", key="url"):
        if not url.strip():
            st.warning("Enter a URL first.")
        else:
            result = analyse_url(url)
            c1, c2 = st.columns([1, 2])
            with c1:
                st.metric("Estimated risk", f"{result['score']}/100")
                st.progress(result["score"] / 100)
                st.error("High risk") if result["score"] >= 65 else st.warning("Use caution") if result["score"] >= 35 else st.success("Lower risk")
            with c2:
                st.markdown("**Assessment**")
                st.write(result["summary"])
                st.markdown("**Signals found**")
                if result["signals"]:
                    for signal in result["signals"]:
                        st.write("• " + signal)
                else:
                    st.write("No obvious URL warning signs were detected.")
            st.caption("The app does not visit the URL, scan its content, or verify domain ownership.")

with tab_about:
    st.subheader("How this prototype works")
    st.write("ShieldAI uses transparent, explainable rules to flag common scam patterns such as urgency, requests for passwords or OTPs, suspicious payment demands, URL shorteners, misleading URL structure, and unusual domain patterns.")
    st.write("The current version is a safe local prototype. It does not submit your text or URLs to an external service.")
    st.info("Important: a low score does not guarantee safety. Never share passwords, OTPs, banking PINs, or recovery codes. Verify important requests through an official app or phone number.")
    st.markdown("**Suggested next upgrades**")
    st.write("1. Train and evaluate a text classifier on a properly licensed, balanced dataset.")
    st.write("2. Add domain-age and reputation checks using trusted threat-intelligence APIs.")
    st.write("3. Add a feedback button and measure precision, recall, and false-positive rate.")

st.divider()
st.caption("ShieldAI • Student project prototype • Python + Streamlit")
