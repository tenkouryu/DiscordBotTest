import discord
import csv
import os
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

        if message.content == '/list':        
            # メンバーのリストを取得
            members = message.guild.members
            # CSVファイルに書き込む
            with open('members_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['名前', '表示名', 'ロール'])  # ヘッダー行
                for member in members:
                    writer.writerow([ member.name, member.display_name, ', '.join([role.name for role in member.roles])])
            # CSVファイルを指定したチャンネルに送信する
            await send_message.send_message_to_channel_with_file(client, message.channel.id, 'メンバーリストを送信します。', 'members_list.csv')
            # 送信後にCSVファイルを削除する
            if os.path.exists('members_list.csv'):
                                os.remove('members_list.csv')