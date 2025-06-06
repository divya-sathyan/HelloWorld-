import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_diff():
    diff = os.popen("git fetch origin main && git diff origin/main...HEAD").read()
    return diff[:4000]

def run_review(diff_text):
    prompt = f"""
You are a senior Spring Boot developer. Review the following Java code diff for:
- Spring best practices
- Clean code and readability
- Possible bugs
- Suggestions for improvement

Code diff:
{diff_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    diff = get_diff()
    if diff:
        print("=== AI Code Review Feedback ===\n")
        print(run_review(diff))
    else:
        print("No code changes to review.")
