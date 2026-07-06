import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.filter_extraction_service import extract_filters_from_question


def main():
    questions = [
        "Show me apartments in Meydan under AED 1.2M",
        "Find villas in Dubai Marina with at least 3 bedrooms",
        "Only show properties below 900000 AED",
    ]

    for question in questions:
        filters = extract_filters_from_question(question)

        print("\nQuestion:", question)
        print("Extracted filters:", filters.model_dump())


if __name__ == "__main__":
    main()
    