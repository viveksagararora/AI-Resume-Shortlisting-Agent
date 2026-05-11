def evaluate_candidate(
    jd,
    resume_text,
    semantic_score
):

    resume_lower = resume_text.lower()

    # ---------------------------
    # RUBRIC SCORES
    # ---------------------------

    # Skills Match (30%)

    if semantic_score >= 85:
        skills_score = 10

    elif semantic_score >= 70:
        skills_score = 8

    elif semantic_score >= 50:
        skills_score = 6

    else:
        skills_score = 3

    # Experience Relevance (25%)

    experience_keywords = [
        "intern",
        "experience",
        "developer",
        "engineer",
        "project"
    ]

    exp_matches = sum(
        keyword in resume_lower
        for keyword in experience_keywords
    )

    if exp_matches >= 4:
        experience_score = 9

    elif exp_matches >= 2:
        experience_score = 7

    else:
        experience_score = 4

    # Education & Certifications (15%)

    education_keywords = [
        "b.tech",
        "computer science",
        "ai",
        "machine learning",
        "certification"
    ]

    edu_matches = sum(
        keyword in resume_lower
        for keyword in education_keywords
    )

    if edu_matches >= 3:
        education_score = 9

    elif edu_matches >= 2:
        education_score = 7

    else:
        education_score = 5

    # Projects / Portfolio (20%)

    project_keywords = [
        "project",
        "github",
        "streamlit",
        "tensorflow",
        "flask",
        "deployment"
    ]

    proj_matches = sum(
        keyword in resume_lower
        for keyword in project_keywords
    )

    if proj_matches >= 4:
        projects_score = 9

    elif proj_matches >= 2:
        projects_score = 7

    else:
        projects_score = 4

    # Communication Quality (10%)

    if len(resume_text.split()) > 350:
        communication_score = 8

    elif len(resume_text.split()) > 200:
        communication_score = 7

    else:
        communication_score = 5

    # ---------------------------
    # WEIGHTED TOTAL
    # ---------------------------

    total_score = (

        skills_score * 0.30 * 10 +

        experience_score * 0.25 * 10 +

        education_score * 0.15 * 10 +

        projects_score * 0.20 * 10 +

        communication_score * 0.10 * 10
    )

    total_score = round(total_score, 2)

    # ---------------------------
    # FINAL RECOMMENDATION
    # ---------------------------

    if total_score >= 70 and semantic_score >= 80:

        recommendation = "Hire"

    elif total_score >= 55 and semantic_score >= 70:

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
            "Calculated using semantic similarity with job description."
        },

        "experience_relevance": {

            "score": experience_score,

            "justification":
            "Relevant experience and domain keywords detected."
        },

        "education": {

            "score": education_score,

            "justification":
            "Education background and certifications evaluated."
        },

        "projects": {

            "score": projects_score,

            "justification":
            "Portfolio and technical projects assessed."
        },

        "communication": {

            "score": communication_score,

            "justification":
            "Resume structure and content quality evaluated."
        },

        "total_score": total_score,

        "recommendation": recommendation
    }
