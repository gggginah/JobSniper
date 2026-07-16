# JobSniper Roadmap

JobSniper is a local, human-in-the-loop job application workflow assistant.

It helps users analyze job descriptions, select relevant experience evidence, generate tailored resume drafts, review risks, and export editable application-ready documents while keeping private career data local.

The project is designed around a practical job application workflow rather than one-off resume rewriting.

---

## ✅ Completed

### v0.1 - Minimal LLM Agent

**Goal:** Build the smallest runnable LLM-powered prototype.

- Connected to the DeepSeek API through the OpenAI-compatible SDK.
- Loaded API credentials from a local `.env` file.
- Sent a basic prompt and received an LLM response.
- Verified that the local Python environment and API connection worked.

---

### v0.2 - Resume Matching Agent

**Goal:** Move from hardcoded prompts to local file-based resume and JD analysis.

- Added local file reading for job descriptions and resume files.
- Compared a job description against multiple resume profiles.
- Generated basic JD-resume match analysis.
- Produced initial outputs such as:
  - match score
  - missing keywords
  - resume improvement suggestions
  - interview question preparation

---

### v0.3 - Resume Router

**Goal:** Reduce prompt length and improve resume selection by routing to the most relevant resume profile.

- Added local job-title-based resume routing.
- Selected one of several resume profiles based on role keywords.
- Supported different resume directions, such as:
  - Support Engineer
  - Customer Success Manager
  - Technical Account Manager
- Reduced unnecessary prompt content by avoiding sending all resumes when one profile was clearly relevant.

---

### v0.4 - Guardrailed Tailored Resume Generator

**Goal:** Generate safer, more usable tailored resume drafts.

- Added tailored English resume generation.
- Added bilingual review notes.
- Separated final resume output from analysis, risks, and explanations.
- Introduced timestamped output folders to avoid overwriting previous runs.
- Generated two main files:
  - `tailored_resume_en.md`
  - `review_notes_bilingual.md`
- Added anti-hallucination rules to avoid inventing unsupported experience, tools, metrics, or responsibilities.

---

### v0.5 - JD Requirement Classification and ATS-like Scoring

**Goal:** Make resume matching more structured and consistent.

- Added JD requirement classification.
- Classified requirements into categories such as:
  - must-have requirements
  - nice-to-have requirements
  - transferable skills
  - red flags
- Added a structured 100-point scoring rubric.
- Improved score consistency with deterministic LLM generation settings.
- Made the output more useful for deciding whether a role is worth applying to.

---

### v0.5.1 - Output Completeness Fix

**Goal:** Improve LLM output reliability and reduce incomplete Markdown generation.

- Increased token limits for long responses.
- Added retry logic for failed or incomplete LLM calls.
- Added marker-based output validation.
- Required exact output markers such as:
  - `===TAILORED_RESUME_EN_MD===`
  - `===REVIEW_NOTES_BILINGUAL_MD===`
- Reduced failures where one of the expected Markdown files was missing.

---

### v0.5.2 - JD-based Fallback Resume Selector

**Goal:** Improve fallback behavior when local title-based routing cannot identify the best resume profile.

- Added an LLM-based fallback resume selection step.
- Used the full JD to choose the most suitable resume direction when the local router returns `UNKNOWN`.
- Supported fallback profile selection among:
  - SE
  - PRESALES_SUPPORT
  - CSM
  - TAM
  - UNKNOWN
- Reused the main resume generation workflow after fallback selection.
- Prevented fallback from using outdated prompts that did not produce the required Markdown outputs.

---

### v0.5.3 - Application Decision Layer

**Goal:** Make match scores actionable for real job application decisions.

- Added score diagnosis.
- Explained why a score is high, medium, or low.
- Distinguished between:
  - true hard-requirement mismatch
  - relevant experience being under-presented
  - resume profile not being ideal
  - ambiguous or hybrid JD
  - stretch role with transferable potential
- Added practical decision outputs:
  - Apply Priority
  - Stretch Fit Potential
  - Resume Fixability
  - Recommended Action
- Helped turn a numeric score into a real application decision.

---

### v0.5.4 - Experience Bank Evidence Selector

**Goal:** Integrate a private career fact base without overloading the final resume generation prompt.

- Added `experience_bank.md` as a private source of truth for confirmed career facts.
- Introduced a two-stage workflow:

  1. **Stage 1: Evidence Selection**
     - Reads the JD and the Chinese Experience Bank.
     - Selects only JD-relevant evidence.
     - Outputs `selected_evidence.md`.

  2. **Stage 2: Resume Generation**
     - Uses the selected resume profile, JD, and selected evidence.
     - Generates the final tailored resume and bilingual review notes.

