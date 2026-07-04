# openai-对象
from openai import OpenAI
# 用于把.env里面的环境变量加载进python
from dotenv import load_dotenv
import os


# 和openai对话的入口

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 用来读取简历文件
def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()
    

# 用来读取jd，第一行必须是jobtitle用来匹配三份简历
def read_jd_file(path):

    """

    读取 JD 文件。

    规则：

    - 第一行是岗位名称 job_title

    - 第二行开始是完整 JD 内容

    """

    content = read_file(path)

    lines = content.splitlines()

    if len(lines) == 0:

        raise ValueError("JD 文件是空的，请在 JDs/jd.txt 中填入岗位名称和 JD 内容。")

    job_title_line = lines[0].strip()

    # 兼容两种写法：

    # 1. Technical Account Manager

    # 2. Job Title: Technical Account Manager

    job_title = job_title_line.replace("Job Title:", "").strip()

    jd_text = "\n".join(lines[1:]).strip()

    if not job_title:

        raise ValueError("没有读取到岗位名称，请把岗位名称放在 JDs/jd.txt 第一行。")

    if not jd_text:

        raise ValueError("没有读取到 JD 内容，请把完整 JD 放在岗位名称下面。")

    return job_title, jd_text


# 真正的jd
jd = read_file("JDs/jd.txt")


# 这里放简历
RESUME_FILES = {

    "SE": "resumes/SupportEngineer.txt",

    "CSM": "resumes/CustomerSuccessManager.txt",

    "TAM": "resumes/TechnicalAccountManager.txt"

}

def load_all_resumes():

    """

    读取三份简历。

    返回一个字典：

    {

        "SE": "...",

        "CSM": "...",

        "TAM": "..."

    }

    """

    resumes = {}

    for role, path in RESUME_FILES.items():

        resumes[role] = read_file(path)

    return resumes




# =========================

# 4. 根据岗位名称做本地简历路由

# =========================

ROLE_TITLE_KEYWORDS = {

    "SE": [

        "solution engineer",

        "solutions engineer",

        "support engineer",

        "technical support engineer",

        "customer support engineer",

        "sales engineer",

        "pre-sales engineer",

        "presales engineer",

        "solution consultant",

        "solutions consultant"

    ],

    "CSM": [

        "customer success manager",

        "customer success",

        "client success manager",

        "client success",

        "customer experience",

        "customer adoption",

        "account manager",

        "customer relationship manager"

    ],

    "TAM": [

        "technical account manager",

        "technical account",

        "tam",

        "implementation manager",

        "implementation consultant",

        "technical consultant",

        "customer engineer",

        "technical customer success manager"

    ]

}


def choose_resume_by_job_title(job_title):

    """

    根据岗位名称判断最适合用哪份简历。

    如果匹配不到，返回 UNKNOWN。

    """

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


# =========================

# 5. Prompt：匹配成功时，只分析一份简历

# =========================

def build_single_resume_prompt(job_title, jd, selected_role, selected_resume, title_scores):

    prompt = f"""

你现在是一个资深招聘专员、简历优化顾问、ATS筛选器和岗位面试官。

我会给你：

1. 一个目标岗位名称

2. 一份目标岗位 JD

3. 一份根据岗位名称初步匹配出的简历

系统已经根据岗位名称做了本地初筛，初步推荐使用的简历方向是：{selected_role}

本地岗位名称匹配分数如下：

{title_scores}

请你基于 JD 和这份简历，完成以下任务。

重要限制：

- 不要编造我没有的经历。

- 只能基于我提供的简历内容进行分析、匹配和改写。

- 如果某个关键词或经历在我的简历中没有体现，请明确指出“缺失”，不要虚构。

- 改写时可以优化表达方式，但不能创造不存在的项目、公司、数据或职责。

- 如果原简历没有量化数据，可以用“建议补充量化数据：...”的方式提醒我，而不是替我编数字。

- 如果你认为本地初筛选择的简历不合适，请明确指出，并说明原因。

====================

任务一：JD核心分析

====================

请输出：

1. 该岗位更接近哪个方向：SE / CSM / TAM / 混合型

2. 岗位核心职责

3. 岗位核心关键词

4. 岗位最看重的能力

5. 该岗位可能的隐藏筛选标准

====================

任务二：简历匹配度分析

====================

请对这份简历和该 JD 的匹配度打分，分数范围为 0-100。

请输出：

- 匹配度：xx/100

- 核心匹配点：

- 明显短板：

- 是否适合投递：

- 是否需要微调：

- 如果不适合，原因是什么：

====================

任务三：缺失信息分析

====================

请先提取 JD 中最重要的核心关键词，然后对比这份简历，列出简历中缺失的前五条关键信息。

请输出：

【JD核心关键词提取】

1.

2.

3.

4.

5.

【简历中缺失的前五条关键信息】

1.

2.

3.

4.

5.

【这些缺失项对投递的影响】

...

====================

任务四：用 Google XYZ 公式改写经历

====================

请基于这份简历，挑选最值得优化的经历 bullet points，用 Google XYZ 公式进行改写。

Google XYZ 公式为：

通过做 Z，达成了 X 成果，并用 Y 量化。

英文表达逻辑为：

Accomplished [X] as measured by [Y], by doing [Z].

要求：

- 自然融入 JD 关键词。

- 不要编造不存在的成果。

- 如果原文没有数字，请保留原事实，并标注“建议补充量化指标”。

- 不要把经历写得过度夸张。

- 输出中请保留“原句”和“改写后”。

请输出至少 3 条改写建议。

====================

任务五：ATS筛选器检查

====================

现在请你扮演 ATS 申请追踪系统筛选器，扫描这份简历和改写建议。

请指出：

1. 哪些板块可能难以被 ATS 识别

2. 哪些关键词缺失

3. 哪些表达过于模糊

4. 哪些格式或内容可能不适合 ATS

5. 如何修改会更容易通过 ATS

====================

任务六：招聘经理面试问题

====================

现在请你担任该岗位的招聘经理。

请基于这份 JD 和我的个人背景，提出 3 个最难、最可能在面试中被问到的专业问题。

然后结合我的简历背景，为每个问题撰写一个参考回答。

要求：

- 问题要贴合该岗位。

- 回答要结合我的真实经历。

- 不要编造不存在的项目。

- 回答要体现岗位匹配度。

- 如果我的背景中信息不足，请指出需要我补充什么。

====================

任务七：最终总结

====================

请给我一个清晰的最终判断：

1. 当前这份简历是否适合投递？

2. 当前匹配度大概是多少？

3. 是否值得投递？

4. 投递前最应该修改的三件事是什么？

5. 这份 JD 对我来说是强匹配、中等匹配还是弱匹配？

请按以下格式输出：

【最终建议】

推荐简历方向：{selected_role}

匹配度：

是否值得投递：

匹配类型：强匹配 / 中等匹配 / 弱匹配

【投递前最重要的三项修改】

1.

2.

3.

【一句话结论】

...

====================

以下是岗位名称：

====================

{job_title}

====================

以下是目标岗位 JD：

====================

{jd}

====================

以下是本地初筛选中的简历：

====================

{selected_resume}

"""

    return prompt

