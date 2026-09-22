from collections.abc import Awaitable, Callable

import discord
from .channel import (
    create as channel_create,
    get as channel_get,
    move as channel_move,
    set as channel_set,
    template as channel_template,
)
from .chat import get as chat_get, template as chat_template
from .scenario import set as scenario_set
from .scenario import start as scenario_start
from .scenario import template as scenario_template
from .scenario import list as scenario_list
from .scenario import delete as scenario_delete
from .member import (
    role_add as member_role_add,
    role_get as member_role_get,
    role_remove as member_role_remove,
    role_set as member_role_set,
    role_template as member_role_template,
)
from .server import (
    member_list as server_member_list,
    role_add as server_role_add,
    role_edit as server_role_edit,
    role_get as server_role_get,
    role_remove as server_role_remove,
    role_set as server_role_set,
    role_template as server_role_template,
)
from function.discord.message import send_message

"""
    Discordメッセージコマンドを解析し、対応する処理へ振り分ける。

    _CommandMessage.__init__ / __getattr__:
        親コマンドを除いたメッセージ内容を保持・転送する。

    _subcommand_message / _resource_subcommand_message / _operation_message:
        コマンド階層を解析して実行対象のハンドラーを取得する。

    _send_command_help:
        利用可能なコマンド一覧を送信する。

    parse_message_command:
        受信したメッセージを対応するコマンド処理へ振り分ける。
"""

class _CommandMessage:
    """既存コマンドへ親コマンドを除いた内容を渡すメッセージ。"""

    def __init__(self, message: discord.Message, content: str) -> None:
        self._message = message
        self.content = content

    def __getattr__(self, name):
        return getattr(self._message, name)


def _subcommand_message(
    message: discord.Message,
    command_prefix: str,
    command_handlers: dict[str, Callable[[discord.Message], Awaitable[None]]],
) -> tuple[Callable[[discord.Message], Awaitable[None]] | None, _CommandMessage | None]:
    _, _, arguments = message.content.partition(' ')
    operation, separator, operation_arguments = arguments.partition(' ')
    handler = command_handlers.get(operation.lower())
    if handler is None:
        return None, None

    content = f'/{command_prefix}_{operation}'
    if separator:
        content += f' {operation_arguments}'
    return handler, _CommandMessage(message, content)


def _resource_subcommand_message(
    message: discord.Message,
    command_prefix: str,
    resource_handlers: dict[
        str,
        dict[str, Callable[[discord.Message], Awaitable[None]]],
    ],
) -> tuple[Callable[[discord.Message], Awaitable[None]] | None, _CommandMessage | None]:
    _, _, arguments = message.content.partition(' ')
    resource, separator, resource_arguments = arguments.partition(' ')
    resource_name = resource.lower()
    command_handlers = resource_handlers.get(resource_name)
    if command_handlers is None:
        return None, None

    operation, operation_separator, operation_arguments = resource_arguments.partition(
        ' '
    )
    handler = command_handlers.get(operation.lower())
    if handler is None:
        return None, None

    content = f'/{command_prefix}_{operation}_{resource_name}'
    if operation_separator:
        content += f' {operation_arguments}'
    return handler, _CommandMessage(message, content)


def _operation_message(
    message: discord.Message,
    command_prefix: str,
    command_handlers: dict[str, Callable[[discord.Message], Awaitable[None]]],
) -> tuple[Callable[[discord.Message], Awaitable[None]] | None, _CommandMessage | None]:
    _, _, arguments = message.content.partition(' ')
    operation, separator, operation_arguments = arguments.partition(' ')
    handler = command_handlers.get(operation.lower())
    if handler is None:
        return None, None

    content = f'/{command_prefix}_{operation}'
    if separator:
        content += f' {operation_arguments}'
    return handler, _CommandMessage(message, content)


