# openai-对象
from openai import OpenAI
# 用于把.env里面的环境变量加载进python
from dotenv import load_dotenv
import os
# 时间戳工具，用于后续生成的output文件名拼接时间戳，每次调用都生成一份文件不被覆盖
from datetime import datetime
import time

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
    

# 用来生成文件夹和.md文件
def create_output_run_folder(job_title):
    """
    Create a unique output folder for each run.

    Example:
    output/2026-07-06_1530_Technical_Account_Manager/
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")

    safe_job_title = job_title.replace(" ", "_").replace("/", "_").replace("\\", "_")
    folder_name = f"{timestamp}_{safe_job_title}"

    output_path = os.path.join("output", folder_name)
    os.makedirs(output_path, exist_ok=True)

    return output_path
    

def save_file(path, content):
    """
    Save text content into a local file.
    Used for writing Markdown output files.
    """
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def extract_markdown_section(full_text, start_marker, end_marker=None):
    """
    Extract a section from the LLM response based on custom markers.

    If the marker is not found, return an empty string.
    This helps split one DeepSeek response into multiple .md files.
    """
    if start_marker not in full_text:
        return ""

    start_index = full_text.find(start_marker) + len(start_marker)

    if end_marker and end_marker in full_text:
        end_index = full_text.find(end_marker)
        return full_text[start_index:end_index].strip()

    return full_text[start_index:].strip()

def save_v04_outputs(result, job_title):

    """

    Save the DeepSeek v0.4 result into two Markdown files:

    1. English tailored resume draft

    2. Bilingual review notes

    """

    output_folder = create_output_run_folder(job_title)

    tailored_resume_en = extract_markdown_section(

        result,

        "===TAILORED_RESUME_EN_MD===",

        "===REVIEW_NOTES_BILINGUAL_MD==="

    )

    review_notes_bilingual = extract_markdown_section(

        result,

        "===REVIEW_NOTES_BILINGUAL_MD==="

    )

    if tailored_resume_en:

        save_file(

            os.path.join(output_folder, "tailored_resume_en.md"),

            tailored_resume_en

        )

    if review_notes_bilingual:

        save_file(

            os.path.join(output_folder, "review_notes_bilingual.md"),

            review_notes_bilingual

        )

    print(f"v0.4 Markdown files saved to: {output_folder}")


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

    "PRESALES_SUPPORT": "resumes/SupportEngineer.txt",

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

    "PRESALES_SUPPORT": [

        "technical sales support",

        "technical sales support specialist",

        "sales support specialist",

        "technical sales specialist",

        "application support specialist",

        "product support specialist",

        "technical specialist"

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

# v0.5.1 兼容presales相关岗位
ROUTE_TO_RESUME_PROFILE = {

    "SE": "SE",

    "PRESALES_SUPPORT": "SE",

    "CSM": "CSM",

    "TAM": "TAM"

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
你现在是一个资深招聘专员、ATS简历优化专家、简历改写专家。

你的任务是：
基于我提供的原始英文简历和目标 JD，生成一份更贴合该岗位的英文 Markdown 简历草稿。

同时，你需要生成一份中英对照的 review notes，用来解释修改逻辑、风险、缺失信息和待确认问题。

非常重要：
你必须严格遵守“事实约束改写”原则。

====================
最高优先级规则
====================

1. 不要编造我没有的经历。
2. 不要添加原简历中不存在的公司、项目、工具、技术、客户、行业、数据、成果。
3. 不要把“参与/协助”夸大成“主导/负责”，除非原简历中明确体现。
4. 不要替我编量化指标。
5. 如果原简历没有数字，不要在英文简历草稿里写占位符。
6. 如果缺少量化数据，请在 tailored_resume_en.md 中写一个不虚构数字的安全表达。
7. 需要补充的量化数据、客户规模、工具细节、业务成果等，统一放到 review_notes_bilingual.md。
8. 如果某个 JD 要求在原简历中没有证据，请明确标记为“缺失，不能生成”，并放到 review_notes_bilingual.md，不要写进英文简历正文。
9. 生成的新简历必须是可信的投递草稿，不是夸张营销文案。
10. 不要为了提高 ATS 命中而牺牲真实性。

====================
简历改写护栏 Resume Guardrails
====================

JD Requirement Classification + Stable ATS-like Match Scoring Rubric：

====================
v0.5 JD Requirement Classification
====================

Before scoring or rewriting the resume, you must first classify the JD requirements into four categories:

1. Must-have Requirements / 硬性要求
These are hard requirements that appear necessary for the role.
They are often indicated by words such as:
required, must have, minimum qualifications, proven experience, hands-on experience, strong knowledge of, fluency in, ability to, years of experience.

2. Nice-to-have Requirements / 加分项
These are preferred or bonus qualifications.
They are often indicated by words such as:
preferred, nice to have, bonus, plus, familiarity with, experience is a plus.

3. Transferable Skills / 可迁移能力
These are skills or experiences that can be demonstrated through adjacent roles or different job titles.
Examples include:
stakeholder management, cross-functional collaboration, technical troubleshooting, customer communication, onboarding, implementation support, process improvement, problem solving, documentation, product feedback, technical communication.

4. Red Flags / 高风险缺口
These are important JD requirements that are clearly missing from the resume and may significantly reduce the chance of passing screening.

Important:
- Do not treat every JD keyword as equally important.
- Must-have requirements should matter more than nice-to-have requirements.
- Transferable skills can count only when supported by concrete evidence from the original resume.
- Red flags must not be hidden or softened.

====================
v0.5 Stable ATS-like Match Scoring Rubric
====================

After classifying the JD requirements, evaluate the original resume against the JD using the fixed scoring rubric below.

Total Score: 100 points

1. Must-have Requirements Match - 35 points
Evaluate how many must-have requirements are clearly supported by the original resume.

2. Transferable Skills Match - 20 points
Evaluate whether the resume contains concrete evidence of transferable skills relevant to this role.

3. Responsibility Alignment - 20 points
Evaluate whether the resume experience aligns with the responsibilities described in the JD.

4. Nice-to-have Coverage - 10 points
Evaluate whether the resume covers preferred or bonus qualifications.

5. ATS Readability - 15 points
Evaluate whether the resume is likely to be parsed clearly by an ATS:
- clear section headings
- standard bullet points
- no tables
- no images
- no text boxes
- clear skills section
- clear job titles and dates if available

Scoring rules:
- The total score must equal the sum of the five dimensions.
- For each dimension, provide a score, evidence, and deduction reason.
- For each dimension, cite matching JD requirements.
- For each dimension, cite evidence from the original resume.
- If there is no direct or transferable evidence from the original resume, that dimension cannot receive more than 40% of its maximum score.
- Must-have requirements should be weighted more heavily than nice-to-have requirements.
- Nice-to-have requirements should not overly penalize the score if missing.
- Transferable skills can improve the score only when supported by concrete resume evidence.
- Do not give an encouraging score just to be nice.
- Do not increase the score based on information that is not present in the resume.
- Do not change the scoring standard based on how strong or weak the candidate seems.


你必须把所有可能的改写分成三类：

A. Safe Rewrite
只改变表达方式，不改变事实含义。
可以用于最终英文简历草稿。

B. Needs Confirmation
基于原简历可以合理推测，但缺少具体证据、数据或边界。
不能直接放入最终英文简历草稿，必须放到 review_notes_bilingual.md 的 Questions to Confirm 部分。

C. Not Allowed
原简历没有证据支持，或会造成夸大、虚构、职责升级。
禁止写入最终英文简历草稿。
只能放到 review_notes_bilingual.md 的 Rejected Claims 部分。

最终生成的 tailored_resume_en.md 只能包含 A 类内容。
B 类和 C 类内容不能进入 tailored_resume_en.md。

====================
你的工作流程
====================

请你严格按以下步骤完成：

第一步：从原始简历中提取“事实库”
- 只提取原简历明确出现的信息。
- 包括：岗位、职责、项目、技能、工具、合作对象、成果、业务场景。
- 不要推测。

第二步：从 JD 中提取“目标画像”
- 提取岗位关键词。
- 提取核心职责。
- 提取硬技能。
- 提取软技能。
- 提取 ATS 可能筛选的关键词。

第三步：建立“JD 要求 ↔ 简历事实证据”映射
- 哪些 JD 要求可以由原简历中的事实支持。
- 哪些 JD 要求没有对应证据。
- 哪些内容可以安全改写。
- 哪些内容不能写进新简历。

第四步：生成 tailored resume draft
- 基于原简历事实。
- 更贴合目标 JD。
- 用 ATS 友好的结构。
- 用清晰的 Markdown 格式。
- 不使用表格。
- 不使用图片。
- 不使用复杂排版。
- 不使用过度花哨标题。
- 不出现中文。
- 不出现修改说明。
- 不出现风险提醒。
- 不出现待确认问题。
- 不出现 [Metric needed] 这类占位符。
- 保留简历基本结构：
  1. Name / Contact，如果原简历有
  2. Professional Summary
  3. Core Skills / Technical Skills
  4. Professional Experience
  5. Education / Certifications，如果原简历有

第五步：生成 review notes
- 用中英对照解释修改逻辑。
- 说明匹配度。
- 说明哪些内容被强化。
- 说明哪些内容因为缺少证据没有写入。
- 说明哪些信息需要我确认。
- 说明每一处关键改写的原简历证据。

第六步：最终自检
在输出 Tailored Resume Draft 之前，请检查每一句新简历内容：

1. 是否能在原简历中找到事实依据？
2. 是否改变了原经历的责任级别？
3. 是否添加了原简历中不存在的技术、工具、客户、数据或成果？
4. 是否为了迎合 JD 而硬塞关键词？
5. 是否听起来像 AI 生成的空泛营销语言？
6. 是否包含任何中文、风险提醒、待确认项或占位符？

如果任一句不通过，请删除或降级表达。
不要为了提高匹配度牺牲真实性。

====================
输出语言要求
====================

1. tailored_resume_en.md 必须全部使用英文。
   - 这是用于真实投递的英文简历草稿。
   - 不要出现中文解释。
   - 不要中英混排。
   - 不要写中文提示。
   - 不要出现 [Metric needed] 或任何占位符。
   - 缺少量化数据时，写安全但不虚构的英文表达。
   - 所有待确认项放到 review_notes_bilingual.md。

2. review_notes_bilingual.md 使用中英对照。
   - 用来帮助我理解修改逻辑。
   - 先英文，后中文。
   - 可以包含分析、修改原因、风险提醒、缺失信息、待确认问题。
   - 不用于投递。

====================
输出格式要求
====================

你必须严格使用以下两个分隔标记，方便程序保存成两个 .md 文件。

===TAILORED_RESUME_EN_MD===

# Tailored Resume Draft

Please generate a complete English Markdown resume draft.

Requirements:
- Use English only.
- This version should be suitable for job application review.
- Keep all factual information grounded in the original resume.
- Do not invent companies, projects, tools, metrics, customers, industries, responsibilities, or achievements.
- Do not exaggerate responsibility level.
- Do not include placeholders such as [Metric needed].
- If metrics are missing, write a safe non-quantified version and mention the metric request only in review notes.
- Use ATS-friendly formatting.
- Do not use tables, images, text boxes, or complex layout.
- Keep the structure:
  1. Name / Contact if available in the original resume
  2. Professional Summary
  3. Core Skills / Technical Skills
  4. Professional Experience
  5. Education / Certifications if available

===REVIEW_NOTES_BILINGUAL_MD===

# Review Notes / 修改复盘

Please provide bilingual review notes. Write English first, then Chinese for each section.

## 1. JD Role Analysis / JD岗位分析

English:
- Job Title:
- Local Router Result:
- Role Type: SE / CSM / TAM / Hybrid
- Core Responsibilities:
- Core ATS Keywords:
- Hidden Screening Criteria:

中文：
- 岗位名称：
- 本地路由结果：
- 岗位类型：SE / CSM / TAM / 混合型
- 核心职责：
- 核心 ATS 关键词：
- 隐藏筛选标准：

## 2. JD Requirement Classification / JD要求分类

English:

### Must-have Requirements

1.

2.

3.

### Nice-to-have Requirements

1.

2.

3.

### Transferable Skills

1.

2.

3.

### Red Flags

1.

2.

3.

中文：

### 硬性要求

1.

2.

3.

### 加分项

1.

2.

3.

### 可迁移能力

1.

2.

3.

### 高风险缺口

1.

2.

3.

## 3. Stable ATS-like Match Score / 稳定 ATS-like 匹配度评分

English:
- Total Score: xx/100
- Match Type: Strong / Medium / Weak

Score Breakdown:
1. Must-have Requirements Match: xx/35
   Matching JD Requirements:
   Evidence From Original Resume:
   Deductions:

2. Transferable Skills Match: xx/20
   Matching JD Requirements:
   Evidence From Original Resume:
   Deductions:

3. Responsibility Alignment: xx/20
   Matching JD Requirements:
   Evidence From Original Resume:
   Deductions:

4. Nice-to-have Coverage: xx/10
   Matching JD Requirements:
   Evidence From Original Resume:
   Deductions:

5. ATS Readability: xx/15
   Evidence From Original Resume:
   Deductions:

Score Diagnosis:
- Main reason for the score: 
  A. True hard-requirement mismatch
  B. Relevant experience exists but is under-presented
  C. Resume profile is not ideal
  D. JD is ambiguous or hybrid
  E. Stretch role with transferable potential
- Explanation:

Application Decision:
- Apply Priority: High / Medium / Low
- Stretch Fit Potential: High / Medium / Low
- Resume Fixability: High / Medium / Low
- Recommended Action: Apply / Apply with light tailoring / Apply with heavy tailoring / Do not prioritize

中文：
- 总分：xx/100
- 匹配类型：强匹配 / 中等匹配 / 弱匹配

评分拆解：
1. 硬性要求匹配：xx/35
   匹配的 JD 要求：
   原简历证据：
   扣分原因：

2. 可迁移能力匹配：xx/20
   匹配的 JD 要求：
   原简历证据：
   扣分原因：

3. 职责匹配：xx/20
   匹配的 JD 要求：
   原简历证据：
   扣分原因：

4. 加分项覆盖：xx/10
   匹配的 JD 要求：
   原简历证据：
   扣分原因：

5. ATS 可读性：xx/15
   原简历证据：
   扣分原因：

分数诊断：
- 当前分数的主要原因：
  A. 真实硬性条件不匹配
  B. 相关经历存在但简历呈现不足
  C. 当前简历方向不够理想
  D. JD 本身模糊或混合
  E. 属于有可迁移潜力的 stretch role
- 解释：

投递决策：
- 投递优先级：高 / 中 / 低
- Stretch Fit 潜力：高 / 中 / 低
- 简历可优化空间：高 / 中 / 低
- 建议动作：投递 / 简单修改后投递 / 深度定制后投递 / 不优先投递

## 4. Evidence-Based Match / 基于证据的匹配分析

For each important JD requirement, provide:

English:
- JD Requirement:
- Evidence From Original Resume:
- Can Be Used in Resume: Yes / No
- Explanation:

中文：
- JD要求：
- 原简历证据：
- 是否可以写进新简历：是 / 否
- 说明：

## 5. Change Log / 修改记录

For each key change:

English:
- Original:
- Rewritten:
- Reason:
- JD Keywords Added:
- Evidence From Original Resume:
- Safety Category: Safe Rewrite / Needs Confirmation / Not Allowed
- New Fact Added: Yes / No
- Needs User Confirmation: Yes / No

中文：
- 原句：
- 改写后：
- 修改原因：
- 加入或强化的 JD 关键词：
- 原简历证据：
- 安全分类：安全改写 / 需要确认 / 禁止写入
- 是否新增事实：是 / 否
- 是否需要我确认：是 / 否

## 6. Rejected Claims / 被拒绝写入的内容

List claims that might help match the JD but cannot be included because the original resume does not provide enough evidence.

English:
- Claim:
- Why Rejected:
- Missing Evidence:
- How User Can Confirm:

中文：
- 被拒绝内容：
- 为什么不能写：
- 缺少什么证据：
- 如果是真的，我需要确认什么：

## 7. Questions to Confirm / 待确认问题

List questions that would help generate a stronger ATS-optimized resume in the next iteration.

English:
- Question:
- Why It Matters:
- Resume Section It Can Improve:

中文：
- 问题：
- 为什么重要：
- 可以优化哪个简历部分：

====================
以下是目标岗位名称
====================

{job_title}

====================
以下是目标岗位 JD
====================

{jd}

====================
以下是原始英文简历
====================

{selected_resume}
"""
    return prompt
