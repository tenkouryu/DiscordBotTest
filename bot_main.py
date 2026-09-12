import json
import discord
import event.on_ready
import event.on_message
import event.on_reaction
import event.on_member_join
import event.on_voice_state_update


#----------Botの設定はここ----------
#Botの設定を読み込み
with open('config/config.json') as f:
    config = json.load(f)
TOKEN = config['BOT_TOKEN']
REDIRECT_CHANNEL_ID = config['REDIRECT_CHANNEL_ID']
# 接続に必要なオブジェクトを生成
intents_set = discord.Intents.default() 
intents_set.message_content = True      #メッセージの内容を取得するために必要
intents_set.reactions = True            #リアクションを取得するために必要
intents_set.members = True              #メンバー情報を取得するために必要
intents_set.voice_states = True         #ボイスチャンネルの状態を取得するために必要
client = discord.Client(intents=intents_set)

#----------イベントハンドラ群はここ----------
"""Bot起動時に実行されるイベントハンドラ"""
@client.event
async def on_ready():
    await event.on_ready.on_ready_main(client)

"""メッセージ受信時に実行されるイベントハンドラ"""
@client.event
async def on_message(message):
    await event.on_message.on_message_main(client, message)

"""リアクション追加時に実行されるイベントハンドラ"""
@client.event
async def on_reaction_add(reaction, user):
   await event.on_reaction.on_reaction_main(client, REDIRECT_CHANNEL_ID, reaction, user)

"""新規メンバー参加時に実行されるイベントハンドラ"""
@client.event
async def on_member_join(member):
    await event.on_member_join.on_member_join_main(client, REDIRECT_CHANNEL_ID, member)

"""メンバーのボイスチャンネル出入り時に実行されるイベントハンドラ"""
@client.event
async def on_voice_state_update(member, before, after):
    await event.on_voice_state_update.on_voice_state_update_main(client, REDIRECT_CHANNEL_ID, member, before, after)

#----------Botの起動処理はここ----------
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)