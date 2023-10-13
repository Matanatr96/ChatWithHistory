import logging
import requests
import json
from discord.ext import commands

logger = logging.getLogger(__name__)


class ChatCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='chat')
    async def chat(self, ctx, *, message: str):
        logger.info(f"Received message: {message}")
        response = self.query_local_model(message)
        await ctx.send(response)


    def query_local_model(self, prompt: str):
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

def setup(bot):
    bot.add_cog(ChatCommands(bot))
