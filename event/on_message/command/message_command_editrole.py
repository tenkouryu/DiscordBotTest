import discord
import function.edit_roll as edit_roll


async def main(message):
    if not message.author.guild_permissions.manage_roles:
        await message.channel.send('ロールを変更する権限がありません。')
        return

    argument = message.content.partition(' ')[2]
    try:
        role_name, setting_name, setting_value = argument.rsplit(' ', 2)
    except ValueError:
        await message.channel.send(
            '使い方: /editrole ロール名 権限名 on|off\n'
            'または /editrole ロール名 color #RRGGBB'
        )
        return

    try:
        if setting_name.lower() == 'color':
            role = await edit_roll.edit_role_color(
                message.guild, role_name, setting_value
            )
            await message.channel.send(
                f'ロール「{role.name}」の色を{setting_value}に変更しました。'
            )
            return

        enabled_text = setting_value.lower()
        if enabled_text not in ('on', 'off'):
            await message.channel.send(
                '権限の設定値は on または off を指定してください。'
            )
            return

        role = await edit_roll.edit_role_permissions(
            message.guild, role_name, setting_name, enabled_text == 'on'
        )
    except ValueError as error:
        await message.channel.send(str(error))
        return
    except discord.Forbidden:
        await message.channel.send('Botにロールを変更する権限がありません。')
        return

    status = '有効' if enabled_text == 'on' else '無効'
    await message.channel.send(
        f'ロール「{role.name}」の権限「{setting_name}」を{status}にしました。'
    )
