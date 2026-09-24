# DiscordBot_Servercontroller

## Overview

This is a Discord bot built with discord.py. It helps manage members, roles, channels, chat attachments, and scenario-based workflows in a Discord server.

## Setup

1. Prepare Python 3.10 or later.
2. Install discord.py.

```powershell
pip install discord.py
```

3. Set the bot token and redirect channel ID in `Src/config/config.json`.

```json
{
  "BOT_TOKEN": "your bot token",
  "REDIRECT_CHANNEL_ID": "notification channel ID"
}
```

4. Enable the following intents in the Discord Developer Portal.
   - Message Content Intent
   - Server Members Intent
   - Reactions
   - Voice States

5. Start the bot.

```powershell
python bot_main.py
```

Do not expose the bot token, and avoid committing `Src/config/config.json` to Git.

## Commands

Commands are used as slash commands. Use `/help` to display all available commands.

### Common commands

```text
/help
```

### Member role commands

```text
/member role add @member role-name
/member role get member-name
/member role set + CSV-file
/member role template
/member role remove @member role-name
```

See `member_role_template.csv` in the [Template files](#template-files) section for the CSV format.

`get` returns the roles of the matching member by username or display name. A mention can also be used.

The `add`, `set`, and `remove` commands require the Manage Roles permission.

### Server role commands

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

### Member list command

```text
/server member list
```

Exports the server member list as a CSV file.

### Channel commands

```text
/channel create text channel-name [category-name]
/channel create voice channel-name [category-name]
/channel move #channel category-name
/channel get
/channel set + CSV-file
/channel template
```

Creating and moving channels requires the Manage Channels permission. If the target category does not exist, it is created automatically.

Use `/channel get` to export the server's channel list as `name,type,category` CSV.

See `channel_template.csv` in the [Template files](#template-files) section for the CSV format.

Set `type` to `text` or `voice`. Existing channels are found by name and moved to the specified category; missing channels are created automatically.

### Chat attachment commands

```text
/chat get #text-channel [start-date YYYY-MM-DD] [extension]
/chat get + CSV-file
/chat template
```

Mention a channel to fetch attachments from that single channel. The optional start date uses `YYYY-MM-DD`; files from 00:00 UTC on that date onward are included. Extensions can be specified as `png` or `.png`, and multiple values can be provided like `png|jpg|gif`.

For multiple channels, set `category_name,channel_name,start_date,extension` in the CSV. Attachments from each channel are combined into a single ZIP file in the structure `category-name/channel-name/file-name`. Leave `start_date` or `extension` blank to skip that filter. The Manage Messages permission is required.

See `chat_template.csv` in the [Template files](#template-files) section for the CSV format.

### Event notification features

These are sample features and can be modified or disabled depending on your production requirements.

- Joining or leaving a voice channel sends a notification to that channel's text chat.
- When a new member joins, a notification is sent to the channel configured in `REDIRECT_CHANNEL_ID`.

### Scenario commands

```text
/scenario template
/scenario set + CSV-file
/scenario list
/scenario start scenario-id [start-step]
/scenario delete scenario-id
/scenario export
```

Scenario definitions are stored in `config/scenario_definitions.json`, and per-server progress is stored in `config/scenario_states.json`. `/scenario set` preserves existing scenarios and appends or updates entries from the CSV. If the same scenario ID and step number already exist, they are updated. `/scenario export` exports registered scenarios as CSV.

See `scenario_template.csv` in the [Template files](#template-files) section for the CSV format and the example `welcome` scenario.

When `completion_type` is `reaction`, the scenario advances when a reaction is added to the current instruction message. If `completion_value` is `*` or empty, any reaction is accepted; if it is a specific emoji, only that emoji is accepted. Sample reactions are automatically added to reaction-based instructions.

Multiple branches can be defined in one row using numbered `branch_reaction_N` and `branch_step_N` columns. Branch targets are limited to steps within the current scenario.

## Template files

CSV templates are stored in the `Src/templates` folder. Edit the linked CSV files and attach them to the corresponding commands.

- [channel_template.csv](../templates/channel_template.csv): Channel configuration
- [chat_template.csv](../templates/chat_template.csv): Attachment retrieval
- [member_role_template.csv](../templates/member_role_template.csv): Member role configuration
- [server_role_template.csv](../templates/server_role_template.csv): Server role configuration
- [scenario_template.csv](../templates/scenario_template.csv): Scenario registration
