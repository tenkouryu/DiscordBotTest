# アプリ構造ドキュメント

## 1. 概要

このアプリは、Discord サーバー運用を支援する Bot です。Discord のイベントを受け取り、メンバー管理、ロール管理、チャンネル管理、添付ファイル取得、シナリオ進行、通知処理をまとめて提供します。

実行の中心は `bot_main.py` で、Discord クライアントを作成し、各イベントハンドラとスラッシュコマンドを登録します。

## 2. 役割分担の全体像

```text
bot_main.py
  └─ Discord クライアントとイベント登録
        ├─ event/on_ready/        : 起動時処理
        ├─ event/on_message/      : メッセージ処理
        ├─ event/on_reaction/     : リアクション処理
        ├─ event/on_member_join/  : 新規参加処理
        ├─ event/on_voice_state_update/ : 入退室監視
        └─ function/              : 実務ロジックと共通処理

Src/config/
   ├─ config.json              : Bot トークンと通知先チャンネル
   ├─ scenario_definitions.json: シナリオ定義
   └─ scenario_states.json     : サーバーごとの進行状態

Src/templates/
   ├─ channel_template.csv
   ├─ chat_template.csv
   ├─ member_role_template.csv
   ├─ server_role_template.csv
   └─ scenario_template.csv

tools/
  └─ scenario_viewer/         : シナリオ確認用 GUI
```

## 3. 主要ディレクトリの責務

### 3.1 `bot_main.py`

アプリケーションのエントリーポイントです。

- Discord クライアントを生成
- Intents を有効化
- スラッシュコマンドの登録
- 各イベントハンドラを紐付け
- `client.run(TOKEN)` で Bot を起動

主な役割は「イベントとコマンドの接続点」です。

### 3.2 `event/`

Discord から発火するイベントを処理する層です。役割ごとにディレクトリが分かれています。

- `on_ready/`: 起動完了時の初期化とログ出力
- `on_message/`: メッセージ受信時の処理
- `on_reaction/`: リアクション時のシナリオ進行判定
- `on_member_join/`: 新規メンバー参加時の通知
- `on_voice_state_update/`: VC の入退室通知

`event/on_message/command/` 配下には、各コマンドの実体があり、`slash_commands.py` でスラッシュコマンドに接続されています。

### 3.3 `function/`

業務ロジックの実体が置かれる層です。

- `function/scenario/`: シナリオ定義の登録、進行、削除、CSV 変換
- `function/file/`: ZIP 圧縮や安全な解凍処理
- `function/discord/`: Discord 向けの通知やメッセージ送信処理
- `function/security/`: 暗号化やセキュリティ関連の処理

ここでは実際の処理が行われ、イベントハンドラは「入口」に近い役割を担います。

#### `function/` のモジュール単位の意図

- `function/scenario/`: シナリオ定義・進行・CSV 変換など、シナリオ運用のコア処理を担う
- `function/file/`: ZIP 圧縮や安全な解凍など、ファイル処理の共通部品を担う
- `function/discord/`: Discord 権限・チャンネル・メッセージ送信など、Discord API を抽象化した処理を担う
- `function/security/`: 暗号化や改ざん検知など、機密情報を扱う共通サービスを担う

この層は、イベントハンドラが直接 API や永続化処理を触らず、共有ロジックをまとめて扱うための層です。

### 3.4 `config/`

Bot 実行時に必要な設定や実行状態を保存します。

- `config.json`: Bot トークンと通知先チャンネルの設定
- `scenario_definitions.json`: すべてのシナリオ定義
- `scenario_states.json`: 各サーバーの進行状態

実際の保存先は `Src/config/` 配下です。

このディレクトリは、Bot の永続化と運用状態の中心です。

### 3.5 `templates/`

CSV 入出力のテンプレートです。

- `channel_template.csv`: チャンネル構成
- `chat_template.csv`: 添付ファイル取得
- `member_role_template.csv`: メンバーのロール設定
- `server_role_template.csv`: サーバーロール設定
- `scenario_template.csv`: シナリオ登録用テンプレート

実際の保存先は `Src/templates/` 配下です。

コマンド実行時に CSV を添付し、処理をまとめて行う構成になっています。

### 3.6 `tools/scenario_viewer/`

シナリオ定義 CSV を読み込んで、各ステップを人間向けに確認するためのビューアです。

- 画面表示用にシナリオを読み込み
- `step`, `instruction`, `response`, `branch` などを表示
- `Enter` で進む、`q` で終了

開発時やシナリオの確認時に利用します。

## 4. コマンドの呼び出しフロー

### スラッシュコマンド経路

```text
Discord interaction
   ↓
slash_commands.py
   ↓
_interactionMessage / _run
   ↓
既存コマンド処理（event/on_message/command/...）
   ↓
function/ 配下のサービスロジック
   ↓
Discord への応答
```

ポイント:

- 直接的な機能実装は `event/on_message/command/...` ではなく、機能ごとの service を経由している
- `slash_commands.py` は新しい UI 層と旧来のコマンド処理をつなぐアダプターの役割を持つ
- これにより、既存のコマンドをそのままスラッシュコマンドとして再利用しやすい

### シナリオ進行の流れ

```text
/scenario set
   ↓
CSV を読み込み
   ↓
scenario_service.register_scenario_csv()
   ↓
config/scenario_definitions.json に保存

/scenario start
   ↓
scenario_service.start_scenario()
   ↓
サーバーごとの状態を config/scenario_states.json に記録

メッセージ受信
   ↓
on_message_main()
   ↓
advance_scenario()
   ↓
次のステップ or 応答メッセージを送信
```

### ビジネスロジックの責務

- `event/`: Discord 層のイベント受付
- `function/`: 実処理と状態更新
- `config/`: 永続化
- `templates/`: CSV 入出力の定義

この分離で、Discord API と実務ロジックが淀みなく分かれているのが特徴です。

## 5. 実装上の設計思想

### 5.1 イベント駆動

Discord はイベント中心の仕組みであるため、各機能がイベントハンドラとして収まりやすい構造になっています。

### 5.2 CSV を通じた運用性

ロールやチャンネル、シナリオの大量設定を CSV で扱えるようにしており、運用者が手作業でコマンドを叩くよりも一括対応しやすくしています。

### 5.3 スラッシュコマンドへの移行対応

従来のメッセージコマンドに近い構造を残しながら、`slash_commands.py` でスラッシュコマンドへ橋渡ししています。これは現状のコードベースを壊しにくくする設計です。

### 5.4 状態管理の明確化

シナリオ進行は JSON に保存され、サーバー単位で状態を持つようになっています。これは Bot が長時間稼働しても進行状況を保持できるようにするためです。

## 6. 新機能追加の考え方

新しい機能を追加する際は、通常次の順序で実装します。

1. `event/` にイベントまたはコマンド入口を追加
2. `function/` に処理ロジックを実装
3. 必要なら `config/` やテンプレートの拡張
4. `slash_commands.py` にスラッシュコマンドを登録
5. `tools/scenario_viewer` の必要があれば対応

この順番にすると責務が分離され、保守しやすくなります。

## 7. 補足

- 実際の Bot の起動入口は `bot_main.py`
- 実際の機能の大半は `function/` と `event/` に分かれている
- 設定値や状態は JSON で保持する設計
- シナリオ記述の確認・視覚化の補助として `scenario_viewer` が存在する

これらを押さえておくと、このアプリのコードを理解しやすくなります。
