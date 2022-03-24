#given command, find targets of command
def parse_target(message, single_target=False):
    try:
        if(single_target):
            return message.mentions[0]
        else:
            return message.mentions
    except:
        return None

def format_list_of_users(user_list):
    try:
        format_string = ""
        for user in user_list:
            if user == user_list[-1]:
                format_string += str(user.mention)
            else:
                format_string += str(user.mention) +", "
        return format_string
    except:
        return ""

def get_twitch_announcements(guild):
    for channel in guild.channels:
        if channel.name == 'twitch-announcements':
            return channel
    return None