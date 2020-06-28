from discord.ext.commands import Bot, Cog, Context
from discord import Message, Member, Game, Reaction, RawReactionActionEvent, Embed
from discord.ext.commands.errors import *
from discord.errors import *
from discord.utils import get, find

from os.path import basename
from random import randint


class Events(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(activity=Game(name="você pela janela, não se segure!"))
        print("Hello world, i'm here!")

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        
        if "bom dia" in message.content.lower():
            reply = f"B{'o' * randint(1, 3)}m di{'a' * randint(1, 5)}!"
            await message.channel.send(reply)

        suggestion_channel = message.guild.get_channel(self.bot.suggestion_channel_id)
        if suggestion_channel:
            if message.channel.id == suggestion_channel.id:
                await message.add_reaction('⬆️')
                await message.add_reaction('⬇️')
        else:
            print(f"Suggestion channel not found.")

            
        #await self.bot.process_commands(message)

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, CommandNotFound):
            await ctx.message.add_reaction('❌')

        elif isinstance(error, MissingPermissions):
            missing_permissions = ', '.join(error.missing_perms)
            await ctx.send(f"Você não possuí permissões o suficientes para executar este comando.\nPermissões faltantes: `{missing_permissions}`")

        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(f"Você não me informou o `{error.param.name}` do comando `{ctx.invoked_with}`.")

        elif isinstance(error, BotMissingPermissions):
            missing_permissions = ', '.join(error.missing_perms)
            await ctx.send(f"Eu não possuio permissões o suficientes para executar este comando.\nPermissões faltantes: `{missing_permissions}`")

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

        log_channel = member.guild.get_channel(self.bot.log_channel_id)
        if log_channel:
            await log_channel.send(message)
        else:
            print(f"Log channel not found.")
        
        main_channel = member.guild.get_channel(self.bot.main_channel_id)
        if self.main_channel:
            await main_channel.send(message)
        else:
            print(f"Main channel not found.")

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        log_channel = member.guild.get_channel(self.bot.log_channel_id)
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
            
            Embed(
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
                        embed.set_image(url=(attachment.proxy_url or attachment.url))
                        break

            await starboard.send(embed=embed)

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
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
