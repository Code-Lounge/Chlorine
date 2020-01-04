from discord.ext.commands import Cog, Bot, command, Context, has_permissions
from discord import Member, Guild
from discord.errors import HTTPException
from asyncio import sleep
from os.path import basename


class Moderation(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx: Context, target: Member, reason: str="...") -> None:
        try:
            await ctx.guild.ban(target, reason=reason, delete_message_days=0)
        except HTTPException as error:
            await ctx.send(f"Não foi possível banir {target.mention}. {error.text}")
        else:
            await ctx.send(f"{target.mention} foi banido do servidor.")

    @command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx: Context, target: Member, reason: str="...") -> None:
        raise NotImplementedError()

        try:
            await ctx.guild.kick(target, reason=reason, delete_message_days=0)
        except HTTPException as error:
            await ctx.send(f"Não foi possível expulsar {target.mention}. {error.text}")
        else:
            await ctx.send(f"{target.mention} foi expulso do servidor.")

    @command()
    @has_permissions(manage_roles=True)
    async def mute(self, ctx: Context, target: Member, reason: str="...", timeout: int=1):
        raise NotImplementedError()

        try:
            await target.add_roles(self.mute_role)
        except HTTPException:
            await ctx.send(f"Não foi possível adicionar o cargo para {target.mention}.")
        else:
            await ctx.send(f"{target.mention} foi mutado por {timeout} hora{'s' if timeout != 1 else ''}!")
            await sleep(60 * 60 * timeout)
            await target.remove_roles(self.mute_role)

    @command()
    @has_permissions(manage_roles=True)
    async def trustworthy(self, ctx: Context, target: Member):
        try:
            await target.add_roles(self.trustworthy_role)
        except HTTPException as error:
            await ctx.send(f"Não foi possível adicionar o cargo para {target.mention}. {error.text}")
        else:
            await ctx.send(f"{target.mention} agora possuí o cargo `{self.trustworthy_role.name}`!")


def setup(bot: Bot) -> None:
    # ~On load
    try:
        bot.add_cog(Moderation(bot))
    except Exception as error:
        print("{0.__class__.__name__}: {0}".format(error))
    else:
        print(f"[{basename(__file__).upper()}] has been loaded.")

def teardown(bot: Bot) -> None:
    # ~On unload
    print(f"[{basename(__file__).upper()}] has been unloaded.")
