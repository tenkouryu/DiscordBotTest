# DiscordBotTest

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

### General

```text
/help
```

### Member roles

```text
/member role add @member role-name
/member role get member-name
/member role set + CSV-file
/member role template
/member role remove @member role-name
```

`get` replies with the roles of a member matching their username or display name. You can also specify a member by mention.

The `add`, `set`, and `remove` commands require the Manage Roles permission.

### Server roles

```text
/server role add role-name
/server role edit role-name permission-name on|off
/server role edit role-name color #RRGGBB
/server role get
/server role set + CSV-file
/server role template
/server role remove role-name
```

The `add`, `edit`, `set`, and `remove` commands require the Manage Roles permission.

### Member list

```text
/server member list
```

Exports the server member list as a CSV file.

### Channels

```text
/channel create text channel-name [category-name]
/channel create voice channel-name [category-name]
/channel move #channel category-name
/channel set + CSV-file
/channel template
```

Creating and moving channels requires the Manage Channels permission. A specified category is created automatically if it does not exist.

The CSV format for `/channel set` is:

```csv
name,type,category
channel-name,text,category-name
```

Set `type` to `text` or `voice`. Existing channels are found by name and moved to the specified category; missing channels are created. Missing categories are created automatically.

### Event notifications

These are sample features. Change or disable the behavior and notification destinations to suit your production requirements.

- Adding a thumbs-up reaction replies in the channel containing the reacted message.
- Joining or leaving a voice channel sends a notification to that voice channel's text chat.
- When a new member joins, a notification is sent to the channel specified by `REDIRECT_CHANNEL_ID`.

## CSV

### Member role operations

Get a template with:

```text
/member role template
```

The CSV has these three columns:

```csv
add/remove,display-name,role
```

Replace the example row with actual values and attach the file to:

```text
/member role set + CSV-file
```

Set `add/remove` to `add` or `remove`.

### Server role configuration

Get a template with:

```text
/server role template
```

The `name` column is required. The `color` and permission columns are optional; only the columns included in the CSV are configured. Remove columns that should not be configured.

```text
/server role set + CSV-file
```

If a role with the specified name does not exist, it is created. Set permission values to `true` or `false`.

To export the role list as a configuration CSV, use:

```text
/server role get
```

### Channel configuration

Get a template with:

```text
/channel template
```

The CSV has these three fields:

```csv
name,type,category
channel-name,text,category-name
```

- `name`: The channel name to create or configure
- `type`: `text` or `voice`
- `category`: The category name. Remove this column if no category should be configured.

Attach the CSV file and run:

```text
/channel set + CSV-file
```

Existing channels are found by name and moved to the specified category. Missing channels are created, and missing categories are created automatically.