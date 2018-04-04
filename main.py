import chardet
import configparser
import time
import discord

# read config
config = configparser.ConfigParser()
config.read('./config.ini')
TOKEN = config.get('DISCORD', 'TOKEN')
TEXT_CHANNEL_ID = config.get('DISCORD', 'TEXT_CHANNEL_ID')

def second_to_hour(second_float):
    hour = int(second_float // 3600)
    minute = int(second_float // 60) % 60
    second_int = int(second_float) % 60
    return '{:d}:{:02d}:{:02d}'.format(hour, minute, second_int)

client = discord.Client()
join_time = {}

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_voice_state_update(before, after):
# on mutedでもこの関数は呼ばれるので, 動作をbefore, afterいずれかがNoneのときに限定
    if not before.voice.voice_channel and after.voice.voice_channel:    # join
        join_time[after.name] = time.time()
    elif before.voice.voice_channel and not after.voice.voice_channel:  # leave
        if join_time.get(after.name):    # 起動時に既にjoinしていた場合は除外
            diff_float = time.time() - join_time.get(after.name)
            diff_str = second_to_hour(diff_float)
            message = '{} has connected to voice channels for {}.'.format(after.mention, diff_str)
            await client.send_message(client.get_channel(TEXT_CHANNEL_ID), message)
            join_time.pop(after.name)   # join_timeの削除

client.run(TOKEN)
