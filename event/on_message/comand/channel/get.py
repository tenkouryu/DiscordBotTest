import csv
import io

import discord


def export_channels_to_csv(guild: discord.Guild) -> bytes:
    """サーバーのチャンネル一覧をCSVデータとして作成する。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["name", "type", "category"])
    for channel in guild.channels:
        if isinstance(channel, discord.TextChannel):
            channel_type = "text"
        elif isinstance(channel, discord.VoiceChannel):
            channel_type = "voice"
        else:
            continue

        writer.writerow([
            channel.name,
            channel_type,
            channel.category.name if channel.category else "",
        ])

    return output.getvalue().encode("utf-8-sig")


async def main(message: discord.Message) -> None:
    """サーバーのチャンネル一覧をCSVファイルとして送信する。"""
    if message.content.partition(" ")[2].strip() == "-h":
        await message.channel.send(
            "/channel get\n"
            "サーバーのチャンネル一覧をCSVファイルで取得します。"
        )
        return

    if not message.author.guild_permissions.manage_channels:
        await message.channel.send("チャンネルを管理する権限がありません。")
        return

    await message.channel.send(
        "チャンネル一覧を送信します。",
        file=discord.File(
            io.BytesIO(export_channels_to_csv(message.guild)),
            filename="channels_list.csv",
        ),
    )