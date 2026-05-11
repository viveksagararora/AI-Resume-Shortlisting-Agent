def evaluate_candidate(
    jd,
    resume_text,
    semantic_score
):

    resume_lower = resume_text.lower()

    # ---------------------------
    # SKILLS SCORE (30%)
    # ---------------------------

    skills_score = 5

    skills = [
        "python",
        "machine learning",
        "tensorflow",
        "pytorch",
        "sql",
        "nlp",
        "llm",
        "streamlit"
    ]

    matched_skills = 0

    for skill in skills:

        if skill in resume_lower:

            matched_skills += 1

    skills_score += min(matched_skills, 5)

    skills_score = min(skills_score, 10)

    # ---------------------------
    # EXPERIENCE SCORE (25%)
    # ---------------------------

    experience_keywords = [
        "internship",
        "experience",
        "worked",
        "developed",
        "implemented",
        "project"
    ]

    exp_matches = 0

    for word in experience_keywords:

        if word in resume_lower:

            exp_matches += 1

    experience_score = min(5 + exp_matches, 10)

    # ---------------------------
    # EDUCATION SCORE (15%)
    # ---------------------------

    education_score = 7

    if "b.tech" in resume_lower:
        education_score += 1

    if "ai" in resume_lower or "ml" in resume_lower:
        education_score += 1

    education_score = min(education_score, 10)

    # ---------------------------
    # PROJECT SCORE (20%)
    # ---------------------------

    project_keywords = [
        "project",
        "github",
        "deployment",
        "model",
        "application"
    ]

    proj_matches = 0

    for word in project_keywords:

        if word in resume_lower:

            proj_matches += 1

    projects_score = min(5 + proj_matches, 10)

    # ---------------------------
    # COMMUNICATION SCORE (10%)
    # ---------------------------

    communication_score = 7

    if len(resume_text.split()) > 300:
        communication_score += 1

    communication_score = min(
        communication_score,
        10
    )

    # ---------------------------
    # WEIGHTED TOTAL SCORE
    # ---------------------------

    total_score = (

        (skills_score * 0.30) +

        (experience_score * 0.25) +

        (education_score * 0.15) +

        (projects_score * 0.20) +

        (communication_score * 0.10)

    ) * 10

    # Blend semantic score slightly
    total_score = (total_score * 0.65) + (
        semantic_score * 0.35
    )

    total_score = round(total_score, 2)

    # ---------------------------
    # RECOMMENDATION
    # ---------------------------

    if total_score >= 65 and semantic_score >= 80:

        recommendation = "Hire"

    elif total_score >= 50 and semantic_score >= 65:

        recommendation = "Maybe"

    else:

        recommendation = "Reject"

    # ---------------------------
    # RETURN JSON
    # ---------------------------

    return {

        "skills_match": {

            "score": skills_score,

            "justification":
            f"{matched_skills} relevant technical skills detected"
        },

        "experience_relevance": {

            "score": experience_score,

            "justification":
            "Relevant practical and internship exposure"
        },

        "education": {

            "score": education_score,

            "justification":
            "Strong academic background"
        },

        "projects": {

            "score": projects_score,

            "justification":
            "Relevant project work detected"
        },

        "communication": {

            "score": communication_score,

            "justification":
            "Resume clarity and structure evaluated"
        },

        "total_score": total_score,

        "recommendation": recommendation
    }