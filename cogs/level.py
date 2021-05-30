import discord
from discord.ext import commands
from pymongo import MongoClient
from cogs import currency

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

level = ["yee", "chutney", "sambar", "gulu"]
levelnum = [5, 10, 15, 17]

cluster = MongoClient("mongodb+srv://bmer:Akshara1234@discordbot.hgnme.mongodb.net/discordBot?retryWrites=true&w=majority")
levelling = cluster["discord"]["leveling"]


class Levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        stats = levelling.find_one({"id": message.author.id})
        if not message.author.bot:
            if stats is None:
                newuser = {"id": message.author.id, "xp": 100}
                levelling.insert_one(newuser)
            else:
                xp = stats["xp"]+5
                levelling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                lvl = 0

                while True:
                    if xp < ((50*(lvl ** 2)) + (50 * lvl)):
                        break
                    lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                if xp == 0:
                    await message.channel.send(f"Well done {message.author.mention}! you reached **level:{lvl}**.")
                    await currency.open_account(message.author)
                    await currency.update_bank(message.author, 10*lvl, "bank")
                    await message.channel.send(f"You have received {10*lvl} berry as a reward!")
                    for i in range(len(level)):
                        if lvl == levelnum[i]:
                            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                            embed = discord.Embed(description=f"{message.author.mention} got the role **{level[i]}**.")
                            await message.channel.send(embed=embed)

    @commands.command(aliases=['level'])
    async def rank(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        stats = levelling.find_one({"id": member.id})
        if stats is None:
            embed = discord.Embed(description="You have not sent any messages!\nInteract to get a rank.")
            await ctx.channel.send(embed=embed)
        else:
            xp = stats["xp"]
            lvl = 0
            rank = 0
            while True:
                if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                    break
                lvl += 1
            xp -= ((50 * ((lvl-1) ** 2)) + (50 * (lvl - 1)))
            boxes = int((xp/(200*((1/2)*lvl)))*20)
            rankings = levelling.find().sort("xp", -1)
            for x in rankings:
                rank += 1
                if stats["id"] == x["id"]:
                    break
            embed = discord.Embed(title="{}'s level stats".format(member.name))
            embed.add_field(name="level", value=f"{lvl}", inline=True)
            embed.add_field(name="XP", value=f"{xp}/{(200*((1/2)*lvl))}", inline=True)
            embed.add_field(name="rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
            embed.add_field(name="progress bar [lvl]", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=True)
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(Levelsys(client))
