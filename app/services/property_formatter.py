from bson.decimal128 import Decimal128


def to_float(value, default=0.0):
    if value is None:
        return default

    try:
        if isinstance(value, Decimal128):
            return float(value.to_decimal())

        return float(value)

    except (ValueError, TypeError):
        return default


def convert_property_to_text(property_data):
    rental_yield = to_float(property_data.get("rental_yield", 0)) * 100

    return f"""
    {property_data.get("property_name")} is a
    {property_data.get("bedrooms_total")} bedroom
    {property_data.get("property_type")} located in
    {property_data.get("development")}
    {property_data.get("area")}
    {property_data.get("city_name")}.
    
    The property spans
    {property_data.get("total_area_sqft")} square feet
    and is listed for 
    {property_data.get("asking_price")} AED.
    
    It contains 
    {property_data.get("bathrooms_total")} bathrooms.
    
    The rental yield is approximately
    {rental_yield:.2f}%.
    
    The ROI over year is 
    {property_data.get("roi_15")}%.
    
    Description:
    {property_data.get("description", "")}    
    """
