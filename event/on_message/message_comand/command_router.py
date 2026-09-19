import discord
from . import member_add_role
from . import server_add_role
from . import server_edit_role
from . import member_edit_role
from . import member_get_list
from . import member_remove_role
from . import server_remove_role
from . import server_get_role_csv
from . import channel_edit
import function.send_message as send_message


async def _send_command_help(message):
    """利用可能なコマンドの一覧を送信する。"""
    await message.channel.send(
        '利用可能なコマンド一覧:\n'
        '/help - このコマンド一覧を表示\n'
        '/member_add_role @メンバー ロール名 - メンバーにロールを追加\n'
        '/member_edit_role + CSVファイル - メンバーのロールを CSV から更新\n'
        '/member_get_list - メンバー一覧を CSV で取得\n'
        '/member_remove_role @メンバー ロール名 - メンバーからロールを削除\n'
        '/server_add_role ロール名 - ロールを追加\n'
        '/server_edit_role ロール名 権限名 on|off - ロール権限を変更\n'
        '/server_edit_role ロール名 color #RRGGBB - ロール色を変更\n'
        '/server_get_role_csv - ロール一覧を CSV で取得\n'
        '/server_remove_role ロール名 - ロールを削除\n'
        '/channel create text|voice チャンネル名 [カテゴリー名] - チャンネルを作成\n'
        '/channel move #チャンネル カテゴリー名 - チャンネルを移動\n'
        '各コマンドに -h を付けると詳細を表示します。'
    )


async def parse_message_command(client, message):
    # メッセージコマンドの振り分け
    command = message.content.partition(' ')[0]

    match command:
        case '/help':
            await _send_command_help(message)
        case '/member_add_role':
            await member_add_role.main(message)
        case '/member_edit_role':
            await member_edit_role.main(message)
        case '/member_get_list':
            await member_get_list.main(client, message)
        case '/member_remove_role':
            await member_remove_role.main(message)
        case '/server_add_role':
            await server_add_role.main(message)
        case '/server_edit_role':
            await server_edit_role.main(message)
        case '/server_get_role_csv':
            await server_get_role_csv.main(client, message)
        case '/server_remove_role':
            await server_remove_role.main(message)
        case '/channel':
            await channel_edit.main(message)
        case _:
            await send_message.send_message_to_channel(
                client,
                message.channel.id,
                '未定義のコメントが指定されました。',
            )

