# Changelog

This file records the development history of JobSniper.

## v0.1 - Minimal LLM Agent

### Goal
Build the first runnable AI agent prototype.

### Features
- Set up Python virtual environment.
- Connected to an LLM API through the OpenAI-compatible SDK.
- Sent a hardcoded job description prompt to the model.
- Printed the model response in the terminal.

### Notes
This version proved that the local Python environment, API key loading, and model call worked successfully.

---

## v0.2 - Resume Matching Agent

### Goal
Allow the agent to read local job descriptions and multiple resume versions.

### Features
- Added local file reading with `read_file()`.
- Added `JDs/jd.txt` as the job description input.
- Added multiple resume profiles:
  - SE
  - CSM
  - TAM
- Sent JD and resume content to the LLM.
- Asked the model to analyze resume-job fit, match score, missing keywords, ATS risks, and interview questions.

### Notes
This version turned the project from a simple prompt script into a resume matching workflow.

---

## v0.3 - Resume Router

### Goal
Reduce prompt length and avoid sending all resumes to the LLM by default.

### Features
- Added job title parsing from the first line of `JDs/jd.txt`.
- Added local job-title-based resume routing.
- Matched job titles to the most relevant resume profile:
  - SE
  - CSM
  - TAM
- Sent only the selected resume to the LLM for deeper analysis.
- Added fallback logic: if no local match is found, send all three resumes to the LLM for comparison.

### Notes
This version introduced local decision logic before calling the LLM, making the agent faster, cheaper, and more structured.

---
## v0.4 - Guardrailed Tailored Resume Generator

### Goal
Generate a JD-tailored resume draft while preventing hallucinated or exaggerated resume content.

### Features
- Generates Markdown resume package under `output/`.
- Creates a unique output folder for each run.
- Produces:
  - `tailored_resume.md`
  - `optimization_report.md`
  - `change_log.md`
  - `rejected_claims.md`
  - `questions_to_confirm.md`
- Adds resume rewrite guardrails:
  - Safe Rewrite
  - Needs Confirmation
  - Not Allowed
- Requires evidence from the original resume for each major rewrite.
- Separates unsafe or unsupported claims from the final resume draft.

### Notes
This version moves the project from analysis-only output to controlled resume generation with human review.
