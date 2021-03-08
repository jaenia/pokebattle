from celery.utils.log import get_task_logger

from pokebattle.celery import app as celery_app
from pokemons.services import get_all_pokemons, get_pokemon_by_name
from pokemons.models import Pokemon

logger = get_task_logger(__name__)


@celery_app.task
def save_all_pokemons_from_pokeapi():
    pokemons = get_all_pokemons()

    for pokemon in pokemons:
        existing_pokemon = Pokemon.objects.filter(name=pokemon["name"]).first()

        if existing_pokemon:
            continue

        new_pokemon = get_pokemon_by_name(pokemon["name"])
        poke_id = new_pokemon["id"]
        name = new_pokemon["name"]
        attack = new_pokemon["stats"][1]["base_stat"]
        defense = new_pokemon["stats"][2]["base_stat"]
        hit_points = new_pokemon["stats"][0]["base_stat"]
        image = new_pokemon["sprites"]["front_default"]

        Pokemon.objects.create(
            poke_id=poke_id,
            name=name,
            attack=attack,
            defense=defense,
            hit_points=hit_points,
            image=image,
        )

    logger.info("[Save all Pokemons] Save all Pokemons from PokéAPI")
