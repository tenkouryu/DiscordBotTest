import discord

"""
    Discordチャンネルへのメッセージ送信を行う共通処理。

    send_message_to_channel:
        指定したチャンネルへテキストメッセージを送信する。

    send_message_to_channel_with_file:
        指定したチャンネルへテキストメッセージとファイルを送信する。
"""
async def send_message_to_channel(
    client: discord.Client,
    channel_id: int,
    message_text: str,
) -> None:
    channel = client.get_channel(channel_id)
    if channel is not None:
        await channel.send(message_text)
    else:
        print(f'チャンネルID {channel_id} が見つかりませんでした。')

async def send_message_to_channel_with_file(
    client: discord.Client,
    channel_id: int,
    message_text: str,
    file_path: str,
) -> None:
    channel = client.get_channel(channel_id)
    if channel is not None:
        await channel.send(message_text, file=discord.File(file_path))
    else:
        print(f'チャンネルID {channel_id} が見つかりませんでした。')
