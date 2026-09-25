import csv
import io
import re

import discord
import function.discord.channel.edit_channel as edit_channel
from function.file.template_output_service import save_template_output

"""
    CSVによるチャンネル設定コマンドを処理する。

    set_channels_from_csv:
        CSVの内容をもとにチャンネルを作成または設定する。

    main:
        添付CSVを読み込み、チャンネル設定を実行する。
"""

async def set_channels_from_csv(
    guild: discord.Guild,
    csv_text: str,
) -> tuple[int, bytes]:
    """CSVからチャンネルを設定し、各行の結果を含むCSVを返す。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    reader = csv.DictReader(io.StringIO(csv_text))
    required_columns = {"name", "type", "category"}
    if not required_columns.issubset(reader.fieldnames or set()):
        raise ValueError("CSVには name、type、category 列が必要です。")

    fieldnames = list(reader.fieldnames or [])
    result_field = "result"
    reason_field = "reason"
    if result_field not in fieldnames:
        fieldnames.append(result_field)
    if reason_field not in fieldnames:
        fieldnames.append(reason_field)

    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(fieldnames)
    success_count = 0
    for row in reader:
        channel_name = (row.get("name") or "").strip()
        channel_type = (row.get("type") or "").strip().lower()
        category_name = (row.get("category") or "").strip()
        role_columns = sorted(
            (
                key
                for key in row
                if re.fullmatch(r"role_\d+", key or "")
            ),
            key=lambda key: int(key.rsplit("_", 1)[1]),
        )
        role_names = [
            (row.get(column) or "").strip()
            for column in role_columns
            if (row.get(column) or "").strip()
        ]
        result = "成功"
        reason = ""
        try:
            if not channel_name:
                raise ValueError("チャンネル名が空です。")
            if channel_type not in {"text", "voice"}:
                raise ValueError("type は text または voice を指定してください。")

            existing_channel = discord.utils.get(
                guild.channels,
                name=channel_name,
            )
            if existing_channel is None:
                if channel_type == "text":
                    existing_channel = await edit_channel.create_text_channel(
                        guild,
                        channel_name,
                        category_name or None,
                    )
                else:
                    existing_channel = await edit_channel.create_voice_channel(
                        guild,
                        channel_name,
                        category_name or None,
                    )
            else:
                expected_type = (
                    "text"
                    if isinstance(existing_channel, discord.TextChannel)
                    else "voice"
                    if isinstance(existing_channel, discord.VoiceChannel)
                    else None
                )
                if expected_type != channel_type:
                    raise ValueError(
                        f'既存チャンネルの種類が一致しません（{expected_type or "その他"}）。'
                    )
                if category_name:
                    await edit_channel.move_channel_to_category(
                        existing_channel,
                        category_name,
                    )

            if role_names:
                await edit_channel.sync_channel_role_access(
                    existing_channel,
                    role_names,
                )

            success_count += 1
        except (ValueError, discord.Forbidden, discord.HTTPException) as error:
            result = "失敗"
            reason = str(error)

        output_row = [row.get(fieldname) or "" for fieldname in fieldnames]
        output_row[fieldnames.index(result_field)] = result
        output_row[fieldnames.index(reason_field)] = reason
        writer.writerow(output_row)

    return success_count, output.getvalue().encode("utf-8-sig")


async def main(message: discord.Message) -> None:
    """添付されたCSVからチャンネルを作成または設定する。"""
    if message.content.partition(" ")[2].strip() == "-h":
        await message.channel.send(
            "/channel set + CSVファイル\n"
            "CSV形式: name,type,category,role_1,role_2,...（role_列は追加可能）\n"
            "type は text または voice を指定します。処理結果を追記したCSVを返信します。"
        )
        return

    if not message.author.guild_permissions.manage_channels:
        await message.channel.send("チャンネルを管理する権限がありません。")
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
            "CSVファイルを添付してください。使い方: /channel set + CSVファイル"
        )
        return

    try:
        csv_text = (await csv_attachment.read()).decode("utf-8-sig")
        success_count, result_csv = await set_channels_from_csv(
            message.guild,
            csv_text,
        )
    except (UnicodeDecodeError, ValueError) as error:
        await message.channel.send(f"CSVを読み込めませんでした: {error}")
        return

    result_path = save_template_output(
        "set/response",
        f"channel_set_{message.guild.id}",
        result_csv,
    )
    await message.channel.send(
        f"{success_count}件のチャンネルを設定しました。結果CSVを添付します。",
        file=discord.File(result_path, filename=result_path.name),
    )
