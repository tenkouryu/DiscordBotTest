import discord
from .command import message_command
import function.send_message as send_message

#----------メッセージ受信時の処理はここ----------
async def on_message_main(client, message):
       # デバッグログ
        print(f'{message.author}からのメッセージ：{message.content}')
    
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return
        if '管理人' in [role.name for role in message.author.roles]:  # 例: 特定ロールからの送信の場合
            # 管理者専用の処理
             print(f'管理者：{message.author}からのメッセージ：{message.content}')
        if 0:
            # 「Hi」と発言したら「Hi」が返る処理
            if message.content == 'Hi':
                # メッセージを送信する(message自体が送ってきたチャンネルを持ってるので、そこに送信する場合はmessage.channel.sendを使う)
                await message.channel.send('Hi')
                #特定のチャンネルに送信する場合は、send_message_to_channel関数を使う
                await send_message.send_message_to_channel(client, message.channel, 'Hi')

        # /から始まるコマンドの処理
        await message_command.parse_message_command(client, message)  # メッセージコマンドの処理を呼び出す
        