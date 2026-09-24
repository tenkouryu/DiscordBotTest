from collections.abc import Iterable
from datetime import datetime

import discord

"""
    Discordの埋め込みメッセージを作成する共通処理。

    create_embed_message:
        タイトル、本文、色、フィールド、画像などを設定したEmbedを作成する。
"""


EmbedField = tuple[str, str, bool]


# 埋め込みメッセージを作成する共通処理。

def create_embed_message(
    title: str | None = None,
    description: str | None = None,
    *,
    color: int | discord.Colour = discord.Colour.blurple(),
    url: str | None = None,
    fields: Iterable[EmbedField] | None = None,
    thumbnail_url: str | None = None,
    image_url: str | None = None,
    footer_text: str | None = None,
    author_name: str | None = None,
    timestamp: datetime | None = None,
) -> discord.Embed:
    """指定した内容からDiscord用の埋め込みメッセージを作成する。"""
    embed = discord.Embed(
        title=title,
        description=description,
        colour=color,
        url=url,
        timestamp=timestamp,
    )

    if fields is not None:
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
    if image_url:
        embed.set_image(url=image_url)
    if footer_text:
        embed.set_footer(text=footer_text)
    if author_name:
        embed.set_author(name=author_name)

    return embed
