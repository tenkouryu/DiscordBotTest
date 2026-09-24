from __future__ import annotations

import argparse
import csv
import io
import sys
from pathlib import Path
from typing import TextIO


_REQUIRED_COLUMNS = {
    "scenario_id",
    "step",
    "instruction",
    "completion_type",
    "completion_value",
    "response",
}


def load_scenarios(csv_path: Path) -> dict[str, list[dict[str, str]]]:
    """CSVを読み込み、シナリオIDごとにステップをまとめる。"""
    last_decode_error: UnicodeDecodeError | None = None
    for encoding in ("utf-8-sig", "utf-8", "cp932", "utf-16"):
        try:
            text = csv_path.read_text(encoding=encoding)
            sample = "\n".join(text.splitlines()[:3])
            try:
                delimiter = csv.Sniffer().sniff(sample, delimiters=",\t;").delimiter
            except csv.Error:
                delimiter = max((",", "\t", ";"), key=sample.count)

            reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
            if reader.fieldnames:
                reader.fieldnames = [field.strip() for field in reader.fieldnames]
            columns = set(reader.fieldnames or [])
            missing_columns = _REQUIRED_COLUMNS - columns
            if missing_columns:
                missing = ", ".join(sorted(missing_columns))
                detected = ", ".join(sorted(columns)) or "なし"
                raise ValueError(
                    f"CSVに必要な列がありません: {missing}（検出した列: {detected}）"
                )

            scenarios: dict[str, list[dict[str, str]]] = {}
            for row_number, row in enumerate(reader, start=2):
                scenario_id = (row.get("scenario_id") or "").strip()
                if not scenario_id:
                    raise ValueError(f"{row_number}行目: scenario_idが空です")

                step_text = (row.get("step") or "").strip()
                try:
                    int(step_text)
                except ValueError as error:
                    raise ValueError(f"{row_number}行目: stepは整数で指定してください") from error

                normalized_row = {
                    key: (value or "").strip()
                    for key, value in row.items()
                    if key is not None
                }
                scenarios.setdefault(scenario_id, []).append(normalized_row)
            break
        except UnicodeDecodeError as error:
            last_decode_error = error
    else:
        raise ValueError(f"CSVの文字コードを判定できませんでした: {last_decode_error}")

    for steps in scenarios.values():
        steps.sort(key=lambda row: int(row["step"]))
    return scenarios


def _print_line(output: TextIO, label: str, value: str) -> None:
    if value:
        print(f"  {label}: {value}", file=output)


def print_step(output: TextIO, step: dict[str, str], step_index: int, total_steps: int) -> None:
    """現在のステップを表示する。"""
    print(f"\n[{step_index}/{total_steps}] Step {step['step']}", file=output)
    _print_line(output, "指示", step.get("instruction", ""))
    _print_line(output, "完了条件", step.get("completion_type", ""))
    _print_line(output, "完了値", step.get("completion_value", ""))
    _print_line(output, "返信", step.get("response", ""))

    branches = []
    for key, value in step.items():
        if not key.startswith("branch_reaction_") or not value:
            continue
        suffix = key.removeprefix("branch_reaction_")
        target_step = step.get(f"branch_step_{suffix}", "")
        branches.append(f"{value} -> step {target_step}")
    if branches:
        _print_line(output, "分岐", ", ".join(branches))


def run_scenario(output: TextIO, scenario_id: str, steps: list[dict[str, str]]) -> None:
    """シナリオを1ステップずつ表示し、入力後に次へ進む。"""
    print(f"\n=== {scenario_id} ({len(steps)} steps) ===", file=output)
    for index, step in enumerate(steps, start=1):
        print_step(output, step, index, len(steps))
        if index == len(steps):
            print("\nシナリオが完了しました。", file=output)
            return
        try:
            command = input("\nEnterで次のステップ、qで終了: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nシナリオ表示を終了しました。", file=output)
            return
        if command == "q":
            print("シナリオ表示を終了しました。", file=output)
            return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="シナリオCSVを読み込み、ステップと分岐を表示します。CSVをexeへドラッグ＆ドロップして起動できます。"
    )
    parser.add_argument(
        "csv_file",
        type=Path,
        help="表示するシナリオCSVファイル（exeへのドラッグ＆ドロップに対応）",
    )
    parser.add_argument(
        "--scenario",
        help="表示するシナリオID。省略した場合はCSV内の全シナリオを表示",
    )
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    args = parse_args()
    if not args.csv_file.is_file():
        print(f"CSVファイルが見つかりません: {args.csv_file}")
        return 1

    try:
        scenarios = load_scenarios(args.csv_file)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"CSVを読み込めませんでした: {error}")
        return 1

    if args.scenario:
        steps = scenarios.get(args.scenario)
        if steps is None:
            print(f"シナリオが見つかりません: {args.scenario}")
            return 1
        run_scenario(sys.stdout, args.scenario, steps)
        return 0

    if len(scenarios) == 1:
        scenario_id, steps = next(iter(scenarios.items()))
        run_scenario(sys.stdout, scenario_id, steps)
        return 0

    print("表示するシナリオを選択してください:")
    scenario_ids = list(scenarios)
    for index, scenario_id in enumerate(scenario_ids, start=1):
        print(f"  {index}. {scenario_id}")
    try:
        selection = int(input("番号: ").strip())
    except (ValueError, EOFError, KeyboardInterrupt):
        print("シナリオが選択されませんでした。")
        return 1
    if not 1 <= selection <= len(scenario_ids):
        print("無効な番号です。")
        return 1
    scenario_id = scenario_ids[selection - 1]
    run_scenario(sys.stdout, scenario_id, scenarios[scenario_id])
    return 0


if __name__ == "__main__":
    exit_code = main()
    try:
        input("\nEnterで終了します。")
    except (EOFError, KeyboardInterrupt):
        pass
    raise SystemExit(exit_code)
