from utils.file_io import load_prompt
from utils.file_io import save_file
import os
from config import EXPERIENCE_BANK_PATH
from config import EVIDENCE_MARKERS
from utils.file_io import read_file
from services.llm_client import ask_deepseek
from utils.markdown import extract_markdown_section



def build_evidence_selection_prompt(job_title, jd, experience_bank):

    template = load_prompt(
        "PROMPT/evidence_selection_step2.md"
    )

    return template.format(
        job_title=job_title,
        jd=jd,
        experience_bank=experience_bank
    )


def save_selected_evidence(selected_evidence, output_folder):
    save_file(
        os.path.join(output_folder, "selected_evidence.md"),
        selected_evidence
    )

    print(f"selected_evidence.md saved to: {output_folder}")



def run_stage1_evidence_selection(job_title, jd, output_folder):
    print("开始 Stage 1：根据 JD 从 Experience Bank 选择相关 evidence...")

    if not os.path.exists(EXPERIENCE_BANK_PATH):
        raise FileNotFoundError("没有找到 experience_bank.md，请先在项目根目录创建该文件。")

    experience_bank = read_file(EXPERIENCE_BANK_PATH)

    evidence_prompt = build_evidence_selection_prompt(
        job_title=job_title,
        jd=jd,
        experience_bank=experience_bank
    )

    selected_evidence_result = ask_deepseek(
        evidence_prompt,
        required_markers=EVIDENCE_MARKERS,
        max_tokens=5000
    )

    selected_evidence = extract_markdown_section(
        selected_evidence_result,
        "===SELECTED_EVIDENCE_MD==="
    )

    if not selected_evidence:
        raise ValueError("Stage 1 failed: selected evidence was empty.")

    save_selected_evidence(selected_evidence, output_folder)

    return selected_evidence


