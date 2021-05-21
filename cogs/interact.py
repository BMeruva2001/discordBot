import discord
import random
from discord.ext import commands


class Interact(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} joined the server')
        await member.send("Welcome bitch!")

    @commands.command(aliases=['hey', 'sup', 'hi', 'Hey', 'Hello', 'Hi', 'howdy', 'Howdy'])
    async def hello(self, ctx):
        greetings = ["Hey.",
                     "Heyyy!",
                     "Sup homie.",
                     "Hello.",
                     "Hi.",
                     "Why you!",
                     "Howdy.",
                     "We aren't that close dude.",
                     "It’s good to see you.",
                     "G’day!",
                     "Hello there.",
                     "Greetings.",
                     "ew."]
        await ctx.send(f'{random.choice(greetings)}')

    @commands.command()
    async def audios(self, ctx):
        await ctx.send('videos')

    @commands.command(aliases=['Bye', 'adios', 'Goodbye', 'goodbye', 'Adios', 'Farewell', 'farewell'])
    async def bye(self, ctx):
        farewell = ['Bye.',
                    'Goodbye.',
                    'Adios.',
                    'Farewell.',
                    "I'll miss you babe.",
                    "See you soon.",
                    "Finallyyy.",
                    "Alreadyyy.",
                    "What's the rush darling.",
                    "You better be back soon!"]
        await ctx.send(f'{random.choice(farewell)}')

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "What do you think?",
                     "Let's just sit and think about it first.",
                     "really?",
                     "Whatever you want dude.",
                     "Isn't it obvious.",
                     "I honestly don't care.",
                     "You broke the ball with that question.",
                     "Please try again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        await ctx.send(f'{random.choice(responses)}')

    @commands.command(aliases=['cointoss'])
    async def coinflip(self, ctx):
        sides = ["Heads.",
                 "tails."]
        await ctx.send(f'{random.choice(sides)}')


def setup(client):
    client.add_cog(Interact(client))
