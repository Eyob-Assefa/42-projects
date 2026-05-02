# Importing spellbook at the top level while spellbook is still initializing
from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed: list[str] = dark_spell_allowed_ingredients()
    ingredients_lower: str = ingredients.lower()
    is_valid: bool = any(item in ingredients_lower for item in allowed)

    status: str = "VALID" if is_valid else "INVALID"
    return f"{ingredients} {status}"
