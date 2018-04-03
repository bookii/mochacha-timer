import chardet
import configparser
import time
import discord

# read config
config = configparser.ConfigParser()
config.read('./config.ini')
SERVER_ID = config.get('DISCORD', 'server_id')
TOKEN = config.get('DISCORD', 'token')

class MemberLog:
    def __init__(self, member):
        self.member = member
        self.join_time = None

    def set_join_time(self):
        self.join_time = time.time()
    
    def get_join_time(self):
        return self.join_time

def secs_to_hours(secs):
    hours = secs // 3600
    minutes = secs // 60
    return '%d:%02d:%02d' % (hours, minutes, int(secs))

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
            if member_after.voice.voice_channel:
                print(member_after.voice.voice_channel.id)
                member_log.set_join_time()
            elif member_before.voice.voice_channel:
                if member_log.get_join_time:    # 起動時に既にjoinしていた場合は除外
                    diff_secs = time.time() - member_log.get_join_time()
                    print(secs_to_hours(diff_secs))

client.run(TOKEN)