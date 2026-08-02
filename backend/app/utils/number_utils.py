from typing import TypeAlias


NumericValue: TypeAlias = float | int | str


def clamp_score(
    value: NumericValue | None,
    default: float = 0.0,
) -> float:
    """
    Convert a value to a float and constrain it to the range 0.0–1.0.
    Invalid or missing values return the supplied default.
    """

    numeric_value = to_float(value)

    if numeric_value is None:
        return max(0.0, min(1.0, default))

    return max(0.0, min(1.0, numeric_value))


def to_float(
    value: NumericValue | None,
) -> float | None:
    """
    Convert a supported numeric value to float.
    Return None when the value is missing or cannot be converted.
    """

    if value is None or value == "":
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None