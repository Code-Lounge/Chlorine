from discord.ext.commands import Cog, command, Bot, Context
from os.path import basename
from discord import Webhook, AsyncWebhookAdapter
from aiohttp import ClientSession


class Anything(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        
        self.wh_url = ""

    @command()
    async def suggestion(self, ctx: Context, *, message):
        #raise NotImplementedError()
        async with ClientSession() as session:
            adapter = AsyncWebhookAdapter(session)

            try:
                webhook = Webhook.from_url(self.wh_url, adapter=adapter)
                await webhook.send(message, username=f"Sugestão ~ {ctx.author.name}", avatar_url=ctx.author.avatar_url)
            except:
                #raised by Webhook.from_url ~ InvalidArgument – The URL is invalid.
                await ctx.send(f"Não foi possível enviar a sua sugestão...")
            else:
                await ctx.send(f"Obrigado pela sua sugestão! Ela foi encaminhada para os moderadores!")


def setup(bot: Bot) -> None:
    # ~On load
    try:
        bot.add_cog(Anything(bot))
    except Exception as error:
        print("{0.__class__.__name__}: {0}".format(error))
    else:
        print(f"[{basename(__file__).upper()}] has been loaded.")

def teardown(bot: Bot) -> None:
    # ~On unload
    print(f"[{basename(__file__).upper()}] has been unloaded.")
