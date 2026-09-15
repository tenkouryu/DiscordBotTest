import discord
from . import message_command_addrole
from . import message_command_editrole
from . import message_command_list
from . import message_command_removerole
import function.send_message as send_message

async def parse_message_command(client, message):
    # メッセージコマンドの振り分け
    command = message.content.partition(' ')[0]

    match command:
        case '/list':
            await message_command_list.main(client, message)
        case '/addrole':
            await message_command_addrole.main(message)
        case '/removerole':
            await message_command_removerole.main(message)
        case '/editrole':
            await message_command_editrole.main(message)
        case _:
            await send_message.send_message_to_channel(
                client,
                message.channel.id,
                '未定義のコメントが指定されました。',
            )

