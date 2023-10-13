from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

    @commands.command(name='help')
    async def help(self, ctx):
        await ctx.send("List of commands: !help, !ping, !chat, !serverinfo")

    @commands.command(name='serverinfo')
    async def serverinfo(self, ctx):
        server = ctx.guild
        num_users = len(server.members)
        num_text_channels = len(server.text_channels)
        await ctx.send(f"Matanatr96 is your supreme leader, anything he says goes")


def setup(bot):
    bot.add_cog(BasicCommands(bot))
