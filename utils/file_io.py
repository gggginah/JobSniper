from config import RESUME_FILES
import os
from datetime import datetime

def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
    
def save_file(path, content):
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def load_prompt(path):

    """

    Load prompt template from markdown file.

    """

    if not os.path.exists(path):

        raise FileNotFoundError(

            f"Prompt file not found: {path}"

        )

    return read_file(path)



def read_jd_file(path):
    content = read_file(path)
    lines = content.splitlines()

    if len(lines) == 0:
        raise ValueError("JD 文件是空的，请在 JDs/jd.txt 中填入岗位名称和 JD 内容。")

    job_title_line = lines[0].strip()
    job_title = job_title_line.replace("Job Title:", "").strip()
    jd_text = "\n".join(lines[1:]).strip()

    if not job_title:
        raise ValueError("没有读取到岗位名称，请把岗位名称放在 JDs/jd.txt 第一行。")

    if not jd_text:
        raise ValueError("没有读取到 JD 内容，请把完整 JD 放在岗位名称下面。")

    return job_title, jd_text


def load_all_resumes():
    resumes = {}

    for role, path in RESUME_FILES.items():
        resumes[role] = read_file(path)

    return resumes


def sanitize_job_title(job_title):
    safe_job_title = (
        job_title
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "")
        .replace("*", "")
        .replace("?", "")
        .replace('"', "")
        .replace("<", "")
        .replace(">", "")
        .replace("|", "")
    )

    return safe_job_title


def create_output_run_folder(job_title):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    safe_job_title = sanitize_job_title(job_title)

    folder_name = f"{timestamp}_{safe_job_title}"
    output_path = os.path.join("output", folder_name)

    os.makedirs(output_path, exist_ok=True)

    return output_path
