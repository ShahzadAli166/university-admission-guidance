"""Agent 1: reviews the supplied admission requirements."""
from crewai import Agent, Task


def create_requirements_agent(llm):
    return Agent(
        role="University Admission Requirements Reviewer",
        goal=(
            "Organize the admission criteria supplied by the user and identify which requirements "
            "need verification from official university sources."
        ),
        backstory=(
            "You are a careful admissions information assistant. You distinguish supplied facts "
            "from assumptions, never invent deadlines or cutoffs, and explicitly flag missing information."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )


def create_requirements_task(agent):
    return Task(
        description=(
            "Review the supplied university and program details.\n\n"
            "University: {university}\nProgram: {program}\nAdmission cycle: {admission_cycle}\n"
            "Student profile: {student_profile}\n"
            "Requirements supplied by the user: {admission_requirements}\n\n"
            "Produce: (1) a concise checklist of the requirements actually supplied, "
            "(2) which requirements appear satisfied based only on the profile, "
            "(3) which items are missing or unclear, and (4) what must be checked on the official website. "
            "Do not invent official requirements. If no requirements were supplied, state that clearly."
        ),
        expected_output=(
            "A structured requirements checklist with supplied facts, unclear items, and official verification steps."
        ),
        agent=agent,
        async_execution=True,
    )
