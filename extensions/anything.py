from discord.ext.commands import Cog, command, Bot, Context
from os import path, getenv
from discord import Webhook, AsyncWebhookAdapter, Member, Embed
from aiohttp import ClientSession
from datetime import datetime
WH_URL = getenv('URL_WEBHOOK')

class Anything(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    async def suggestion(self, ctx: Context, *, message):
        #raise NotImplementedError()
        async with ClientSession() as session:
            adapter = AsyncWebhookAdapter(session)

            try:
                webhook = Webhook.from_url(WH_URL, adapter=adapter)
                webhookSend = await webhook.send(message, username=f"Sugestão ~ {ctx.author.name}", avatar_url=ctx.author.avatar_url)
            except:
                # raised by Webhook.from_url ~ InvalidArgument – The URL is invalid.
                await ctx.send(f"Não foi possível enviar a sua sugestão...")
            else:
                await ctx.send(f"Obrigado pela sua sugestão! Ela foi encaminhada para os moderadores!")
    
    @command()
    async def info(self, ctx: Context, member: Member):
        info_embed = Embed(colour=member.color)
        roles = [role.name for role in filter(
            lambda role: not role.is_default(), member.roles)]
        activity = member.activity if member.activity else "jogando nada no momento"
        create_at_days = self.time_days(member.created_at)
        joined_at_days = self.time_days(member.joined_at)
        info_embed\
            .set_author(name=member.name, icon_url=member.avatar_url if member.avatar_url else member.default_avatar_url)\
            .add_field(name='💎 Usuário: ', value=f'***```css\n{member.name}```***')\
            .add_field(name='🔰 ID Discord: ', value=f'```{member.id}```')\
            .add_field(name='🍩 Jogando: ', value=f'```Markdown\n# {activity}```')\
            .add_field(name='⏰ Conta criada: ', value=f'***```prolog\n{create_at_days} dias```***')\
            .add_field(name='💡 Apelido: ', value=f'```{member.nick if member.nick else "sem apelido"}```')\
            .add_field(name='⏰ Entrou no Servidor há: ', value=f'***```prolog\n{joined_at_days} dias atrás```***')\
            .add_field(name='♣ Cargos: ', value=" | ".join(roles))
        await ctx.send(embed=info_embed)

    @command()
    async def server(self, ctx: Context):
        server_embed = Embed(colour=65280)
        now = datetime.now()
        create_server = ctx.guild.created_at
        bot_entry_server = ctx.guild.me.joined_at
        server_embed\
            .set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)\
            .add_field(name='Chefe do Servidor: ', value=ctx.guild.owner)\
            .add_field(name='ID do Dono: ', value=f'```{ctx.guild.owner_id}```')\
            .add_field(name=':date: Servidor criado em: ', value=f'**{create_server.__format__("%d/%m/%y")}**')\
            .add_field(name='⏰ Servidor criado há: ', value=f'**```{self.time_days(create_server)} dias```**')\
            .add_field(name='🔰 ID do servidor: ', value=ctx.guild.id)\
            .add_field(name='⚽ Região: ', value=ctx.guild.region)\
            .add_field(name='📥 Bot adicionado em: ', value=f'**{bot_entry_server.__format__("%d/%m/%y")}**')\
            .add_field(name='📥 Bot adicionado há: ', value=f'**```{self.time_days(bot_entry_server)} dias```**')\
            .add_field(name='🎎 Total de Membros: ', value=f'```{len(ctx.guild.members)} membros```')\
            .add_field(name='📌 Total de Cargos: ', value=f'```{len(ctx.guild.roles)}```')\
            .set_thumbnail(url=ctx.guild.icon_url_as(size=2048))

        await ctx.send(embed=server_embed)

    @command()
    async def avatar(self, ctx: Context, member: Member):
        member_avatar = member.avatar_url if member.avatar_url else member.default_avatar_url
        avatar_embed = Embed(colour=65280, description=f'***Avatar de {member.mention}***')
        avatar_embed\
            .add_field(name='***Donwload Imagem:***', value=f'***[download]({member_avatar})***')\
            .set_image(url=member_avatar)
            
        await ctx.send(embed=avatar_embed)

    def time_days(self, date):
        return (datetime.now() - date).days


def setup(bot: Bot) -> None:
    # ~On load
    try:
        bot.add_cog(Anything(bot))
    except Exception as error:
        print("{0.__class__.__name__}: {0}".format(error))
    else:
        print(f"[{path.basename(__file__).upper()}] has been loaded.")


def teardown(bot: Bot) -> None:
    # ~On unload
    print(f"[{path.basename(__file__).upper()}] has been unloaded.")
