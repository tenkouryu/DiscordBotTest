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
        "welcome",
        "1",
        "参加ありがとうございます。確認できたら任意のリアクションを押してください。",
        "reaction",
        "*",
        "ありがとうございます。次の確認へ進みます。",
        "👍",
        "welcome",
        "2",
        "👎",
        "welcome",
        "1",
    ])
    writer.writerow([
        "welcome",
        "2",
        "名前を確認します。確認できたら✅を押してください。",
        "reaction",
        "✅",
        "名前を確認しました。最後の確認へ進みます。",
        "",
        "",
        "",
        "",
        "",
        "",
    ])
    writer.writerow([
        "welcome",
        "3",
        "最後に🎉を押してください。",
        "reaction",
        "🎉",
        "シナリオが完了しました。",
        "",
        "",
        "",
        "",
        "",
        "",
    ])
    return io.BytesIO(output.getvalue().encode("utf-8-sig"))
