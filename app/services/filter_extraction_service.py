import json

from openai import OpenAI

from app.core.config import CHAT_MODEL, OPENAI_API_KEY
from app.schemas.filter_schema import PropertyFilters

client = OpenAI(api_key=OPENAI_API_KEY)

def clean_json_response(content: str) -> str:
    content = content.strip()

    if content.startswith("```json"):
        content = content.replace("```json", "", 1)

    if content.startswith("```"):
        content = content.replace("```", "", 1)

    if content.endswith("```"):
        content = content[:-3]

    return content.strip()

def extract_filters_from_question(question: str) -> PropertyFilters:
    prompt = f"""
Extract real estate search filters from the user's question.property

Return ONLY valid JSON.

Supported fields:
- city: string or null
- area: string or null
- development: string or null
- property_type: string or null
- max_price: number or null
- min_bedrooms: integer or null

Rules:
- If a value is not mentioned, return null.
- Do not guess missing values.
- Convert prices like "1.2M", "1.2 million", and "AED 1.2M" into numeric values.
- "apartments" → property_type = "Apartment"
- "villas" → property_type = "Villa"
- "townhouses" → property_type = "Townhouse"
- If the user mentions an area or community (e.g., Meydan, Dubai Marina, Downtown Dubai), map it to the `development` field because the current dataset stores location information there.
- Return valid JSON only. Do not include Markdown or code fences.

User question:
{question}
"""

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You extract structured real estate filters from user questions.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
    )

    DEFAULT_FILTERS = PropertyFilters()

    content = response.choices[0].message.content

    if content is None:
        return DEFAULT_FILTERS

    try:
        cleaned_content = clean_json_response(content)
        return PropertyFilters.model_validate_json(cleaned_content)
    except ValueError:
        return DEFAULT_FILTERS
