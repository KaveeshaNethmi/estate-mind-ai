def merge_search_state(
    current_state: dict,
    city: str | None = None,
    area: str | None = None,
    development: str | None = None,
    property_type: str | None = None,
    max_price: float | None = None,
    min_bedrooms: int | None = None,
) -> dict:
    updated_state = current_state.copy() if current_state else {}

    incoming_filters = {
        "city": city,
        "area": area,
        "development": development,
        "property_type": property_type,
        "max_price": max_price,
        "min_bedrooms": min_bedrooms,
    }

    for key, value in incoming_filters.items():
        if value is not None:
            updated_state[key] = value

    return updated_state
