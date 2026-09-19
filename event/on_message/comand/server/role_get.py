import csv
import os

import function.edit_roll as edit_roll
import function.send_message as send_message


def export_roles_to_csv(guild, file_path: str) -> str:
	"""サーバーのロール設定を CSV ファイルに出力する。"""
	if guild is None:
		raise ValueError("サーバーが指定されていません。")

	role_settings = [
		edit_roll.get_role_settings(guild, role.name)
		for role in guild.roles
		if not role.is_default()
	]
	permission_names = sorted(
		{
			permission_name
			for settings in role_settings
			for permission_name in settings["permissions"]
		}
	)
	field_names = ["id", "name", "color", *permission_names]

	with open(file_path, "w", newline="", encoding="utf-8-sig") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(field_names)
		for settings in role_settings:
			writer.writerow(
				[
					settings["id"],
					settings["name"],
					settings["color"],
					*[settings["permissions"].get(permission_name, False)
					  for permission_name in permission_names],
				]
			)

	return file_path


async def main(client, message):
	"""ロール設定を CSV に出力して、実行チャンネルへ送信する。"""
	if message.content.partition(" ")[2].strip() == "-h":
		await message.channel.send(
			"/server role get: サーバーのロール情報を CSV ファイルで取得します。"
		)
		return

	file_path = "roles_list.csv"
	try:
		export_roles_to_csv(message.guild, file_path)
		await send_message.send_message_to_channel_with_file(
			client,
			message.channel.id,
			"サーバーのロール一覧を送信します。",
			file_path,
		)
	finally:
		if os.path.exists(file_path):
			os.remove(file_path)