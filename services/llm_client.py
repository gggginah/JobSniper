from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os
import time
import sys



client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def ask_deepseek(prompt, required_markers=None, max_tokens=8000):
    max_retries = 3

    for attempt in range(max_retries):
        try:
            final_prompt = prompt

            if required_markers and attempt > 0:
                final_prompt = prompt + """

IMPORTANT:
Your previous response was incomplete or did not follow the required output format.
You must include all required exact markers.
Do not rename the markers.
Do not omit required sections.
"""

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "user", "content": final_prompt}
                ],
                temperature=0,
                max_tokens=max_tokens,
                timeout=60
            )

            result = response.choices[0].message.content

            if required_markers:
                missing_markers = [
                    marker for marker in required_markers
                    if marker not in result
                ]

                if not missing_markers:
                    return result

                print(f"DeepSeek output format incomplete. Attempt {attempt + 1}/{max_retries}")
                print("Missing markers:", missing_markers)

                if attempt < max_retries - 1:
                    print("Retrying with stricter format instruction in 5 seconds...")
                    time.sleep(5)
                    continue

                raise ValueError(f"DeepSeek response missing required markers: {missing_markers}")

            return result

        except Exception as error:
            print(f"DeepSeek API call failed. Attempt {attempt + 1}/{max_retries}")
            print("Error:", error)

            if attempt < max_retries - 1:
                print("Retrying in 5 seconds...")
                time.sleep(5)
            else:
                raise

