import discord
import function.send_message as send_message

#----------リアクション追加時の処理はここ----------
async def on_reaction_main(
    client: discord.Client,
    reaction: discord.Reaction,
    user: discord.User,
) -> None:
    print(f'{user}がリアクションを追加しました：{reaction.emoji}')
    # リアクションを付けたユーザーがBotだった場合は無視する
    if user.bot:
        return
    # リアクションが「👍」だった場合に「Good!」と返す処理
    if str(reaction.emoji) == '👍':
        await send_message.send_message_to_channel(
            client,
            reaction.message.channel.id,
            'Good!',
        )