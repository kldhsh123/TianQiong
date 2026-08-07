"""昆仑·四象：配置之道（json/configparser 薄壳）。

四象者，青龙白虎朱雀玄武，各守一方之键值。所包者，json 耳。
"""

from __future__ import annotations

import json


def 立四象(**键值) -> dict:
    """立一四象（dict）。"""
    return dict(键值)


def 观象(象: dict, 键: str, 缺=None):
    """观一象之键（dict.get）。"""
    return 象.get(键, 缺)


def 定象(象: dict, 键: str, 值) -> dict:
    """定一象之键（dict.__setitem__），返象以便链式。"""
    象[键] = 值
    return 象


def 化文(象: dict) -> str:
    """化四象为文（json.dumps，保汉字）。"""
    return json.dumps(象, ensure_ascii=False, indent=2)


def 解文(文: str) -> dict:
    """解文为四象（json.loads）。"""
    return json.loads(文)


def 存象(象: dict, 径: str) -> None:
    """存四象于卷。"""
    with open(径, "w", encoding="utf-8") as 卷:
        卷.write(化文(象))


def 载象(径: str) -> dict:
    """自卷载四象。"""
    with open(径, "r", encoding="utf-8") as 卷:
        return 解文(卷.read())
