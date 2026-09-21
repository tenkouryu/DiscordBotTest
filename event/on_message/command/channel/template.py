import csv
import io

import discord


async def main(message: discord.Message) -> None:
    """チャンネル設定用 CSV テンプレートを送信する。"""
    if message.content.partition(" ")[2].strip() == "-h":
        await message.channel.send(
            "/channel template\n"
            "チャンネル設定用 CSV テンプレートを取得します。"
        )
        return

    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["name", "type", "category"])
    writer.writerow([
        "設定するチャンネル名を入力",
        "text または voice を入力",
        "所属カテゴリー名を入力（設定しない場合は列を削除）",
    ])
    await message.channel.send(
        "チャンネル設定用 CSV テンプレートです。",
        file=discord.File(
            io.BytesIO(output.getvalue().encode("utf-8-sig")),
            filename="channel_template.csv",
        ),
    )
