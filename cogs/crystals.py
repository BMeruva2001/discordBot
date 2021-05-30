import discord
from discord.ext import commands
import random
import json

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

crystals = [{"emoji": "<:ruby:846644957854695424>", "name": "ruby"},
            {"emoji": "<:emerald:847025055531008040>", "name": "emerald"},
            {"emoji": "<:bismuth:848478636142493736>", "name": "bismuth"},
            {"emoji": "<:sapphire:848478655940263946>", "name": "sapphire"}]


async def open_crystals(user):
    users = await get_crystals_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["emoji"] = 0
        users[str(user.id)]["name"] = 0

    with open("crystals.json", "w") as f:
        json.dump(users, f)
    return True


async def get_crystals_data():
    with open("crystals.json", "r") as f:
        users = json.load(f)
    return users


async def update_crystals(user, amount):
    num = random.randrange(20)
    if num == 0:
        name_1 = "bismuth"
    elif 5 >= num > 0:
        name_1 = "sapphire"
    elif 11 >= num > 5:
        name_1 = "emerald"
    else:
        name_1 = "ruby"

    for item in crystals:
        name = item["name"].lower()
        if name == name_1:
            emoji = item["emoji"]
            await update_clusters(user, name, emoji, amount)

    return name_1


async def update_clusters(user, name, emoji, amount):
    users = await get_crystals_data()
    try:
        index = 0
        t = None
        for thing in users[str(user.id)]:
            n = thing["name"]
            if n == name:
                users[str(user.id)][index]["name"] = name
                users[str(user.id)][index]["emoji"] = emoji
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)][index]["amount"] = new_amt
                t = 1
                break
            index += 1

        if t is None:
            obj = {"emoji": emoji, "name": name, "amount": amount}
            users[str(user.id)].append(obj)

    except:
        obj = {"emoji": emoji, "name": name, "amount": amount}
        users[str(user.id)] = [obj]

    with open("crystals.json", "w") as f:
        json.dump(users, f)

    return


class Crystals(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clusters(self, ctx):
        await open_crystals(ctx.author)
        user = ctx.author
        users = await get_crystals_data()
        try:
            bag = users[str(user.id)]
        except:
            bag = []

        em = discord.Embed(title="clusters")
        for item in bag:
            emoji = item["emoji"]
            name = item["name"]
            amount = item["amount"]

            em.add_field(name=name + emoji, value=amount)

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Crystals(client))
