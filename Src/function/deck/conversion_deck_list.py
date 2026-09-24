import re

"""
    MTGアリーナからエクスポートされたテキストから不要な情報を削除してカード名だけにする処理。

    1. Commander / Deck の行は無視する
    2. 行頭の「数字 + 半角スペース」を削除する
    3. 「(」以降と、その直前の半角スペースを削除する

    Args:
        data:
            テキスト文字列 または 文字列のリスト（スプレッドシート取得対応）
    
    Return:
        カード名だけにした文字列のリスト

    author:Mikado Ohkouchi
"""
def create_card_list(data: str | list[str] | list[list[str]]) -> list[str]:

    # Discordから取得したテキストを想定する。
    if isinstance(data, str):
        lines = data.splitlines()
    elif isinstance(data, list):
        lines = []

        for row in data:
            # Sheets APIの [["AAA"], ["BBB"]] を想定する。
            if isinstance(row, list):
                lines.extend(row)
            else:
                # ["AAA", "BBB"] を想定する。
                lines.append(row)
    else:
        # どの形式でもない場合は形式不備として扱う。
        print("形式不備！")


    card_list = []

    for line in lines:

        # Noneなどを考慮して文字列かどうかを確認する。
        if not isinstance(line, str):
            continue

        # 前後の空白を削除する。
        line = line.strip()

        # 空行を無視する。
        if not line:
            continue

        # Commander / Deckの行を無視する。
        if line in ("Commander", "Deck"):
            continue

        # 行頭の「数字 + 半角スペース」を削除する。
        line = re.sub(r"^\d+\s", "", line)

        # 「(」以降と、その直前の半角スペースを削除する。
        line = re.sub(r"\s+\(.*$", "", line)

        card_list.append(line)

    return card_list