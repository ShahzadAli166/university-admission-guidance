import streamlit as st
from crew_manager import run_admission_assessment

st.set_page_config(
    page_title="University Admission Guidance",
    page_icon="🎓",
    layout="wide",
)

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 10% 0%, #e8f3ff 0, transparent 34%),
                linear-gradient(135deg, #f7f9ff 0%, #eef4fb 55%, #f8f5ff 100%);
}
.hero {
    padding: 1.6rem 1.8rem;
    border-radius: 22px;
    color: white;
    background: linear-gradient(120deg, #102a56, #1767a8 58%, #6847a5);
    box-shadow: 0 12px 32px rgba(24, 62, 120, .18);
    margin-bottom: 1.1rem;
}
.hero h1 { margin: 0; font-size: 2.15rem; }
.hero p { margin: .45rem 0 0; color: #e6f2ff; }
.panel {
    background: rgba(255,255,255,.88);
    border: 1px solid #dbe6f5;
    border-radius: 18px;
    padding: 1rem 1.2rem;
    margin-bottom: .9rem;
}
.small-note { color: #52647d; font-size: .92rem; }
div.stButton > button {
    border-radius: 12px;
    font-weight: 650;
    min-height: 2.8rem;
}
@media (max-width: 700px) {
    .hero { padding: 1.2rem; }
    .hero h1 { font-size: 1.6rem; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🎓 University Admission Guidance</h1>
  <p>Three specialist AI agents work in parallel to review requirements, assess eligibility, and suggest suitable programs.</p>
</div>
""", unsafe_allow_html=True)

st.warning(
    "This is an educational guidance tool, not an official admission decision. "
    "AI can make mistakes. Confirm every requirement on the university's official website."
)

with st.sidebar:
    st.header("⚙️ Assessment settings")
    st.caption("Your API key is stored in Streamlit Cloud Secrets, not in this code.")
    st.markdown("---")
    st.markdown("**Parallel agents**")
    st.write("1. Admission Requirements")
    st.write("2. Eligibility Assessment")
    st.write("3. Program Recommendation")
    st.markdown("---")
    st.caption("Tip: paste the university's official requirements below for a more grounded assessment.")

col_a, col_b = st.columns(2)
with col_a:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("👤 Student profile")
    student_name = st.text_input("Name (optional)", placeholder="e.g., Student")
    education_level = st.selectbox(
        "Current / completed qualification",
        ["Intermediate / HSSC", "A Levels", "Bachelor's degree", "DAE / Diploma", "Other"],
    )
    grades = st.text_area(
        "Grades, marks, GPA, subjects",
        placeholder="e.g., HSSC Pre-Engineering: 78%; Mathematics 82%, Physics 75%",
        height=110,
    )
    subjects = st.text_area(
        "Relevant subjects, tests, or other details (optional)",
        placeholder="e.g., entry test score, English test score, completed prerequisites",
        height=90,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🏛️ Target university and program")
    university = st.text_input("University / institution", placeholder="e.g., Example University")
    program = st.text_input("Program / degree", placeholder="e.g., BS Computer Science")
    admission_cycle = st.text_input("Admission cycle (optional)", placeholder="e.g., Fall 2027")
    admission_requirements = st.text_area(
        "Official admission requirements (strongly recommended)",
        placeholder=(
            "Paste eligibility criteria, minimum marks/GPA, required subjects, "
            "entry-test rules, deadlines, and any program-specific conditions."
        ),
        height=230,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with st.expander("How this system works"):
    st.write(
        "When you click Assess admission, three separate CrewAI tasks are launched as asynchronous "
        "tasks. They review the same supplied profile and requirements at the same time. "
        "The app then displays each result separately; it does not use a manager agent or a complex hierarchy."
    )

if st.button("✨ Assess admission and recommend programs", type="primary", use_container_width=True):
    missing = []
    if not grades.strip():
        missing.append("grades / marks / GPA")
    if not university.strip():
        missing.append("university name")
    if not program.strip():
        missing.append("target program")
    if missing:
        st.error("Please provide: " + ", ".join(missing) + ".")
    else:
        profile = (
            f"Name: {student_name.strip() or 'Not provided'}\n"
            f"Current/completed qualification: {education_level}\n"
            f"Grades, marks, GPA, subjects: {grades.strip()}\n"
            f"Other details: {subjects.strip() or 'Not provided'}"
        )
        with st.spinner("The three admission agents are working in parallel. This may take a minute..."):
            try:
                groq_api_key = st.secrets.get("GROQ_API_KEY", "")
                if not groq_api_key:
                    st.error("GROQ_API_KEY is missing. Open your Streamlit app settings → Secrets and add your Groq API key.")
                    st.stop()

                results = run_admission_assessment(
                    groq_api_key=groq_api_key,
                    student_profile=profile,
                    university=university.strip(),
                    program=program.strip(),
                    admission_cycle=admission_cycle.strip() or "Not specified",
                    admission_requirements=admission_requirements.strip() or
                        "No official requirements were supplied. Clearly label university-specific facts as unverified and do not invent exact cutoffs.",
                )
                st.session_state["admission_results"] = results
                st.session_state["admission_inputs"] = {
                    "university": university.strip(),
                    "program": program.strip(),
                }
            except Exception as exc:
                st.error(
                    "The assessment could not be completed. Check that GROQ_API_KEY is configured, "
                    "the model is available to your Groq account, and your API quota has not been exceeded."
                )
                with st.expander("Technical details (for troubleshooting)"):
                    st.code(str(exc))

if st.session_state.get("admission_results"):
    info = st.session_state.get("admission_inputs", {})
    st.markdown("---")
    st.header(f"📊 Assessment results: {info.get('university', '')}")
    st.caption(f"Target program: {info.get('program', '')}")
    st.info("The three agent reports are independent and may overlap. Treat uncertain items as questions to verify.")

    results = st.session_state["admission_results"]
    tabs = st.tabs([
        "📋 Requirements",
        "✅ Eligibility",
        "🧭 Program recommendation",
    ])
    labels = ["requirements", "eligibility", "recommendation"]
    for tab, key in zip(tabs, labels):
        with tab:
            st.markdown(results.get(key, "No result was returned for this section."))
    st.download_button(
        "Download assessment as text",
        data=(
            f"UNIVERSITY ADMISSION GUIDANCE\n\n"
            f"REQUIREMENTS REVIEW\n{results.get('requirements', '')}\n\n"
            f"ELIGIBILITY ASSESSMENT\n{results.get('eligibility', '')}\n\n"
            f"PROGRAM RECOMMENDATION\n{results.get('recommendation', '')}\n"
        ),
        file_name="admission_assessment.txt",
        mime="text/plain",
        use_container_width=True,
    )

st.markdown(
    '<p class="small-note">Privacy: the information you enter is sent to the configured Groq model for analysis. '
    'This starter app does not intentionally save student profiles to a database. Avoid entering national ID numbers, '
    'passwords, or other unnecessary sensitive information.</p>',
    unsafe_allow_html=True,
)
