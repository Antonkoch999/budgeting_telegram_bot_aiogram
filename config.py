import environs

env = environs.Env()
env.read_env()

bot_token = env.str('BOT_TOKEN')
database_async_url = env.str('DATABASE_ASYNC_URL')
alembic_database_url = env.str('ALEMBIC_DATABASE_ASYNC_URL')
encoding_key = env.str('ENCODING_KEY')
