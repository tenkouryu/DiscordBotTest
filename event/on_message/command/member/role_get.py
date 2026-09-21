import discord


def _find_members(
    guild: discord.Guild,
    member_name: str,
) -> list[discord.Member]:
    """名前または表示名が一致するメンバーを取得する。"""
    return [
        member
        for member in guild.members
        if member.name == member_name or member.display_name == member_name
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

    if message.mentions:
        members = [message.mentions[0]]
    else:
        members = _find_members(message.guild, argument)

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
