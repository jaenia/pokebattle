from celery.utils.log import get_task_logger

from common.constants import POKEAPI_POKEMONS_LIMIT
from pokebattle.celery import app as celery_app
from pokemons.services import get_pokemon_list

logger = get_task_logger(__name__)


@celery_app.task
def save_all_pokemons_from_pokeapi():
    from pokemons.models import Pokemon

    pokemons = get_pokemon_list(POKEAPI_POKEMONS_LIMIT)
    for pokemon in pokemons:
        existing_pokemon = Pokemon.objects.filter(name=pokemon["name"]).first()

        if existing_pokemon:
            break

        poke_id = pokemon["id"]
        name = pokemon["name"]
        attack = pokemon["stats"][1]["base_stat"]
        defense = pokemon["stats"][2]["base_stat"]
        hit_points = pokemon["stats"][0]["base_stat"]
        image = pokemon["sprites"]["front_default"]

        Pokemon.objects.create(
            poke_id=poke_id,
            name=name,
            attack=attack,
            defense=defense,
            hit_points=hit_points,
            image=image,
        )

    logger.info("[Save all Pokemons] Save all Pokemons from PokéAPI")
