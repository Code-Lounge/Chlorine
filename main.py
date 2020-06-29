from discord.ext.commands import Bot
from dotenv import load_dotenv

from os import walk, name, getenv
from os.path import join, splitext, abspath, split
from json import load

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')

bot = Bot(command_prefix='.', case_insensitive=True)

root = "extensions"
files = ["anything", "events", "moderation"]

if __name__ == "__main__":
    for file in files:
        path = "{}.{}".format(root, file)

        try:
            bot.load_extension(path)
        except Exception as error:
            print("{0.__class__.__name__}: {0}".format(error))

    bot.run(TOKEN)
