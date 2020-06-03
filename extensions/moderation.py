from discord.ext.commands import Cog, Bot, command, Context, has_permissions, bot_has_permissions
from discord import Member, Guild, Role
from discord.errors import HTTPException

from asyncio import sleep
from os.path import basename


class Moderation(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def ban(self, ctx: Context, target: Member, reason: str="...") -> None:
        try:
            await ctx.guild.ban(target, reason=reason, delete_message_days=0)
        except HTTPException:
            #A pessoa pode estar em uma posição hierarquica maior do que a do bot.
            await ctx.send(f"Não foi possível banir {target.mention}.")
        else:
            await ctx.send(f"{target.mention} foi banido do servidor.")

    @command()
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    async def kick(self, ctx: Context, target: Member, reason: str="...") -> None:
        try:
            await ctx.guild.kick(target, reason=reason, delete_message_days=0)
        except HTTPException:
            #A pessoa pode estar em uma posição hierarquica maior do que a do bot.
            await ctx.send(f"Não foi possível expulsar {target.mention}.")
        else:
            await ctx.send(f"{target.mention} foi expulso do servidor.")

    @command()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def mute(self, ctx: Context, target: Member, reason: str="...", timeout: int=1):
        mute_role = ctx.guild.get_role(self.bot.mute_role)
        if mute_role:
            try:
                await target.add_roles(mute_role, reason=reason)
            except HTTPException:
                await ctx.send(f"Não foi possível adicionar o cargo de mute para {target.mention}.")
            else:
                await ctx.send(f"{target.mention} foi mutado por {timeout} hora{'s' if timeout != 1 else ''}!")
                await sleep(60 * 60 * timeout)
                await target.remove_roles(self.mute_role)
        else:
            await ctx.send("O cargo de mute não está definido ou não foi encontrado.")

    @command()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def role(self, ctx: Context, target: Member, role: Role):
        try:
            await target.add_roles(role)
        except HTTPException:
            await ctx.send(f"Não foi possível adicionar o cargo {role.name} para {target.mention}.")
        else:
            await ctx.send(f"O cargo {role.name} foi adicionado à {target.mention}.")


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
