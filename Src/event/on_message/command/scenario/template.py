import discord

from function.scenario.scenario_template import create_scenario_template

"""
    台本進行用CSVテンプレートコマンドを処理する。

    main:
        台本登録用CSVテンプレートを作成して送信する。
"""


async def main(message: discord.Message) -> None:
    """台本登録用CSVテンプレートを送信する。"""
    if message.content.partition(" ")[2].strip() == "-h":
        await message.channel.send(
            "/scenario template\n"
            "台本登録用CSVテンプレートを取得します。"
        )
        return

    await message.channel.send(
        "台本登録用CSVテンプレートです。",
        file=discord.File(
            create_scenario_template(),
            filename="scenario_template.csv",
        ),
    )
