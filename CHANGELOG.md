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

## 🧭 v0.5.2 - JD-based Fallback Resume Selector

### 🎯 Goal

Improve fallback behavior when the local title-based router cannot confidently match a job title to an existing resume direction.

Previously, when the job title did not match the predefined routing keywords, the agent entered an older fallback path. That fallback path could analyze multiple resumes, but it did not follow the current marker-based output format, which sometimes caused missing Markdown outputs or marker validation failures.

### ✨ Features

- Adds a JD-based fallback resume selection step.
- Uses the full job description when the local title-based router returns `UNKNOWN`.
- Asks the LLM to select the most suitable resume direction from:
  - SE
  - PRESALES_SUPPORT
  - CSM
  - TAM
  - UNKNOWN
- Keeps fallback lightweight by using it only for resume direction selection.
- Adds `parse_selected_resume_profile()` to extract the selected profile from the LLM response.
- Adds route-to-resume mapping so hybrid directions such as `PRESALES_SUPPORT` can reuse the closest existing resume profile.
- Reuses the existing main resume generation workflow after fallback selection.
- Prevents fallback from using outdated prompts that do not generate the required Markdown sections.
- Allows ambiguous or out-of-pool job titles to still produce the expected output files:
  - `tailored_resume_en.md`
  - `review_notes_bilingual.md`

### 🧩 Notes

This version changes the role of fallback.

Instead of directly generating resume analysis or Markdown files, fallback now acts as a JD-based resume selector. Once a resume direction is selected, the agent returns to the main v0.5 generation workflow.

This keeps the generation logic unified and reduces failures caused by ambiguous job titles.

## 🧭 v0.5.3 - Application Decision Layer

### 🎯 Goal

Make match scores more actionable for job application decisions.

Previous versions generated a match score and score breakdown, but the score alone was not enough to determine whether a role was worth applying to. This version adds an application decision layer to help interpret medium or borderline scores.

### ✨ Features

- Adds score diagnosis to explain why the match score is high, medium, or low.
- Distinguishes between:
  - True hard-requirement mismatch
  - Relevant experience being under-presented
  - Resume profile not being ideal
  - Ambiguous or hybrid JD
  - Stretch role with transferable potential
- Adds application decision outputs:
  - Apply Priority
  - Stretch Fit Potential
  - Resume Fixability
  - Recommended Action
- Helps decide whether to apply, lightly tailor, heavily tailor, or deprioritize a role.
- Makes mid-range scores such as 50–60 easier to interpret.

### 🧩 Notes

This version does not change the scoring rubric itself. It improves how the score is interpreted and used for real application decisions.


## 🧠 v0.5.4 - Experience Bank Evidence Selector

### 🎯 Goal

Introduce a two-stage, human-in-the-loop resume tailoring workflow by connecting the Chinese Experience Bank to JobSniper.

Instead of passing the full Experience Bank directly into the final resume generation prompt, this version first selects JD-relevant evidence and saves it as `selected_evidence.md`. The user can review or edit the selected evidence before running Stage 2 to generate the final tailored resume.

### ✨ Features

- Added `experience_bank.md` as a private source of truth for confirmed career facts.
- Added Stage 1: JD-based Evidence Selector.
- Generates `selected_evidence.md` for each application run.
- Added Stage 2-only mode with `--stage2`.
- Allows manual review and editing of `selected_evidence.md` before final resume generation.
- Uses selected evidence to strengthen the base resume instead of generating a resume from scratch.
- Preserves project separation between Project 01, Project 02, and JobSniper.
- Prevents metrics and facts from being mixed across projects.
- Keeps Chinese facts as the source of truth while generating English resume output.

### 🧩 Notes

This is a major workflow upgrade. JobSniper now supports an evidence-first resume tailoring process: select evidence, review evidence, then generate the final resume.

## 📄 v0.6 - DOCX Resume Exporter

### 🎯 Goal

Reduce manual copy-paste and formatting work by converting the tailored Markdown resume into an editable Word document.

Previously, JobSniper generated `tailored_resume_en.md`, but the user still needed to manually copy the content into a resume template and adjust formatting before submission. This version adds a DOCX export step so the tailored resume can be opened directly in Word or WPS for final review.

### ✨ Features

- Added DOCX resume export using `python-docx`.
- Converts `tailored_resume_en.md` into `tailored_resume.docx`.
- Saves the DOCX file in the same timestamped output folder.
- Applies basic resume-style formatting:
  - centered candidate name
  - contact information line
  - section headings
  - bullet points
  - consistent font and margins
- Added Markdown-to-DOCX conversion logic for structured resume content.
- Added support for an export-only workflow so an existing `tailored_resume_en.md` can be converted again without rerunning the full LLM workflow.
- Keeps Markdown output as the editable content source and DOCX as the application-ready document format.

### 🧩 Notes

This version significantly improves JobSniper’s practical usability. The project now supports a more complete application workflow: JD analysis, evidence selection, tailored resume generation, review notes, and editable DOCX resume export.

The current DOCX output is usable but still needs formatting refinement. Future versions will focus on spacing, one-page layout, right-aligned dates and locations, styled education tags, clickable links, and more polished resume formatting.