import discord
from function.security.permissions import can_manage_roles

"""
    メンバーのロール取得コマンドを処理する。

    _find_members_by_username:
        Discordユーザー名からメンバーを検索する。

    main:
        指定したメンバーのロール一覧を送信する。
"""

def _find_members_by_username(
    guild: discord.Guild,
    username: str,
) -> list[discord.Member]:
    """Discordユーザー名が一致するメンバーを取得する。"""
    return [
        member
        for member in guild.members
        if member.name.casefold() == username.casefold()
    ]


async def main(message: discord.Message) -> None:
    """指定したメンバーのロール一覧を返信する。"""
    argument = message.content.partition(" ")[2].strip()
    if argument == "-h" or not argument:
        await message.channel.send(
            "/member role get メンバー名\n"
            "指定したメンバーのロール一覧を表示します。"
        )
        return

    if not can_manage_roles(message.author):
        await message.channel.send('メンバーのロールを取得する権限がありません。')
        return

    if message.mentions:
        members = [message.mentions[0]]
    else:
        members = _find_members_by_username(message.guild, argument)

    if not members:
        await message.channel.send(f'メンバー「{argument}」が見つかりません。')
        return

    if len(members) > 1:
        names = ", ".join(f"{member.display_name} ({member.name})" for member in members)
        await message.channel.send(
            f'メンバー「{argument}」が複数見つかりました。名前を正確に指定してください: {names}'
        )
        return

    member = members[0]
    role_names = [role.name for role in member.roles]
    await message.channel.send(
        f'{member.mention} のロール: {", ".join(role_names)}'
    )
