import discord
import function.edit_roll as edit_roll


async def main(message):
    if message.content.partition(' ')[2].strip() == '-h':
        await message.channel.send(
            '/member role add @メンバー ロール名\n'
            '指定したメンバーにロールを追加します。'
        )
        return

    if not message.author.guild_permissions.manage_roles:
        await message.channel.send('メンバーのロールを追加する権限がありません。')
        return

    argument = message.content.partition(' ')[2]
    if not message.mentions:
        await message.channel.send(
            '使い方: /member role add @メンバー ロール名'
        )
        return

    _, _, role_name = argument.partition(' ')
    try:
        role = await edit_roll.add_role_to_member(
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
        f'{message.mentions[0].mention} にロール「{role.name}」を追加しました。'
    )
