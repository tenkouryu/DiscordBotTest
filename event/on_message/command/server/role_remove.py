import discord
import function.edit_roll as edit_roll


async def main(message: discord.Message) -> None:
    if message.content.partition(' ')[2].strip() == '-h':
        await message.channel.send(
            '/server remove_role ロール名\n'
            'サーバーからロールを削除します。'
        )
        return

    if not message.author.guild_permissions.manage_roles:
        await message.channel.send('ロールを削除する権限がありません。')
        return

    try:
        role = await edit_roll.remove_role_from_server(
            message.guild,
            message.content.partition(' ')[2],
        )
    except ValueError as error:
        await message.channel.send(str(error))
        return
    except discord.Forbidden:
        await message.channel.send('Botにロールを削除する権限がありません。')
        return
    except discord.NotFound:
        await message.channel.send('指定したロールはすでに削除されています。')
        return

    await message.channel.send(f'ロール「{role.name}」を削除しました。')
