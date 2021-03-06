# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: Helixcs
 Site: https://iliangqunru.bitcron.com/
 File: unity.py
 Time: 10/27/18
 常用方法
"""
import random

__all__ = ['open_file', 'is_blank', 'is_not_blank', 'get_mime', 'get_suffix', 'assert_state', 'equal_ignore',
           'AtomicInt','generate_random_string_with_digest']
import threading
from contextlib import contextmanager
from typing import Optional, Union

from py_fortify.constants import MIME_DICT


@contextmanager
def open_file(file_name: str, mode: str = 'wb'):
    file = open(file=file_name, mode=mode)
    yield file
    file.flush()
    file.close()


def is_blank(value: Optional[Union[int, str, dict, list]]) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return True if value is None or value.strip('') == '' else False
    if isinstance(value, dict):
        return True if len(value) > 0 else False
    if isinstance(value, list):
        return True if len(value) > 0 else False
    return False


def is_not_blank(value: Optional[Union[int, str, dict, list]]) -> bool:
    return not is_blank(value=value)


def generate_random_string_with_digest(length: int = 6) -> str:
    _seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    _sa = []
    for i in range(length):
        _sa.append(random.choice(_seed))
    _rds = "".join(_sa)
    return _rds


def get_mime(suffix: str) -> Optional[str]:
    return MIME_DICT.get(suffix)


def get_suffix(mime: str) -> Optional[str]:
    for k, v in MIME_DICT.items():
        if v == mime:
            return k
    return None


def assert_state(state: bool, message: str) -> None:
    if state:
        raise Exception(message)


def equal_ignore(foo: str, bar: str) -> bool:
    if foo is None and bar is None: return True
    if foo is None: return False
    if bar is None: return False
    return foo.strip().lower() == bar.strip().lower()


# TODO 可重入
class AtomicInt(object):
    __slots__ = ['_current_thread', '_value', '_lock']

    def __init__(self, value: int = 0) -> None:
        self._value = value
        self._lock = threading.Lock()
        self._current_thread = threading.current_thread()

    @property
    def get(self) -> int:
        with self._lock:
            return self._value

    @get.setter
    def set(self, value: int) -> None:
        with self._lock:
            self._value = value

    def get_and_increment(self) -> int:
        with self._lock:
            self._value += 1
            return self._value

    def get_and_decrement(self) -> int:
        with self._lock:
            self._value += -1
            return self._value
