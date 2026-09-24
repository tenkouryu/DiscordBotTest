import csv
import io

import discord

"""
    サーバーロール設定CSVテンプレートコマンドを処理する。

    main:
        サーバーロール設定用CSVテンプレートを作成して送信する。
"""

async def main(message: discord.Message) -> None:
    """サーバーロール設定用 CSV テンプレートを送信する。"""
    if message.content.partition(" ")[2].strip() == "-h":
        await message.channel.send(
            "/server role template\n"
            "サーバーロール設定用 CSV テンプレートを取得します。"
        )
        return

    field_names = ["name", "color", *discord.Permissions.VALID_FLAGS]
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(field_names)
    writer.writerow([
        "設定するロール名を入力",
        "色を #RRGGBB 形式で入力（設定しない場合は列を削除）",
        *([
            "true または false を入力（設定しない場合は列を削除）"
        ] * len(discord.Permissions.VALID_FLAGS)),
    ])
    await message.channel.send(
        "サーバーロール設定用 CSV テンプレートです。",
        file=discord.File(
            io.BytesIO(output.getvalue().encode("utf-8-sig")),
            filename="server_role_template.csv",
        ),
    )
