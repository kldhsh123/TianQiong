"""CLI：天穹之行，自此而始。

  天穹 运行 <卷.天穹>     —— 执行
  天穹 问道             —— 交互问道（REPL）
  天穹 观天 <卷.天穹>     —— 静态检查，不执行
  天穹 窥豹 <卷.天穹>     —— 出示"源码级降级导出"（生成之 Python 源码）
  天穹 传火 [名目]      —— 起新项之 scaffold
"""

from __future__ import annotations

import ast
import sys

from . import __版本__
from .baocuo import 报编译误, 化公文, 安装钩子
from .cifa import 词法错误
from .tian_di import 筑天地
from .yufa import 语法分析, 语法错误

用法 = """天穹 —— 面向全场景的自主创新编程语言

用法：
  天穹 运行 <卷.天穹>      执行天穹源码
  天穹 问道              进入交互问道之境
  天穹 观天 <卷.天穹>      静态检查（观天象而不动）
  天穹 窥豹 <卷.天穹>      源码级降级导出（出示 Python 等价物）
  天穹 传火 [名目]       起新项（传火于后世）
  天穹 铸器 [名目]       铸天穹解释器为独行之器（单个 exe）
  天穹 版本              出示版本

直书卷名亦可：天穹 你好.天穹
"""


def _读卷(径: str) -> str | None:
    try:
        with open(径, "r", encoding="utf-8") as 卷:
            return 卷.read()
    except FileNotFoundError:
        print(f"天穹运行错误：\n求索无门\n  寻不见此卷「{径}」", file=sys.stderr)
        return None
    except OSError as 失:
        print(化公文(失), file=sys.stderr)
        return None


def _编译(源码: str, 源名: str):
    """源码 → 代码对象；失败则出示公文并返回 None。"""
    try:
        树 = 语法分析(源码)
    except (词法错误, 语法错误) as 误:
        print(报编译误(源名, 误.行, 误.缘由), file=sys.stderr)
        return None
    try:
        return compile(树, 源名, "exec")
    except SyntaxError as 误:
        print(化公文(误, 源名), file=sys.stderr)
        return None


def 令运行(径: str) -> int:
    源码 = _读卷(径)
    if 源码 is None:
        return 1
    码 = _编译(源码, 径)
    if 码 is None:
        return 1
    安装钩子(径)
    天地 = 筑天地()
    try:
        exec(码, 天地)
    except SystemExit as 退:
        return int(退.code or 0)
    except Exception:
        # 交由 excepthook 出示公文
        类, 异常, 溯源 = sys.exc_info()
        sys.excepthook(类, 异常, 溯源)
        return 1
    return 0


def 令观天(径: str) -> int:
    源码 = _读卷(径)
    if 源码 is None:
        return 1
    if _编译(源码, 径) is None:
        return 1
    print(f"天穹提示：\n  观天已毕\n  「{径}」章法无亏，可堪运行")
    return 0


def 令窥豹(径: str) -> int:
    源码 = _读卷(径)
    if 源码 is None:
        return 1
    try:
        树 = 语法分析(源码)
    except (词法错误, 语法错误) as 误:
        print(报编译误(径, 误.行, 误.缘由), file=sys.stderr)
        return 1
    print("# 天穹源码级降级导出")
    print("# 为满足与既有生态之互操作需求，特出示等价物如下：")
    print()
    print(ast.unparse(ast.fix_missing_locations(树)))
    return 0


脚手架 = '''混沌 {名目}

盘古 启动
    【注】天穹初辟，先立一言
    阴 问候 为 "天穹既启，万物咸新"
    阳 输出 问候
'''


def 令传火(名目: str) -> int:
    import os
    径 = f"{名目}.天穹"
    if os.path.exists(径):
        print(f"天穹警示：\n  传火未成\n  「{径}」已存于世，不可覆之", file=sys.stderr)
        return 1
    with open(径, "w", encoding="utf-8") as 卷:
        卷.write(脚手架.format(名目=名目))
    print(f"天穹提示：\n  传火已竟\n  「{径}」已立，可以「天穹 运行 {径}」启之")
    return 0


