from openai import OpenAI, api_key

from app.core.config import CHAT_MODEL, OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def format_search_state(search_state: dict) -> str:
    active_filters = [
        f"{key}: {value}" for key, value in search_state.items() if value is not None
    ]

    if not active_filters:
        return "No active serach filters."

    return "\n".join(active_filters)


def rewrite_query(question: str, chat_history: str, search_state: dict) -> str:
    """
    Convert a potentially incomplete follow-up question into a
    sef-contained query suitable for semantic retrieval.
    """

    state_text = format_search_state(search_state)

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You rewrite real estate search questions for semantic "
                    "retrieva;. Return only the rewitten query without "
                    "expectations, labels, quotation marks, or Markdown"
                ),
            },
            {
                "role": "user",
                "content": f"""
Rewrite the current question as a clear, self-contained real estate
retrieval query.

Use the previous conversation and active search filters only when they
help clarify the user's meaning.

Rules:
- Preserve the user's original intent.
- Resolve references such as "those", "them", "which one", and "the cheaper one".
- Include relevant active filters naturally.
- Do not invent property details or filters.
- Do not answer the question.
- Return only one rewritten query.
- If the current question is already self-contained, return it unchanged.

Previous conversation:
{chat_history}

Active search filters:
{state_text}

Current question:
{question}
""",
            },
        ],
        temperature=0,
    )

    rewritten_query = response.choices[0].message.content

    if rewritten_query is None or not rewritten_query.strip():
        return question
    
    return rewritten_query.strip()