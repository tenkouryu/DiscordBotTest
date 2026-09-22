from __future__ import annotations

import os
from pathlib import Path
import zipfile

"""
    ファイルやディレクトリのZIP圧縮と、安全なZIP解凍を行う共通処理。

    compress_files:
        複数のファイルをZIP形式で圧縮する。

    compress_directory:
        ディレクトリ内のファイルを相対パスを維持して再帰的に圧縮する。

    extract_zip:
        ZIP内のパスが解凍先ディレクトリ外へ移動しないことを確認してから解凍する。
        パストラバーサル攻撃を防止する。
"""


def compress_files(
    file_paths: list[str | os.PathLike[str]],
    zip_path: str | os.PathLike[str],
) -> Path:
    """複数のファイルをZIP形式で圧縮する。"""
    if not file_paths:
        raise ValueError("圧縮するファイルを1つ以上指定してください。")

    output_path = Path(zip_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in file_paths:
            path = Path(file_path)
            if not path.is_file():
                raise FileNotFoundError(f"ファイルが見つかりません: {path}")
            archive.write(path, arcname=path.name)

    return output_path


def compress_directory(
    directory_path: str | os.PathLike[str],
    zip_path: str | os.PathLike[str],
) -> Path:
    """ディレクトリ内のファイルをZIP形式で再帰的に圧縮する。"""
    source_path = Path(directory_path)
    if not source_path.is_dir():
        raise NotADirectoryError(f"ディレクトリが見つかりません: {source_path}")

    output_path = Path(zip_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.is_relative_to(source_path):
        raise ValueError("出力先ZIPは圧縮元ディレクトリの外に指定してください。")

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in source_path.rglob("*"):
            if path.is_file():
                archive.write(path, arcname=path.relative_to(source_path))

    return output_path


def extract_zip(
    zip_path: str | os.PathLike[str],
    destination_path: str | os.PathLike[str],
) -> Path:
    """ZIPファイルを指定ディレクトリへ安全に解凍する。"""
    archive_path = Path(zip_path)
    if not archive_path.is_file():
        raise FileNotFoundError(f"ZIPファイルが見つかりません: {archive_path}")

    output_path = Path(destination_path)
    output_path.mkdir(parents=True, exist_ok=True)
    output_root = output_path.resolve()

    with zipfile.ZipFile(archive_path, "r") as archive:
        for member in archive.infolist():
            member_path = (output_root / member.filename).resolve()
            if not member_path.is_relative_to(output_root):
                raise ValueError(f"安全でないZIP内パスです: {member.filename}")
        archive.extractall(output_root)

    return output_root