from utils.file_io import load_prompt
from utils.markdown import extract_markdown_section
import os
from utils.file_io import save_file
from exporters.docx_exporter import convert_markdown_to_docx
from services.llm_client import ask_deepseek
from config import FINAL_OUTPUT_MARKERS

def build_single_resume_prompt(
        job_title,
        jd,
        selected_role,
        selected_resume,
        title_scores,
        selected_evidence
):

    template = load_prompt(
        "PROMPT/resume_generation_step3.md"
    )

    return template.format(
        job_title=job_title,
        jd=jd,
        selected_role=selected_role,
        selected_resume=selected_resume,
        title_scores=title_scores,
        selected_evidence=selected_evidence
    )   




def save_final_outputs(result, output_folder):
    tailored_resume_en = extract_markdown_section(
        result,
        "===TAILORED_RESUME_EN_MD===",
        "===REVIEW_NOTES_BILINGUAL_MD==="
    )

    review_notes_bilingual = extract_markdown_section(
        result,
        "===REVIEW_NOTES_BILINGUAL_MD==="
    )

    tailored_resume_path = os.path.join(output_folder, "tailored_resume_en.md")
    review_notes_path = os.path.join(output_folder, "review_notes_bilingual.md")
    docx_path = os.path.join(output_folder, "tailored_resume.docx")

    if tailored_resume_en:
        save_file(tailored_resume_path, tailored_resume_en)
        print(f"tailored_resume_en.md saved to: {output_folder}")

        convert_markdown_to_docx(
            markdown_path=tailored_resume_path,
            docx_path=docx_path
        )
        print(f"tailored_resume.docx saved to: {output_folder}")

    else:
        print("Warning: tailored_resume_en.md was not generated. Resume marker not found.")

    if review_notes_bilingual:
        save_file(review_notes_path, review_notes_bilingual)
        print(f"review_notes_bilingual.md saved to: {output_folder}")
    else:
        print("Warning: review_notes_bilingual.md was not generated. Review notes marker not found.")

    print(f"Final files saved to: {output_folder}")



def run_stage2_resume_generation(job_title, jd, selected_role, selected_resume, title_scores, selected_evidence, output_folder):
    print("开始 Stage 2：基于 selected resume + selected evidence 生成最终简历...")

    prompt = build_single_resume_prompt(
        job_title=job_title,
        jd=jd,
        selected_role=selected_role,
        selected_resume=selected_resume,
        title_scores=title_scores,
        selected_evidence=selected_evidence
    )

    result = ask_deepseek(
        prompt,
        required_markers=FINAL_OUTPUT_MARKERS,
        max_tokens=9000
    )

    print("\n====================")
    print("DeepSeek Final Result")
    print("====================\n")
    print(result)

    save_final_outputs(result, output_folder)

