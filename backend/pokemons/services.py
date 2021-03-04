import requests

from common.constants import POKEAPI_BASE_URL


def pokemon_exists(pokemon_id):
    response = requests.head(f"{POKEAPI_BASE_URL}pokemon/{pokemon_id}")
    return bool(response)


def get_pokemon(pokemon_id):
    response = requests.get(f"{POKEAPI_BASE_URL}pokemon/{pokemon_id}")
    if response.status_code == 404:
        raise Exception(f"Pokemon not found: {pokemon_id}")
    if response.status_code != 200:
        raise Exception("Error fetching pokemon")
    pokemon_data = response.json()
    return pokemon_data


def get_pokemon_list(limit):
    response = requests.get(f"{POKEAPI_BASE_URL}pokemon?limit={limit}")
    if response.status_code != 200:
        raise Exception("Error fetching pokemon list")
    pokemon_list = response.json()["results"]
    return pokemon_list
