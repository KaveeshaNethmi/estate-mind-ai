import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.manual_rag.llm_service import generate_answer


def main():
    question = "Show me furnished apartments in Meydan with good rental yield"

    response = generate_answer(question, top_k=5)

    print("\nAI Answer:")
    print(response["answer"])

    print("\nSources:")
    for source in response["sources"]:
        property_data = source["property"]

        print("\n-------------------------")
        print(f"Rank: {source['rank']}")
        print(f"Score: {source['score']}")
        print(f"Name: {property_data.get('property_name')}")
        print(f"Area: {property_data.get('area')}")
        print(f"Price: {property_data.get('price')}")


if __name__ == "__main__":
    main()
