import ctypes
import os
from contextlib import contextmanager
from ctypes import wintypes
from collections.abc import Iterator


ERROR_ALREADY_EXISTS = 183


@contextmanager
def single_instance(name: str) -> Iterator[bool]:
    if os.name != "nt":
        yield True
        return

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateMutexW.argtypes = (
        wintypes.LPVOID,
        wintypes.BOOL,
        wintypes.LPCWSTR,
    )
    kernel32.CreateMutexW.restype = wintypes.HANDLE
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL

    ctypes.set_last_error(0)
    handle = kernel32.CreateMutexW(None, False, name)
    if not handle:
        raise ctypes.WinError(ctypes.get_last_error())

    already_exists = ctypes.get_last_error() == ERROR_ALREADY_EXISTS
    try:
        yield not already_exists
    finally:
        if not kernel32.CloseHandle(handle):
            raise ctypes.WinError(ctypes.get_last_error())