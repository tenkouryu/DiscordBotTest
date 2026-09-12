import re


def create_card_list(data: str | list[str] | list[list[str]]) -> list[str]:
    """
    DiscordまたはGoogle Sheets APIから取得したカードリストから
    カード名のリストを作成する。
    """

    if isinstance(data, str):
        lines = data.splitlines()

    elif isinstance(data, list):
        lines = []

        for row in data:
            if isinstance(row, list):
                lines.extend(row)
            else:
                lines.append(row)

    else:
        raise TypeError("dataにはstrまたはlistを指定してください")

    card_list = []

    for line in lines:

        if not isinstance(line, str):
            continue

        line = line.strip()

        if not line:
            continue

        if line in ("Commander", "Deck"):
            continue

        line = re.sub(r"^\d+\s", "", line)

        line = re.sub(r"\s+\(.*$", "", line)

        card_list.append(line)

    return card_list


# ========================================
# Discordのテスト
# ========================================

discord_data = """Commander
1 Yuriko, the Tiger's Shadow (FCA) 60

Deck
1 Ornithopter (BRR) 37
8 Island (NEO) 296
7 Swamp (NEO) 297
1 A-Futurist Operative (NEO) 53
1 A-Thousand-Faced Shadow (NEO) 86
1 Ingenious Prodigy (WOE) 56
1 Siren Stormtamer (XLN) 79
1 Mox Amber (BRR) 35
1 Brainstorm (FCA) 28
"""

result = create_card_list(discord_data)

print("=== Discord ===")
for card in result:
    print(card)


# ========================================
# Google Sheets APIのテスト
# ========================================

sheets_data = [
    ["Commander"],
    ["1 Yuriko, the Tiger's Shadow (FCA) 60"],
    ["Deck"],
    ["1 Ornithopter (BRR) 37"],
    ["8 Island (NEO) 296"],
    ["7 Swamp (NEO) 297"],
    ["1 A-Futurist Operative (NEO) 53"],
    ["1 A-Thousand-Faced Shadow (NEO) 86"],
    ["1 Ingenious Prodigy (WOE) 56"],
    ["1 Siren Stormtamer (XLN) 79"],
    ["1 Mox Amber (BRR) 35"],
    ["1 Brainstorm (FCA) 28"]
]

result = create_card_list(sheets_data)

print()
print("=== Google Sheets API ===")
for card in result:
    print(card)