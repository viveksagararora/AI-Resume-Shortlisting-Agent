import streamlit as st
import pandas as pd

from utils.parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from utils.embeddings import (
    get_embedding,
    cosine_similarity
)

from utils.scorer import (
    evaluate_candidate
)

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="AI Resume Shortlisting Agent",
    layout="wide"
)

st.title("🤖 AI Resume Shortlisting Agent")



# ---------------------------
# JOB DESCRIPTION INPUT
# ---------------------------

st.header("📄 Job Description")

jd_text = st.text_area(
    "Paste Job Description (Optional)"
)

jd_file = st.file_uploader(
    "OR Upload JD File",
    type=["pdf", "docx", "txt"]
)

# ---------------------------
# RESUME UPLOAD
# ---------------------------

st.header("📂 Upload Resumes")

uploaded_files = st.file_uploader(
    "Upload Resume Files",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

# ---------------------------
# SESSION STATE
# ---------------------------

if "processed" not in st.session_state:

    st.session_state.processed = False

# ---------------------------
# PROCESS BUTTON
# ---------------------------

if st.button("🚀 Process Resumes"):

    st.session_state.processed = True

# ---------------------------
# MAIN PROCESSING
# ---------------------------

if st.session_state.processed:

    extracted_jd = ""

    # ---------------------------
    # JD EXTRACTION
    # ---------------------------

    if jd_file:

        if jd_file.name.endswith(".pdf"):

            extracted_jd = extract_text_from_pdf(
                jd_file
            )

        elif jd_file.name.endswith(".docx"):

            extracted_jd = extract_text_from_docx(
                jd_file
            )

        elif jd_file.name.endswith(".txt"):

            extracted_jd = str(
                jd_file.read(),
                "utf-8"
            )

    elif jd_text.strip():

        extracted_jd = jd_text

    else:

        st.error(
            "Please paste or upload a Job Description."
        )

        st.stop()

    # ---------------------------
    # VALIDATE RESUMES
    # ---------------------------

    if not uploaded_files:

        st.error(
            "Please upload at least one resume."
        )

        st.stop()

    # ---------------------------
    # DISPLAY JD
    # ---------------------------

    st.subheader(
        "📄 Extracted Job Description"
    )

    st.text_area(
        "JD Content",
        extracted_jd,
        height=250
    )

    # ---------------------------
    # JD EMBEDDING
    # ---------------------------

    jd_embedding = get_embedding(
        extracted_jd
    )

    candidate_scores = []

    # ---------------------------
    # PROCESS RESUMES
    # ---------------------------

    for file in uploaded_files:

        st.divider()

        st.subheader(
            f"📄 Resume: {file.name}"
        )

        # ---------------------------
        # EXTRACT RESUME TEXT
        # ---------------------------

        if file.name.endswith(".pdf"):

            resume_text = extract_text_from_pdf(
                file
            )

        elif file.name.endswith(".docx"):

            resume_text = extract_text_from_docx(
                file
            )

        else:

            resume_text = "Unsupported format"

        # ---------------------------
        # RESUME EMBEDDING
        # ---------------------------

        resume_embedding = get_embedding(
            resume_text
        )

        # ---------------------------
        # SEMANTIC MATCH
        # ---------------------------

        similarity_score = cosine_similarity(
            jd_embedding,
            resume_embedding
        )

        match_percentage = round(
            similarity_score * 100,
            2
        )

        # ---------------------------
        # AI EVALUATION
        # ---------------------------

        with st.spinner(
            "Generating AI Evaluation..."
        ):

            evaluation = evaluate_candidate(
                extracted_jd,
                resume_text,
                match_percentage
            )

        total_score = evaluation.get(
            "total_score",
            0
        )

        recommendation = evaluation.get(
            "recommendation",
            "Unknown"
        )

        # ---------------------------
        # HR OVERRIDE
        # ---------------------------

        override_key = f"override_{file.name}"

        if override_key not in st.session_state:

            st.session_state[
                override_key
            ] = recommendation

        override = st.selectbox(

            f"HR Override - {file.name}",

            [
                "Hire",
                "Maybe",
                "Reject"
            ],

            key=override_key
        )

        recommendation = override

        # ---------------------------
        # OVERRIDE REASON
        # ---------------------------

        override_reason = ""

        if override != evaluation.get(
            "recommendation",
            "Unknown"
        ):

            override_reason = st.text_input(

                f"Reason for Override - {file.name}"
            )

        # ---------------------------
        # STORE DATA
        # ---------------------------

        candidate_scores.append({

            "Candidate Name":
            file.name,

            "Semantic Match %":
            match_percentage,

            # ---------------------------
            # RUBRIC BREAKDOWN
            # ---------------------------

            "Skills Match Score":
            evaluation["skills_match"]["score"],

            "Skills Justification":
            evaluation["skills_match"]["justification"],

            "Experience Relevance Score":
            evaluation["experience_relevance"]["score"],

            "Experience Justification":
            evaluation["experience_relevance"]["justification"],

            "Education Score":
            evaluation["education"]["score"],

            "Education Justification":
            evaluation["education"]["justification"],

            "Projects Score":
            evaluation["projects"]["score"],

            "Projects Justification":
            evaluation["projects"]["justification"],

            "Communication Score":
            evaluation["communication"]["score"],

            "Communication Justification":
            evaluation["communication"]["justification"],

            # ---------------------------
            # FINAL RESULTS
            # ---------------------------

            "AI Total Score":
            total_score,

            "Recommendation":
            recommendation,

            "Override Reason":
            override_reason
        })

        # ---------------------------
        # DISPLAY RESULTS
        # ---------------------------

        st.success(
            f"Semantic Match Score: {match_percentage}%"
        )

        st.metric(
            "AI Total Score",
            f"{total_score}/100"
        )

        st.info(
            f"Recommendation: {recommendation}"
        )

        # ---------------------------
        # RESUME TEXT
        # ---------------------------

        with st.expander(
            "View Extracted Resume Text"
        ):

            st.text_area(
                "Resume Content",
                resume_text,
                height=250
            )

        # ---------------------------
        # AI JSON
        # ---------------------------

        st.subheader(
            "🤖 AI Evaluation"
        )

        st.json(evaluation)

    # ---------------------------
    # FINAL RANKINGS
    # ---------------------------

    st.divider()

    st.header(
        "🏆 Candidate Rankings"
    )

    sorted_candidates = sorted(

        candidate_scores,

        key=lambda x:
        x["AI Total Score"],

        reverse=True
    )

    for idx, candidate in enumerate(

        sorted_candidates,

        start=1
    ):

        st.write(
            f"""
            {idx}. 
            {candidate['Candidate Name']}
            → AI Score:
            {candidate['AI Total Score']}/100
            | Semantic Match:
            {candidate['Semantic Match %']}%
            | Recommendation:
            {candidate['Recommendation']}
            """
        )

    # ---------------------------
    # EXPORT REPORT
    # ---------------------------

    st.divider()

    st.header(
        "📥 Export Shortlist Report"
    )

    report_df = pd.DataFrame(
        sorted_candidates
    )

    csv = report_df.to_csv(
        index=False
    )

    st.download_button(

        label="Download CSV Report",

        data=csv,

        file_name=
        "candidate_shortlist_report.csv",

        mime="text/csv"
    )