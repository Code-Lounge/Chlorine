from discord.ext.commands import Bot
from os import walk
from os.path import join, splitext
from json import load


class NPC(Bot):
    def __init__(self, *args, **kwargs) -> None:
        with open("database.json", encoding="utf-8") as file:
            self.database = load(file)

        super().__init__(*args, **kwargs)


bot = NPC(command_prefix='ch ', case_insensitive=True)

def extensions(tree: str) -> list:
    """
    :param tree: str - tree of extensions.
    :return: list - extensions list of tree.
        Syntax:
            [(path, file), (path, file), ...]
    """
    for item in walk(tree):
        #item return: (actual_path, folders_in_path, files_in_path)
        files = filter(lambda file: file.endswith(".py"), item[-1])
        for file in files:
            yield (item[0], file)

if __name__ == "__main__":
    for extension in extensions("extensions"):
        path = join(*extension)
        try:
            path, ext = splitext(path)
            bot.load_extension(path.replace("\\", '.'))
        except Exception as error:
            print("{0.__class__.__name__}: {0}".format(error))

    bot.run("")
