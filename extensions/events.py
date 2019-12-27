from discord.ext.commands import Bot, Cog, Context
from discord import Message, Member, Game
from os.path import basename
from discord.ext.commands.errors import *
from discord.errors import *
from random import randint


class Events(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

        self.log_channel_id = bot.database["Channels"]["log"]
        self.main_channel_id = bot.database["Channels"]["main"]

    @Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(activity=Game(name="você pela janela, não se segure!"))
        print("Hello world, i'm here!")

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if "bom dia" in message.content.lower():
            reply = f"B{'o' * randint(1, 3)}m di{'a' * randint(1, 5)}!"
            await message.channel.send(reply)

        #await self.bot.process_commands(message)

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, CommandNotFound):
            await ctx.add_reaction('❌')
        elif isinstance(error, MissingPermissions):
            missing_permissions = ', '.join(error.missing_perms)
            await ctx.send(f"Você não possuí permissões o suficientes para executar este comando.\nPermissões faltantes: `{missing_permissions}`")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Você não me informou o `{error.param.name}` do comando `{ctx.invoked_with}`.")
        elif isinstance(error, BadArgument):
            await ctx.send(f"Você me passou uma informação errada para o comando `{ctx.invoked_with}`!")
        elif isinstance(error, CommandInvokeError):
            if isinstance(error.original, NotImplementedError):
                await ctx.send(f"O comando `{ctx.invoked_with}` ainda não foi implementado.")
            else:
                raise error
        else:
            raise error

    @Cog.listener()
    async def on_error(self, event, *args, **kwargs) -> None:
        pass

    @Cog.listener()
    async def on_member_join(self, member: Member):
        message = f"{member.mention} entrou no servidor."

        log_channel = member.guild.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(message)
        else:
            print(f"Log channel not found.")
        
        main_channel = member.guild.get_channel(self.main_channel_id)
        if self.main_channel:
            await main_channel.send(message)
        else:
            print(f"Main channel not found.")

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        log_channel = member.guild.get_channel(self.log_channel_id)
        if log_channel:
            await log_channel.send(f"{member.mention} deixou o servidor.")
        else:
            print(f"Log channel not found.")

    @Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        return
        raise NotImplementedError()
        
        if before.roles != after.roles:
            #Roles has been changed
            pass


def setup(bot: Bot) -> None:
    # ~On load
    try:
        bot.add_cog(Events(bot))
    except Exception as error:
        print("{0.__class__.__name__}: {0}".format(error))
    else:
        print(f"[{basename(__file__).upper()}] has been loaded.")

def teardown(bot: Bot) -> None:
    # ~On unload
    print(f"[{basename(__file__).upper()}] has been unloaded.")
