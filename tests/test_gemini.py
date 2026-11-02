
from llm import ask_gemini

question = "What is late delivery in e-commerce analytics?"

try:
    answer = ask_gemini(question)

    print("\nGemini Response:")
    print(answer)

except Exception as e:
    print("\nGemini connection failed:")
    print(e)
