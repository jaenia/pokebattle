import requests

from common.constants import POKEAPI_BASE_URL


def pokemon_exists(pokemon_id):
    response = requests.head(f"{POKEAPI_BASE_URL}pokemon/{pokemon_id}")
    return bool(response)


def get_pokemon_by_id(pokemon_id):
    response = requests.get(f"{POKEAPI_BASE_URL}pokemon/{pokemon_id}")
    if response.status_code == 404:
        raise Exception(f"Pokemon not found: {pokemon_id}")
    if response.status_code != 200:
        raise Exception("Error fetching pokemon")
    pokemon_data = response.json()
    return pokemon_data


def get_pokemon_by_name(name):
    response = requests.get(f"{POKEAPI_BASE_URL}pokemon/{name}")
    if response.status_code == 404:
        raise Exception(f"Pokemon not found: {name}")
    if response.status_code != 200:
        raise Exception("Error fetching pokemon")
    pokemon_data = response.json()
    return pokemon_data


def get_all_pokemons():
    response = requests.get(f"{POKEAPI_BASE_URL}pokemon?limit=60")
    if response.status_code != 200:
        raise Exception("Error fetching pokemon list")

    has_response_next = response.json()["next"]
    pokemon_list = response.json()["results"]
    offset = 0

    while has_response_next != "null":
        offset += 60
        response = requests.get(f"{POKEAPI_BASE_URL}pokemon?limit=60&offset={offset}")
        has_response_next = response.json()["next"]
        if response.status_code != 200:
            raise Exception("Error fetching pokemon list")
        pokemon_list += response.json()["results"]

    return pokemon_list
