import csv
import io

import discord
import function.discord.channel.edit_channel as edit_channel

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
) -> tuple[int, list[str]]:
    """CSVからチャンネルを作成またはカテゴリー設定する。"""
    if guild is None:
        raise ValueError("サーバーが指定されていません。")

    reader = csv.DictReader(io.StringIO(csv_text))
    required_columns = {"name", "type", "category"}
    if not required_columns.issubset(reader.fieldnames or set()):
        raise ValueError("CSVには name、type、category 列が必要です。")

    success_count = 0
    errors: list[str] = []
    for row_number, row in enumerate(reader, start=2):
        channel_name = (row.get("name") or "").strip()
        channel_type = (row.get("type") or "").strip().lower()
        category_name = (row.get("category") or "").strip()

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
                    await edit_channel.create_text_channel(
                        guild,
                        channel_name,
                        category_name or None,
                    )
                else:
                    await edit_channel.create_voice_channel(
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

            success_count += 1
        except (ValueError, discord.Forbidden, discord.HTTPException) as error:
            errors.append(f"{row_number}行目（{channel_name or '名前なし'}）: {error}")

    return success_count, errors


async def main(message: discord.Message) -> None:
    """添付されたCSVからチャンネルを作成または設定する。"""
    if message.content.partition(" ")[2].strip() == "-h":
        await message.channel.send(
            "/channel set + CSVファイル\n"
            "CSV形式: name,type,category\n"
            "type は text または voice を指定します。"
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
        success_count, errors = await set_channels_from_csv(
            message.guild,
            csv_text,
        )
    except (UnicodeDecodeError, ValueError) as error:
        await message.channel.send(f"CSVを読み込めませんでした: {error}")
        return

    result = f"{success_count}件のチャンネルを設定しました。"
    if errors:
        result += "\n" + "\n".join(errors)
    await message.channel.send(result)
