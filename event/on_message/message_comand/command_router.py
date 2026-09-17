import discord
from . import member_add_role
from . import server_add_role
from . import server_edit_role
from . import member_edit_role
from . import member_list
from . import member_remove_role
from . import server_remove_role
from . import server_get_role_csv
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
        '/editmemberrole + CSVファイル - メンバーのロールを CSV から更新\n'
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
            await member_list.main(client, message)
        case '/addrole':
            await server_add_role.main(message)
        case '/addmemberrole':
            await member_add_role.main(message)
        case '/removerole':
            await server_remove_role.main(message)
        case '/removememberrole':
            await member_remove_role.main(message)
        case '/editrole':
            await server_edit_role.main(message)
        case '/editmemberrole':
            await member_edit_role.main(message)
        case '/getrole':
            await server_get_role_csv.main(client, message)
        case _:
            await send_message.send_message_to_channel(
                client,
                message.channel.id,
                '未定義のコメントが指定されました。',
            )