# =========================

# 6. Prompt：匹配失败时，fallback 三份简历结合一下分析哪份更适合，主要的分析工作还是留给主流程做

# =========================
def build_fallback_prompt(job_title, jd, title_scores):
    prompt = f"""
You are a resume routing assistant.

The local title-based router could not confidently match this job title to a resume profile.

Your task is to analyze the full job description and select the most suitable resume profile.

Available resume profiles:

1. SE
Use this profile when the role is closest to:
- Support Engineer
- Technical Support Engineer
- Product Support
- Application Support
- Solution Engineer
- Pre-sales Engineer
- Technical troubleshooting
- Technical customer communication

2. PRESALES_SUPPORT
Use this profile when the role is closest to:
- Technical Sales
- Technical Sales Support
- Sales Support with technical responsibilities
- Solution support
- Pre-sales support
- Product consultation
- Customer-facing technical sales support

3. CSM
Use this profile when the role is closest to:
- Customer Success Manager
- Customer Success
- Customer Adoption
- Customer Relationship Management
- Account growth
- Renewal / retention support
- Customer onboarding from a relationship perspective

4. TAM
Use this profile when the role is closest to:
- Technical Account Manager
- Implementation Consultant
- Technical Consultant
- Customer Engineer
- Enterprise technical relationship management
- Post-sales technical ownership
- Implementation / integration support

5. UNKNOWN
Use UNKNOWN only when the JD is clearly outside these directions or there is not enough evidence to choose.

Important rules:
- Do not rely only on the job title.
- Use the full JD responsibilities and requirements.
- Prefer the profile that best matches the actual work described in the JD.
- If the role is hybrid, choose the closest primary profile.
- Return only one final selected profile.
- Do not generate a resume.
- Do not generate full review notes.
- Keep the reason brief.
- The final resume and bilingual review notes will be generated by another prompt later.

Output format:
You must use exactly this format:

SELECTED_PROFILE: SE / PRESALES_SUPPORT / CSM / TAM / UNKNOWN
REASON_EN: one short English explanation
REASON_ZH: 一句简短中文解释

====================
Job Title
====================
{job_title}

====================
Local Router Scores
====================
{title_scores}

====================
Job Description
====================
{jd}
"""
    return prompt


