import discord
import function.edit_roll as edit_roll


async def main(message):
    if not message.author.guild_permissions.manage_roles:
        await message.channel.send('ロールを追加する権限がありません。')
        return

    try:
        role = await edit_roll.add_role_to_server(message.guild, message.content.partition(' ')[2])
    except ValueError as error:
        await message.channel.send(str(error))
        return
    except discord.Forbidden:
        await message.channel.send('Botにロールを追加する権限がありません。')
        return

    await message.channel.send(f'ロール「{role.name}」を追加しました。')
