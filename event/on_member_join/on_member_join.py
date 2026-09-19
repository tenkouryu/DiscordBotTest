import discord

def on_member_join_main(
    client: discord.Client,
    channel_id: int,
    member: discord.Member,
) -> None:
    print(f'{member}がメンバーとして参加しました')
    # 新規メンバーが参加したら「ようこそ！」と返す処理
    discord.utils.get(client.get_all_channels(), id=channel_id).send('ようこそ！')