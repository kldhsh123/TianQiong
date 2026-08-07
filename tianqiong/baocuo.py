"""报错：凡有所失，皆行公文。

格式定式：
    天穹编译错误：
    语义未定义
      于「某.天穹」第 5 行
      天地间未闻此名「某某」

级别：提示 < 警示 < 错误 < 阴阳冲突
"""

from __future__ import annotations

import sys
import traceback


# Python 异常 → （名目， 公文模板）
映射 = {
    "NameError": ("语义未定义", "天地间未闻此名"),
    "SyntaxError": ("章法有误", "不合天穹文法"),
    "IndentationError": ("章法有误", "缩进不齐，乾坤未开"),
    "TypeError": ("五行相克", "类型不协"),
    "ValueError": ("数不合度", "其值有亏"),
    "KeyError": ("查无此键", "典中无此目"),
    "IndexError": ("逾界之失", "索引越其疆界"),
    "AttributeError": ("无此法门", "其物无此属性"),
    "ZeroDivisionError": ("数不合度", "以零为除，数理不容"),
    "FileNotFoundError": ("求索无门", "寻不见此卷"),
    "PermissionError": ("求索无门", "此卷不可开"),
    "RecursionError": ("天道循环至极", "递归过深，乾坤颠倒"),
    "StopIteration": ("行至终章", "遍历已竟"),
    "ImportError": ("昆仑无此卷", "所引之库不可得"),
    "ModuleNotFoundError": ("昆仑无此卷", "所引之库不可得"),
}


def _提取天穹帧(溯源) -> list[tuple[str, int]]:
    """只留 .天穹 之帧；内部 .py 帧一概折叠（幻觉不可破）。"""
    帧们 = []
    for 帧 in traceback.extract_tb(溯源):
        if 帧.filename.endswith(".天穹"):
            帧们.append((帧.filename, 帧.lineno or 0))
    return 帧们


def _提取细节(异常: BaseException) -> str:
    """从异常消息里摘出用户能看懂的只言片语。"""
    言 = str(异常)
    if isinstance(异常, NameError):
        # "name 'xxx' is not defined" → 只留名
        名 = getattr(异常, "name", None)
        if 名:
            return f"「{名}」"
    if isinstance(异常, SyntaxError):
        # 语法错误之消息多为英文；若位于 .天穹 卷，弃其原言，只书行号
        卷 = getattr(异常, "filename", "") or ""
        if 卷.endswith(".天穹") or 卷 == "<问道>":
            return ""
    if isinstance(异常, (FileNotFoundError, PermissionError)):
        名 = getattr(异常, "filename", None)
        if 名:
            return f"「{名}」"
    return f"（{言}）" if 言 else ""


def 化公文(异常: BaseException, 源名: str | None = None) -> str:
    """化异常为一纸公文。"""
    类名 = type(异常).__name__
    名目, 套话 = 映射.get(类名, ("天穹运行错误", "有司未能尽详"))
    行们 = [f"天穹{'编译' if 类名.endswith('SyntaxError') or 类名 == 'IndentationError' else '运行'}错误：", 名目]

    帧们 = _提取天穹帧(异常.__traceback__) if 异常.__traceback__ else []
    if 帧们:
        文件, 行号 = 帧们[-1]
        行们.append(f"  于「{文件}」第 {行号} 行")
    elif 源名:
        行号 = getattr(异常, "lineno", None)
        if 行号:
            行们.append(f"  于「{源名}」第 {行号} 行")

    细节 = _提取细节(异常)
    if 细节:
        行们.append(f"  {套话}{细节}")
    else:
        行们.append(f"  {套话}")
    return "\n".join(行们)


def 报编译误(源名: str, 行: int, 缘由: str) -> str:
    """词法/语法阶段之公文。"""
    return f"天穹编译错误：\n章法有误\n  于「{源名}」第 {行} 行\n  {缘由}"


def 安装钩子(源名: str | None = None) -> None:
    """安装 excepthook，此后一切未捕之异常皆行公文。"""

    def 钩子(类, 异常, 溯源):
        if issubclass(类, KeyboardInterrupt):
            print("\n天穹提示：\n  运行时断\n  有司奉命中止", file=sys.stderr)
            return
        异常.__traceback__ = 溯源
        print(化公文(异常, 源名), file=sys.stderr)

    sys.excepthook = 钩子
