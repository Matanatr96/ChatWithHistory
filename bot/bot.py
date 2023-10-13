import os

from discord import Intents
from discord.ext import commands
from flask import Flask, request, jsonify

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# TODO: fix this
def setup_bot():
    bot.load_extension("cogs.chat_commands")
    # bot.load_extension("cogs.admin")
    # bot.load_extension("cogs.events")


setup_bot()

if __name__ == "__main__":
    disc_token = os.environ.get('DISCORD_BOT_TOKEN')
    bot.run(disc_token)
    print('am running this')
