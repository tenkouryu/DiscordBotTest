import discord
from .command import router
import function.discord.message.send_message as send_message

"""
    Discordメッセージ受信イベントを処理する。

    on_message_main:
        Bot自身のメッセージを除外し、コマンドルーターへ処理を渡す。
"""

async def on_message_main(
    client: discord.Client,
    message: discord.Message,
) -> None:
    # デバッグログを出力する。
        print(f'{message.author}からのメッセージ：{message.content}')
    
        # メッセージ送信者がBotの場合は無視する。
        if message.author.bot:
            return
        # 特定ロールからの送信の場合は管理者用処理を行う。
        if '管理人' in [role.name for role in message.author.roles]:
            # 管理者専用の処理。
             print(f'管理者：{message.author}からのメッセージ：{message.content}')
        if 0:
            # 「Hi」と発言したら「Hi」を返す。
            if message.content == 'Hi':
                # メッセージ自身のチャンネルへ送信する場合はmessage.channel.sendを使う。
                await message.channel.send('Hi')
                # 特定のチャンネルへ送信する場合はsend_message_to_channelを使う。
                await send_message.send_message_to_channel(client, message.channel, 'Hi')

        # /から始まるコマンドを処理する。
        # メッセージコマンドの処理を呼び出す。
        await router.parse_message_command(client, message)
        