# 🗺️ Roadmap

This file records the planned development path for **JobSniper**.

JobSniper is developed through iterative, pain-point-driven upgrades. Each version either adds a planned capability or addresses a real issue discovered during resume tailoring workflows.

---

## ✅ Completed Versions

### 🐣 v0.1 - Minimal LLM Agent

Build the first runnable prototype.

- Set up the local Python environment.
- Connected to an LLM API through the OpenAI-compatible SDK.
- Sent a hardcoded prompt to the model.
- Printed the model response in the terminal.

---

### 📄 v0.2 - Resume Matching Agent

Allow the agent to read local JD and resume files.

- Added local file reading.
- Added `JDs/jd.txt`.
- Added multiple resume profiles.
- Sent JD and resumes to the LLM for matching analysis.

---

### 🧭 v0.3 - Resume Router

Add local routing before calling the LLM.

- Parsed job title from the JD file.
- Matched job titles to resume profiles.
- Sent only the selected resume to the LLM when routing succeeded.
- Added fallback when the local router could not decide.

---

### 🛡️ v0.4 - Guardrailed Tailored Resume Generator

Move from analysis-only output to controlled resume generation.

- Generated `tailored_resume_en.md`.
- Generated `review_notes_bilingual.md`.
- Added hallucination guardrails.
- Separated application-ready resume content from review notes.
- Saved outputs in timestamped folders.

---

### 📊 v0.5 - JD Requirement Classification and ATS-like Scoring

Improve match scoring stability and explainability.

- Added JD requirement classification:
  - Must-have Requirements
  - Nice-to-have Requirements
  - Transferable Skills
  - Red Flags
- Added fixed ATS-like scoring rubric.
- Added `temperature=0`.
- Required evidence and deduction reasons for each scoring dimension.

---

### 🧯 v0.5.1 - Output Completeness Fix

Improve long-output reliability.

- Increased the maximum output token limit for DeepSeek responses.
- Reduced missing Markdown sections after the v0.5 prompt became more complex.
- Kept the existing single-prompt workflow.
- Preserved v0.5 JD classification and ATS-like scoring logic.

---

### 🧭 v0.5.2 - JD-based Fallback Resume Selector

Improve fallback behavior for ambiguous or out-of-pool job titles.

- Uses the full JD when the local title-based router cannot decide.
- Lets the LLM select the most suitable resume direction:
  - SE
  - PRESALES_SUPPORT
  - CSM
  - TAM
  - UNKNOWN
- Adds parsing logic to extract the selected profile.
- Maps hybrid directions to existing resume profiles.
- Reuses the main resume generation workflow after fallback selection.
- Prevents fallback from failing due to outdated output format.

---

## 🚧 Planned Versions

### 🧱 v0.5.3 - Experience Bank

Create a structured factual experience database.

The current system relies mainly on several pre-written resume profiles. However, these profiles do not fully represent all past experience, project evidence, transferable skills, or gap-period output.

Planned improvements:

- Add `experience_bank.md`.
- Store company-level experience.
- Store project-level evidence.
- Store transferable skills.
- Store safe English resume wording.
- Store personal projects such as JobSniper.
- Record “Do Not Overstate” boundaries to prevent exaggeration.
- Use Chinese as the source of truth and English as resume-ready phrasing.

Expected sections:

- Company-level Experience
- Project-level Evidence
- Personal Projects
- Safe English Wording
- Do Not Overstate

---

### 🔎 v0.5.4 - JD-based Evidence Selector

Use the JD and experience bank to identify relevant evidence beyond existing resume profiles.

Planned improvements:

- Read `experience_bank.md`.
- Analyze the target JD.
- Identify relevant experience items from the experience bank.
- Select project evidence that supports JD requirements.
- Identify transferable skills that can safely support the application.
- Separate confirmed evidence from items that need user confirmation.
- Prepare selected evidence for future resume generation.

Goal:

Move JobSniper from choosing between fixed resume profiles to selecting evidence from a broader factual experience base.

---

### 🧩 v0.5.5 - Split Prompt / Two-step Generation

Split the large generation prompt into smaller LLM calls if output reliability becomes an issue again.

Planned improvements:

- Generate `tailored_resume_en.md` in one LLM call.
- Generate `review_notes_bilingual.md` in a separate LLM call.
- Reduce the risk of missing long review sections.
- Make each output easier to validate and debug.

Note:

This is no longer the immediate next step because v0.5.1 improved output completeness through token settings. It remains a planned reliability upgrade.

---

### 📄 v0.6 - DOCX Resume Exporter

Convert the generated Markdown resume into an editable Word document.

Planned improvements:

- Read `tailored_resume_en.md`.
- Generate `tailored_resume.docx`.
- Apply ATS-friendly formatting.
- Support:
  - Font size
  - Bold headings
  - Section dividers
  - Bullet points
  - Resume-style spacing
  - Simple, editable layout
- Avoid tables, images, text boxes, and complex designs.

Goal:

Move from Markdown resume drafts to editable Word resume files.

---

### 🧾 v0.7 - PDF Export

Export the formatted DOCX resume into a final PDF version.

Planned improvements:

- Convert `tailored_resume.docx` to `tailored_resume.pdf`.
- Preserve formatting from the DOCX version.
- Keep PDF as the final application-ready format.

Note:

PDF export should happen after DOCX export because DOCX is easier to review and edit manually.

---

### 📦 v0.8 - Application Package Generator

Generate a complete application package for each job.

Planned outputs:

    application_package/
    ├── tailored_resume.docx
    ├── tailored_resume.pdf
    ├── cover_letter.md
    ├── application_answers.md
    └── application_checklist.md

Planned improvements:

- Generate cover letter drafts.
- Generate answers for common application questions.
- Generate a pre-submission checklist.
- Highlight items that require user confirmation.
- Keep the user in control before submission.

---

### 🤝 v1.0 - Human-in-the-loop Application Assistant

Integrate resume tailoring, scoring, evidence selection, document export, and application material generation into a complete job application workflow.

Target workflow:

    Input JD
    ↓
    Local title router
    ↓
    JD-based fallback selector if needed
    ↓
    Experience bank evidence selection
    ↓
    Tailored resume generation
    ↓
    Bilingual review notes
    ↓
    ATS-like scoring
    ↓
    DOCX export
    ↓
    PDF export
    ↓
    Cover letter and application answers
    ↓
    Human review
    ↓
    User decides whether to submit

Positioning:

JobSniper is not intended to be a fully automated application bot. It is a human-in-the-loop job application assistant that helps organize, generate, review, and prepare application materials while keeping final decisions under human control.