def 令铸器(名目: str = "天穹") -> int:
    """铸天穹解释器本体为独行之器（PyInstaller 单文件 exe）。

    所得之器即完整 CLI：器 运行 卷.天穹 / 问道 / 观天 / 窥豹 / 传火 / 版本。
    """
    import os
    import shutil
    import subprocess
    import tempfile

    if shutil.which("pyinstaller") is None:
        try:
            import PyInstaller  # noqa: F401
        except ImportError:
            print("天穹运行错误：\n昆仑无此卷\n  铸器之具「PyInstaller」未具，请先备之（pip install pyinstaller）", file=sys.stderr)
            return 1

    工棚 = tempfile.mkdtemp(prefix="天穹铸器_")
    try:
        引导 = os.path.join(工棚, f"{名目}_引导.py")
        with open(引导, "w", encoding="utf-8") as 卷:
            卷.write(
                '# -*- coding: utf-8 -*-\n'
                '"""天穹独行之器之引导。"""\n'
                'from tianqiong.cli import 主函数\n'
                '主函数()\n'
            )
        # 寻得 tianqiong 包之源头，随器俱铸（绿色免装之要义）
        import tianqiong
        包源 = os.path.dirname(os.path.dirname(os.path.abspath(tianqiong.__file__)))
        令 = [
            sys.executable, "-m", "PyInstaller",
            "--onefile", "--name", 名目,
            "--paths", 包源,
            "--hidden-import", "tianqiong",
            "--hidden-import", "tianqiong.kunlun.you",
            "--hidden-import", "tianqiong.kunlun.xingchen",
            "--hidden-import", "tianqiong.kunlun.xuanwu",
            "--hidden-import", "tianqiong.kunlun.sixiang",
            "--distpath", os.getcwd(),
            "--workpath", os.path.join(工棚, "工"),
            "--specpath", 工棚,
            引导,
        ]
        print(f"天穹提示：\n  铸器之初\n  正铸天穹解释器为「{名目}」，请少待……")
        果 = subprocess.run(令, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if 果.returncode != 0:
            print("天穹运行错误：\n铸器未成\n  有司报曰：", file=sys.stderr)
            print(果.stdout[-2000:], file=sys.stderr)
            print(果.stderr[-2000:], file=sys.stderr)
            return 1
        器名 = 名目 + (".exe" if os.name == "nt" else "")
        print(f"天穹提示：\n  铸器已竟\n  「{器名}」已出世，置之 PATH，则「{名目} 运行 卷.天穹」随处可用")
        return 0
    finally:
        shutil.rmtree(工棚, ignore_errors=True)


def 令问道() -> int:
    print(f"天穹问道 · 版本 {__版本__}")
    print("书「归墟」以退，书「观 <名>」以察一物之真身")
    天地 = 筑天地()
    安装钩子("<问道>")
    块首 = ("造化", "若", "遍历", "周而复始", "盘古")
    while True:
        try:
            行 = input("问道> ")
        except (EOFError, KeyboardInterrupt):
            print("\n问道已竟，山水有相逢。")
            return 0
        行 = 行.rstrip()
        if not 行.strip():
            continue
        if 行.strip() == "归墟":
            print("问道已竟，山水有相逢。")
            return 0
        # 观 <名> —— 内省一物之真身（揭底）
        if 行.startswith("观 "):
            名 = 行[2:].strip()
            try:
                物 = eval(名, 天地)
            except Exception:
                类, 异常, 溯源 = sys.exc_info()
                sys.excepthook(类, 异常, 溯源)
                continue
            print(f"  其名：{名}")
            print(f"  其行：{type(物).__name__}")
            真身 = getattr(物, "__module__", None)
            本体 = getattr(物, "__name__", None)
            if 真身 or 本体:
                print(f"  真身：{真身 or '?'}.{本体 or '?'}")
            else:
                print(f"  真身：{物!r}")
            continue
        # 块结构之句：续行以纳其体，空行乃竟
        首词 = 行.strip().split()[0] if 行.strip() else ""
        if 首词 in 块首:
            行们 = [行]
            while True:
                try:
                    续 = input("  … ")
                except (EOFError, KeyboardInterrupt):
                    续 = ""
                if not 续.strip():
                    break
                行们.append(续)
            行 = "\n".join(行们)
        # 问道之境宽容些：裸「输出 某某」视同「阳 输出 某某」
        首词 = 行.strip().split()[0] if 行.strip() else ""
        if 首词 not in ("阳", "阴", "混沌", "盘古", "造化", "若", "遍历", "周而复始", "归一"):
            行 = "阳 " + 行
        try:
            树 = 语法分析(行 + "\n")
            exec(compile(树, "<问道>", "exec"), 天地)
        except (词法错误, 语法错误) as 误:
            print(报编译误("<问道>", 误.行, 误.缘由), file=sys.stderr)
        except Exception:
            类, 异常, 溯源 = sys.exc_info()
            sys.excepthook(类, 异常, 溯源)


def 主函数() -> None:
    参 = sys.argv[1:]
    if not 参 or 参[0] in ("-h", "--help", "助", "帮助"):
        print(用法)
        sys.exit(0)
    令, 余 = 参[0], 参[1:]
    if 令 == "运行":
        if not 余:
            print("天穹提示：「运行」之后当书卷名", file=sys.stderr)
            sys.exit(2)
        sys.exit(令运行(余[0]))
    if 令 == "观天":
        if not 余:
            print("天穹提示：「观天」之后当书卷名", file=sys.stderr)
            sys.exit(2)
        sys.exit(令观天(余[0]))
    if 令 == "窥豹":
        if not 余:
            print("天穹提示：「窥豹」之后当书卷名", file=sys.stderr)
            sys.exit(2)
        sys.exit(令窥豹(余[0]))
    if 令 == "传火":
        sys.exit(令传火(余[0] if 余 else "新篇"))
    if 令 == "铸器":
        sys.exit(令铸器(余[0] if 余 else "天穹"))
    if 令 == "问道":
        sys.exit(令问道())
    if 令 == "版本":
        print(f"天穹 版本 {__版本__}")
        sys.exit(0)
    # 直接书卷名，视同「运行」
    if 令.endswith(".天穹"):
        sys.exit(令运行(令))
    print(f"天穹提示：\n  未闻此令「{令}」\n  可书「天穹 帮助」以观诸令", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    主函数()
