import discord
import function.edit_channel as edit_channel


async def main(message: discord.Message) -> None:
    arguments = message.content.partition(' ')[2].strip()
    if arguments in ('', '-h'):
        await message.channel.send(
            '/channel create text チャンネル名 [カテゴリー名]\n'
            '/channel create voice チャンネル名 [カテゴリー名]'
        )
        return

    if not message.author.guild_permissions.manage_channels:
        await message.channel.send('チャンネルを管理する権限がありません。')
        return

    parts = arguments.split(maxsplit=2)
    if len(parts) < 3:
        await message.channel.send('作成するチャンネルの種類と名前を指定してください。')
        return

    channel_type = parts[0].lower()
    channel_name, separator, category_name = parts[2].partition(' ')
    category_name = category_name.strip() if separator else None
    category_name = category_name or None

    try:
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
    except ValueError as error:
        await message.channel.send(str(error))
        return
    except discord.Forbidden:
        await message.channel.send('Botにチャンネルを管理する権限がありません。')
        return

    await message.channel.send(f'チャンネル「{channel.name}」を作成しました。')