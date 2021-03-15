from celery.utils.log import get_task_logger

from pokebattle.celery import app as celery_app
from pokemons.services import get_all_pokemons, get_pokemon_by_name
from pokemons.models import Pokemon

logger = get_task_logger(__name__)


@celery_app.task
def save_all_pokemons_from_pokeapi():
    pokemons = get_all_pokemons()
    pokemon_names = set(p["name"] for p in pokemons)
    existing_pokemon_names = set(
        Pokemon.objects.filter(name__in=pokemon_names).values_list("name", flat=True)
    )
    missing_pokemon_names = pokemon_names - existing_pokemon_names

    pokemons_to_be_created = []
    for name in missing_pokemon_names:
        new_pokemon = get_pokemon_by_name(name)
        pokemons_to_be_created.append(
            Pokemon(
                poke_id=new_pokemon["id"],
                name=new_pokemon["name"],
                attack=new_pokemon["stats"][1]["base_stat"],
                defense=new_pokemon["stats"][2]["base_stat"],
                hit_points=new_pokemon["stats"][0]["base_stat"],
                image=new_pokemon["sprites"]["front_default"],
            )
        )
    Pokemon.objects.bulk_create(pokemons_to_be_created)

    existing_pokemons = Pokemon.objects.filter(name__in=existing_pokemon_names)
    pokemons_to_be_updated = []
    for pokemon in existing_pokemons:
        updated_pokemon = get_pokemon_by_name(pokemon.name)
        pokemons_to_be_updated.append(
            Pokemon(
                id=pokemon.id,
                poke_id=updated_pokemon["id"],
                name=updated_pokemon["name"],
                attack=updated_pokemon["stats"][1]["base_stat"],
                defense=updated_pokemon["stats"][2]["base_stat"],
                hit_points=updated_pokemon["stats"][0]["base_stat"],
                image=updated_pokemon["sprites"]["front_default"],
            )
        )

    Pokemon.objects.bulk_update(
        pokemons_to_be_updated, ["poke_id", "name", "attack", "defense", "hit_points", "image"]
    )

    logger.info("[Save all Pokemons] Save all Pokemons from PokéAPI")
