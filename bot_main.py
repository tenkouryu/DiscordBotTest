import json
import discord
from event.on_ready import on_ready as on_ready_event
from event.on_message import on_message as on_message_event
from event.on_reaction import on_reaction as on_reaction_event
from event.on_member_join import on_member_join as on_member_join_event
from event.on_voice_state_update import on_voice_state_update as on_voice_state_update_event


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
async def on_ready() -> None:
    await on_ready_event.on_ready_main(client)

"""メッセージ受信時に実行されるイベントハンドラ"""
@client.event
async def on_message(message: discord.Message) -> None:
    await on_message_event.on_message_main(client, message)

"""リアクション追加時に実行されるイベントハンドラ"""
@client.event
async def on_reaction_add(
    reaction: discord.Reaction,
    user: discord.User,
) -> None:
    await on_reaction_event.on_reaction_main(client, reaction, user)

"""新規メンバー参加時に実行されるイベントハンドラ"""
@client.event
async def on_member_join(member: discord.Member) -> None:
    await on_member_join_event.on_member_join_main(client, REDIRECT_CHANNEL_ID, member)

"""メンバーのボイスチャンネル出入り時に実行されるイベントハンドラ"""
@client.event
async def on_voice_state_update(
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState,
) -> None:
    await on_voice_state_update_event.on_voice_state_update_main(client, REDIRECT_CHANNEL_ID, member, before, after)

#----------Botの起動処理はここ----------
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)