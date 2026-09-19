import csv
import io
import os
import tempfile

import discord
import function.edit_roll as edit_roll


def _find_member_by_display_name(guild, display_name):
    """表示名から対象メンバーを特定する。"""
    matches = [
        member
        for member in guild.members
        if member.display_name == display_name
    ]
    return matches[0] if len(matches) == 1 else None


def _find_role(guild, role_name):
    """変更可能なロールを名前から取得する。"""
    return next(
        (
            role
            for role in guild.roles
            if role.name == role_name
            and not role.is_default()
            and not role.managed
        ),
        None,
    )


async def _execute_row(guild, action, display_name, role_name):
    """CSV 1 行分のロール操作を実行する。"""
    if action not in ("追加", "削除"):
        return "失敗: 1列目は「追加」または「削除」を指定してください。"
    if not display_name:
        return "失敗: 表示名が空です。"
    if not role_name:
        return "失敗: ロール名が空です。"

    member = _find_member_by_display_name(guild, display_name)
    if member is None:
        return f"失敗: 表示名「{display_name}」のメンバーが見つかりません。"

    role = _find_role(guild, role_name)
    try:
        if action == "追加":
            if role is None:
                role = await edit_roll.add_role_to_server(guild, role_name)
            await member.add_roles(role)
            return "成功: ロールを追加しました。"

        if role is None:
            return f"失敗: ロール「{role_name}」が見つかりません。"
        await member.remove_roles(role)
        return "成功: ロールを削除しました。"
    except (discord.Forbidden, discord.HTTPException):
        return "失敗: Discordの権限または通信エラーで操作できませんでした。"
    except ValueError as error:
        return f"失敗: {error}"


async def update_member_roles_from_csv(guild, csv_text: str) -> tuple[str, int]:
    """CSVを処理し、実行結果列を追加したCSVを返す。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    reader = csv.DictReader(io.StringIO(csv_text))
    required_columns = {"追加/削除", "表示名", "ロール"}
    if not required_columns.issubset(reader.fieldnames or set()):
        raise ValueError("CSVには「追加/削除」「表示名」「ロール」列が必要です。")

    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["追加/削除", "表示名", "ロール", "実行結果"])
    success_count = 0

    for row in reader:
        action = row.get("追加/削除", "").strip()
        display_name = row.get("表示名", "").strip()
        role_name = row.get("ロール", "").strip()
        result = await _execute_row(guild, action, display_name, role_name)
        if result.startswith("成功"):
            success_count += 1
        writer.writerow([action, display_name, role_name, result])

    return output.getvalue(), success_count


async def main(message):
    """添付されたCSVからメンバーのロールを操作し、結果CSVを送信する。"""
    if message.content.partition(" ")[2].strip() == "-h":
        await message.channel.send(
            "/member role edit + CSVファイル\n"
            "CSV形式: 追加/削除,表示名,ロール\n"
            "処理結果を「実行結果」列に追加したCSVを返信します。"
        )
        return

    if not message.author.guild_permissions.manage_roles:
        await message.channel.send("メンバーのロールを変更する権限がありません。")
        return

    csv_attachment = next(
        (
            attachment
            for attachment in message.attachments
            if attachment.filename.lower().endswith(".csv")
        ),
        None,
    )
    if csv_attachment is None:
        await message.channel.send(
            "CSVファイルを添付してください。使い方: /member role edit + CSVファイル"
        )
        return

    try:
        csv_text = (await csv_attachment.read()).decode("utf-8-sig")
        result_csv, success_count = await update_member_roles_from_csv(
            message.guild,
            csv_text,
        )
    except (UnicodeDecodeError, ValueError) as error:
        await message.channel.send(f"CSVを読み込めませんでした: {error}")
        return

    file_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8-sig",
            newline="",
            suffix="_result.csv",
            delete=False,
        ) as result_file:
            result_file.write(result_csv)
            file_path = result_file.name

        await message.channel.send(
            f"{success_count}件の処理が成功しました。実行結果CSVを添付します。",
            file=discord.File(file_path, filename="member_roles_result.csv"),
        )
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
