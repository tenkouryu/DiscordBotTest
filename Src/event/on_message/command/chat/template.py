import csv
import io

import discord

"""
    チャット添付ファイル取得用CSVテンプレートコマンドを処理する。

    main:
        添付ファイル取得用CSVテンプレートを作成して送信する。
"""

async def main(message: discord.Message) -> None:
    """チャット添付ファイル取得用CSVテンプレートを送信する。"""
    if message.content.partition(" ")[2].strip() == "-h":
        await message.channel.send(
            "/chat template\n"
            "カテゴリ名、チャンネル名、開始日を指定するCSVテンプレートを取得します。"
        )
        return

    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["category_name", "channel_name", "start_date", "extension"])
    writer.writerow(["カテゴリー名", "チャンネル名", "YYYY-MM-DD", "png"])
    await message.channel.send(
        "チャット添付ファイル取得用CSVテンプレートです。",
        file=discord.File(
            io.BytesIO(output.getvalue().encode("utf-8-sig")),
            filename="chat_template.csv",
        ),
    )