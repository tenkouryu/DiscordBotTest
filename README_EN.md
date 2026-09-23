# DiscordBot_Servercontroller

## Overview

This is a Discord bot built with discord.py. It manages members, roles, and channels, and supports bulk role configuration updates using CSV files.

## Setup

1. Prepare Python 3.14 or later.
2. Install discord.py.

```powershell
pip install discord.py
```

3. Set the bot token and notification channel ID in `config/config.json`.

```json
{
	"BOT_TOKEN": "your bot token",
	"REDIRECT_CHANNEL_ID": "notification channel ID"
}
```

4. Enable the following intents for the bot in the Discord Developer Portal.
   - Message Content Intent
   - Server Members Intent
   - Reactions and Voice States are used by the code.

5. Start the bot.

```powershell
python bot_main.py
```

Do not expose your bot token or commit `config/config.json` to Git.

## Commands

Add `-h` to any command to display its usage.

### General features

```text
/help
```

### Member role features

```text
/member role add @member role-name
/member role get member-name
/member role set + CSV-file
/member role template
/member role remove @member role-name
```

See `member_role_template.csv` in the [Template files](#template-files) section for the CSV format.

`get` replies with the roles of a member matching their username or display name. You can also specify a member by mention.

The `add`, `set`, and `remove` commands require the Manage Roles permission.

### Server role features

```text
/server role add role-name
/server role edit role-name permission-name on|off
/server role edit role-name color #RRGGBB
/server role get
/server role set + CSV-file
/server role template
/server role remove role-name
```

See `server_role_template.csv` in the [Template files](#template-files) section for the CSV format.

The `add`, `edit`, `set`, and `remove` commands require the Manage Roles permission.

### Member list features

```text
/server member list
```

Exports the server member list as a CSV file.

### Channel features

```text
/channel create text channel-name [category-name]
/channel create voice channel-name [category-name]
/channel move #channel category-name
/channel get
/channel set + CSV-file
/channel template
```

Creating and moving channels requires the Manage Channels permission. A specified category is created automatically if it does not exist.

Use `/channel get` to export the server's channels as a CSV file in `name,type,category` format.

See `channel_template.csv` in the [Template files](#template-files) section for the CSV format.

Set `type` to `text` or `voice`. Existing channels are found by name and moved to the specified category; missing channels are created. Missing categories are created automatically.

### Chat attachment features

```text
/chat get #text-channel [start-date YYYY-MM-DD] [extension]
/chat get + CSV-file
/chat template
```

Mention a channel to download attachments from a single channel. The start date is optional and must use `YYYY-MM-DD`; messages from 00:00 UTC on that date onward are included. Extensions can be specified as `png` or `.png`, and multiple extensions can be specified as `png|jpg|gif`.

For multiple channels, set `category_name,channel_name,start_date,extension` in the CSV. Attachments from each channel are collected into one ZIP file organized as `category-name/channel-name/file-name`. Leave `start_date` or `extension` blank to omit that filter. The Manage Messages permission is required.

See `chat_template.csv` in the [Template files](#template-files) section for the CSV format.

### Event notification features

These are sample features. Change or disable the behavior and notification destinations to suit your production requirements.

- Joining or leaving a voice channel sends a notification to that voice channel's text chat.
- When a new member joins, a notification is sent to the channel specified by `REDIRECT_CHANNEL_ID`.

### Scenario features

```text
/scenario template
/scenario set + CSV-file
/scenario list
/scenario start scenario-id [start-step]
/scenario delete scenario-id
```

Scenario definitions are stored in `config/scenario_definitions.json`, while per-server progress is stored in `config/scenario_states.json`. `/scenario set` appends CSV entries while preserving existing scenarios. The same scenario ID and step number are updated.

See `scenario_template.csv` in the [Template files](#template-files) section for the CSV format and the three-step `welcome` scenario example.

When `completion_type` is `reaction`, the scenario advances when a reaction is added to the current instruction message. An empty `completion_value` or `*` accepts any reaction; a specific emoji accepts only that emoji. Example reactions are automatically added to reaction-based instruction messages.

Define multiple branches in one row with numbered `branch_reaction_N` and `branch_step_N` columns. Branches always target steps in the current scenario.

## Template files

CSV templates are stored in the `templates` folder at the repository root. Edit the linked CSV and attach it to the corresponding command.

- [channel_template.csv](templates/channel_template.csv): Channel configuration
- [chat_template.csv](templates/chat_template.csv): Attachment download
- [member_role_template.csv](templates/member_role_template.csv): Member role configuration
- [server_role_template.csv](templates/server_role_template.csv): Server role configuration
- [scenario_template.csv](templates/scenario_template.csv): Scenario registration