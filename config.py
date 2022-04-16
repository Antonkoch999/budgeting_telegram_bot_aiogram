import environs

env = environs.Env()
env.read_env()

bot_token = env.str('BOT_TOKEN')
database_async_url = env.str('DATABASE_ASYNC_URL')
