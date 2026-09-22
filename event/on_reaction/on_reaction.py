import discord
import function.discord.message.send_message as send_message

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
    # リアクションが「👍」の場合に「Good!」と返す。
    if str(reaction.emoji) == '👍':
        await send_message.send_message_to_channel(
            client,
            reaction.message.channel.id,
            'Good!',
        )