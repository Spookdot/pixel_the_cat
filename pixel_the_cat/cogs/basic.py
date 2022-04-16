from discord.ext import commands
from discord import app_commands
import discord


class BasicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command()
    async def avatar(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.send_message(user.avatar.url)


async def setup(bot: commands.Bot):
    await bot.add_cog(BasicCog(bot))
