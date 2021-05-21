import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
os.chdir("C:\\Users\\Bharath Reddy Meruva\\Desktop\\my code\\discord bot\\cogs")

mainshop = [{"emoji": "🔷", "name": "blue badge", "description": "display on profile", "price": "500"},
            {"emoji": "👑", "name": "crown", "description": "idk man", "price": "100"}]


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("bank.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)
    return users


async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("bank.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            emoji = item["emoji"]
            break
    if name_ is None:
        return [False, 1]
    cost = int(price * amount)
    users = await get_bank_data()
    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1

        if t is None:
            obj = {"emoji": emoji, "item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)

    except:
        obj = {"emoji": emoji, "item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("bank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "wallet")
    return [True, "Worked"]


async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = discord.Embed(title="inventory")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name=name, value=amount)

    await ctx.send(embed=em)


class Shop(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def shop(self, ctx):
        em = discord.Embed(title="shop")
        for item in mainshop:
            emoji = item["emoji"]
            name = item["name"]
            price = item["price"]
            desc = item["description"]
            em.add_field(name=emoji + name, value=f"{price} berries| {desc}")

        await ctx.send(embed=em)

    @commands.command()
    async def buy(self, ctx, *, item, amount=1):
        await open_account(ctx.author)

        res = await buy_this(ctx.author, item, amount)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("the item is not available")
                return
            if res[1] == 2:
                await ctx.send(f"You don't have enough berry to buy this item.")
                return

        await ctx.send(f"{item} acquired.")

    @commands.command()
    async def inventory(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()
        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em = discord.Embed(title="inventory")
        for item in bag:
            name = item["item"]
            amount = item["amount"]
            emoji = item["emoji"]
            em.add_field(name=emoji + name, value=amount, inline=False)

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Shop(client))
