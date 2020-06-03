from discord.ext.commands import Bot
#from dotenv import load_dotenv

from os import walk, name, getenv
from os.path import join, splitext, abspath, split
from json import load

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')


class NPC(Bot):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        with open("database.json", encoding="utf-8") as file:
            self.database = load(file)

        self.log_channel_id = self.database["Channels"]["log"]
        self.main_channel_id = self.database["Channels"]["main"]
        self.suggestion_channel_id = self.database["Channels"]["suggestion"]
        self.trustworthy_role = self.database["Roles"]["trustworthy"]
        

bot = NPC(command_prefix='.', case_insensitive=True)

if __name__ == "__main__":
    for item in walk("extensions"):
        files = filter(lambda file: file.endswith(".py"), item[-1])

        for file in files:
            file_name, ext = splitext(file)
            path = join("extensions", file_name)

            try:
                bot.load_extension(path.replace("\\", '.').replace('/', '.'))
            except Exception as error:
                print("{0.__class__.__name__}: {0}".format(error))

    bot.run(TOKEN)
