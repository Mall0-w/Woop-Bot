import discord
import os
import util

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content.startswith('$test'):
        await message.channel.send('test!')

    if message.content.startswith('$hydropump'):
        if any(role.permissions.kick_members for role in message.author.roles):
            targets = util.parse_target(message)
            if(targets == None or len(targets) == 0):
                await message.channel.send("Wooper needs a target for HydroPump! Make sure to @ your target!")
            else:
                await message.channel.send('Wooper used HyrdroPump on {}! \nhttps://c.tenor.com/cVBqmR1xsysAAAAM/wooper-snek.gif'.format(util.format_list_of_users(targets)))
                for user in targets:
                    await user.kick()
        else:
            await message.channel.send("Wooper says you must be able to kick members to use this command!\nhttps://media0.giphy.com/media/tRUtppFnqVGzC/giphy.gif")

         

client.run(os.getenv('TOKEN'))