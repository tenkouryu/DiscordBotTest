import re

import discord
import function.edit_channel as edit_channel


def _arguments(message):
    return message.content.partition(' ')[2].strip()


async def _send_help(message):
    await message.channel.send(
        '/channel create text チャンネル名 [カテゴリー名]\n'
        '/channel create voice チャンネル名 [カテゴリー名]\n'
        '/channel move #チャンネル カテゴリー名'
    )


async def main(message):
    arguments = _arguments(message)
    if arguments in ('', '-h'):
        await _send_help(message)
        return

    if not message.author.guild_permissions.manage_channels:
        await message.channel.send('チャンネルを管理する権限がありません。')
        return

    parts = arguments.split(maxsplit=2)
    action = parts[0].lower()

    try:
        if action == 'create':
            if len(parts) < 3:
                raise ValueError('作成するチャンネルの種類と名前を指定してください。')

            channel_type = parts[1].lower()
            channel_name, separator, category_name = parts[2].partition(' ')
            if not separator:
                channel_name = channel_name.strip()
                category_name = None
            else:
                channel_name, category_name = channel_name.strip(), category_name.strip()
                if not category_name:
                    category_name = None

            if channel_type == 'text':
                channel = await edit_channel.create_text_channel(
                    message.guild,
                    channel_name,
                    category_name,
                )
            elif channel_type == 'voice':
                channel = await edit_channel.create_voice_channel(
                    message.guild,
                    channel_name,
                    category_name,
                )
            else:
                raise ValueError('種類は text または voice を指定してください。')

            await message.channel.send(f'チャンネル「{channel.name}」を作成しました。')
            return

        if action == 'move':
            if len(parts) < 2:
                raise ValueError('移動先のカテゴリー名を指定してください。')

            channel = message.channel_mentions[0] if message.channel_mentions else message.channel
            category_name = re.sub(r'<#\d+>', '', arguments[len('move'):], count=1).strip()
            if not category_name:
                raise ValueError('移動先のカテゴリー名を指定してください。')

            moved_channel = await edit_channel.move_channel_to_category(
                channel,
                category_name,
            )
            await message.channel.send(
                f'チャンネル「{moved_channel.name}」をカテゴリー「{category_name}」へ移動しました。'
            )
            return

        raise ValueError('操作は create または move を指定してください。')
    except ValueError as error:
        await message.channel.send(str(error))
    except discord.Forbidden:
        await message.channel.send('Botにチャンネルを管理する権限がありません。')
