from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from config import JD_PATH
from workflow.resume_router import choose_resume_by_job_title
from workflow.resume_router import build_fallback_resume_selection_prompt
from workflow.resume_router import select_resume
from workflow.resume_router import parse_selected_resume_profile
from utils.file_io import read_file
from utils.file_io import save_file
from utils.file_io import load_prompt
from utils.file_io import read_jd_file
from utils.file_io import load_all_resumes
from utils.file_io import sanitize_job_title
from utils.file_io import create_output_run_folder
from services.llm_client import ask_deepseek
from utils.markdown import extract_markdown_section
from utils.markdown import clean_markdown_bold
from utils.cli import get_stage2_folder_from_args
from utils.cli import get_export_docx_folder_from_args
from workflow.evidence_selection import build_evidence_selection_prompt
from workflow.evidence_selection import save_selected_evidence
from workflow.evidence_selection import run_stage1_evidence_selection
from workflow.resume_generation import run_stage2_resume_generation
from workflow.resume_generation import build_single_resume_prompt
from exporters.docx_exporter import convert_markdown_to_docx
from exporters.docx_exporter import add_bottom_border




load_dotenv()


def main():

    export_docx_folder = get_export_docx_folder_from_args()

    if export_docx_folder:

        markdown_path = os.path.join(export_docx_folder, "tailored_resume_en.md")

        docx_path = os.path.join(export_docx_folder, "tailored_resume.docx")

        if not os.path.exists(markdown_path):

            raise FileNotFoundError(f"没有找到 tailored_resume_en.md: {markdown_path}")

        convert_markdown_to_docx(

            markdown_path=markdown_path,

            docx_path=docx_path

        )

        print(f"tailored_resume.docx exported to: {export_docx_folder}")

        return

    job_title, jd = read_jd_file(JD_PATH)

    print("读取到岗位名称:", job_title)

    stage2_folder = get_stage2_folder_from_args()

    selected_role, selected_resume, title_scores = select_resume(job_title, jd)

    if stage2_folder:
        print("\n====================")
        print("Stage 2 only mode")
        print("====================")
        print(f"读取人工编辑后的 selected_evidence.md: {stage2_folder}")

        output_folder = stage2_folder
        selected_evidence_path = os.path.join(output_folder, "selected_evidence.md")

        if not os.path.exists(selected_evidence_path):
            raise FileNotFoundError(f"没有找到 selected_evidence.md: {selected_evidence_path}")

        selected_evidence = read_file(selected_evidence_path)

        if not selected_evidence.strip():
            raise ValueError("selected_evidence.md 是空的，请先补充内容。")

    else:
        print("\n====================")
        print("Full mode")
        print("====================")
        print("将先生成 selected_evidence.md，再生成最终简历。")

        output_folder = create_output_run_folder(job_title)

        selected_evidence = run_stage1_evidence_selection(
            job_title=job_title,
            jd=jd,
            output_folder=output_folder
        )

    run_stage2_resume_generation(
        job_title=job_title,
        jd=jd,
        selected_role=selected_role,
        selected_resume=selected_resume,
        title_scores=title_scores,
        selected_evidence=selected_evidence,
        output_folder=output_folder
    )


if __name__ == "__main__":
    main()