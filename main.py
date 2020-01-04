from discord.ext.commands import Bot
from os import walk, name
from os.path import join, splitext, abspath, split
from json import load


class NPC(Bot):
    def __init__(self, *args, **kwargs) -> None:

        with open("database.json", encoding="utf-8") as file:
            self.database = load(file)

        self.log_channel_id = self.database["Channels"]["log"]
        self.main_channel_id = self.database["Channels"]["main"]

        super().__init__(*args, **kwargs)


bot = NPC(command_prefix='ch ', case_insensitive=True)

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

    bot.run("")
