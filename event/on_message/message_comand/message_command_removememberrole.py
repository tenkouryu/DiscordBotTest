import discord
import function.edit_roll as edit_roll


async def main(message):
    if not message.author.guild_permissions.manage_roles:
        await message.channel.send('メンバーのロールを削除する権限がありません。')
        return

    argument = message.content.partition(' ')[2]
    if not message.mentions:
        await message.channel.send(
            '使い方: /removememberrole @メンバー ロール名'
        )
        return

    _, _, role_name = argument.partition(' ')
    try:
        role = await edit_roll.remove_role_from_member(
            message.mentions[0],
            role_name,
        )
    except ValueError as error:
        await message.channel.send(str(error))
        return
    except discord.Forbidden:
        await message.channel.send('Botにメンバーのロールを変更する権限がありません。')
        return

    await message.channel.send(
        f'{message.mentions[0].mention} からロール「{role.name}」を削除しました。'
    )
