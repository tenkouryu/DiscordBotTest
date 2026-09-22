import csv
import io


"""
    台本進行用CSVテンプレートを作成する共通処理。

    create_scenario_template:
        台本ID、ステップ、指示、完了条件、返信内容を含むCSVを作成する。
"""


def create_scenario_template() -> io.BytesIO:
    """台本進行用のCSVテンプレートを作成する。"""
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow([
        "scenario_id",
        "step",
        "instruction",
        "completion_type",
        "completion_value",
        "response",
        "branch_reaction_1",
        "branch_scenario_id_1",
        "branch_step_1",
        "branch_reaction_2",
        "branch_scenario_id_2",
        "branch_step_2",
    ])
    writer.writerow([
        "example",
        "1",
        "参加者に準備ができたか確認する。どのリアクションでも進行する",
        "reaction",
        "*",
        "確認しました。次の指示へ進みます。",
        "👍",
        "success",
        "1",
        "👎",
        "retry",
        "1",
    ])
    return io.BytesIO(output.getvalue().encode("utf-8-sig"))
