from tabnanny import check
import discord
import os
from twitch_util import check_user_online
import util
from discord.ext import commands, tasks
import sys

client = discord.Client()

notif_sent_out = False

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    notif_sent_out = False
    send_twitch_notif.start()


@client.event
async def on_guild_join(guild):
    for channel in guild.channels:
        if channel.name == 'twitch-announcements':
            return
    await guild.create_text_channel('twitch-announcements')

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return

    if message.content.startswith('$test'):
        print("TESTING IN $test")
        data = check_user_online()
        if(data):
            await message.channel.send('{} is live and playing {}! Check them out! https://twitch.tv/{}'.format(data.user_name,data.game_name,data.user_name))
        else:
            #take out when actually set up interval to check twitch api
            await message.channel.send('No data found!')
    
    if message.content.startswith('$woop woop'):
        for guild in client.guilds:
            try:
                data = check_user_online()
                if(data):
                    print('data found')
                    await util.get_twitch_announcements(guild).send(
                        '@everyone {} is live and playing {}! Check them out! https://twitch.tv/{}'.format(data.user_name,data.game_name,data.user_name))
                else:
                    await util.get_twitch_announcements(guild).send(
                        'No Stream right now :('
                    )
            except Exception as e:
                print(str(e), file=sys.stderr)


            

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


@tasks.loop(minutes=1)
async def send_twitch_notif():
    print('test', len(client.guilds))
    for guild in client.guilds:
        try:
            global notif_sent_out
            data = check_user_online()
            if(data and not notif_sent_out):
                print('data found')
                await util.get_twitch_announcements(guild).send(
                    '@everyone {} is live and playing {}! Check them out! https://twitch.tv/{}'.format(data.user_name,data.game_name,data.user_name))
                notif_sent_out = True

            elif (not data and notif_sent_out):
                notif_sent_out = False
                await util.get_twitch_announcements(guild).send(
                'Wooper would like to say thank you to everyone who joined the stream!')
            # else:
            #     print('no data found')
            #     print('test again')
            #     print(util.get_twitch_announcements(guild))
            #     await util.get_twitch_announcements(guild).send(
            #         'no stream atm :(')
        except Exception as e:
            print(str(e), file=sys.stderr)

client.run(os.getenv('TOKEN'))