import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from app.services.entity_reference_service import (
    detect_entity_reference,
    resolve_entity_reference,
)


def retrieval_results_to_properties(
    retrieval_results: list[dict],
) -> list[dict]:
    """
    Convert resolved retrieval results back into the stored-property
    structure used as current_selection.
    """

    properties: list[dict] = []

    for result in retrieval_results:
        property_data = result.get("property", {})

        properties.append(
            {
                "rank": result.get("rank"),
                "score": result.get("score"),
                **property_data,
            }
        )

    return properties


def main() -> None:
    # The complete result set from the latest real search.
    # This must remain unchanged during follow-up questions.
    search_results = [
        {
            "rank": 1,
            "score": 0.91,
            "property_id": "property-1",
            "property_name": "Meydan Residence A",
            "price": 950000,
            "rental_yield": 6.1,
            "roi_15": 72.0,
        },
        {
            "rank": 2,
            "score": 0.88,
            "property_id": "property-2",
            "property_name": "Meydan Residence B",
            "price": 1100000,
            "rental_yield": 5.7,
            "roi_15": 79.0,
        },
        {
            "rank": 3,
            "score": 0.85,
            "property_id": "property-3",
            "property_name": "Meydan Residence C",
            "price": 1020000,
            "rental_yield": 6.5,
            "roi_15": 76.0,
        },
    ]

    # After a new search, the current selection initially contains all
    # returned properties.
    current_selection = search_results.copy()

    # There is no focused property until a follow-up resolves to one item.
    focused_property: dict | None = None

    chat_history = (
        "USER: Show me apartments in Meydan.\n"
        "ASSISTANT: I found three matching properties."
    )

    questions = [
        "Compare the first two.",
        "Which is the cheaper one?",
        "What is its ROI?",
        "Compare the first three again.",
        "Which one has the highest rental yield?",
        "Show me villas in another development.",
    ]

    for question in questions:
        reference = detect_entity_reference(
            question=question,
            chat_history=chat_history,
            search_results=search_results,
            current_selection=current_selection,
            focused_property=focused_property,
        )

        selected_results = resolve_entity_reference(
            reference=reference,
            search_results=search_results,
            current_selection=current_selection,
            focused_property=focused_property,
        )

        reused_previous_results = bool(selected_results)

        print("\n" + "=" * 70)
        print("Question:", question)
        print("Reference:", reference.model_dump())
        print("Reused previous results:", reused_previous_results)

        if selected_results:
            selected_names = [
                result.get("property", {}).get("property_name")
                for result in selected_results
            ]

            print("Selected:", selected_names)

            # Simulate save_current_selection().
            current_selection = retrieval_results_to_properties(
                selected_results
            )

            # Simulate focused_property behavior.
            focused_property = (
                current_selection[0]
                if len(current_selection) == 1
                else None
            )

        else:
            print("Selected: []")

            if reference.action == "new_search":
                print(
                    "A new Pinecone retrieval should be performed here."
                )

        print(
            "Current selection:",
            [
                property_data.get("property_name")
                for property_data in current_selection
            ],
        )

        print(
            "Focused property:",
            (
                focused_property.get("property_name")
                if focused_property
                else None
            ),
        )

        # Simulate adding the turn to conversation history.
        chat_history += (
            f"\nUSER: {question}"
            f"\nASSISTANT: Test response generated."
        )


if __name__ == "__main__":
    main()