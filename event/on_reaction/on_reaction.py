import discord
import function.discord.message.send_message as send_message
from function.scenario.scenario_service import (
    advance_scenario,
    set_scenario_message_id,
)

"""
    Discordメッセージへのリアクション追加イベントを処理する。

    on_reaction_main:
        ユーザーのリアクションを確認し、条件に応じて返信する。
"""

async def on_reaction_main(
    client: discord.Client,
    reaction: discord.Reaction,
    user: discord.User,
) -> None:
    print(f'{user}がリアクションを追加しました：{reaction.emoji}')
    # リアクションを付けたユーザーがBotの場合は無視する。
    if user.bot:
        return

    if reaction.message.guild is not None:
        try:
            scenario_result = advance_scenario(
                reaction.message.guild.id,
                str(reaction.emoji),
                reaction.message.id,
            )
        except (OSError, ValueError) as error:
            await reaction.message.channel.send(
                f"台本を進行できませんでした: {error}"
            )
            return
        if scenario_result is not None:
            if scenario_result["response"]:
                await reaction.message.channel.send(scenario_result["response"])
            if scenario_result["instruction"]:
                next_message = await reaction.message.channel.send(
                    scenario_result["instruction"]
                )
                try:
                    set_scenario_message_id(
                        reaction.message.guild.id,
                        next_message.id,
                    )
                except (OSError, ValueError) as error:
                    await reaction.message.channel.send(
                        f"台本の状態を保存できませんでした: {error}"
                    )
            return

    # リアクションが「👍」の場合に「Good!」と返す。
    if str(reaction.emoji) == '👍':
        await send_message.send_message_to_channel(
            client,
            reaction.message.channel.id,
            'Good!',
        )