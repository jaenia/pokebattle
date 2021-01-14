from pokemons.models import Pokemon
from pokemons.services import get_pokemon


def save_pokemon(poke_id):
    pokemon = Pokemon.objects.filter(poke_id=poke_id).first()

    if pokemon:
        return pokemon

    data = get_pokemon(poke_id)
    attack = data["stats"][4]["base_stat"]
    defense = data["stats"][3]["base_stat"]
    hit_points = data["stats"][5]["base_stat"]

    pokemon = Pokemon.objects.create(
        poke_id=poke_id,
        name=data["name"],
        attack=attack,
        defense=defense,
        hit_points=hit_points
    )

    return pokemon
