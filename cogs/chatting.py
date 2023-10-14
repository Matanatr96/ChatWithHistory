import logging
import requests
import json
from discord.ext import commands
from cogs.schema import ChatRequest, ChatResponse, ChatbotAPIError

logger = logging.getLogger(__name__)


def query_local_model(request_data: ChatRequest):
    try:
        logger.info("Querying local model")
        response = requests.post("http://localhost:1234/v1/chat/completions",
                                 headers={"Content-Type": "application/json"},
                                 json=request_data.model_dump())
        response_data = ChatResponse(**json.loads(response.text))
        response_content = response_data.choices[0]['message']['content']
        logger.info(f"Response from local model: {response_content}")
        return response_content
    except requests.exceptions.RequestException as e:
        raise ChatbotAPIError(f"An error occurred while querying the chatbot API: {e}")


class Chatting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='chat')
    async def chat(self, ctx, *, message: str):
        logger.info(f"Received message: {message}")
        request_data = ChatRequest(
            messages=[
                {
                    "role": "system",
                    "content": "### System: You are a chatbot. Respond to the user with a funny answer with a very slight sarcastic undertone"
                },
                {
                    "role": "user",
                    "content": message + " ### Response: "
                }
            ],
            stop=["### Instruction:"],
            temperature=0.7,
            max_tokens=256,
            stream=False
        )

        try:
            response = query_local_model(request_data)
            await ctx.send(response)
        except ChatbotAPIError as e:
            logger.error(str(e))
            await ctx.send("An error occurred while querying the chatbot API. Please try again later.")


async def setup(bot):
    await bot.add_cog(Chatting(bot))
