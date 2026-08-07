"""语法：化令牌之流为 Python 抽象语法树。

章法总览（M2 数值之窗）：
  混沌 <名称>                       —— 程序宣言
  盘古 启动                         —— 入口块
  阴 <名> 为 <式>                   —— 声明
  阳 <名> [式…] [存于 <名>]          —— 执行（参数可逗号分隔）
  式                                —— 运算表达式

数术（中缀，由疏而密）：
  或 | 且 | 非 | 比较 | 加 减 | 乘 除以 整除 余 | 幂 | 一元 | 管道

管道：
  <值> | <名> [参数…]   —— 以左值为先参，行右名之事
"""

from __future__ import annotations

import ast

from .cifa import 令牌, 令牌类, 词法分析


class 语法错误(Exception):
    def __init__(self, 行: int, 缘由: str):
        self.行 = 行
        self.缘由 = 缘由
        super().__init__(f"第 {行} 行：{缘由}")


# 中缀算符 → ast 节点
比较表 = {
    "等于": ast.Eq, "==": ast.Eq,
    "大于": ast.Gt, ">": ast.Gt,
    "小于": ast.Lt, "<": ast.Lt,
}
加法表 = {"加": ast.Add, "+": ast.Add, "减": ast.Sub, "-": ast.Sub}
乘法表 = {
    "乘": ast.Mult, "*": ast.Mult,
    "除以": ast.Div, "/": ast.Div,
    "整除": ast.FloorDiv,
    "余": ast.Mod, "%": ast.Mod,
}


