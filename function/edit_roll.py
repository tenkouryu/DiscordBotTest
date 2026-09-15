import discord

"""サーバーのロールを操作する共通処理。"""
async def add_role_to_server(
    guild: discord.Guild, role_name: str
) -> discord.Role:
    """指定した名前のロールをサーバーに追加する。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    role_name = role_name.strip()
    if not role_name:
        raise ValueError("ロール名を指定してください。")

    return await guild.create_role(name=role_name)

async def remove_role_from_server(
    guild: discord.Guild, role_name: str
) -> discord.Role:
    """指定した名前のロールをサーバーから削除する。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    role_name = role_name.strip()
    if not role_name:
        raise ValueError("削除するロール名を指定してください。")

    role = next(
        (
            role
            for role in guild.roles
            if role.name == role_name and not role.is_default()
        ),
        None,
    )
    if role is None:
        raise ValueError(f'ロール「{role_name}」が見つかりません。')

    await role.delete()
    return role

async def edit_role_permissions(
    guild: discord.Guild,
    role_name: str,
    permission_name: str,
    enabled: bool,
) -> discord.Role:
    """指定したロールの権限を有効または無効にする。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    role_name = role_name.strip()
    permission_name = permission_name.strip().lower()
    if not role_name:
        raise ValueError("ロール名を指定してください。")
    if not permission_name:
        raise ValueError("権限名を指定してください。")

    role = next(
        (
            role
            for role in guild.roles
            if role.name == role_name and not role.is_default()
        ),
        None,
    )
    if role is None:
        raise ValueError(f'ロール「{role_name}」が見つかりません。')

    permissions = role.permissions
    if permission_name not in permissions.VALID_FLAGS:
        raise ValueError(f'権限「{permission_name}」は存在しません。')

    permissions.update(**{permission_name: enabled})
    return await role.edit(permissions=permissions)

"""メンバーのロールを操作する共通処理。"""
async def add_role_to_member(
    member: discord.Member, role_name: str
) -> discord.Role:
    """指定したメンバーにロールを追加する。"""
    if member is None:
        raise ValueError("メンバーが指定されていません。")

    role_name = role_name.strip()
    if not role_name:
        raise ValueError("ロール名を指定してください。")

    role = next(
        (role for role in member.guild.roles if role.name == role_name),
        None,
    )
    if role is None:
        raise ValueError(f'ロール「{role_name}」が見つかりません。')

    await member.add_roles(role)
    return role


async def remove_role_from_member(
    member: discord.Member, role_name: str
) -> discord.Role:
    """指定したメンバーからロールを削除する。"""
    if member is None:
        raise ValueError("メンバーが指定されていません。")

    role_name = role_name.strip()
    if not role_name:
        raise ValueError("ロール名を指定してください。")

    role = next(
        (role for role in member.guild.roles if role.name == role_name),
        None,
    )
    if role is None:
        raise ValueError(f'ロール「{role_name}」が見つかりません。')

    await member.remove_roles(role)
    return role
