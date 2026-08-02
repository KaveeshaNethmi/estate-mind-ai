from pydantic import BaseModel


class PropertyFilters(BaseModel):
    city: str | None = None
    area: str | None = None
    development: str | None = None
    property_type: str | None = None
    max_price: float | None = None
    min_bedrooms: int | None = None