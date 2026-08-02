

from typing import Literal

from pydantic import BaseModel, Field


class EntityReference(BaseModel):
    uses_previous_results: bool = False

    action: Literal[
        "new_search",
        "select_by_rank",
        "select_from_current",
        "use_focused",
    ] = "new_search"

    ranks: list[int] = Field(default_factory=list)

    operation: Literal[
        "none",
        "cheapest",
        "most_expensive",
        "highest_rental_yield",
        "lowest_rental_yield",
        "highest_roi",
        "lowest_roi",
    ] = "none"

    property_name: str | None = None