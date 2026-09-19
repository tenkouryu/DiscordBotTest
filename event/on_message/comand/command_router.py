from collections.abc import Awaitable, Callable

import discord
from .member import role_add as member_role_add
from .member import role_edit as member_role_edit
from .member import role_remove as member_role_remove
from .server import member_list as server_member_list
from .server import role_add as server_role_add
from .server import role_edit as server_role_edit
from .server import role_get as server_role_get
from .server import role_remove as server_role_remove
from .channel import create as channel_create
from .channel import move as channel_move
import function.send_message as send_message


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
        '/member role edit + CSVファイル - メンバーのロールを CSV から更新\n'
        '/member role remove @メンバー ロール名 - メンバーからロールを削除\n'
        '/server role add ロール名 - ロールを追加\n'
        '/server role edit ロール名 権限名 on|off - ロール権限を変更\n'
        '/server role edit ロール名 color #RRGGBB - ロール色を変更\n'
        '/server role get - ロール一覧を CSV で取得\n'
        '/server role remove ロール名 - ロールを削除\n'
        '/server member list - メンバー一覧を CSV で取得\n'
        '/channel create text|voice チャンネル名 [カテゴリー名] - チャンネルを作成\n'
        '/channel move #チャンネル カテゴリー名 - チャンネルを移動\n'
        '各コマンドに -h を付けると詳細を表示します。'
    )


async def parse_message_command(
    client: discord.Client,
    message: discord.Message,
) -> None:
    # メッセージコマンドの振り分け
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
                        'edit': member_role_edit.main,
                        'remove': member_role_remove.main,
                    },
                },
            )
            if handler is None:
                await message.channel.send(
                    '使い方: /member role add|edit|remove'
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
                    '使い方: /server role add|edit|get|remove または /server member list'
                )
            else:
                await handler(command_message)
        case '/channel':
            handler, command_message = _operation_message(
                message,
                'channel',
                {
                    'create': channel_create.main,
                    'move': channel_move.main,
                },
            )
            if handler is None:
                await message.channel.send('使い方: /channel create|move')
            else:
                await handler(command_message)
        case _:
            await send_message.send_message_to_channel(
                client,
                message.channel.id,
                '未定義のコメントが指定されました。',
            )

