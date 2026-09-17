import discord
from . import message_command_addmemberrole
from . import message_command_addrole
from . import message_command_editrole
from . import message_command_memberlist
from . import message_command_removememberrole
from . import message_command_removerole
from . import message_comand_getrole2csv
import function.send_message as send_message


async def _send_command_help(message):
    """利用可能なコマンドの一覧を送信する。"""
    await message.channel.send(
        '利用可能なコマンド一覧:\n'
        '/help - このコマンド一覧を表示\n'
        '/list - メンバー一覧を CSV で取得\n'
        '/addrole ロール名 - ロールを追加\n'
        '/addmemberrole @メンバー ロール名 - メンバーにロールを追加\n'
        '/removerole ロール名 - ロールを削除\n'
        '/removememberrole @メンバー ロール名 - メンバーからロールを削除\n'
        '/editrole ロール名 権限名 on|off - ロール権限を変更\n'
        '/editrole ロール名 color #RRGGBB - ロール色を変更\n'
        '/getrole - ロール一覧を CSV で取得\n'
        '各コマンドに -h を付けると詳細を表示します。'
    )


async def parse_message_command(client, message):
    # メッセージコマンドの振り分け
    command = message.content.partition(' ')[0]

    match command:
        case '/help':
            await _send_command_help(message)
        case '/list':
            await message_command_memberlist.main(client, message)
        case '/addrole':
            await message_command_addrole.main(message)
        case '/addmemberrole':
            await message_command_addmemberrole.main(message)
        case '/removerole':
            await message_command_removerole.main(message)
        case '/removememberrole':
            await message_command_removememberrole.main(message)
        case '/editrole':
            await message_command_editrole.main(message)
        case '/getrole':
            await message_comand_getrole2csv.main(client, message)
        case _:
            await send_message.send_message_to_channel(
                client,
                message.channel.id,
                '未定義のコメントが指定されました。',
            )

