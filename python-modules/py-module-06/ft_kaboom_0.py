import alchemy.grimoire.light_spellbook

print("=== Kaboom 0 ===")
print("Using grimoire module directly")

spell_result = alchemy.grimoire.light_spellbook.light_spell_record(
    'Fantasy', 'Earth, wind and fire'
)

print(f"Testing record light spell: {spell_result}")