class 语法分析器:
    def __init__(self, 流: list[令牌]):
        self.流 = 流
        self.位 = 0

    # ---- 基本动作 ----
    def 窥(self, 移: int = 0) -> 令牌:
        位 = min(self.位 + 移, len(self.流) - 1)
        return self.流[位]

    def 进(self) -> 令牌:
        令 = self.流[self.位]
        if self.位 < len(self.流) - 1:
            self.位 += 1
        return 令

    def 是(self, 类: 令牌类, 值: object = None) -> bool:
        令 = self.窥()
        if 令.类 is not 类:
            return False
        return 值 is None or 令.值 == 值

    def 是号(self, *值们: str) -> bool:
        令 = self.窥()
        return 令.类 is 令牌类.号 and 令.值 in 值们

    def 是名(self, *值们: str) -> bool:
        令 = self.窥()
        return 令.类 is 令牌类.名 and 令.值 in 值们

    def 取(self, 类: 令牌类, 值: object = None, 缘由: str = "章法有误") -> 令牌:
        if not self.是(类, 值):
            令 = self.窥()
            raise 语法错误(令.行, 缘由)
        return self.进()

    def 吞换行(self) -> None:
        self.取(令牌类.换行, 缘由="句读未竟，章法有误")

    @staticmethod
    def _定位(节点: ast.AST, 令: 令牌) -> ast.AST:
        节点.lineno = 令.行
        节点.col_offset = 0
        节点.end_lineno = 令.行
        节点.end_col_offset = 0
        return 节点

    # ---- 顶层 ----
    def 析模块(self) -> ast.Module:
        句们: list[ast.stmt] = []
        while True:
            if self.是(令牌类.止, "终止"):
                break
            if self.是(令牌类.换行):
                self.进()
                continue
            句们.append(self.析顶层句())
        return ast.Module(body=句们 or [ast.Pass()], type_ignores=[])

    def 析顶层句(self) -> ast.stmt:
        if self.是名("混沌"):
            return self.析混沌()
        if self.是名("盘古"):
            return self.析盘古()
        return self.析句()

    def 析混沌(self) -> ast.stmt:
        首 = self.进()  # 混沌
        名令 = self.取(令牌类.名, 缘由="「混沌」之后当立项目之名")
        self.吞换行()
        return self._定位(ast.Assign(
            targets=[ast.Name(id="__混沌__", ctx=ast.Store())],
            value=ast.Constant(value=str(名令.值)),
        ), 首)

    def 析盘古(self) -> ast.stmt:
        首 = self.进()  # 盘古
        self.取(令牌类.名, "启动", 缘由="「盘古」之后当书「启动」")
        self.吞换行()
        体 = self.析块()
        判 = ast.Compare(
            left=ast.Name(id="__name__", ctx=ast.Load()),
            ops=[ast.Eq()],
            comparators=[ast.Constant(value="__main__")],
        )
        return self._定位(ast.If(test=判, body=体 or [ast.Pass()], orelse=[]), 首)

    def 析块(self) -> list[ast.stmt]:
        令 = self.窥()
        if 令.类 is not 令牌类.缩进:
            raise 语法错误(令.行, "此处当起缩进之块（乾坤未开）")
        self.进()
        句们: list[ast.stmt] = []
        while True:
            if self.是(令牌类.退格) or self.是(令牌类.止, "终止"):
                if self.是(令牌类.退格):
                    self.进()
                break
            if self.是(令牌类.换行):
                self.进()
                continue
            句们.append(self.析句())
        return 句们

    # ---- 语句 ----
    def 析句(self) -> ast.stmt:
        令 = self.窥()
        if self.是名("阴"):
            return self.析阴()
        if self.是名("阳"):
            return self.析阳()
        if self.是名("若"):
            return self.析若()
        if self.是名("遍历"):
            return self.析遍历()
        if self.是名("周而复始"):
            return self.析周而复始()
        if self.是名("造化"):
            return self.析造化()
        if self.是名("归一"):
            return self.析归一()
        if self.是名("盘古"):
            return self.析盘古()
        raise 语法错误(令.行, f"未闻此句法，起首之「{令.值}」不合章法")

    def 析若(self) -> ast.stmt:
        首 = self.进()  # 若
        判 = self.析式()
        self.吞换行()
        体 = self.析块()
        余: list[ast.stmt] = []
        if self.是名("否则"):
            self.进()
            self.吞换行()
            余 = self.析块()
        return self._定位(ast.If(test=判, body=体 or [ast.Pass()], orelse=余), 首)

    def 析遍历(self) -> ast.stmt:
        首 = self.进()  # 遍历
        名令 = self.取(令牌类.名, 缘由="「遍历」之后当立名")
        self.取(令牌类.名, "于", 缘由="遍历当书「于」：遍历 某 于 某列")
        列 = self.析式()
        self.吞换行()
        体 = self.析块()
        return self._定位(ast.For(
            target=self._定位(ast.Name(id=str(名令.值), ctx=ast.Store()), 名令),
            iter=列, body=体 or [ast.Pass()], orelse=[],
        ), 首)

    def 析周而复始(self) -> ast.stmt:
        首 = self.进()  # 周而复始
        判 = self.析式()
        self.吞换行()
        体 = self.析块()
        return self._定位(ast.While(test=判, body=体 or [ast.Pass()], orelse=[]), 首)

    def 析造化(self) -> ast.stmt:
        首 = self.进()  # 造化
        名令 = self.取(令牌类.名, 缘由="「造化」之后当立法名")
        参名们: list[str] = []
        if self.是名("以"):
            self.进()
            while self.窥().类 is 令牌类.名 and not self.是名("为", "于"):
                参名们.append(str(self.进().值))
        self.吞换行()
        体 = self.析块()
        return self._定位(ast.FunctionDef(
            name=str(名令.值),
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg=名) for 名 in 参名们],
                kwonlyargs=[], kw_defaults=[], defaults=[],
            ),
            body=体 or [ast.Pass()],
            decorator_list=[],
        ), 首)

    def 析归一(self) -> ast.stmt:
        首 = self.进()  # 归一
        if self.是(令牌类.换行):
            self.吞换行()
            return self._定位(ast.Return(value=None), 首)
        值 = self.析式()
        self.吞换行()
        return self._定位(ast.Return(value=值), 首)

    def 析阴(self) -> ast.stmt:
        首 = self.进()  # 阴
        名令 = self.取(令牌类.名, 缘由="「阴」之后当立名")
        self.取(令牌类.名, "为", 缘由="声明当书「为」")
        值 = self.析式()
        self.吞换行()
        return self._定位(ast.Assign(
            targets=[ast.Name(id=str(名令.值), ctx=ast.Store())],
            value=值,
        ), 首)

    def 析阳(self) -> ast.stmt:
        首 = self.进()  # 阳
        名令 = self.取(令牌类.名, 缘由="「阳」之后当书所行之事")
        参们 = self._析裸调用列()
        存名: str | None = None
        if self.是名("存于"):
            self.进()
            存令 = self.取(令牌类.名, 缘由="「存于」之后当立名")
            存名 = str(存令.值)
        self.吞换行()
        调 = self._定位(ast.Call(
            func=self._定位(ast.Name(id=str(名令.值), ctx=ast.Load()), 名令),
            args=参们, keywords=[],
        ), 首)
        if 存名 is not None:
            return self._定位(ast.Assign(
                targets=[ast.Name(id=存名, ctx=ast.Store())],
                value=调,
            ), 首)
        return self._定位(ast.Expr(value=调), 首)

    def _析裸调用列(self) -> list[ast.expr]:
        """析「阳」之后的参数串：名 若直随 字/数 且同行，视同调用（菲波 10）。"""
        参们: list[ast.expr] = []
        while True:
            if self.是(令牌类.换行) or self.是(令牌类.止, "终止"):
                break
            if self.是号(")", "|"):
                break
            if self.是名("存于"):
                break
            if self.是号(","):
                self.进()
                continue
            首 = self.窥()
            元 = self.析式()
            后 = self.窥()
            # 唯首令牌为字/数且式恰为裸名，方许裸调粘连（匾额 牖 则否）
            if isinstance(元, ast.Name) and 首.类 in (令牌类.字, 令牌类.数) \
                    and 后.行 == 元.lineno \
                    and 后.类 in (令牌类.字, 令牌类.数, 令牌类.名) \
                    and not (后.类 is 令牌类.名 and 后.值 in (
                        "加", "减", "乘", "除以", "整除", "余", "幂",
                        "且", "或", "大于", "小于", "等于", "存于", "于", "之")):
                余参 = self._析裸调用列()
                元 = self._定位(ast.Call(func=元, args=余参, keywords=[]), 后)
            参们.append(元)
        return 参们

    def _析参列(self, 允许裸调: bool = False) -> list[ast.expr]:
        """析一串以逗号或空白相隔之式，止于换行/「存于」/闭括/管道。"""
        参们: list[ast.expr] = []
        while True:
            if self.是(令牌类.换行) or self.是(令牌类.止, "终止"):
                break
            if self.是号(")", "|"):
                break
            if self.是名("存于"):
                break
            if self.是号(","):
                self.进()
                continue
            参们.append(self._析参(允许裸调))
        return 参们

    def _析参(self, 允许裸调: bool) -> ast.expr:
        """析一参。允许裸调时，若其式恰好是一裸名，则后随字/数皆为其参（菲波 10）。"""
        元 = self.析式()
        后 = self.窥()
        if 允许裸调 and isinstance(元, ast.Name) and 后.行 == 元.lineno \
                and 后.类 in (令牌类.字, 令牌类.数):
            余参 = self._析参列(允许裸调=True)
            return self._定位(ast.Call(func=元, args=余参, keywords=[]), 后)
        return 元

    # ---- 表达式（由疏而密） ----
    def 析式(self) -> ast.expr:
        return self.析管道()

    def 析管道(self) -> ast.expr:
        左 = self.析或()
        while self.是号("|"):
            令 = self.进()
            名令 = self.取(令牌类.名, 缘由="「|」之后当书所行之事")
            余参 = self._析参列()
            左 = self._定位(ast.Call(
                func=self._定位(ast.Name(id=str(名令.值), ctx=ast.Load()), 名令),
                args=[左] + 余参, keywords=[],
            ), 令)
        return 左

    def 析或(self) -> ast.expr:
        左 = self.析且()
        while self.是名("或"):
            令 = self.进()
            右 = self.析且()
            左 = self._定位(ast.BoolOp(op=ast.Or(), values=[左, 右]), 令)
        return 左

    def 析且(self) -> ast.expr:
        左 = self.析非()
        while self.是名("且"):
            令 = self.进()
            右 = self.析非()
            左 = self._定位(ast.BoolOp(op=ast.And(), values=[左, 右]), 令)
        return 左

    def 析非(self) -> ast.expr:
        if self.是名("非"):
            令 = self.进()
            return self._定位(ast.UnaryOp(op=ast.Not(), operand=self.析非()), 令)
        return self.析比较()

    def 析比较(self) -> ast.expr:
        左 = self.析加減()
        令 = self.窥()
        键 = 令.值 if 令.类 in (令牌类.名, 令牌类.号) else None
        if 键 in 比较表:
            self.进()
            右 = self.析加減()
            return self._定位(ast.Compare(
                left=左, ops=[比较表[键]()], comparators=[右],
            ), 令)
        return 左

    def 析加減(self) -> ast.expr:
        左 = self.析乘除()
        while True:
            令 = self.窥()
            键 = 令.值 if 令.类 in (令牌类.名, 令牌类.号) else None
            if 键 not in 加法表:
                return 左
            self.进()
            右 = self.析乘除()
            左 = self._定位(ast.BinOp(left=左, op=加法表[键](), right=右), 令)

    def 析乘除(self) -> ast.expr:
        左 = self.析幂()
        while True:
            令 = self.窥()
            键 = 令.值 if 令.类 in (令牌类.名, 令牌类.号) else None
            if 键 not in 乘法表:
                return 左
            self.进()
            右 = self.析幂()
            左 = self._定位(ast.BinOp(left=左, op=乘法表[键](), right=右), 令)

    def 析幂(self) -> ast.expr:
        基 = self.析一元()
        if self.是名("幂"):
            令 = self.进()
            指 = self.析幂()  # 右结合
            return self._定位(ast.BinOp(left=基, op=ast.Pow(), right=指), 令)
        return 基

    def 析一元(self) -> ast.expr:
        if self.是号("-"):
            令 = self.进()
            return self._定位(ast.UnaryOp(op=ast.USub(), operand=self.析一元()), 令)
        if self.是号("+"):
            令 = self.进()
            return self._定位(ast.UnaryOp(op=ast.UAdd(), operand=self.析一元()), 令)
        return self.析后缀()

    def 析后缀(self) -> ast.expr:
        元 = self.析元()
        while True:
            if self.是名("之"):
                令 = self.进()
                名令 = self.窥()
                if 名令.类 is 令牌类.名:
                    self.进()
                    元 = self._定位(ast.Attribute(
                        value=元, attr=str(名令.值), ctx=ast.Load(),
                    ), 令)
                    continue
                # 之 <式> → 取项
                索 = self.析元()
                元 = self._定位(ast.Subscript(
                    value=元, slice=索, ctx=ast.Load(),
                ), 令)
                continue
            if self.是号("("):
                令 = self.进()
                参们 = self._析参列()
                self.取(令牌类.号, ")", 缘由="括号未合，章法有误")
                元 = self._定位(ast.Call(func=元, args=参们, keywords=[]), 令)
                continue
            return 元

    def 析元(self) -> ast.expr:
        令 = self.窥()
        if 令.类 is 令牌类.字:
            self.进()
            return self._定位(ast.Constant(value=令.值), 令)
        if 令.类 is 令牌类.数:
            self.进()
            return self._定位(ast.Constant(value=令.值), 令)
        if 令.类 is 令牌类.名:
            self.进()
            if 令.值 == "太极":
                return self._定位(ast.Constant(value=True), 令)
            if 令.值 == "太初":
                return self._定位(ast.Constant(value=None), 令)
            return self._定位(ast.Name(id=str(令.值), ctx=ast.Load()), 令)
        if 令.类 is 令牌类.号 and 令.值 == "(":
            self.进()
            式 = self.析式()
            self.取(令牌类.号, ")", 缘由="括号未合，章法有误")
            return 式
        显 = 令.值 if 令.值 is not None else 令.类.name
        raise 语法错误(令.行, f"此处当为值（字、数或名），而遇「{显}」")


def 语法分析(源码: str) -> ast.Module:
    """源码 → Python AST（已 fix_missing_locations）。"""
    流 = 词法分析(源码)
    树 = 语法分析器(流).析模块()
    return ast.fix_missing_locations(树)