# =========================

# 6. Prompt：匹配失败时，fallback 三份简历都分析

# =========================

def build_fallback_prompt(job_title, jd, resumes, title_scores):

    prompt = f"""

你现在是一个资深招聘专员、简历优化顾问和岗位匹配专家。

我会给你：

1. 一个目标岗位名称

2. 一份目标岗位 JD

3. 三份不同方向的简历：SE、CSM、TAM

系统曾尝试根据岗位名称进行本地匹配，但没有匹配成功。

本地岗位名称匹配分数如下：

{title_scores}

因此现在请你直接对三份简历进行比较，判断哪一份最适合用于投递该 JD。

重要限制：

- 不要编造我没有的经历。

- 只能基于我提供的简历内容进行分析。

- 如果某个关键词或经历在我的简历中没有体现，请明确指出“缺失”，不要虚构。

请完成以下任务：

1. 判断这份 JD 更接近哪个岗位方向：SE / CSM / TAM / 混合型

2. 分析三份简历分别和这份 JD 的匹配度，给出 0-100 分

3. 推荐最适合用于投递这份 JD 的简历版本

4. 说明推荐理由

5. 指出推荐简历中缺失的前五条关键信息

6. 给出投递前最重要的三条修改建议

7. 给出最终是否值得投递的判断

请按以下格式输出：

【JD岗位方向判断】

...

【三份简历匹配度】

SE:

- 匹配度：

- 核心匹配点：

- 明显短板：

CSM:

- 匹配度：

- 核心匹配点：

- 明显短板：

TAM:

- 匹配度：

- 核心匹配点：

- 明显短板：

【推荐投递版本】

推荐使用：SE / CSM / TAM

【推荐理由】

...

【缺失的前五条关键信息】

1.

2.

3.

4.

5.

【投递前最重要的三项修改】

1.

2.

3.

【一句话结论】

...

====================

以下是岗位名称：

====================

{job_title}

====================

以下是目标岗位 JD：

====================

{jd}

====================

以下是 SE 简历：

====================

{resumes["SE"]}

====================

以下是 CSM 简历：

====================

{resumes["CSM"]}

====================

以下是 TAM 简历：

====================

{resumes["TAM"]}

"""

    return prompt

# =========================

# 7. 调用 DeepSeek

# =========================

def ask_deepseek(prompt):

    response = client.chat.completions.create(

        model="deepseek-chat",

        messages=[

            {"role": "user", "content": prompt}

        ]

    )

    return response.choices[0].message.content

# =========================

# 8. 主流程

# =========================

def main():

    job_title, jd = read_jd_file("JDs/jd.txt")

    print("读取到岗位名称:", job_title)

    print("开始进行本地简历路由...")

    best_role, title_scores = choose_resume_by_job_title(job_title)

    print("本地路由分数:", title_scores)

    resumes = load_all_resumes()

    if best_role == "UNKNOWN":

        print("岗位名称未匹配到明确简历方向，启动 fallback：交给 DeepSeek 分析三份简历。")

        prompt = build_fallback_prompt(

            job_title=job_title,

            jd=jd,

            resumes=resumes,

            title_scores=title_scores

        )

    else:

        print(f"本地路由成功：推荐使用 {best_role} 简历。")

        selected_resume = resumes[best_role]

        prompt = build_single_resume_prompt(

            job_title=job_title,

            jd=jd,

            selected_role=best_role,

            selected_resume=selected_resume,

            title_scores=title_scores

        )

    print("开始调用 DeepSeek 分析...")

    result = ask_deepseek(prompt)

    print("\n====================")

    print("DeepSeek 分析结果")

    print("====================\n")

    print(result)

if __name__ == "__main__":

    main()