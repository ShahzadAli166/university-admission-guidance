"""Agent 3: suggests program options based on the supplied student profile."""
from crewai import Agent, Task


def create_program_recommender_agent(llm):
    return Agent(
        role="University Program Recommendation Adviser",
        goal=(
            "Suggest sensible program options aligned with the student's stated qualifications and interests, "
            "while separating suggestions from verified admission eligibility."
        ),
        backstory=(
            "You are a student guidance adviser. You explain why an option may fit, ask for missing preferences, "
            "and never claim that a university offers a program or that a student qualifies unless the input supports it."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )


def create_program_recommendation_task(agent):
    return Task(
        description=(
            "Recommend a short list of possible program directions for this student.\n\n"
            "Target university: {university}\nTarget program: {program}\n"
            "Admission cycle: {admission_cycle}\nStudent profile: {student_profile}\n"
            "Requirements supplied by the user: {admission_requirements}\n\n"
            "Include: (1) fit with the stated academic background, (2) the target program's apparent fit, "
            "(3) alternative program areas only when supported by the profile, (4) questions that would improve "
            "the recommendation, and (5) verification steps. Do not claim a program is offered by the named "
            "university unless the user-provided information establishes it. Label alternatives as ideas to research."
        ),
        expected_output=(
            "A concise recommendation report with reasons, uncertainties, questions, and verification steps."
        ),
        agent=agent,
        async_execution=True,
    )
