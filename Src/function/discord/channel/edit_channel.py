import discord

"""
    Discordサーバーのカテゴリーとチャンネルを操作する共通処理。

    get_or_create_category:
        指定した名前のカテゴリーを取得し、なければ作成する。

    create_text_channel / create_voice_channel:
        テキストまたはボイスチャンネルを作成する。

    move_channel_to_category:
        チャンネルを指定したカテゴリーへ移動する。

    move_text_channel_to_category:
        テキストチャンネルを指定したカテゴリーへ移動する。

    move_voice_channel_to_category:
        ボイスチャンネルを指定したカテゴリーへ移動する。
"""


async def get_or_create_category(
    guild: discord.Guild,
    category_name: str,
) -> discord.CategoryChannel:
    """指定した名前のカテゴリーを取得し、なければ作成する。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    category_name = category_name.strip()
    if not category_name:
        raise ValueError("カテゴリー名を指定してください。")

    category = discord.utils.get(guild.categories, name=category_name)
    if category is None:
        category = await guild.create_category(category_name)
    return category


async def create_text_channel(
    guild: discord.Guild,
    channel_name: str,
    category_name: str | None = None,
) -> discord.TextChannel:
    """テキストチャンネルを作成し、指定があればカテゴリーへ配置する。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    channel_name = channel_name.strip()
    if not channel_name:
        raise ValueError("テキストチャンネル名を指定してください。")

    category = None
    if category_name is not None:
        category = await get_or_create_category(guild, category_name)

    return await guild.create_text_channel(channel_name, category=category)


async def create_voice_channel(
    guild: discord.Guild,
    channel_name: str,
    category_name: str | None = None,
) -> discord.VoiceChannel:
    """ボイスチャンネルを作成し、指定があればカテゴリーへ配置する。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    channel_name = channel_name.strip()
    if not channel_name:
        raise ValueError("ボイスチャンネル名を指定してください。")

    category = None
    if category_name is not None:
        category = await get_or_create_category(guild, category_name)

    return await guild.create_voice_channel(channel_name, category=category)


async def move_channel_to_category(
    channel: discord.abc.GuildChannel,
    category_name: str,
) -> discord.abc.GuildChannel:
    """指定したチャンネルをカテゴリーへ移動する。"""
    if channel is None:
        raise ValueError("チャンネルが指定されていません。")
    if channel.guild is None:
        raise ValueError("サーバーのチャンネルを指定してください。")

    category = await get_or_create_category(channel.guild, category_name)
    return await channel.edit(category=category)


async def move_text_channel_to_category(
    channel: discord.TextChannel,
    category_name: str,
) -> discord.TextChannel:
    """テキストチャンネルをカテゴリーへ移動する。"""
    if not isinstance(channel, discord.TextChannel):
        raise ValueError("テキストチャンネルを指定してください。")

    return await move_channel_to_category(channel, category_name)


async def move_voice_channel_to_category(
    channel: discord.VoiceChannel,
    category_name: str,
) -> discord.VoiceChannel:
    """ボイスチャンネルをカテゴリーへ移動する。"""
    if not isinstance(channel, discord.VoiceChannel):
        raise ValueError("ボイスチャンネルを指定してください。")

    return await move_channel_to_category(channel, category_name)


async def grant_channel_role_access(
    channel: discord.abc.GuildChannel,
    role_name: str,
) -> discord.abc.GuildChannel:
    """指定ロールにチャンネル参加権限を付与する。"""
    if channel is None or channel.guild is None:
        raise ValueError("サーバーのチャンネルを指定してください。")

    role_name = role_name.strip()
    if not role_name:
        raise ValueError("ロール名を指定してください。")

    role = discord.utils.get(channel.guild.roles, name=role_name)
    if role is None:
        raise ValueError(f"ロールが見つかりません: {role_name}")

    permissions = {"view_channel": True}
    if isinstance(channel, discord.TextChannel):
        permissions.update(
            send_messages=True,
            read_message_history=True,
        )
    elif isinstance(channel, discord.VoiceChannel):
        permissions.update(connect=True, speak=True)
    else:
        raise ValueError("テキストまたはボイスチャンネルを指定してください。")

    await channel.set_permissions(role, **permissions)
    return channel


async def grant_channel_member_access(
    channel: discord.abc.GuildChannel,
    member: discord.Member,
) -> discord.abc.GuildChannel:
    """指定メンバーにチャンネルへの閲覧・利用権限を付与する。"""
    if channel is None or channel.guild is None:
        raise ValueError("サーバーのチャンネルを指定してください。")
    if member.guild != channel.guild:
        raise ValueError("同じサーバーのメンバーを指定してください。")

    if isinstance(channel, discord.TextChannel):
        permissions = {
            "view_channel": True,
            "send_messages": True,
            "read_message_history": True,
        }
    elif isinstance(channel, discord.VoiceChannel):
        permissions = {
            "view_channel": True,
            "connect": True,
            "speak": True,
        }
    else:
        raise ValueError("テキストまたはボイスチャンネルを指定してください。")

    await channel.set_permissions(member, **permissions)
    return channel


async def sync_channel_role_access(
    channel: discord.abc.GuildChannel,
    role_names: list[str],
) -> discord.abc.GuildChannel:
    """指定ロールだけにチャンネルアクセスを許可する。"""
    if channel is None or channel.guild is None:
        raise ValueError("サーバーのチャンネルを指定してください。")

    managed_permissions = (
        ("view_channel", "send_messages", "read_message_history")
        if isinstance(channel, discord.TextChannel)
        else ("view_channel", "connect", "speak")
        if isinstance(channel, discord.VoiceChannel)
        else None
    )
    if managed_permissions is None:
        raise ValueError("テキストまたはボイスチャンネルを指定してください。")

    role_names = list(dict.fromkeys(name.strip() for name in role_names if name.strip()))
    roles_by_name = {role.name: role for role in channel.guild.roles}
    missing_roles = [name for name in role_names if name not in roles_by_name]
    if missing_roles:
        raise ValueError("ロールが見つかりません: " + ", ".join(missing_roles))

    allowed_roles = {roles_by_name[name] for name in role_names}
    for role in channel.guild.roles:
        if role.is_default() or role in allowed_roles:
            continue

        overwrite = channel.overwrites_for(role)
        changed = False
        for permission in managed_permissions:
            if getattr(overwrite, permission) is True:
                setattr(overwrite, permission, None)
                changed = True
        if changed:
            await channel.set_permissions(
                role,
                overwrite=None if overwrite.is_empty() else overwrite,
            )

    for role in allowed_roles:
        await channel.set_permissions(
            role,
            **{permission: True for permission in managed_permissions},
        )

    return channel