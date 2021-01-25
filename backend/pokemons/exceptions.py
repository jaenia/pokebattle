class PokemonNotFound(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "{} was not found in PokeAPI".format(self.value)
