import discord

"""
    Discordサーバーへのメンバー参加イベントを処理する。

    on_member_join_main:
        新しく参加したメンバーへ歓迎メッセージを送信する。
"""

def on_member_join_main(
    client: discord.Client,
    channel_id: int,
    member: discord.Member,
) -> None:
    print(f'{member}がメンバーとして参加しました')
    # 新規メンバーが参加したら「ようこそ！」と返す。
    discord.utils.get(client.get_all_channels(), id=channel_id).send('ようこそ！')