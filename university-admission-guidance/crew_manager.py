"""Builds and runs the three parallel CrewAI admission tasks."""
from crewai import Crew, LLM, Process

from requirements_agent import create_requirements_agent, create_requirements_task
from eligibility_agent import create_eligibility_agent, create_eligibility_task
from program_recommender_agent import (
    create_program_recommender_agent,
    create_program_recommendation_task,
)


def run_admission_assessment(
    groq_api_key: str,
    student_profile: str,
    university: str,
    program: str,
    admission_cycle: str,
    admission_requirements: str,
) -> dict[str, str]:
    """Run three asynchronous CrewAI tasks and return their reports by section."""
    if not groq_api_key:
        raise RuntimeError("GROQ_API_KEY is missing from Streamlit Secrets.")

    # CrewAI uses LiteLLM to connect to Groq. The provider prefix is important.
    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=groq_api_key,
        temperature=0.1,
    )

    requirements_agent = create_requirements_agent(llm)
    eligibility_agent = create_eligibility_agent(llm)
    recommendation_agent = create_program_recommender_agent(llm)

    tasks = [
        create_requirements_task(requirements_agent),
        create_eligibility_task(eligibility_agent),
        create_program_recommendation_task(recommendation_agent),
    ]

    crew = Crew(
        agents=[requirements_agent, eligibility_agent, recommendation_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=False,
        memory=False,
    )

    result = crew.kickoff(
        inputs={
            "student_profile": student_profile,
            "university": university,
            "program": program,
            "admission_cycle": admission_cycle,
            "admission_requirements": admission_requirements,
        }
    )

    outputs = getattr(result, "tasks_output", []) or []
    text_outputs = [str(getattr(item, "raw", item)) for item in outputs]

    # Defensive fallback in case a CrewAI version returns only the final text.
    if len(text_outputs) < 3:
        combined = str(getattr(result, "raw", result))
        return {
            "requirements": combined,
            "eligibility": "Separate task output was not exposed by this CrewAI version. Review the combined report above.",
            "recommendation": "Separate task output was not exposed by this CrewAI version. Review the combined report above.",
        }

    return {
        "requirements": text_outputs[0],
        "eligibility": text_outputs[1],
        "recommendation": text_outputs[2],
    }
