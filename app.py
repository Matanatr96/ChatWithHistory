import os
from flask import Flask, request, jsonify
import logging
import discord
from discord import Intents
from discord.ext import commands
import requests
from dotenv import load_dotenv
load_dotenv()
import json

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger(__name__)

# Setup Discord bot
TOKEN = os.environ.get('DISCORD_BOT_TOKEN')

intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


@bot.command(name='chat')
async def chat(ctx, *, message: str):
    # response = ask_openai(message)
    # await ctx.send(response)
    logger.info(f"Received message: {message}")
    response = query_local_model(message)
    await ctx.send(response)

def query_local_model(prompt: str):
    try:
        logger.info("Querying local model")
        data = {
            "messages": [
                {
                    "role": "system",
                    "content": "### System: You are a chatbot. Respond to the user with a funny answer with a very slight sarcastic undertone"
                },
                {
                    "role": "user",
                    "content": prompt + " ### Response: "
                }
            ],
            "stop": ["### Instruction:"], "temperature": 0.7, "max_tokens": 256, "stream": False
        }

        response = requests.post("http://localhost:1234/v1/chat/completions",
                                 headers={"Content-Type": "application/json"},
                                 json=data)
        response_content = json.loads(response.text)['choices'][0]['message']['content']
        logger.info(f"Response from local model: {response_content}")
        return response_content
    except requests.exceptions.RequestException as e:
        # TODO: Throw an actual error here
        print(f"An error occurred: {e}")
        return None

@app.route('/start_bot', methods=['POST'])
def start_bot():
    bot.run(TOKEN)
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(port=5000)