import discord

#メッセージ送信に関する処理はここ
"""指定したチャンネルにメッセージを送信する共通処理"""
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

"""指定したチャンネルに添付ファイル付きメッセージを送信する共通処理"""
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
