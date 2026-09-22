import discord

from function.scenario.scenario_service import (
    get_scenario_reaction_examples,
    set_scenario_message_id,
    start_scenario,
)

"""
    台本開始コマンドを処理する。

    main:
        指定した台本をサーバー単位で開始する。
"""


async def main(message: discord.Message) -> None:
    """指定した台本を開始し、最初の指示を送信する。"""
    arguments = message.content.partition(" ")[2].strip()
    if arguments in {"", "-h"}:
        await message.channel.send(
            "/scenario start 台本ID [開始step]\n"
            "サーバー単位で台本を指定stepから開始します。"
        )
        return
    if message.guild is None:
        await message.channel.send("サーバー内で実行してください。")
        return

    scenario_id, _, start_step_text = arguments.partition(" ")
    start_step = None
    if start_step_text:
        try:
            start_step = int(start_step_text.strip())
        except ValueError:
            await message.channel.send("開始stepは整数で指定してください。")
            return

    try:
        step = start_scenario(message.guild.id, scenario_id, start_step)
    except (OSError, ValueError) as error:
        await message.channel.send(f"台本を開始できませんでした: {error}")
        return

    sent_message = await message.channel.send(
        step["instruction"] or "台本を開始しました。"
    )
    for reaction in get_scenario_reaction_examples(step):
        await sent_message.add_reaction(reaction)
    try:
        set_scenario_message_id(
            message.guild.id,
            sent_message.id,
            message.channel.id,
        )
    except (OSError, ValueError) as error:
        await message.channel.send(f"台本の状態を保存できませんでした: {error}")
