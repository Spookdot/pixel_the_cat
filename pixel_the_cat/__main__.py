import asyncio
from . import PixelBot
from .cogs import meme
from discord import app_commands
from dotenv import load_dotenv
import discord
import os

load_dotenv()
main_guild = discord.Object(id=os.getenv("GUILD_ID"))
bot = PixelBot(intents=discord.Intents.default())


async def main():
    async with bot:
        await bot.load_extension(".cogs.meme", package="pixel_the_cat")
        await bot.load_extension(".cogs.basic", package="pixel_the_cat")
        if os.getenv("DEBUG") == "TRUE":
            bot.tree.copy_global_to(guild=main_guild)

        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())
