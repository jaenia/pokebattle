from decouple import config  # noqa
from templated_email import send_templated_mail


def compare_pokemons(pokemon_1, pokemon_2):
    pokemon_1_victory_points = 0
    pokemon_2_victory_points = 0

    if pokemon_1.attack > pokemon_2.defense:
        pokemon_1_victory_points += 1
    else:
        pokemon_2_victory_points += 1

    if pokemon_2.attack > pokemon_1.defense:
        pokemon_2_victory_points += 1
    else:
        pokemon_1_victory_points += 1

    if pokemon_1_victory_points == 2:  # pokemon_1 wins # noqa
        return pokemon_1
    elif pokemon_2_victory_points == 2:  # pokemon_2 wins
        return pokemon_2
    elif pokemon_1.hit_points > pokemon_2.hit_points:  # in case of draw
        return pokemon_1
    else:
        return pokemon_2


def get_battle_result(battle):
    creator_victory_points = 0
    opponent_victory_points = 0

    # check if opponent has pokemons
    opponent_pokemons = [
        battle.opponent_pokemon_1,
        battle.opponent_pokemon_2,
        battle.opponent_pokemon_3,
    ]
    if all(pokemon is None for pokemon in opponent_pokemons):
        return None

    pokemon_pairs = [
        (battle.creator_pokemon_1, battle.opponent_pokemon_1),
        (battle.creator_pokemon_2, battle.opponent_pokemon_2),
        (battle.creator_pokemon_3, battle.opponent_pokemon_3),
    ]

    for creator_pokemon, opponent_pokemon in pokemon_pairs:
        winner = compare_pokemons(creator_pokemon, opponent_pokemon)
        if winner == creator_pokemon:
            creator_victory_points += 1
        else:
            opponent_victory_points += 1

    if creator_victory_points > opponent_victory_points:  # noqa
        return battle.creator
    else:
        return battle.opponent


def send_battle_result(battle):
    send_templated_mail(
        template_name="battle_result",
        from_email=config("EMAIL_ADDRESS"),
        recipient_list=[battle.creator.email, battle.opponent.email],
        context={
            "battle_creator": battle.creator.email,
            "battle_opponent": battle.opponent.email,
            "battle_winner": battle.winner.email,
            "battle_id": battle.id,
            "battle_creator_pokemon_1": battle.creator_pokemon_1.name,
            "battle_creator_pokemon_2": battle.creator_pokemon_2.name,
            "battle_creator_pokemon_3": battle.creator_pokemon_3.name,
            "battle_opponent_pokemon_1": battle.opponent_pokemon_1.name,
            "battle_opponent_pokemon_2": battle.opponent_pokemon_2.name,
            "battle_opponent_pokemon_3": battle.opponent_pokemon_3.name,
        },
    )
