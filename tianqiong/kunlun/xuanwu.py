"""昆仑·玄武：安全之道（hashlib/hmac/secrets 薄壳）。

玄武者，龟蛇相守，主印验之职。所包者，hashlib 耳。
"""

from __future__ import annotations

import hashlib
import hmac
import secrets


def 铸印(文: str, 法: str = "sha256") -> str:
    """铸一印（哈希十六进制）。"""
    算法表 = {
        "sha256": hashlib.sha256, "sha512": hashlib.sha512,
        "md5": hashlib.md5, "sha1": hashlib.sha1,
        "国密": hashlib.sha256,  # 戏言：国密者，sha256 之别名也
    }
    造 = 算法表.get(str(法).lower(), hashlib.sha256)
    return 造(str(文).encode("utf-8")).hexdigest()


def 验印(文: str, 印: str, 法: str = "sha256") -> bool:
    """验印之真伪。"""
    return hmac.compare_digest(铸印(文, 法), str(印))


def 密押(文: str, 钥: str, 法: str = "sha256") -> str:
    """以钥铸押（HMAC）。"""
    算法表 = {"sha256": hashlib.sha256, "sha512": hashlib.sha512}
    造 = 算法表.get(str(法).lower(), hashlib.sha256)
    return hmac.new(str(钥).encode("utf-8"),
                    str(文).encode("utf-8"), 造).hexdigest()


def 验押(文: str, 钥: str, 押: str, 法: str = "sha256") -> bool:
    """验押之真伪。"""
    return hmac.compare_digest(密押(文, 钥, 法), str(押))


def 灵符(长: int = 16) -> str:
    """铸一灵符（随机十六进制，长字节数）。"""
    return secrets.token_hex(int(长))


def 天衍(始: int, 终: int) -> int:
    """天衍之数（安全随机整数，含始含终）。"""
    return secrets.randbelow(int(终) - int(始) + 1) + int(始)
