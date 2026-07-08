# 📝 Changelog

This file records the development history of **JobSniper**.

---

## 🐣 v0.1 - Minimal LLM Agent

### 🎯 Goal

Build the first runnable AI agent prototype.

### ✨ Features

- Set up Python virtual environment.
- Connected to an LLM API through the OpenAI-compatible SDK.
- Sent a hardcoded job description prompt to the model.
- Printed the model response in the terminal.

### 🧩 Notes

This version proved that the local Python environment, API key loading, and model call worked successfully.

---

## 📄 v0.2 - Resume Matching Agent

### 🎯 Goal

Allow the agent to read local job descriptions and multiple resume versions.

### ✨ Features

- Added local file reading with `read_file()`.
- Added `JDs/jd.txt` as the job description input.
- Added multiple resume profiles:
  - SE
  - CSM
  - TAM
- Sent JD and resume content to the LLM.
- Asked the model to analyze resume-job fit, match score, missing keywords, ATS risks, and interview questions.

### 🧩 Notes

This version turned the project from a simple prompt script into a resume matching workflow.

---

## 🧭 v0.3 - Resume Router

### 🎯 Goal

Reduce prompt length and avoid sending all resumes to the LLM by default.

### ✨ Features

- Added job title parsing from the first line of `JDs/jd.txt`.
- Added local job-title-based resume routing.
- Matched job titles to the most relevant resume profile:
  - SE
  - CSM
  - TAM
- Sent only the selected resume to the LLM for deeper analysis.
- Added fallback logic: if no local match is found, send all three resumes to the LLM for comparison.

### 🧩 Notes

This version introduced local decision logic before calling the LLM, making the agent faster, cheaper, and more structured.

---

## 🛡️ v0.4 - Guardrailed Tailored Resume Generator

### 🎯 Goal

Move from analysis-only output to a controlled resume generation workflow.

Instead of only printing resume feedback in the terminal, this version generates Markdown files that can be reviewed, copied, and manually converted into a polished resume.

### ✨ Features

- Generates a JD-tailored English resume draft based on the selected resume profile.
- Saves output into a unique timestamped folder under `output/`.
- Produces two Markdown files:
  - `tailored_resume_en.md`
  - `review_notes_bilingual.md`
- Keeps the tailored resume draft fully in English for real job application use.
- Keeps explanations, risks, missing information, and confirmation questions in a separate bilingual review file.
- Adds safety guardrails to prevent hallucinated or exaggerated resume content.
- Separates safe resume rewrites from unsupported or risky claims.
- Requires rewritten content to be grounded in the original resume.
- Avoids adding fake metrics, tools, customers, projects, responsibilities, or achievements.
- Keeps generated output files out of GitHub through `.gitignore`.

### 📁 Output Structure

    output/
    └── <timestamp>_<job_title>/
        ├── tailored_resume_en.md
        └── review_notes_bilingual.md

### 🧩 Notes

This version turned JobSniper from a resume analysis assistant into a controlled resume drafting agent.

The generated English resume is still treated as a draft. Final formatting, fact-checking, and PDF conversion remain human-reviewed steps.

---

## 📊 v0.5 - JD Requirement Classification and ATS-like Match Scoring

### 🎯 Goal

Improve the stability and explainability of resume-JD match scoring.

Previous versions allowed the LLM to provide an overall match score directly, which could vary depending on prompt wording. This version introduces JD requirement classification and a fixed ATS-like scoring rubric to reduce score drift.

### ✨ Features

- Adds JD requirement classification before scoring:
  - Must-have Requirements
  - Nice-to-have Requirements
  - Transferable Skills
  - Red Flags
- Adds a fixed 100-point ATS-like scoring rubric:
  - Must-have Requirements Match: 35 points
  - Transferable Skills Match: 20 points
  - Responsibility Alignment: 20 points
  - Nice-to-have Coverage: 10 points
  - ATS Readability: 15 points
- Requires evidence from the original resume for each scoring dimension.
- Requires matching JD requirements for each scoring dimension.
- Requires deduction reasons for each scoring dimension.
- Prevents high scores when the original resume lacks supporting evidence.
- Adds `temperature=0` to reduce randomness in LLM output.
- Outputs requirement classification and score breakdown in `review_notes_bilingual.md`.

### 🧩 Notes

This version does not connect to a real ATS system. Instead, it simulates ATS-style resume screening using a fixed, evidence-based scoring framework.

---

## 🧯 v0.5.1 - Output Completeness Fix

### 🎯 Goal

Improve output completeness and reduce missing Markdown sections after introducing the v0.5 JD classification and ATS-like scoring workflow.

After the v0.5 prompt became more complex, the model sometimes returned a shortened response and omitted parts of the expected output, especially the bilingual review notes section.

### ✨ Features

- Increases the maximum output token limit for DeepSeek responses.
- Improves the chance of generating both expected Markdown sections:
  - `tailored_resume_en.md`
  - `review_notes_bilingual.md`
- Keeps the existing single-prompt workflow.
- Preserves the v0.5 JD requirement classification and ATS-like scoring logic.
- Improves reliability when generating longer JD analysis and review notes.

### 🧩 Notes

This version does not split the prompt into multiple LLM calls yet. Prompt splitting is planned as a future reliability upgrade if the single-prompt workflow becomes unstable again.