async def _send_command_help(message: discord.Message) -> None:
    """利用可能なコマンドの一覧を送信する。"""
    await message.channel.send(
        '利用可能なコマンド一覧:\n'
        '/help - このコマンド一覧を表示\n'
        '/member role add @メンバー ロール名 - メンバーにロールを追加\n'
        '/member role get メンバー名 - メンバーのロール一覧を表示\n'
        '/member role set + CSVファイル - メンバーのロールを CSV から更新\n'
        '/member role template - メンバーロール設定 CSV のテンプレートを取得\n'
        '/member role remove @メンバー ロール名 - メンバーからロールを削除\n'
        '/server role add ロール名 - ロールを追加\n'
        '/server role edit ロール名 権限名 on|off - ロール権限を変更\n'
        '/server role edit ロール名 color #RRGGBB - ロール色を変更\n'
        '/server role get - ロール一覧を CSV で取得\n'
        '/server role set + CSVファイル - CSVからロール設定を更新\n'
        '/server role template - サーバーロール設定 CSV のテンプレートを取得\n'
        '/server role remove ロール名 - ロールを削除\n'
        '/server member list - メンバー一覧を CSV で取得\n'
        '/channel create text|voice チャンネル名 [カテゴリー名] - チャンネルを作成\n'
        '/channel move #チャンネル カテゴリー名 - チャンネルを移動\n'
        '/channel get - チャンネル一覧を CSV で取得\n'
        '/channel set + CSVファイル - CSVからチャンネルを作成・設定\n'
        '/channel template - チャンネル設定 CSV のテンプレートを取得\n'
        '/chat get #チャンネル [開始日] [拡張子] または + CSVファイル - 添付ファイルを ZIP で取得\n'
        '/chat template - チャット添付ファイル取得CSVのテンプレートを取得\n'
        '/scenario template - 台本登録用CSVのテンプレートを取得\n'
        '/scenario set + CSVファイル - 台本を登録\n'
        '/scenario start 台本ID - 台本を開始\n'
        '/scenario list - 登録済み台本の一覧を表示\n'
        '/scenario delete 台本ID - 台本を削除\n'
        '各コマンドに -h を付けると詳細を表示します。'
    )


async def parse_message_command(
    client: discord.Client,
    message: discord.Message,
) -> None:
    # メッセージコマンドを振り分ける。
    command = message.content.partition(' ')[0]

    match command:
        case '/help':
            await _send_command_help(message)
        case '/member':
            handler, command_message = _resource_subcommand_message(
                message,
                'member',
                {
                    'role': {
                        'add': member_role_add.main,
                        'get': member_role_get.main,
                        'set': member_role_set.main,
                        'template': member_role_template.main,
                        'remove': member_role_remove.main,
                    },
                },
            )
            if handler is None:
                await message.channel.send(
                    '使い方: /member role add|get|set|template|remove'
                )
            else:
                await handler(command_message)
        case '/server':
            handler, command_message = _resource_subcommand_message(
                message,
                'server',
                {
                    'role': {
                        'add': server_role_add.main,
                        'edit': server_role_edit.main,
                        'get': lambda current_message: server_role_get.main(
                            client,
                            current_message,
                        ),
                        'set': server_role_set.main,
                        'template': server_role_template.main,
                        'remove': server_role_remove.main,
                    },
                    'member': {
                        'list': lambda current_message: server_member_list.main(
                            client,
                            current_message,
                        ),
                    },
                },
            )
            if handler is None:
                await message.channel.send(
                    '使い方: /server role add|edit|get|set|template|remove または /server member list'
                )
            else:
                await handler(command_message)
        case '/channel':
            handler, command_message = _operation_message(
                message,
                'channel',
                {
                    'create': channel_create.main,
                    'get': channel_get.main,
                    'move': channel_move.main,
                    'set': channel_set.main,
                    'template': channel_template.main,
                },
            )
            if handler is None:
                await message.channel.send('使い方: /channel create|get|move|set|template')
            else:
                await handler(command_message)
        case '/chat':
            handler, command_message = _operation_message(
                message,
                'chat',
                {'get': chat_get.main, 'template': chat_template.main},
            )
            if handler is None:
                await message.channel.send(
                    '使い方: /chat get #チャンネル [開始日] [拡張子] または + CSVファイル'
                    '、/chat template'
                )
            else:
                await handler(command_message)
        case '/scenario':
            handler, command_message = _operation_message(
                message,
                'scenario',
                {
                    'template': scenario_template.main,
                    'set': scenario_set.main,
                    'start': scenario_start.main,
                    'list': scenario_list.main,
                    'delete': scenario_delete.main,
                },
            )
            if handler is None:
                await message.channel.send(
                    '使い方: /scenario template|set|start'
                )
            else:
                await handler(command_message)
        case _:
            await send_message.send_message_to_channel(
                client,
                message.channel.id,
                '未定義のコメントが指定されました。',
            )

