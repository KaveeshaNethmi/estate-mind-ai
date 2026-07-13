import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.query_rewriting_service import rewrite_query


def main():
    test_cases = [
        {
            "question": "Which one has the best rental yield?",
            "chat_history": (
                "USER: Show me apartments in Meydan under AED 1.2M.\n"
                "ASSISTANT: I found several matching apartments."
            ),
            "search_state": {
                "city": None,
                "area": None,
                "development": "Meydan",
                "property_type": "Apartment",
                "max_price": 1_200_000,
                "min_bedrooms": None,
            },
        },
        {
            "question": "Show me villas in Dubai with at least 3 bedrooms.",
            "chat_history": "No previous conversation.",
            "search_state": {
                "city": "Dubai",
                "area": None,
                "development": None,
                "property_type": "Villa",
                "max_price": None,
                "min_bedrooms": 3,
            },
        },
    ]

    for test_case in test_cases:
        rewritten = rewrite_query(
            question=test_case["question"],
            chat_history=test_case["chat_history"],
            search_state=test_case["search_state"],
        )

        print("\nOriginal:")
        print(test_case["question"])

        print("\nRewritten:")
        print(rewritten)

        print("-" * 60)


if __name__ == "__main__":
    main()