- Added `selected_evidence.md` as a human-review checkpoint.
- Added Stage 2-only mode with `--stage2`, allowing users to manually edit selected evidence before regenerating the final resume.
- Preserved strict project separation between different work experiences and the personal project.
- Reduced hallucination risk by making selected evidence the bridge between raw experience facts and final resume wording.

---

### v0.6 - DOCX Resume Exporter

**Goal:** Reduce manual copy-paste and formatting work by converting tailored Markdown resumes into editable Word documents.

- Added DOCX export using `python-docx`.
- Converts `tailored_resume_en.md` into `tailored_resume.docx`.
- Saves the DOCX file in the same timestamped output folder.
- Applies basic resume-style formatting:
  - centered candidate name
  - contact information line
  - section headings
  - bullet points
  - consistent font and margins
- Added Markdown-to-DOCX conversion logic for structured resume content.
- Added export-only workflow so an existing `tailored_resume_en.md` can be converted again without rerunning the full LLM workflow.
- Keeps Markdown as the editable content source and DOCX as the application-ready document format.

---

## 🚧 Planned

### v0.6.1 - DOCX Formatting Optimization

**Goal:** Polish the generated DOCX so it is closer to a final resume template.

- Improve spacing, margins, bullet indentation, and section heading layout.
- Reduce unnecessary blank space to better support one-page resumes.
- Attach divider lines more cleanly to section headings.
- Add right-aligned dates and locations.
- Improve company, project, and education title formatting.
- Render education labels such as `tag:211` and `tag:Double 1st-Class` as styled visual tags.
- Make GitHub and email links clickable where appropriate.
- Optimize the Technical Skills section into a more compact format.

---

### v0.7 - PDF Export

**Goal:** Generate submission-ready PDF resumes after DOCX formatting becomes stable.

- Export `tailored_resume.docx` to PDF.
- Keep DOCX as the editable source file.
- Keep PDF as the final submission format.
- Ensure the exported PDF preserves resume formatting and ATS-friendly structure.

---

### v0.8 - Application Package Generator

**Goal:** Expand from resume generation to full application material preparation.

- Generate role-specific cover letters.
- Generate answers for common application form questions.
- Generate recruiter message drafts.
- Generate short professional summaries for job platforms.
- Generate JD-specific interview preparation notes.

---

### v0.9 - Interview Answer Bank

**Goal:** Build reusable interview answers for common HR and recruiter questions.

- Create a structured answer bank for:
  - self-introduction
  - voluntary resignation
  - gap period
  - career transition
  - customer-facing experience
  - English communication
  - salary expectation
- Adapt answers based on target role type.
- Support English versions for international company interviews.
- Help reduce repeated interview preparation work.

---

### v1.0 - RAG-based Experience Retrieval

**Goal:** Make Experience Bank retrieval more scalable and precise.

- Split `experience_bank.md` into searchable chunks.
- Retrieve only JD-relevant facts instead of sending the full Experience Bank.
- Add embedding-based or keyword-based retrieval.
- Improve evidence selection accuracy as the Experience Bank grows.
- Reduce prompt length and token usage.

---

### v1.1 - Risk and Hallucination Reviewer

**Goal:** Add a dedicated review step before final resume export.

- Check generated resume content against selected evidence.
- Detect unsupported claims.
- Detect mixed project facts.
- Detect overstated metrics or responsibilities.
- Produce a structured risk report before DOCX/PDF export.
- Strengthen the human-in-the-loop review process.

---

### v1.2 - Application Tracker

**Goal:** Track real job applications and generated materials.

- Track applied companies, roles, dates, locations, and statuses.
- Link each application to its output folder.
- Record resume version, score, decision notes, and interview progress.
- Help manage follow-ups and rejection records.

---

### v1.3 - Interactive UI

**Goal:** Make JobSniper usable without terminal commands.

- Add a simple local web interface using Streamlit or a similar framework.
- Allow users to paste JDs.
- Allow users to review selected evidence.
- Allow users to trigger resume generation and DOCX export from the UI.
- Display output folders and generated files more clearly.

---

### v1.4 - Multi-Agent Workflow

**Goal:** Split the workflow into specialized reasoning roles.

Possible agents:

- JD Analyst
- Resume Router
- Evidence Selector
- Resume Writer
- Risk Reviewer
- Application Advisor
- Interview Coach

The goal is not to overcomplicate the system, but to separate responsibilities once the single-agent workflow becomes too large.

---

## Long-term Vision

JobSniper aims to become a private, local-first job application assistant that helps users turn scattered career experience into targeted, evidence-based application materials.

It should not replace human judgment. Instead, it should reduce repetitive work, improve consistency, and help users make better application decisions.

The long-term workflow is:

1. Read a job description.
2. Select the best resume direction.
3. Retrieve relevant evidence from a private Experience Bank.
4. Generate tailored application materials.
5. Review risks and unsupported claims.
6. Export polished documents.
7. Track applications and prepare for interviews.