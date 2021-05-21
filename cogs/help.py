import discord
from pymongo import MongoClient
from discord.ext import commands

from cogs import currency

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

cluster = MongoClient("mongodb+srv://bmer:Akshara1234@discordbot.hgnme.mongodb.net/discordBot?retryWrites=true&w=majority")
levelling = cluster["discord"]["leveling"]


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['server'])
    async def serverinfo(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)

        owner = str(ctx.guild.owner)
        ids = str(ctx.guild.id)
        region = str(ctx.guild.region)
        membercount = str(ctx.guild.member_count)

        icon = str(ctx.guild.icon_url)

        embed = discord.Embed(
            title="🤖 " + name + " info",
            description=description,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=ids, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=membercount, inline=True)

        await ctx.send(embed=embed)

    @commands.command(aliases=['user'])
    async def userinfo(self, ctx, member: discord.Member = None):
        global emoji
        member = ctx.author if not member else member
        embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
        embed.set_author(name=f'User info : {member}')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'Requested by : {ctx.author}')
        embed.add_field(name='ID:', value=member.id)
        embed.add_field(name='Guild name:', value=member.display_name)
        embed.add_field(name='Joined at:', value=member.joined_at)
        stats = levelling.find_one({"id": member.id})
        xp = stats["xp"]
        lvl = 0
        while True:
            if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                break
            lvl += 1
        embed.add_field(name="Level", value=f"{lvl}")
        embed.add_field(name='Top role:', value=member.top_role.mention)
        await currency.open_account(member)
        users = await currency.get_bank_data()
        wallet = users[str(member.id)]["wallet"]
        bankbal = users[str(member.id)]["bank"]
        embed.add_field(name="Wallet", value=wallet)
        embed.add_field(name="Bank balance", value=bankbal)
        '''user = member
        bag = users[str(user.id)]["bag"]
        for item in bag:
            emoji = item["emoji"]
            embed.add_field(name="Items", value=f"{emoji}")'''

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
