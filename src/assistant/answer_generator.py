import json
from llm import ask_gemini


def generate_answer(question, sql, rows):

    # 1. Handle empty database results
    if not rows:
        return "No matching data was found for your question."

    # 2. Convert database results into JSON
    result_data = json.dumps(
        rows,
        indent=2,
        default=str
    )

    # 3. Prepare business explanation prompt
    prompt = f"""
You are TrustLens, an e-commerce business intelligence assistant.

Your task is to answer the user's business question
using ONLY the supplied SQL results.

USER QUESTION:
{question}

SQL EXECUTED:
{sql}

DATABASE RESULTS:
{result_data}

STRICT INSTRUCTIONS:

1. Give a clear and professional business answer.
2. Mention important numbers from the results.
3. Explain rankings and patterns when relevant.
4. Never invent facts, statistics or figures.
5. Never assume information that is not in the results.
6. If the results contain no matching records,
   explain that clearly.
7. Keep the answer concise and easy to understand.
8. Do not claim causation from correlations.
9. Do not claim that a trend exists unless the results
   support that conclusion.
10. If the results are insufficient to answer the question,
    clearly mention the limitation.
11. Never use the term statistically significant unless
   a statistical test supports it.

12. Treat NULL or unknown classifications separately.
   Do not classify NULL as late or on-time.

13. Do not claim causation from comparisons or correlations.
BUSINESS ANSWER:
"""

    # 4. Generate answer using Gemini
    answer = ask_gemini(prompt)

    # 5. Check empty response
    if not answer or not answer.strip():
        return "Unable to generate a business explanation."

    return answer.strip()
