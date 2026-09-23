# DiscordBot_Servercontroller

## 概要

Discord.py で作成した Discord Bot です。メンバー・ロール・チャンネルの管理、CSV によるロール設定の一括更新などを行えます。

## セットアップ

1. Python 3.14 以降を用意します。
2. discord.py をインストールします。

```powershell
pip install discord.py
```

3. `config/config.json` に Bot トークンと通知先チャンネル ID を設定します。

```json
{
	"BOT_TOKEN": "Botのトークン",
	"REDIRECT_CHANNEL_ID": "通知先チャンネルのID"
}
```

4. Discord Developer Portal で、Bot の以下の Intent を有効にします。
   - Message Content Intent
   - Server Members Intent
   - Reactions と Voice States はコードで使用しています。

5. 起動します。

```powershell
python bot_main.py
```

Bot トークンは公開せず、`config/config.json` を Git にコミットしないでください。

## コマンド

すべてのコマンドは `-h` を付けると個別の使い方を表示できます。

### 共通機能

```text
/help
```

### メンバーロール機能

```text
/member role add @メンバー ロール名
/member role get メンバー名
/member role set + CSVファイル
/member role template
/member role remove @メンバー ロール名
```

CSV形式は [テンプレートファイル](#テンプレートファイル) の `member_role_template.csv` を参照してください。

`get` はメンバー名または表示名に一致するメンバーのロール一覧を返信します。メンションで指定することもできます。

`add`、`set`、`remove` には「ロールの管理」権限が必要です。

### サーバーロール機能

```text
/server role add ロール名
/server role edit ロール名 権限名 on|off
/server role edit ロール名 color #RRGGBB
/server role get
/server role set + CSVファイル
/server role template
/server role remove ロール名
```

CSV形式は [テンプレートファイル](#テンプレートファイル) の `server_role_template.csv` を参照してください。

`add`、`edit`、`set`、`remove` には「ロールの管理」権限が必要です。

### メンバー一覧機能

```text
/server member list
```

サーバーのメンバー一覧を CSV ファイルで取得します。

### チャンネル機能

```text
/channel create text チャンネル名 [カテゴリー名]
/channel create voice チャンネル名 [カテゴリー名]
/channel move #チャンネル カテゴリー名
/channel get
/channel set + CSVファイル
/channel template
```

チャンネルの作成・移動には「チャンネルの管理」権限が必要です。指定したカテゴリーが存在しない場合は自動作成します。

`/channel get` でサーバーのチャンネル一覧を `name,type,category` 形式の CSV ファイルとして取得できます。

CSV形式は [テンプレートファイル](#テンプレートファイル) の `channel_template.csv` を参照してください。

`type` には `text` または `voice` を指定します。既存チャンネルは名前で検索してカテゴリーを変更し、存在しない場合は新規作成します。カテゴリーが存在しない場合は自動作成します。

### チャット添付ファイル機能

```text
/chat get #テキストチャンネル [開始日 YYYY-MM-DD] [拡張子]
/chat get + CSVファイル
/chat template
```

チャンネルをメンションすると、単一チャンネルの添付ファイルを取得できます。開始日は省略可能で、指定する場合は `YYYY-MM-DD` 形式です。指定日の00:00（UTC）以降が対象になります。拡張子は `png` または `.png` の形式で指定でき、`png|jpg|gif` のように複数指定できます。

CSVに `category_name,channel_name,start_date,extension` を指定すると、各行のチャンネルから開始日以降の添付ファイルを取得し、`カテゴリー名/チャンネル名/ファイル名` の構成で1つの ZIP ファイルにまとめて返信します。`start_date` または `extension` を空欄にすると、その条件では絞り込みません。実行には「メッセージの管理」権限が必要です。

CSV形式は [テンプレートファイル](#テンプレートファイル) の `chat_template.csv` を参照してください。

### イベント通知機能

以下はサンプル機能です。運用環境の要件に合わせて、処理内容や通知先を変更・無効化してください。

- ボイスチャンネルへ参加・退出すると、対象ボイスチャンネルのテキストチャットへ通知します。
- 新規メンバー参加時は、`REDIRECT_CHANNEL_ID` で指定したチャンネルへ通知します。

### シナリオ進行機能

```text
/scenario template
/scenario set + CSVファイル
/scenario list
/scenario start シナリオID [開始step]
/scenario delete シナリオID
```

シナリオは `config/scenario_definitions.json` に保存され、サーバーごとの進行状態は `config/scenario_states.json` に保存されます。`/scenario set` は既存のシナリオを保持したままCSVの内容を追記します。同じシナリオIDとステップ番号がある場合は更新されます。

CSV形式と `welcome` シナリオの例は [テンプレートファイル](#テンプレートファイル) の `scenario_template.csv` を参照してください。

`completion_type` が `reaction` の場合、現在の指示メッセージにリアクションが付くと次へ進みます。`completion_value` が `*` または空欄なら任意のリアクション、絵文字を指定した場合はその絵文字だけが有効です。リアクション条件の指示メッセージには、見本となるリアクションが自動で追加されます。

複数の分岐は、1行に `branch_reaction_N` と `branch_step_N` の列を追加して指定できます。分岐先は現在のシナリオ内のstepに限定されます。

## テンプレートファイル

各種CSVテンプレートはルート直下の `templates` フォルダに保存しています。リンク先のCSVを編集して各コマンドに添付してください。

- [channel_template.csv](templates/channel_template.csv): チャンネル設定
- [chat_template.csv](templates/chat_template.csv): 添付ファイル取得
- [member_role_template.csv](templates/member_role_template.csv): メンバーロール設定
- [server_role_template.csv](templates/server_role_template.csv): サーバーロール設定
- [scenario_template.csv](templates/scenario_template.csv): シナリオ登録