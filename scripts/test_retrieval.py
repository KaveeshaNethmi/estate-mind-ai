import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.retrieval_service import retrieve_similar_properties

print(__name__)


def main():
    query = "Show me furnished apartments in Meydan with good rental yield"

    results = retrieve_similar_properties(query, top_k=5)

    for result in results:
        property_data = result["property"]

        print("\n-------------------------")
        print(f"Rank: {result['rank']}")
        print(f"Score: {result['score']}")
        print(f"Name: {property_data.get('property_name')}")
        print(f"Area: {property_data.get('area')}")
        print(f"Development: {property_data.get('development')}")
        print(f"Price: {property_data.get('price')}")
        print(f"Bedrooms: {property_data.get('bedrooms')}")


if __name__ == "__main__":
    main()
