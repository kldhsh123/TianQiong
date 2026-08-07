"""词法：化天穹源码为字符之流（token 流）。

文法大意：
  混沌 <名称>            —— 程序宣言
  盘古 启动              —— 入口，其后缩进块为正文
  阴 <名> 为 <值>        —— 声明绑定
  阳 <名> [参数…] [存于 <名>]   —— 执行调用
  【注】…… / 批曰：……  —— 批注
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class 令牌类(Enum):
    名 = auto()
    字 = auto()
    数 = auto()
    号 = auto()   # 符号：括号、逗号、算符、管道
    换行 = auto()
    缩进 = auto()
    退格 = auto()
    止 = auto()


# 语法关键字：词法阶段原样放行，由语法阶段裁决
关键字 = {
    "混沌", "盘古", "启动", "阴", "阳", "为", "存于",
    "乾坤", "天地", "四象", "五行", "星辰", "同耀", "昆仑", "玄武",
    "若", "否则", "遍历", "于", "周而复始", "造化", "以", "归一", "观",
    "太极", "太初",  # 预留：真 / 空
    "加", "减", "乘", "除以", "整除", "余", "幂",  # 数术（中缀算符）
    "之",  # 属性/取项：图 之 宽度、典 之 "键"
}

注释记号 = ("【注】", "批曰：")

# 符号（含全角变体）：算符、括弧、句读
符号表 = {
    "（": "(", "）": ")", "，": ",", "＝": "=",
    "＋": "+", "－": "-", "×": "*", "÷": "/",
    "＞": ">", "＜": "<", "｜": "|", "：": ":",
}
符号集 = set("()+-*/%|,:=") | set(符号表.keys())


@dataclass
class 令牌:
    类: 令牌类
    值: object
    行: int

    def __repr__(self) -> str:  # 便于调试
        return f"令牌({self.类.name}, {self.值!r}, 行={self.行})"


class 词法错误(Exception):
    """章法层面的基础错误（如括号未配对）。"""

    def __init__(self, 行: int, 缘由: str):
        self.行 = 行
        self.缘由 = 缘由
        super().__init__(f"第 {行} 行：{缘由}")


def _去注释(行文: str) -> str:
    """剔除行内批注；引号内的批注记号不算数。"""
    于引号中 = False
    引号 = ""
    位置 = 0
    while 位置 < len(行文):
        字 = 行文[位置]
        if 于引号中:
            if 字 == "\\":
                位置 += 2
                continue
            if 字 == 引号:
                于引号中 = False
        elif 字 in ('"', "'"):
            于引号中 = True
            引号 = 字
        else:
            for 记号 in 注释记号:
                if 行文.startswith(记号, 位置):
                    return 行文[:位置]
        位置 += 1
    return 行文


def _析词(行文: str, 行号: int) -> list[令牌]:
    """把一行正文拆成令牌。空白为界，引号成字，符号自立。"""
    流: list[令牌] = []
    位置 = 0
    长度 = len(行文)
    while 位置 < 长度:
        字 = 行文[位置]
        if 字.isspace():
            位置 += 1
            continue
        if 字 in ('"', "'"):
            终点 = 位置 + 1
            片段 = []
            while 终点 < 长度:
                if 行文[终点] == "\\" and 终点 + 1 < 长度:
                    片段.append(行文[终点:终点 + 2])
                    终点 += 2
                    continue
                if 行文[终点] == 字:
                    break
                片段.append(行文[终点])
                终点 += 1
            if 终点 >= 长度:
                raise 词法错误(行号, "引号未合，章法有误")
            原文 = "".join(片段)
            # 交由 ast.literal_eval 解读转义
            import ast as _ast
            try:
                值 = _ast.literal_eval(字 + 原文 + 字)
            except Exception:
                raise 词法错误(行号, f"字串「{原文}」不合章法")
            流.append(令牌(令牌类.字, 值, 行号))
            位置 = 终点 + 1
            continue
        if 字 == "「":
            终点 = 行文.find("」", 位置 + 1)
            if 终点 == -1:
                raise 词法错误(行号, "「」未合，章法有误")
            流.append(令牌(令牌类.字, 行文[位置 + 1:终点], 行号))
            位置 = 终点 + 1
            continue
        if 字 in 符号集:
            流.append(令牌(令牌类.号, 符号表.get(字, 字), 行号))
            位置 += 1
            continue
        # 连续非空白非符号即一词
        终点 = 位置
        while 终点 < 长度 and not 行文[终点].isspace() and 行文[终点] not in 符号集:
            终点 += 1
        词 = 行文[位置:终点]
        位置 = 终点
        try:
            流.append(令牌(令牌类.数, int(词), 行号))
            continue
        except ValueError:
            pass
        try:
            流.append(令牌(令牌类.数, float(词), 行号))
            continue
        except ValueError:
            pass
        流.append(令牌(令牌类.名, 词, 行号))
    return 流


def 词法分析(源码: str) -> list[令牌]:
    """主入口：源码 → 令牌流（含缩进/退格/换行/止）。"""
    流: list[令牌] = []
    缩进栈 = [0]
    行们 = 源码.splitlines()
    for 序号, 原文 in enumerate(行们, 1):
        行号 = 序号
        无注 = _去注释(原文)
        if not 无注.strip():
            continue
        # 计算缩进（tab 视同四空格）
        展开 = 无注.expandtabs(4)
        缩进 = len(展开) - len(展开.lstrip(" "))
        正文 = 展开.strip()
        if 缩进 > 缩进栈[-1]:
            缩进栈.append(缩进)
            流.append(令牌(令牌类.缩进, 缩进, 行号))
        else:
            while 缩进 < 缩进栈[-1]:
                缩进栈.pop()
                流.append(令牌(令牌类.退格, "退格", 行号))
            if 缩进 != 缩进栈[-1]:
                raise 词法错误(行号, "缩进不齐，章法有误")
        流.extend(_析词(正文, 行号))
        流.append(令牌(令牌类.换行, None, 行号))
    while len(缩进栈) > 1:
        缩进栈.pop()
        末行 = len(行们) or 1
        流.append(令牌(令牌类.退格, "退格", 末行))
    流.append(令牌(令牌类.止, "终止", len(行们) or 1))
    return 流