def parse_selected_resume_profile(selection_result):
    """
    Parse the selected resume profile from the fallback selection result.

    Expected format:
    SELECTED_PROFILE: SE
    or
    SELECTED_PROFILE: PRESALES_SUPPORT
    or
    SELECTED_PROFILE: CSM
    or
    SELECTED_PROFILE: TAM
    or
    SELECTED_PROFILE: UNKNOWN
    """

    valid_profiles = ["SE", "PRESALES_SUPPORT", "CSM", "TAM", "UNKNOWN"]

    for line in selection_result.splitlines():
        line = line.strip()

        if line.startswith("SELECTED_PROFILE:"):
            profile = line.replace("SELECTED_PROFILE:", "").strip()

            if profile in valid_profiles:
                return profile

    return "UNKNOWN"



# =========================

# 7. 调用 DeepSeek
# v0.5新增重试机制以防连接不稳定报错
# v0.6新增prompt束缚，否则会出现输出太多偷懒
# =========================
from openai import APIConnectionError
REQUIRED_MARKERS = [

    "===TAILORED_RESUME_EN_MD===",

    "===REVIEW_NOTES_BILINGUAL_MD==="

]

def ask_deepseek(prompt):

    max_retries = 3

    for attempt in range(max_retries):

        try:

            final_prompt = prompt

            if attempt > 0:

                final_prompt = prompt + """

IMPORTANT:

Your previous response was incomplete or did not follow the required output format.

You must include BOTH of the following exact markers:

===TAILORED_RESUME_EN_MD===

===REVIEW_NOTES_BILINGUAL_MD===
If the content is long, make the review notes concise, but do not omit them.

Do not stop after the tailored resume.

Do not omit the review notes.

Do not rename the markers.

Output both sections completely.

"""

            response = client.chat.completions.create(

                model="deepseek-chat",

                messages=[

                    {"role": "user", "content": final_prompt}

                ],

                temperature=0,

                max_tokens=8000,

                timeout=60

            )

            result = response.choices[0].message.content

            missing_markers = [

                marker for marker in REQUIRED_MARKERS

                if marker not in result

            ]

            if not missing_markers:

                return result

            print(f"DeepSeek output format incomplete. Attempt {attempt + 1}/{max_retries}")

            print("Missing markers:", missing_markers)

            if attempt < max_retries - 1:

                print("Retrying with stricter format instruction in 5 seconds...")

                time.sleep(5)

            else:

                raise ValueError(f"DeepSeek response missing required markers: {missing_markers}")

        except Exception as error:

            print(f"DeepSeek API call failed. Attempt {attempt + 1}/{max_retries}")

            print("Error:", error)

            if attempt < max_retries - 1:

                print("Retrying in 5 seconds...")

                time.sleep(5)

            else:

                raise            

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

        print("岗位名称未匹配到明确简历方向，启动 fallback：让 DeepSeek 根据完整 JD 选择简历方向。")

        selection_prompt = build_fallback_prompt(

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

        prompt = build_single_resume_prompt(

            job_title=job_title,

            jd=jd,

            selected_role=selected_route,

            selected_resume=selected_resume,

            title_scores=title_scores

        )


    else:
        print(f"本地路由成功：推荐使用 {best_role} 简历。")
        selected_resume = resumes[best_role]
        selected_resume_profile = ROUTE_TO_RESUME_PROFILE[best_role]
        selected_resume = resumes[selected_resume_profile]
        print(f"本地路由成功：岗位方向为 {best_role}，实际使用 {selected_resume_profile} 简历。")

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

    save_v04_outputs(result, job_title)

if __name__ == "__main__":
    main()
