import discord
from discord import app_commands, ui
from discord.ext import commands
from typing import Optional
from io import BytesIO
from .. import PixelBot

from pixel_pyme.dict_types import ShortMemeData, MemeData
from pixel_pyme import PymeGen


class MemeModal(ui.Modal, title="Make a Meme"):
    def __init__(self, meme_name: str, pyme_gen: PymeGen, **kwargs):
        super().__init__(**kwargs)
        self.meme_name = meme_name
        self.pyme_gen = pyme_gen

    async def on_submit(self, interaction: discord.Interaction):
        img = await self.pyme_gen.make_meme(self.meme_name, [i.value for i in self.children])
        file = BytesIO()
        file.name = "meme.png"
        img.image.save(file)
        file.seek(0)
        await interaction.response.send_message(file=discord.File(file))


class MemeCog(commands.Cog):
    def __init__(self, bot: PixelBot):
        self.bot = bot

    @property
    def meme_gen(self) -> PymeGen:
        return self.bot.meme_gen

    @app_commands.command()
    async def meme_old(self, interaction: discord.Interaction, meme_name: str, arg1: Optional[str] = "", arg2: Optional[str] = "",
                       arg3: Optional[str] = "", arg4: Optional[str] = ""):
        img = await self.meme_gen.make_meme(meme_name, [arg1, arg2, arg3, arg4])
        file = BytesIO()
        file.name = "meme.png"
        img.image.save(file)
        file.seek(0)
        await interaction.response.send_message(file=discord.File(file))

    @app_commands.command()
    async def meme(self, interaction: discord.Interaction, meme_name: str):
        meme: MemeData = await self.meme_gen.get_meme(meme_name)
        modal = MemeModal(meme_name, self.meme_gen)
        for i in range(len(meme["parameter"])):
            modal.add_item(ui.TextInput(
                label=f"Argument {i + 1}", required=False))
        await interaction.response.send_modal(modal)

    @meme.autocomplete('meme_name')
    async def meme_name_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        memes = await self.meme_gen.get_memes()
        meme_names = [meme["name"] for meme in memes]
        return [
            app_commands.Choice(name=meme, value=meme)
            for meme in meme_names
            if meme.startswith(current)
        ]

    @app_commands.command()
    async def list_memes(self, interaction: discord.Interaction):
        memes: list[ShortMemeData] = await self.meme_gen.get_memes()
        await interaction.response.send_message(
            " ".join([i["name"] for i in memes]),
            ephemeral=True
        )


async def setup(bot: PixelBot):
    await bot.add_cog(MemeCog(bot))
