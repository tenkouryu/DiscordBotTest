import discord
from .command import router
import function.discord.message.send_message as send_message
from function.scenario.scenario_service import (
    advance_scenario,
    has_active_scenario,
    get_scenario_wait_type,
    resolve_scenario_mentions,
)

"""
    Discordメッセージ受信イベントを処理する。

    on_message_main:
        Bot自身のメッセージを除外し、コマンドルーターへ処理を渡す。
"""

async def on_message_main(
    client: discord.Client,
    message: discord.Message,
) -> None:
    # デバッグログを出力する。
        print(f'{message.author}からのメッセージ：{message.content}')
    
        # メッセージ送信者がBotの場合は無視する。
        if message.author.bot:
            return
        # 特定ロールからの送信の場合は管理者用処理を行う。
        if '管理人' in [role.name for role in message.author.roles]:
            # 管理者専用の処理。
             print(f'管理者：{message.author}からのメッセージ：{message.content}')
        if 0:
            # 「Hi」と発言したら「Hi」を返す。
            if message.content == 'Hi':
                # メッセージ自身のチャンネルへ送信する場合はmessage.channel.sendを使う。
                await message.channel.send('Hi')
                # 特定のチャンネルへ送信する場合はsend_message_to_channelを使う。
                await send_message.send_message_to_channel(client, message.channel, 'Hi')

        if message.guild is not None:
            try:
                active_scenario = has_active_scenario(message.guild.id)
                wait_type = get_scenario_wait_type(
                    message.guild.id,
                    message.channel.id,
                )
            except (OSError, ValueError) as error:
                await message.channel.send(f"台本を進行できませんでした: {error}")
                return

            if active_scenario:
                if wait_type is None:
                    return
                if wait_type != "reaction" and not message.content.startswith('/'):
                    try:
                        scenario_result = advance_scenario(
                            message.guild.id,
                            message.content,
                        )
                    except (OSError, ValueError) as error:
                        await message.channel.send(
                            f"台本を進行できませんでした: {error}"
                        )
                        return
                    if scenario_result is not None:
                        if scenario_result["response"]:
                            await message.channel.send(
                                resolve_scenario_mentions(
                                    scenario_result["response"],
                                    message.guild,
                                )
                            )
                        if scenario_result["instruction"]:
                            await message.channel.send(
                                resolve_scenario_mentions(
                                    scenario_result["instruction"],
                                    message.guild,
                                )
                            )
                    return

                # reaction待ち、または台本以外のメッセージは無視する。
                return

        # /から始まるコマンドを処理する。
        # メッセージコマンドの処理を呼び出す。
        await router.parse_message_command(client, message)
        