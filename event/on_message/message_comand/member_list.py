import discord
import csv
import os
import function.send_message as send_message

async def main(client, message):
    if message.content.partition(' ')[2].strip() == '-h':
        await message.channel.send(
            '/member_list\n'
            'サーバーのメンバー一覧を CSV ファイルで取得します。'
        )
        return

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