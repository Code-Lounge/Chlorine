from discord.ext.commands import Bot, Cog, Context
from discord import Message, Member, Game, Reaction, Embed
from discord.ext.commands.errors import *
from discord.errors import *
from discord.utils import get, find

from os.path import basename
from random import randint
from difflib import get_close_matches
from asyncio import TimeoutError


class Events(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        activity = Game(name="você pela janela, não se segure!")
        await self.bot.change_presence(activity=activity)

        l = []
        for command in self.bot.commands:
            l.extend([command.name] + command.aliases)
        self.bot.commands_calls = l

        print("Hello world, i'm here!")

    @Cog.listener()
    async def on_message(self, message: Message):
        channel = message.channel

        if "bom dia" in message.content.lower():
            reply = f"B{'o' * randint(1, 3)}m di{'a' * randint(1, 5)}!"
            await channel.send(reply)

        if channel.name in ["sugestões", "sugestão"]:
            await message.add_reaction('⬆️')
            await message.add_reaction('⬇️')

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if isinstance(error, CommandNotFound):
            matches = get_close_matches(ctx.invoked_with, self.bot.commands_calls) 
            if matches:
                await ctx.message.add_reaction('❔')

                def check(reaction, user) -> bool:
                    return str(reaction.emoji) == '❔' and \
                           reaction.message.id == ctx.message.id and \
                           user == ctx.author

                try:
                    await self.bot.wait_for("reaction_add", check=check, timeout=30)
                except TimeoutError:
                    pass
                else:
                    commands = '.'.join(matches)
                    await ctx.send(f"Os comandos parecidos com `{ctx.invoked_with}` são:```{commands}.```Para saber como utiliza-los, use o comando `{ctx.prefix}help nome_do_commando`!")

            else:
                await ctx.message.add_reaction('❌')

        elif isinstance(error, MissingPermissions):
            missing_permissions = ', '.join(error.missing_perms)
            await ctx.send(f"Você não possuí permissões o suficientes para executar este comando.\nPermissões faltantes: `{missing_permissions}`")

        elif isinstance(error, MissingRequiredArgument):
            parameters = [f"[{param}]" for param in ctx.command.clean_params]
            parameters = ' '.join(parameters)
            await ctx.send(f"```{ctx.invoked_with} {parameters}```")

        elif isinstance(error, BotMissingPermissions):
            missing_permissions = ', '.join(error.missing_perms)
            await ctx.send(f"Eu não possuo permissões o suficientes para executar este comando.\nPermissões faltantes: `{missing_permissions}`")

        elif isinstance(error, BadArgument):
            await ctx.send(f"Você me passou uma informação errada para o comando `{ctx.invoked_with}`!")

        elif isinstance(error, CommandInvokeError):
            if isinstance(error.original, NotImplementedError):
                message = "O comando `{}` ainda não foi implementado.".format(
                    ctx.invoked_with
                )
                await ctx.send(message)
            else:
                raise error
        else:
            raise error

    @Cog.listener()
    async def on_member_join(self, member: Member):
        message = f"{member.mention} entrou no servidor!"

        log_channel = get(member.guild.text_channels, name="log")
        main_channel = get(member.guild.text_channels, name="principal")

        if log_channel:
            await log_channel.send(message)

        if self.main_channel:
            await main_channel.send(message)

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        log_channel = get(member.guild.text_channels, name="log")

        if log_channel:
            await log_channel.send(f"{member.mention} deixou o servidor.")

    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: Member):
        message = reaction.message

        starboard = get(message.guild.text_channels, name="starboard")

        if not starboard:
            return

        if message.channel == starboard:
            return

        if str(reaction.emoji) == '⭐':
            reactions = message.reactions

            def make_check(emoji: str):
                def check(r):
                    return str(r.emoji) == emoji
                return check

            star_two_in_reactions = find(make_check('🌟'), reactions)
            if star_two_in_reactions:
                if star_two_in_reactions.me:
                    return

            star_in_reactions = find(make_check('⭐'), reactions)
            if star_in_reactions:
                stars = find(lambda r: str(r.emoji) == '⭐', reactions)
            else:
                return

            if stars.count <= 2:
                return

            await reaction.message.add_reaction('🌟')

            embed = Embed(
                title="Uma nova pérola apareceu!",
                description=f"Um [brilho]({message.jump_url}) está vindo do canal {message.channel.mention}!\n\n" + (message.content or ''),
                color=0xfcff59,
                url=message.jump_url
            ).set_footer(
                icon_url=message.author.avatar_url,
                text=message.author.name + '#' + message.author.discriminator
            )

            attachments = message.attachments
            if attachments:
                for attachment in attachments:
                    if attachment.height and attachment.width:
                        embed.set_image(url=attachment.url)
                        break

            await starboard.send(embed=embed)


def setup(bot: Bot):
    # ~On load
    try:
        bot.add_cog(Events(bot))
    except Exception as error:
        print("{0.__class__.__name__}: {0}".format(error))
    else:
        print(f"[{basename(__file__).upper()}] has been loaded.")


def teardown(bot: Bot):
    # ~On unload
    print(f"[{basename(__file__).upper()}] has been unloaded.")
