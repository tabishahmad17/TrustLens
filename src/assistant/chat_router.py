from llm import ask_gemini
from assistant import ask_trustlens


def classify_message(question):

    text = question.lower().strip()

    # SQL and programming learning questions
    learning_keywords = [
        "explain", "what is", "difference between",
        "how does", "how to", "where vs having",
        "group by", "order by", "join", "cte",
        "subquery", "primary key", "foreign key",
        "sql", "python", "interview", "query",
        "aggregate", "window function"
    ]

    # TrustLens business analytics questions
    business_keywords = [
        "revenue", "gmv", "sales", "orders",
        "customers", "sellers", "late delivery",
        "late deliveries", "delivery rate",
        "review score", "customer satisfaction",
        "freight", "payment", "business performance",
        "top 10 sellers", "monthly kpi"
    ]

    if any(word in text for word in business_keywords):
        return "BUSINESS"

    if any(word in text for word in learning_keywords):
        return "GENERAL"

    return "GENERAL"



def route_message(question):

    text = question.lower().strip()

    # Handle greetings without Gemini
    greetings = [
        "hello", "hi", "hey",
        "good morning", "good afternoon",
        "good evening"
    ]

    if text in greetings:
        return {
            "type": "general",
            "answer": (
                "Hello! Welcome to TrustLens AI. "
                "I can help you learn SQL and analyze "
                "e-commerce business data."
            )
        }

    intent = classify_message(question)

    if intent == "GENERAL":

        answer = ask_gemini(question)

        return {
            "type": "general",
            "answer": answer
        }

    elif intent == "BUSINESS":

        result = ask_trustlens(question)

        if not result.get("success"):
            return {
                "type": "business",
                "answer": result.get(
                    "error",
                    "Business query failed. Please try again."
                ),
                "sql": result.get("sql"),
                "rows": None
            }

        return {
            "type": "business",
            "answer": result.get("answer"),
            "sql": result.get("sql"),
            "rows": result.get("rows")
        }

    return {
        "type": "clarification",
        "answer": "Could you please clarify your question?"
    }
