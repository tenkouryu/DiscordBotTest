import discord

"""
    Bot起動時のイベントを処理する。

    on_ready_main:
        Botのログイン完了をコンソールへ表示する。
"""

async def on_ready_main(client: discord.Client) -> None:
    # 起動時にターミナルへログイン通知を表示する。
    print(f'{client.user}としてログインしました')
    