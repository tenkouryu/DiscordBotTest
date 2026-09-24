import asyncio

import discord

"""
    Discordチャンネルのメッセージ削除を行う共通処理。

    delete_message_from_channel:
        指定したチャンネルからメッセージを削除する。

    delete_message_after:
        指定した秒数が経過した後にメッセージを削除する。
"""

# メッセージ削除に関する処理。
async def delete_message_from_channel(
    client: discord.Client,
    channel_id: int,
    message_id: int,
) -> None:
    """指定したチャンネルからメッセージを削除する共通処理。"""
    channel = client.get_channel(channel_id)
    if channel is not None:
        message = await channel.fetch_message(message_id)
        await message.delete()
    else:
        print(f"チャンネルID {channel_id} が見つかりませんでした。")


async def delete_message_after(
    client: discord.Client,
    channel_id: int,
    message_id: int,
    delay_seconds: float,
) -> None:
    """指定した秒数の後にメッセージを削除する。"""
    if delay_seconds < 0:
        raise ValueError("削除までの時間は0秒以上で指定してください。")

    await asyncio.sleep(delay_seconds)
    await delete_message_from_channel(client, channel_id, message_id)
