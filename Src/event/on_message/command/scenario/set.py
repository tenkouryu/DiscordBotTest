import discord

from function.scenario.scenario_service import register_scenario_csv

"""
    台本登録コマンドを処理する。

    main:
        添付されたCSVを読み込み、台本定義JSONへ登録する。
"""


async def main(message: discord.Message) -> None:
    """添付CSVを台本定義JSONへ登録する。"""
    if message.content.partition(" ")[2].strip() == "-h":
        await message.channel.send(
            "/scenario set + CSVファイル\n"
            "台本登録用CSVを読み込みます。"
        )
        return

    csv_attachment = next(
        (
            attachment
            for attachment in message.attachments
            if attachment.filename.lower().endswith(".csv")
        ),
        None,
    )
    if csv_attachment is None:
        await message.channel.send(
            "台本登録用のCSVファイルを添付してください。"
        )
        return

    try:
        csv_text = (await csv_attachment.read()).decode("utf-8-sig")
        registered_count = register_scenario_csv(csv_text)
    except (UnicodeDecodeError, OSError, ValueError) as error:
        await message.channel.send(f"台本を登録できませんでした: {error}")
        return

    await message.channel.send(
        f"台本を{registered_count}ステップ登録しました。"
    )
