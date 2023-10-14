import os
import logging

from discord import Intents
from discord.ext import commands
from flask import Flask
from dotenv import load_dotenv
load_dotenv()

# app = Flask(__name__)

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger(__name__)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await bot.load_extension('cogs.basic')
    await bot.load_extension('cogs.chatting')


if __name__ == "__main__":
    bot.run(os.environ.get('DISCORD_BOT_TOKEN'))
