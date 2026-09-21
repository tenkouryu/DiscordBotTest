# DiscordBotTest

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

### 共通

```text
/help
```

### メンバーのロール

```text
/member role add @メンバー ロール名
/member role get メンバー名
/member role set + CSVファイル
/member role template
/member role remove @メンバー ロール名
```

`get` はメンバー名または表示名に一致するメンバーのロール一覧を返信します。メンションで指定することもできます。

`add`、`set`、`remove` には「ロールの管理」権限が必要です。

### サーバーのロール

```text
/server role add ロール名
/server role edit ロール名 権限名 on|off
/server role edit ロール名 color #RRGGBB
/server role get
/server role set + CSVファイル
/server role template
/server role remove ロール名
```

`add`、`edit`、`set`、`remove` には「ロールの管理」権限が必要です。

### メンバー一覧

```text
/server member list
```

サーバーのメンバー一覧を CSV ファイルで取得します。

### チャンネル

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

`/channel set` の CSV は次の形式です。

```csv
name,type,category
チャンネル名,text,カテゴリー名
```

`type` には `text` または `voice` を指定します。既存チャンネルは名前で検索してカテゴリーを変更し、存在しない場合は新規作成します。カテゴリーが存在しない場合は自動作成します。

### チャット添付ファイル

```text
/chat get #テキストチャンネル [開始日 YYYY-MM-DD]
/chat get + CSVファイル
/chat template
```

チャンネルをメンションすると、単一チャンネルの添付ファイルを取得できます。開始日は省略可能で、指定する場合は `YYYY-MM-DD` 形式です。指定日の00:00（UTC）以降が対象になります。

CSVに `category_name,channel_name,start_date` を指定すると、各行のチャンネルから開始日以降の添付ファイルを取得し、`カテゴリー名/チャンネル名/ファイル名` の構成で1つの ZIP ファイルにまとめて返信します。実行には「メッセージの管理」権限が必要です。

```csv
category_name,channel_name,start_date
カテゴリー名,チャンネル名,2026-09-01
```

### イベント通知

以下はサンプル機能です。運用環境の要件に合わせて、処理内容や通知先を変更・無効化してください。

- リアクションに 👍 を付けると、リアクションされたメッセージのチャンネルへ返信します。
- ボイスチャンネルへ参加・退出すると、対象ボイスチャンネルのテキストチャットへ通知します。
- 新規メンバー参加時は、`REDIRECT_CHANNEL_ID` で指定したチャンネルへ通知します。

## CSV

### メンバーロール操作

テンプレートを取得します。

```text
/member role template
```

CSV の列は次の3つです。

```csv
追加/削除,表示名,ロール
```

2行目の説明を実際の値に置き換えてから、次のコマンドへ添付します。

```text
/member role set + CSVファイル
```

`追加/削除` には `追加` または `削除` を指定します。

### サーバーロール設定

テンプレートを取得します。

```text
/server role template
```

CSV の `name` 列は必須です。`color` 列と権限列は任意で、記載した列だけ設定されます。設定しない場合は、その列を CSV から削除してください。

```text
/server role set + CSVファイル
```

指定した名前のロールが存在しない場合は新規作成します。権限値には `true` または `false` を指定します。

ロール一覧を設定 CSV として取得するには、次のコマンドを使用します。

```text
/server role get
```

### チャンネル設定

テンプレートを取得します。

```text
/channel template
```

CSV の項目は次の3つです。

```csv
name,type,category
チャンネル名,text,カテゴリー名
```

- `name`: 作成または設定するチャンネル名
- `type`: `text` または `voice`
- `category`: 所属させるカテゴリー名。設定しない場合は列を削除します。

CSV を添付して実行します。

```text
/channel set + CSVファイル
```

既存チャンネルは名前で検索してカテゴリーを変更し、存在しないチャンネルは新規作成します。カテゴリーが存在しない場合は自動作成します。