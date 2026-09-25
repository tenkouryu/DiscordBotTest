from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


_TEMPLATE_ROOT = Path(__file__).resolve().parents[2] / "templates"
_OUTPUT_FOLDERS = {
    "set/response": _TEMPLATE_ROOT / "set" / "response",
    "get/result": _TEMPLATE_ROOT / "get" / "result",
}


def create_template_output_path(
    category: str,
    prefix: str,
    suffix: str = ".csv",
) -> Path:
    """出力カテゴリ内に一意な成果物パスを作成する。"""
    output_folder = _OUTPUT_FOLDERS.get(category)
    if output_folder is None:
        raise ValueError(f"未対応の出力カテゴリです: {category}")
    if suffix not in {".csv", ".zip"}:
        raise ValueError("出力ファイルの拡張子は .csv または .zip を指定してください。")

    safe_prefix = re.sub(r"[^A-Za-z0-9_-]+", "_", prefix).strip("_")
    if not safe_prefix:
        raise ValueError("出力ファイル名を指定してください。")

    output_folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return output_folder / f"{safe_prefix}_{timestamp}_{uuid4().hex[:8]}{suffix}"


def save_template_output(
    category: str,
    prefix: str,
    content: bytes,
    suffix: str = ".csv",
) -> Path:
    """成果物を分類先へ保存してパスを返す。"""
    output_path = create_template_output_path(category, prefix, suffix)
    output_path.write_bytes(content)
    return output_path