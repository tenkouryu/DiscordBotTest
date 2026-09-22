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