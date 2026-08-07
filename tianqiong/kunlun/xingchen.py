"""昆仑·星辰：同耀并行之道（threading 薄壳）。

星辰者，任务也；同耀者，并行也。所包者，threading 耳。
"""

from __future__ import annotations

import threading


def 同耀(法, *参) -> threading.Thread:
    """起一星，与主道同耀（threading.Thread + start）。"""
    星 = threading.Thread(target=法, args=参, daemon=True)
    星.start()
    return 星


def 待星(星) -> None:
    """候一星之归（Thread.join）。"""
    星.join()


def 安歇(息: float) -> None:
    """安歇片时，以秒计（time.sleep）。"""
    import time
    time.sleep(息)


def 立锁():
    """立一玄锁（threading.Lock）。"""
    return threading.Lock()


def 持锁(锁) -> None:
    """持锁而入（Lock.acquire）。"""
    锁.acquire()


def 释锁(锁) -> None:
    """释锁而出（Lock.release）。"""
    锁.release()
