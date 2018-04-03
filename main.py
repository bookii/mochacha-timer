import chardet
import configparser
import time
import discord

# read config
config = configparser.ConfigParser()
config.read('./config.ini')
TOKEN = config.get('DISCORD', 'TOKEN')
SERVER_ID = config.get('DISCORD', 'SERVER_ID')
CHANNEL_ID = config.get('DISCORD', 'CHANNEL_ID')

class MemberLog:
    def __init__(self, member):
        self.member = member
        self.join_time = None

    def set_join_time(self):
        self.join_time = time.time()
    
    def get_join_time(self):
        return self.join_time

def second_to_hour(second):
    hour = second // 3600
    minute = second // 60
    return '%d:%02d:%02d' % (hour, minute, int(second))

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    for member in client.get_server(SERVER_ID).members:
        member_log = MemberLog(member)
        member_before = member_after = member

        @client.event
        async def on_voice_state_update(member_before, member_after):
            if member_after.voice.voice_channel and member_after.voice.voice_channel.id == CHANNEL_ID:
                member_log.set_join_time()
            elif member_before.voice.voice_channel and member_before.voice.voice_channel.id:
                if member_log.get_join_time():    # 起動時に既にjoinしていた場合は除外
                    diff_second = time.time() - member_log.get_join_time()
                    print(second_to_hour(diff_second))

client.run(TOKEN)