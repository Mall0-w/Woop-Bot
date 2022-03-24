import discord
import os

client= discord.Client()

@client.event
async def on_ready():
    print("Hi there! Im tallyBot, you can learn more about me by using $thelp")

client.run(os.getenv('Token'))