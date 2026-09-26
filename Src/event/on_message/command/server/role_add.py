import discord
import function.discord.role.edit_roll as edit_roll
from function.security.permissions import can_manage_roles

"""
    サーバーへのロール追加コマンドを処理する。

    main:
        サーバーへ新しいロールを追加する。
"""

async def main(message: discord.Message) -> None:
    if message.content.partition(' ')[2].strip() == '-h':
        await message.channel.send(
            '/server add_role ロール名\n'
            'サーバーにロールを追加します。'
        )
        return

    if not can_manage_roles(message.author):
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
