from .light_spellbook import light_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed = light_spell_allowed_ingredients()

    ingredients_lower = ingredients.lower()
    is_valid = any(item in ingredients_lower for item in allowed)

    status = "VALID" if is_valid else "INVALID"
    return f"{ingredients} {status}"
