import discord

from function.scenario.scenario_service import list_scenarios

"""
    台本一覧コマンドを処理する。

    main:
        登録済み台本の一覧を送信する。
"""


async def main(message: discord.Message) -> None:
    """登録済み台本の一覧を送信する。"""
    if message.content.partition(" ")[2].strip() == "-h":
        await message.channel.send(
            "/scenario list\n"
            "登録済み台本の一覧を表示します。"
        )
        return

    try:
        scenarios = list_scenarios()
    except (OSError, ValueError) as error:
        await message.channel.send(f"台本一覧を取得できませんでした: {error}")
        return

    if not scenarios:
        await message.channel.send("登録されている台本はありません。")
        return

    lines = [
        f"- {scenario['scenario_id']} ({scenario['step_count']}ステップ)"
        for scenario in scenarios
    ]
    await message.channel.send("登録済み台本一覧:\n" + "\n".join(lines))