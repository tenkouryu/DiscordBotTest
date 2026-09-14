import discord
import message_command_list
import function.send_message as send_message

async def parse_message_command(client, message):
    # メッセージコマンドの振り分け
    match message.content:
        case '/list':
            await message_command_list.main(client, message)
        case _:
            await send_message.send_message_to_channel(client, message.channel.id, '未定義のコメントが指定されました。')
