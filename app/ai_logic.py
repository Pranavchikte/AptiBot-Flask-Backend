import os
import google.generativeai as genai
from io import StringIO
import sys

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')


def solve_problem(user_query: str, chat_history: list) -> str:
    
    
    chat = model.start_chat(history=chat_history)

    prompt_for_code = f"""You are a Python expert. Convert the following math problem into a Python script that uses the SymPy library to solve it. The script must:

    Import SymPy properly.
    Define and solve the problem step by step.
    Print the final result on a new line, prefixed with "FINAL_ANSWER:".
    Only output the raw Python code. Do not include markdown formatting or commentary.
    
    Problem: "{user_query}"
    """
    
    try:
        
        code_response = chat.send_message(prompt_for_code)
        generated_code = code_response.text.strip().replace("`", "").replace("python", "")
        
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        exec(generated_code)
        sys.stdout = old_stdout
        
        full_output = redirected_output.getvalue().strip()
        
        if "FINAL_ANSWER:" in full_output:
            correct_answer = full_output.split("FINAL_ANSWER:")[-1].strip()
        else:
            correct_answer = full_output.splitlines()[-1] if full_output else "No answer found"

        
        prompt_for_explanation = f"""You are a friendly math professor who explains problems in a clear, structured, and encouraging way.
        The student’s problem is: "{user_query}"
        The correct final answer is: "{correct_answer}"

        Your task:
        Provide a clear step-by-step explanation that logically leads to the final answer.
        Use Hinglish encouragement phrases naturally (e.g., "Chalo, let's start", "Bas thoda aur, ho gaya!").
        Always format all mathematical expressions using proper LaTeX delimiters: $...$ for inline and $$...$$ for block.
        Organize your explanation in numbered steps.
        End with a short, positive summary reinforcing the correct final answer.
        Maintain a warm, motivating, and approachable tone.
        """
    
        explanation_response = chat.send_message(prompt_for_explanation)
        return explanation_response.text

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I encountered an error while trying to solve this problem. Please try rephrasing."
