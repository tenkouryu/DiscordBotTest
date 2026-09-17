"""
禁止カードチェック。
禁止カードのリストとデッキリストの文字列を突合する。

    Returns:
        一致する文字列がない場合:
            (True, [])

        一致する文字列がある場合:
            (False, 一致した文字列のリスト)

    author:Mikado Ohkouchi
"""
def check_banned_list(list1: list[str], list2: list[str]) -> tuple[bool, list[str]]:
    list2_set = set(list2)

    # list1の順番を維持して一致する文字列を取得
    matches = [value for value in list1 if value in list2_set]

    if matches:
        return False, matches

    return True, []


"""
登録デッキチェック。
申請された100枚のデッキリストに、115枚のデッキリストに存在しないカードが含まれているかチェックする。

    Returns:
        True, []
            OK

        False, [不一致文字列...]:
            NG

    author:Mikado Ohkouchi
"""
def check_registered_list(registered_list: list[str], applied_list: list[str]) -> tuple[bool, list[str]]:
    registered_list_set = set(registered_list)

    not_found = [value for value in applied_list if value not in registered_list_set]

    if not_found:
        return False, not_found

    return True, []