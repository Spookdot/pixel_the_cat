from pixel_pyme import PymeGen
from typing import Optional
from discord import app_commands
from discord.ext import commands
import discord


class PixelBot(commands.Bot):
    def __init__(self, intents: discord.Intents) -> None:
        super().__init__("m!", intents=intents)
        self._meme_gen = None

    @property
    def meme_gen(self) -> PymeGen:
        return self._meme_gen

    async def on_ready(self) -> None:
        self._meme_gen = PymeGen()
        await self.tree.sync()
        print("Am ready")
