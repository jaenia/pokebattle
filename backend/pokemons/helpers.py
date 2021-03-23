from pokemons.exceptions import PokemonNotFound
from pokemons.models import Pokemon
from pokemons.services import get_pokemon_by_id, get_pokemon_by_name, pokemon_exists


def save_pokemon(poke_id):
    pokemon = Pokemon.objects.filter(poke_id=poke_id).first()

    if pokemon:
        return pokemon

    data = get_pokemon_by_id(poke_id)
    name = data["name"]
    attack = data["stats"][1]["base_stat"]
    defense = data["stats"][2]["base_stat"]
    hit_points = data["stats"][0]["base_stat"]
    image = data["sprites"]["front_default"]

    pokemon = Pokemon.objects.create(
        poke_id=poke_id,
        name=name,
        attack=attack,
        defense=defense,
        hit_points=hit_points,
        image=image,
    )

    return pokemon


def get_pokemons_points_sum(names):
    points_sum = 0
    pokemons = Pokemon.objects.filter(name__in=names)

    for pokemon in pokemons:
        points_sum += pokemon.attack + pokemon.defense + pokemon.hit_points

    existing_pokemon_names = set(
        Pokemon.objects.filter(name__in=names).values_list("name", flat=True)
    )
    missing_pokemon_names = set(names) - existing_pokemon_names

    for name in missing_pokemon_names:
        if not pokemon_exists(name):
            raise PokemonNotFound(name)
        pokemon = get_pokemon_by_name(name)
        points_sum += (
            pokemon["stats"][1]["base_stat"]
            + pokemon["stats"][2]["base_stat"]
            + pokemon["stats"][0]["base_stat"]
        )

    return points_sum
