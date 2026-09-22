from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any


"""
    台本の登録とサーバーごとの進行状態を管理する共通処理。

    register_scenario_csv:
        CSV形式の台本を定義JSONへ登録する。

    list_scenarios:
        登録済み台本のIDとステップ数を取得する。

    start_scenario:
        サーバーの台本進行を開始し、最初のステップを返す。

    set_scenario_message_id:
        現在の台本指示メッセージIDを保存する。

    advance_scenario:
        現在の指示が完了したかを確認し、完了していれば次のステップへ進める。
"""

_DEFAULT_DEFINITIONS_PATH = Path("config/scenario_definitions.json")
_DEFAULT_STATES_PATH = Path("config/scenario_states.json")
_REQUIRED_COLUMNS = {
    "scenario_id",
    "step",
    "instruction",
    "completion_type",
    "completion_value",
    "response",
}


def _read_json(path: Path, default: Any) -> Any:
    """JSONファイルを読み込み、存在しない場合は初期値を返す。"""
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _write_json(path: Path, data: Any) -> None:
    """JSONを一時ファイルへ書き込み、保存先へ置き換える。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        delete=False,
    ) as temporary_file:
        json.dump(data, temporary_file, ensure_ascii=False, indent=2)
        temporary_path = Path(temporary_file.name)
    temporary_path.replace(path)


def register_scenario_csv(
    csv_text: str,
    definitions_path: str | Path = _DEFAULT_DEFINITIONS_PATH,
) -> int:
    """既存の台本定義を保持し、CSVの台本を定義JSONへ追記する。"""
    reader = csv.DictReader(io.StringIO(csv_text))
    fieldnames = set(reader.fieldnames or [])
    if not _REQUIRED_COLUMNS.issubset(fieldnames):
        missing_columns = _REQUIRED_COLUMNS - fieldnames
        raise ValueError(
            "CSVに必要な列がありません: " + ", ".join(sorted(missing_columns))
        )

    scenarios = _read_json(Path(definitions_path), {})
    registered_count = 0
    for row in reader:
        scenario_id = (row.get("scenario_id") or "").strip()
        if not scenario_id:
            raise ValueError("scenario_idを指定してください。")
        try:
            step = int((row.get("step") or "").strip())
        except ValueError as error:
            raise ValueError("stepは整数で指定してください。") from error
        if step < 1:
            raise ValueError("stepは1以上で指定してください。")

        scenario_steps = scenarios.setdefault(scenario_id, [])
        scenario_steps[:] = [
            current_step
            for current_step in scenario_steps
            if current_step.get("step") != step
        ]
        scenario_steps.append(
            {
                "step": step,
                "instruction": (row.get("instruction") or "").strip(),
                "completion_type": (row.get("completion_type") or "keyword").strip().lower(),
                "completion_value": (row.get("completion_value") or "").strip(),
                "response": (row.get("response") or "").strip(),
            }
        )
        scenario_steps.sort(key=lambda current_step: current_step["step"])
        registered_count += 1

    _write_json(Path(definitions_path), scenarios)
    return registered_count


def list_scenarios(
    definitions_path: str | Path = _DEFAULT_DEFINITIONS_PATH,
) -> list[dict[str, int | str]]:
    """登録済み台本のIDとステップ数を一覧で返す。"""
    scenarios = _read_json(Path(definitions_path), {})
    return [
        {"scenario_id": scenario_id, "step_count": len(steps)}
        for scenario_id, steps in sorted(scenarios.items())
    ]


def start_scenario(
    guild_id: int,
    scenario_id: str,
    definitions_path: str | Path = _DEFAULT_DEFINITIONS_PATH,
    states_path: str | Path = _DEFAULT_STATES_PATH,
) -> dict[str, Any]:
    """指定サーバーの台本進行を開始し、最初のステップを返す。"""
    scenarios = _read_json(Path(definitions_path), {})
    steps = scenarios.get(scenario_id)
    if not steps:
        raise ValueError(f"台本が見つかりません: {scenario_id}")

    states = _read_json(Path(states_path), {})
    states[str(guild_id)] = {
        "scenario_id": scenario_id,
        "step": steps[0]["step"],
        "message_id": None,
    }
    _write_json(Path(states_path), states)
    return steps[0]


def set_scenario_message_id(
    guild_id: int,
    message_id: int,
    states_path: str | Path = _DEFAULT_STATES_PATH,
) -> None:
    """現在の台本指示メッセージIDを保存する。"""
    states = _read_json(Path(states_path), {})
    state = states.get(str(guild_id))
    if state is None:
        raise ValueError("開始中の台本がありません。")
    state["message_id"] = message_id
    _write_json(Path(states_path), states)


def advance_scenario(
    guild_id: int,
    completion_value: str,
    message_id: int | None = None,
    definitions_path: str | Path = _DEFAULT_DEFINITIONS_PATH,
    states_path: str | Path = _DEFAULT_STATES_PATH,
) -> dict[str, Any] | None:
    """現在ステップの完了を確認し、完了時は次のステップを返す。"""
    states = _read_json(Path(states_path), {})
    state = states.get(str(guild_id))
    if state is None:
        return None

    scenarios = _read_json(Path(definitions_path), {})
    steps = scenarios.get(state["scenario_id"], [])
    current_index = next(
        (index for index, step in enumerate(steps) if step["step"] == state["step"]),
        None,
    )
    if current_index is None:
        raise ValueError("現在の台本ステップが見つかりません。")

    current_step = steps[current_index]
    completion_type = current_step["completion_type"]
    if completion_type == "reaction" and state.get("message_id") != message_id:
        return None
    if completion_type != "reaction" and message_id is not None:
        return None
    expected_completion = current_step["completion_value"]
    if (
        completion_type == "reaction"
        and expected_completion not in {"", "*"}
        and completion_value.strip() != expected_completion
    ):
        return None
    if completion_type != "reaction" and completion_value.strip() != expected_completion:
        return None

    response = current_step["response"]
    next_index = current_index + 1
    if next_index >= len(steps):
        del states[str(guild_id)]
        _write_json(Path(states_path), states)
        return {"response": response, "instruction": None, "completed": True}

    next_step = steps[next_index]
    state["step"] = next_step["step"]
    _write_json(Path(states_path), states)
    return {
        "response": response,
        "instruction": next_step["instruction"],
        "completed": False,
    }
