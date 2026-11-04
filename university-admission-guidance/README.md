# University Admission Guidance — Parallel Multi-Agent System

A beginner-friendly Streamlit application using CrewAI and Groq. Three specialist tasks review the same student profile in parallel:

1. **Requirements reviewer** — organizes requirements supplied by the user and flags what needs official verification.
2. **Eligibility assessor** — compares the student's stated record against supplied requirements.
3. **Program adviser** — suggests program directions and explains uncertainties.

There is no manager agent and no hierarchical process. Each task is marked `async_execution=True`, so CrewAI can execute the specialist tasks concurrently. The app displays the three reports separately.

## Important limitations

- This is guidance, not an official admission decision.
- The app does not independently browse university websites. Paste current requirements from the institution's official website for a more grounded review.
- The model may make mistakes. Verify deadlines, test rules, subject prerequisites, cutoffs, and program availability with the university.
- The app does not intentionally store profiles in a database. Inputs are sent to the configured Groq model for analysis.

## Files

- `app.py` — Streamlit interface and input validation.
- `requirements_agent.py` — requirements review agent and task.
- `eligibility_agent.py` — eligibility assessment agent and task.
- `program_recommender_agent.py` — program recommendation agent and task.
- `crew_manager.py` — configures Groq LLM, creates the crew, runs tasks, and returns results.
- `requirements.txt` — package dependencies.
- `.streamlit/secrets.toml.example` — example only; never add a real key here.
- `.gitignore` — excludes secret files and Python cache files.

## Deploy directly from GitHub to Streamlit Community Cloud

No local Python installation or terminal is required.

### 1. Create the GitHub repository

1. Sign in to GitHub and choose **New repository**.
2. Name it `university-admission-guidance`.
3. Choose Public or Private, then create the repository.
4. In the repository, click **Add file → Create new file**.
5. Create each file listed above, keeping the filenames and code exactly as provided.
6. For `.streamlit/secrets.toml.example`, enter that path as the filename; GitHub will create the folder.
7. Commit each file to the repository.

### 2. Create a Groq API key

1. Sign in to the Groq Console: https://console.groq.com/
2. Create an API key.
3. Treat the key like a password. Do not put it in `app.py`, `crew_manager.py`, GitHub, screenshots, or public messages.

### 3. Deploy to Streamlit Community Cloud

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Select **Create app**.
3. Choose the repository `university-admission-guidance`, branch `main`, and main file path `app.py`.
4. Open **Advanced settings** if needed and select Python 3.12 (or another version supported by the selected CrewAI release; avoid Python 3.14).
5. In the **Secrets** box, paste:
   ```toml
   GROQ_API_KEY = "your_actual_groq_api_key"
   ```
6. Click **Deploy** and wait for dependency installation to finish.
7. If deployment fails, open **Manage app → Logs** and inspect the first installation error.

The app reads the key directly using `st.secrets.get("GROQ_API_KEY")`. Do not commit a real secrets file.

### 4. Update the app later

1. Open the relevant file in GitHub.
2. Click the pencil icon to edit.
3. Make the change and click **Commit changes**.
4. Streamlit Community Cloud usually detects the commit and redeploys the app.

## Dependencies and provider setup

The dependency ranges are bounded to avoid unbounded upgrades. CrewAI's Groq connection uses its LiteLLM integration, included through `crewai[litellm]`. The model identifier is `groq/openai/gpt-oss-120b`.

If the selected model is unavailable to your Groq account, check the current model list and access in the Groq Console before changing code. If a provider integration error occurs, check the CrewAI LLM connection documentation and the deployment logs.

## Troubleshooting

| Problem | What to check |
|---|---|
| Missing `GROQ_API_KEY` | Add it under Streamlit app settings → Secrets, then reboot/redeploy. |
| Model not available / model error | Confirm `openai/gpt-oss-120b` is available to your Groq account. |
| Rate limit or quota error | Wait and retry, or review the Groq account's limits. Three parallel tasks may create concurrent requests. |
| `No module named ...` | Confirm `requirements.txt` is in the repository root and inspect dependency installation logs. |
| Requirements resolution error | Keep the bounded requirements ranges; check the first failing package in the build log. |
| Eligibility result seems too certain | Supply official requirements and treat unknown criteria as unverified. Always confirm with admissions staff. |

## Beginner checklist

- [ ] All source files are committed to GitHub.
- [ ] No real API key appears in the repository.
- [ ] `GROQ_API_KEY` is configured in Streamlit Secrets.
- [ ] The app entry point is `app.py`.
- [ ] Python is set to a CrewAI-supported version, such as 3.12.
- [ ] Official university criteria are pasted for the test assessment.
- [ ] Results are verified against the university's official admission page.
