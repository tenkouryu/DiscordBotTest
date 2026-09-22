import discord

from function.scenario.scenario_service import delete_scenario

"""
    台本削除コマンドを処理する。

    main:
        指定した台本を定義と進行状態から削除する。
"""


async def main(message: discord.Message) -> None:
    """指定した台本を削除する。"""
    scenario_id = message.content.partition(" ")[2].strip()
    if scenario_id in {"", "-h"}:
        await message.channel.send(
            "/scenario delete 台本ID\n"
            "指定した台本を削除します。"
        )
        return

    try:
        cleared_guilds = delete_scenario(scenario_id)
    except (OSError, ValueError) as error:
        await message.channel.send(f"台本を削除できませんでした: {error}")
        return

    await message.channel.send(
        f"台本「{scenario_id}」を削除しました。"
        f"進行状態も{cleared_guilds}サーバー分解除しました。"
    )