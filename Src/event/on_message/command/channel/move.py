import re

import discord
import function.discord.channel.edit_channel as edit_channel
from function.security.permissions import can_manage_channels

"""
    チャンネル移動コマンドを処理する。

    main:
        指定したチャンネルをカテゴリーへ移動する。
"""

async def main(message: discord.Message) -> None:
    arguments = message.content.partition(' ')[2].strip()
    if arguments in ('', '-h'):
        await message.channel.send('/channel move #チャンネル カテゴリー名')
        return

    if not can_manage_channels(message.author):
        await message.channel.send('チャンネルを管理する権限がありません。')
        return

    channel = message.channel_mentions[0] if message.channel_mentions else message.channel
    category_name = re.sub(r'<#\d+>', '', arguments, count=1).strip()
    if not category_name:
        await message.channel.send('移動先のカテゴリー名を指定してください。')
        return

    try:
        moved_channel = await edit_channel.move_channel_to_category(
            channel,
            category_name,
        )
    except ValueError as error:
        await message.channel.send(str(error))
        return
    except discord.Forbidden:
        await message.channel.send('Botにチャンネルを管理する権限がありません。')
        return

    await message.channel.send(
        f'チャンネル「{moved_channel.name}」をカテゴリー「{category_name}」へ移動しました。'
    )