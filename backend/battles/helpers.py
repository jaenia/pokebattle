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

    # first round
    first_winner_pokemon = compare_pokemons(battle.creator_pokemon_1, battle.opponent_pokemon_1)
    if first_winner_pokemon == battle.creator_pokemon_1:
        creator_victory_points += 1
    else:
        opponent_victory_points += 1

    # second round
    second_winner_pokemon = compare_pokemons(battle.creator_pokemon_2, battle.opponent_pokemon_2)
    if second_winner_pokemon == battle.creator_pokemon_2:
        creator_victory_points += 1
    else:
        opponent_victory_points += 1

    # third round
    third_winner_pokemon = compare_pokemons(battle.creator_pokemon_3, battle.opponent_pokemon_3)
    if third_winner_pokemon == battle.creator_pokemon_3:
        creator_victory_points += 1
    else:
        opponent_victory_points += 1

    if creator_victory_points > opponent_victory_points:  # noqa
        return battle.creator
    else:
        return battle.opponent
