import os
from bot.bot import bot
import logging

from flask import Flask
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    disc_token = os.environ.get('DISCORD_BOT_TOKEN')
    bot.run(disc_token)

    # start app
    app.run(port=5000)
