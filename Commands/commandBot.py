import discord
from discord.ext import commands
import Selenuim.playgroundaiCom
import os
intents = discord.Intents.default()  # Set up default intents
intents.message_content = True  # Enable typing events if you need them
bot = commands.Bot(command_prefix='/', intents=intents)
@bot.command()
async def imagine(ctx, *args):
    """
    /imagine str
    """
    str = ' '.join(args)

    path = Selenuim.playgroundaiCom.create_image(str)

    if not (path == "An Error Occured, Please try again"):
        await ctx.send(file=discord.File(path))
        os.remove(path)

    else:
        await ctx.send(path)




@bot.command()
async def info(ctx):
    """
    ctx - context (information about how the command was exectued)

    /info
    """

    await ctx.send(ctx.guild)
    await ctx.send(ctx.author)
    await ctx.send(ctx.message.id)
def run_bot():


    bot.run('bot_token')

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running')