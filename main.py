from discord.ext.commands import Bot
from dotenv import load_dotenv

import contextlib
from os import walk, name, getenv
from os.path import join, splitext, abspath, split
from json import load

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

root = "extensions"
files = ["anything", "events", "moderation"]

@contextlib.contextmanager
def setup_logging() -> None:
    try:
        # __enter__
        datetime_format = r'%Y-%m-%d %H:%M:%S'

        logging.getLogger('discord').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.WARNING)

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        handler = logging.FileHandler(filename='chlorine.log', encoding='utf-8', mode='w')
        formatter = logging.Formatter('[{asctime}] [{levelname:}] {name}: {message}', datetime_format, style='{')
    
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        yield
    finally:
        # __exit__
        for handler in logger.handlers:
            handler.close()
            logger.removeHandler(handler)
            
def main():
    bot = Bot(command_prefix='.', case_insensitive=True)

    for file in files:
        path = "{}.{}".format(root, file)

        try:
            bot.load_extension(path)
        except Exception as error:
            print("{0.__class__.__name__}: {0}".format(error))

    bot.run(TOKEN)

if __name__ == "__main__":
    with setup_logging():
        main()