from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    # Internal tasks
    "clearsessions": {"schedule": crontab(hour=3, minute=0), "task": "users.tasks.clearsessions"},
    "save_all_pokemons_from_pokeapi": {
        "schedule": crontab(hour=7, minute=30, day_of_week=5),
        "task": "pokemon.tasks.save_pokemon_from_pokeapi_weekly",
    },
}
