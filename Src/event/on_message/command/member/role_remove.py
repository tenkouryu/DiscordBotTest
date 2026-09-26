import discord
import function.discord.role.edit_roll as edit_roll
from function.security.permissions import can_manage_roles

"""
    メンバーからのロール削除コマンドを処理する。

    main:
        指定したメンバーからロールを削除する。
"""

async def main(message: discord.Message) -> None:
    if message.content.partition(' ')[2].strip() == '-h':
        await message.channel.send(
            '/member role remove @メンバー ロール名\n'
            '指定したメンバーからロールを削除します。'
        )
        return

    if not can_manage_roles(message.author):
        await message.channel.send('メンバーのロールを削除する権限がありません。')
        return

    argument = message.content.partition(' ')[2]
    if not message.mentions:
        await message.channel.send(
            '使い方: /member role remove @メンバー ロール名'
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
