import datetime
import discord
import json
import os
import random
from discord.ext import commands

from main import client

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

mainshop = [{"emoji": "🔷", "name": "blue badge", "description": "display on profile", "price": "500"},
            {"emoji": "👑", "name": "crown", "description": "idk man", "price": "100"}]

os.chdir("C:\\Users\\Bharath Reddy Meruva\\Desktop\\my code\\discord bot\\cogs")


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


class Currency(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        await open_account(ctx.author)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining_time = str(datetime.timedelta(seconds=int(error.retry_after)))
            em = discord.Embed(title="Calm Down!")
            msg = "Try again after " + str(remaining_time)
            em.add_field(name=msg, value="You can only mine twice in a minute.")
            await ctx.channel.send(embed=em)

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            await open_account(ctx.author)
            user = ctx.author
        else:
            await open_account(member)
            user = member

        users = await get_bank_data()

        wallet_amt = users[str(user.id)]["wallet"]
        bank_amt = users[str(user.id)]["bank"]

        em = discord.Embed(title=f"{user.name}'s balance")
        em.set_thumbnail(url=user.avatar_url)
        em.add_field(name="Wallet", value=wallet_amt)
        em.add_field(name="Bank balance", value=bank_amt)
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
    async def daily(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        earnings = 250

        await ctx.send(f"You received a daily bonus of {earnings} berry")

        users[str(user.id)]["wallet"] += earnings

        with open("bank.json", "w") as f:
            json.dump(users, f)
        return True

    @commands.command()
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def mine(self, ctx):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        earnings = random.randrange(51)

        await ctx.send(f"You found {earnings} berry")

        users[str(user.id)]["wallet"] += earnings

        with open("bank.json", "w") as f:
            json.dump(users, f)
        return True

    @commands.command(aliases=['wit'])
    async def withdraw(self, ctx, amount=None):
        await open_account(ctx.author)
        if amount is None:
            await ctx.send("Please enter the amount")
            return

        bal = await update_bank(ctx.author)
        if amount == "max":
            amount = bal[1]
        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("You broke bro.\nSorry.")
            return
        if amount < 0:
            await ctx.send("Has to be a positive number genius!")
            return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "bank")

        await ctx.send(f"You withdrew {amount} berry!")

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount=None):
        await open_account(ctx.author)
        if amount is None:
            await ctx.send("Please enter the amount")
            return

        bal = await update_bank(ctx.author)
        if amount == "max":
            amount = bal[0]
        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("LOL \nNext time, check your wallet first.")
            return
        if amount < 0:
            await ctx.send("Has to be a positive number genius!")
            return

        await update_bank(ctx.author, -1 * amount)
        await update_bank(ctx.author, amount, "bank")

        await ctx.send(f"You deposited {amount} berry!")

    @commands.command(aliases=['gift', 'send'])
    async def transfer(self, ctx, member: discord.Member, amount=None):
        await open_account(ctx.author)
        await open_account(member)
        if amount is None:
            await ctx.send("Please enter the amount")
            return

        bal = await update_bank(ctx.author)
        if amount == "max":
            amount = bal[1]
        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("bank kinda dry my dude.")
            return
        if amount < 0:
            await ctx.send("Has to be a positive number genius!")
            return

        await update_bank(ctx.author, -1 * amount, "bank")
        await update_bank(member, amount, "bank")

        await ctx.send(f"You transferred {amount} berry!")

    @commands.command()
    async def gamble(self, ctx, amount=None):
        await open_account(ctx.author)
        if amount is None:
            await ctx.send("Please enter the amount")
            return

        bal = await update_bank(ctx.author)
        if amount == "max":
            amount = bal[0]
        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("LOL \nNext time, check your wallet first.")
            return
        if amount < 0:
            await ctx.send("Has to be a positive number genius!")
            return
        if amount < 200:
            await ctx.send("Has to be at least 200 berry!")
            return

        final = []
        for i in range(3):
            a = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
            final.append(a)

        await ctx.send("If at least 2 of the 3 letters match you double your gamble!")
        await ctx.send(str(final))

        if final[0] is final[1] and final[0] is final[2]:
            await update_bank(ctx.author, 4 * amount)
            await ctx.send(f"JACKPOT!!!\nYou won {5 * amount} berry!")
            return

        if final[0] is final[1] or final[0] is final[2] or final[2] is final[1]:
            await update_bank(ctx.author, amount)
            await ctx.send(f"You won {2 * amount} berry!")
        else:
            await update_bank(ctx.author, -1 * amount)
            await ctx.send("You lost, but you can always mine some more!")

    @commands.command(aliases=['steal'])
    async def rob(self, ctx, member: discord.Member):
        await open_account(ctx.author)
        await open_account(member)

        bal = await update_bank(member)
        robber = await update_bank(ctx.author)

        if member is ctx.author:
            await ctx.send("Are you actually trying to rob yourself?")
            return
        if robber[0] < 100:
            await ctx.send("You need at least 100 berry to rob another person.\nTry mining some berry.")
            return
        if bal[0] < 100:
            await ctx.send(f"{member.name} barely has any money.\nTry someone else.")
            return
        if member is None:
            await ctx.send("Mention who you are robbing next time.")
            return

        half_bal = int(bal[0] / 2)
        amount = random.randrange(0, half_bal)

        succ = random.randrange(2)

        if succ == 0:
            await update_bank(ctx.author, amount)
            await update_bank(member, -1 * amount)
            await ctx.send(f"You robbed {amount} berry from {member.name}!")
        else:
            bal_loss = await update_bank(ctx.author)
            loss = int(bal_loss[0] / 10)
            await update_bank(ctx.author, -1 * loss)
            await ctx.send(f"You were caught!\nYou lost {loss} berry in the process.")

    @commands.command()
    async def leaderboard(self, ctx, x=10):
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total, reverse=True)

        em = discord.Embed(title=f"Top {x} Richest People")
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            mem = client.get_user(id_)
            name = mem.name
            em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
            if index == x:
                break
            else:
                index += 1

        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Currency(client))
