import re

CITATION_PATTERN = re.compile(r"\[(\d+)]")


def add_citation_ids(results: list[dict]) -> list[dict]:
    """
    Add stable citation identifiers to the final reranked results.
    """

    cited_results: list[dict] = []

    for index, result in enumerate(results, start=1):
        updated_result = result.copy()
        updated_result["citation_id"] = index
        cited_results.append(updated_result)

    return cited_results


def build_citation_context(results: list[dict]) -> str:
    """
    Create the property context passed to the answer-generating model.
    """

    context_parts: list[str] = []

    for result in results:
        property_data = result.get("property", {})
        citation_id = result.get("citation_id")

        context_parts.append(f"""
Source [{citation_id}]
Property ID: {property_data.get("property", {})}
Name: {property_data.get("property_name")}
City: {property_data.get("city")}
Area: {property_data.get("area")}
Development: {property_data.get("development")}
City: {property_data.get("area")}
Area: {property_data.get("area")}
Development: {property_data.get("development")}
Type: {property_data.get("property_type")}
Price: {property_data.get("price")}
Bedrooms: {property_data.get("bedrooms")}
Bathrooms: {property_data.get("bathrooms")}
Rental Yield: {property_data.get("rental_yield")}
ROI: {property_data.get("roi_15")}
Details: {property_data.get("semantic_text")}
""".strip())

    return "\n\n".join(context_parts)


def extract_citations(
    answer: str,
    results: list[dict],
) -> list[dict]:
    """
    Extract valid citation references used in the generated answer.
    """

    cited_ids = {int(match) for match in CITATION_PATTERN.findall(answer)}

    citations: list[dict] = []

    for result in results:
        citation_id = result.get("citation_id")

        if citation_id not in cited_ids:
            continue

        property_data = result.get("property", {})

        citations.append(
            {
                "citation_id": citation_id,
                "property_id": property_data.get("property_id"),
                "property_name": property_data.get("property_name"),
                "city": property_data.get("city"),
                "area": property_data.get("area"),
                "development": property_data.get("development"),
                "price": property_data.get("price"),
                "rental_yield": property_data.get("rental_yield"),
                "roi_15": property_data.get("roi_15"),
                "rerank_score": result.get("rerank_score"),
            }
        )

    citations.sort(key=lambda citation: citation["citation_id"])

    return citations


def remove_invalid_citations(
    answer: str,
    results: list[dict],
) -> str:
    """
    Remove citation numbers that do not correspond to a supplied source.
    """

    valid_ids = {result.get("citation_id") for result in results}

    def replace_invalid(match: re.Match[str]) -> str:
        citation_id = int(match.group(1))

        if citation_id in valid_ids:
            return match.group(0)

        return ""

    return CITATION_PATTERN.sub(
        replace_invalid,
        answer,
    )
