# Application Structure Document

## 1. Overview

This application is a Discord bot designed to support server operations. It receives Discord events and provides a unified set of features for member management, role management, channel management, attachment retrieval, scenario progression, and notifications.

The main execution point is `bot_main.py`, which creates the Discord client and registers event handlers and slash commands.

## 2. Overall Responsibility Map

```text
bot_main.py
  └─ Creates the Discord client and registers events
        ├─ event/on_ready/        : startup logic
        ├─ event/on_message/      : message handling
        ├─ event/on_reaction/     : reaction handling
        ├─ event/on_member_join/  : member join handling
        ├─ event/on_voice_state_update/ : voice state monitoring
        └─ function/              : business logic and shared utilities

Src/config/
   ├─ config.json              : Bot token and redirect channel settings
   ├─ scenario_definitions.json: scenario definitions
   └─ scenario_states.json     : per-server progress state

Src/templates/
   ├─ channel_template.csv
   ├─ chat_template.csv
   ├─ member_role_template.csv
   ├─ server_role_template.csv
   └─ scenario_template.csv

tools/
  └─ scenario_viewer/         : scenario review GUI
```

## 3. Responsibilities by Directory

### 3.1 `bot_main.py`

This is the application entry point.

- Creates the Discord client
- Enables required Intents
- Registers slash commands
- Connects event handlers
- Starts the bot via `client.run(TOKEN)`

Its main responsibility is acting as the connection point for events and commands.

### 3.2 `event/`

This layer processes Discord events triggered by the platform. Each area is separated by responsibility.

- `on_ready/`: startup initialization and login logging
- `on_message/`: message reception processing
- `on_reaction/`: reaction-based progression for scenarios
- `on_member_join/`: member join notifications
- `on_voice_state_update/`: voice channel join/leave notifications

The `event/on_message/command/` directory contains the individual command implementations, and they are connected to slash commands via `slash_commands.py`.

### 3.3 `function/`

This layer holds the actual business logic.

- `function/scenario/`: scenario registration, progression, deletion, and CSV conversion
- `function/file/`: ZIP compression and safe extraction
- `function/discord/`: Discord API wrappers for notifications and message sending
- `function/security/`: encryption and security-related utilities

This is where the real processing occurs; event handlers mostly act as entry points.

#### Module-level intent of `function/`

- `function/scenario/`: handles scenario definitions, progression, and CSV conversion
- `function/file/`: provides reusable file-processing utilities such as ZIP packaging and extraction
- `function/discord/`: abstracts Discord operations like channel management and message sending
- `function/security/`: handles encryption, validation, and sensitive data protection

This separation keeps Discord-specific code and persistence logic out of the event handlers.

### 3.4 `config/`

This directory stores runtime settings and state used by the bot.

- `config.json`: Bot token and redirect channel settings
- `scenario_definitions.json`: all scenario definitions
- `scenario_states.json`: per-server scenario progression state

The real storage path is `Src/config/`.

This is the persistence layer for the bot's operational state.

### 3.5 `templates/`

This contains the CSV templates used for bulk operations.

- `channel_template.csv`: channel configuration
- `chat_template.csv`: attachment retrieval setup
- `member_role_template.csv`: member role assignments
- `server_role_template.csv`: server role definitions
- `scenario_template.csv`: scenario registration template

The real storage path is `Src/templates/`.

Commands typically receive CSV files from these templates for bulk updates.

### 3.6 `tools/scenario_viewer/`

This is a viewer for scenario CSV files, designed to help review each step in a human-readable way.

- loads scenario definitions from CSV
- displays `step`, `instruction`, `response`, and branches
- uses `Enter` to move forward and `q` to exit

It is mainly used for scenario validation and debugging during development.

## 4. Command Invocation Flow

### Slash command route

```text
Discord interaction
   ↓
slash_commands.py
   ↓
_interactionMessage / _run
   ↓
legacy command handlers in event/on_message/command/...
   ↓
function/ service layer
   ↓
Discord response
```

Key points:

- The actual implementation is not placed directly in the event layer
- `slash_commands.py` acts as an adapter between slash commands and the older command-processing flow
- This allows existing command logic to be reused through the newer Discord slash-command interface

### Scenario progression flow

```text
/scenario set
   ↓
CSV is parsed
   ↓
scenario_service.register_scenario_csv()
   ↓
config/scenario_definitions.json is updated

/scenario start
   ↓
scenario_service.start_scenario()
   ↓
server progress is stored in config/scenario_states.json

incoming message
   ↓
on_message_main()
   ↓
advance_scenario()
   ↓
next step or response message is sent
```

### Responsibility split

- `event/`: receives Discord events
- `function/`: contains the actual business logic and state updates
- `config/`: persists operational data
- `templates/`: defines CSV input/output formats

This structure keeps the Discord API layer separate from the real operational logic.

## 5. Design Principles Behind the Implementation

### 5.1 Event-driven design

Discord is an event-driven platform, so the application naturally organizes functions around event handlers.

### 5.2 CSV-driven operations

Roles, channels, and scenarios can be managed in bulk via CSV files. This makes large operational changes simpler than repeated manual commands.

### 5.3 Compatibility with slash commands

The project keeps an older message-based command structure and exposes it through `slash_commands.py` as slash commands. This reduces the risk of breaking existing behavior while modernizing the interface.

### 5.4 Clear state management

Scenario progression is stored in JSON files per server, allowing the bot to keep track of active flows even while running for long periods.

## 6. How New Features Should Be Added

A typical pattern for adding new features is:

1. Add an event or command entry under `event/`
2. Implement the processing logic in `function/`
3. Extend `config/` or templates if needed
4. Register the feature as a slash command in `slash_commands.py`
5. Add a viewer or helper if scenario inspection is needed

This keeps responsibilities clean and makes the system easier to maintain.

## 7. Notes

- The real startup entry point is `bot_main.py`
- Most features are split between `event/` and `function/`
- Runtime configuration and state are stored in JSON files
- `scenario_viewer` exists as an aid for validating scenario definitions visually

Understanding these layers makes the codebase much easier to navigate.
