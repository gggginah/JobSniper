from config import ROLE_TITLE_KEYWORDS
from config import ROUTE_TO_RESUME_PROFILE
from utils.file_io import load_all_resumes
from utils.file_io import load_prompt
from services.llm_client import ask_deepseek

def choose_resume_by_job_title(job_title):
    title = job_title.lower()
    scores = {}

    for role, keywords in ROLE_TITLE_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            if keyword in title:
                score += 1

        scores[role] = score

    best_role = max(scores, key=scores.get)

    if scores[best_role] == 0:
        return "UNKNOWN", scores

    return best_role, scores



def select_resume(job_title, jd):
    print("开始进行本地简历路由...")

    best_role, title_scores = choose_resume_by_job_title(job_title)

    print("本地路由分数:", title_scores)

    resumes = load_all_resumes()

    if best_role == "UNKNOWN":
        print("岗位名称未匹配到明确简历方向，启动 fallback：让 DeepSeek 根据完整 JD 选择简历方向。")

        selection_prompt = build_fallback_resume_selection_prompt(
            job_title=job_title,
            jd=jd,
            title_scores=title_scores
        )

        selection_result = ask_deepseek(selection_prompt)

        print("\n====================")
        print("Fallback Resume Selection Result")
        print("====================\n")
        print(selection_result)

        selected_route = parse_selected_resume_profile(selection_result)

        if selected_route == "UNKNOWN":
            raise ValueError("Fallback could not select a suitable resume profile. Please review the JD manually.")

        selected_resume_profile = ROUTE_TO_RESUME_PROFILE[selected_route]
        selected_resume = resumes[selected_resume_profile]

        print(f"Fallback 选择岗位方向：{selected_route}")
        print(f"实际使用简历：{selected_resume_profile}")

        return selected_route, selected_resume, title_scores

    selected_resume_profile = ROUTE_TO_RESUME_PROFILE.get(best_role, best_role)
    selected_resume = resumes[selected_resume_profile]

    print(f"本地路由成功：岗位方向为 {best_role}，实际使用 {selected_resume_profile} 简历。")

    return best_role, selected_resume, title_scores



def build_fallback_resume_selection_prompt(job_title, jd, title_scores):
        template = load_prompt(

        "PROMPT/fallback_resume_selection.md"

    )

        return template.format(

            job_title=job_title,

            jd=jd,

            title_scores=title_scores

        )


def parse_selected_resume_profile(selection_result):
    valid_profiles = ["SE", "PRESALES_SUPPORT", "CSM", "TAM", "UNKNOWN"]

    for line in selection_result.splitlines():
        line = line.strip()

        if line.startswith("SELECTED_PROFILE:"):
            profile = line.replace("SELECTED_PROFILE:", "").strip()

            if profile in valid_profiles:
                return profile

    return "UNKNOWN"

