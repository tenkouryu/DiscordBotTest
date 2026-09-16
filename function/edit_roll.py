import discord
import re

"""サーバーのロールを操作する共通処理。"""
def get_role_settings(
    guild: discord.Guild, role_name: str
) -> dict:
    """指定したロールの基本設定と権限を読み出す。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    role_name = role_name.strip()
    if not role_name:
        raise ValueError("ロール名を指定してください。")

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

    permissions = {
        permission_name: getattr(role.permissions, permission_name)
        for permission_name in role.permissions.VALID_FLAGS
    }

    return {
        "id": role.id,
        "name": role.name,
        "color": f"#{role.color.value:06X}",
        "permissions": permissions,
    }

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

async def edit_role_color(
    guild: discord.Guild,
    role_name: str,
    color_text: str,
) -> discord.Role:
    """指定したロールの色を変更する。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    role_name = role_name.strip()
    color_text = color_text.strip()
    if not role_name:
        raise ValueError("ロール名を指定してください。")
    if not re.fullmatch(r"#?[0-9a-fA-F]{6}", color_text):
        raise ValueError("色は #RRGGBB 形式で指定してください。")

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

    color = discord.Colour(int(color_text.lstrip("#"), 16))
    return await role.edit(color=color)

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
