"""Agent 2: assesses the student's apparent eligibility from provided facts."""
from crewai import Agent, Task


def create_eligibility_agent(llm):
    return Agent(
        role="Student Eligibility Assessment Specialist",
        goal=(
            "Compare the student's stated academic record against the supplied criteria without "
            "fabricating marks, subjects, test scores, or eligibility rules."
        ),
        backstory=(
            "You are a cautious admissions assessor. You label each criterion as Met, Not Met, or "
            "Unknown / Not Demonstrated and explain what evidence supports the classification."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )


def create_eligibility_task(agent):
    return Task(
        description=(
            "Assess the student's apparent eligibility for the stated program.\n\n"
            "University: {university}\nProgram: {program}\nAdmission cycle: {admission_cycle}\n"
            "Student profile: {student_profile}\n"
            "Requirements supplied by the user: {admission_requirements}\n\n"
            "For every criterion you can identify, use only these labels: Met, Not Met, or Unknown / Not Demonstrated. "
            "Explain the evidence briefly. Do not guess conversions between grading systems. "
            "If official criteria are absent, do not give a definitive eligible/ineligible decision; "
            "give a preliminary assessment and list the missing facts."
        ),
        expected_output=(
            "A preliminary eligibility report with criterion-by-criterion status, evidence, uncertainties, and next steps."
        ),
        agent=agent,
        async_execution=True,
    )
