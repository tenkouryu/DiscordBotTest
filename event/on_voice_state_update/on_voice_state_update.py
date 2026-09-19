import discord
import function.send_message as send_message

async def on_voice_state_update_main(
    client: discord.Client,
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState,
) -> None:
    print(f'{member}のボイス状態が変更されました')
    # メンバーがボイスチャンネルに参加した場合
    if before.channel is None and after.channel is not None:
        await send_message.send_message_to_channel(
            client,
            after.channel.id,
            f'{member.display_name}さんがボイスチャンネルに参加しました！',
        )
    # メンバーがボイスチャンネルから退出した場合
    elif before.channel is not None and after.channel is None:
        await send_message.send_message_to_channel(
            client,
            before.channel.id,
            f'{member.display_name}さんがボイスチャンネルから退出しました！',
        )