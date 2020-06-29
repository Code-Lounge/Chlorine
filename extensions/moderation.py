from discord.ext.commands import Cog, Bot, command, Context, has_permissions, bot_has_permissions, guild_only
from discord import Member, Guild, Role
from discord.errors import HTTPException
from discord.utils import get

from asyncio import sleep
from os.path import basename


class Moderation(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @guild_only()
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    @command(name="ban", aliases=["banir",])
    async def ban_command(self, ctx: Context, target: Member, reason: str="..."):
        """
        Bane um membro do servidor.
        É possível passar o motivo do banimento (fica salvo no registro de auditoria).
        """
        try:
            await ctx.guild.ban(target, reason=reason, delete_message_days=0)
        except HTTPException:
            #A pessoa pode estar em uma posição hierarquica maior do que a do bot.
            await ctx.send(f"Não foi possível banir {target.mention}.")
        else:
            await ctx.send(f"{target.mention} foi banido do servidor.")

    @guild_only()
    @has_permissions(kick_members=True)
    @bot_has_permissions(kick_members=True)
    @command(name="kick", aliases=["expulsar",])
    async def kick_command(self, ctx: Context, target: Member, reason: str="..."):
        """
        Expulsa um membro do servidor.
        É possível passar o motivo da expulsão (fica salvo no registro de auditoria).
        """
        try:
            await ctx.guild.kick(target, reason=reason, delete_message_days=0)
        except HTTPException:
            #A pessoa pode estar em uma posição hierarquica maior do que a do bot.
            await ctx.send(f"Não foi possível expulsar {target.mention}.")
        else:
            await ctx.send(f"{target.mention} foi expulso do servidor.")

    @guild_only()
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    @command(name="mute", aliases=["mutar",])
    async def mute_command(self, ctx: Context, target: Member, reason: str="...", timeout: int=1):
        """
        Adiciona o cargo "Mutado" à um membro do servidor.
        É possivel adicionar um motivo e o tempo em horas que o membro ficará mutado.
        O servidor precisa ter um cargo chamado "Mutado" para este comando funcionar.
        """
        mute_role = get(ctx.guild.text_channels, name="Mutado")

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
            await ctx.send("O servidor não possuí um cargo chamado `Mutado` para o uso deste comando.")

    @guild_only()
    @command(name="role")
    @has_permissions(manage_roles=True)
    @bot_has_permissions(manage_roles=True)
    async def role_command(self, ctx: Context, target: Member, role: Role):
        """
        Adiciona um cargo qualquer a um membro.
        Você pode passar o nome, id ou menção em ambos, membro ou cargo.
        """
        try:
            await target.add_roles(role)
        except HTTPException:
            await ctx.send(f"Não foi possível adicionar o cargo {role.name} para {target.mention}.")
        else:
            await ctx.send(f"O cargo {role.name} foi adicionado à {target.mention}.")

def setup(bot: Bot):
    # ~On load
    try:
        bot.add_cog(Moderation(bot))
    except Exception as error:
        print("{0.__class__.__name__}: {0}".format(error))
    else:
        print(f"[{basename(__file__).upper()}] has been loaded.")

def teardown(bot: Bot):
    # ~On unload
    print(f"[{basename(__file__).upper()}] has been unloaded.")
