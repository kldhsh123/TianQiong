"""M1 开天 · 验收测试。"""

from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout, redirect_stderr

from tianqiong.cifa import 词法分析, 词法错误, 令牌类
from tianqiong.yufa import 语法分析, 语法错误
from tianqiong.tian_di import 筑天地
from tianqiong.baocuo import 报编译误, 化公文


def 运行源码(源码: str) -> str:
    """跑一段天穹源码，收其输出。"""
    树 = 语法分析(源码)
    码 = compile(树, "<试>", "exec")
    天地 = 筑天地()
    缓冲 = io.StringIO()
    with redirect_stdout(缓冲):
        exec(码, 天地)
    return 缓冲.getvalue()


class 词法之试(unittest.TestCase):
    def test_令牌流有序(self):
        流 = 词法分析('混沌 试\n盘古 启动\n    阴 甲 为 1\n')
        类序 = [令.类 for 令 in 流]
        self.assertIn(令牌类.缩进, 类序)
        self.assertIn(令牌类.退格, 类序)
        self.assertEqual(流[-1].值, "终止")

    def test_批注剔除(self):
        流 = 词法分析('阴 甲 为 1 【注】此言不足观\n')
        值序 = [令.值 for 令 in 流]
        self.assertNotIn("【注】", 值序)
        self.assertIn(1, 值序)

    def test_引号内批注不剔(self):
        流 = 词法分析('阴 甲 为 "批曰：非注也"\n')
        字们 = [令.值 for 令 in 流 if 令.类 is 令牌类.字]
        self.assertEqual(字们, ["批曰：非注也"])

    def test_缩进不齐则误(self):
        with self.assertRaises(词法错误):
            词法分析('盘古 启动\n    阴 甲 为 1\n  阴 乙 为 2\n')


class 语法之试(unittest.TestCase):
    def test_混沌化注记(self):
        树 = 语法分析("混沌 试\n")
        import ast
        self.assertIsInstance(树.body[0], ast.Assign)
        self.assertEqual(树.body[0].targets[0].id, "__混沌__")

    def test_盘古化主判(self):
        import ast
        树 = 语法分析("盘古 启动\n    阳 输出 1\n")
        self.assertIsInstance(树.body[0], ast.If)

    def test_章法有误则报(self):
        with self.assertRaises(语法错误):
            语法分析("盘古\n")


class 运行之试(unittest.TestCase):
    def test_你好天穹(self):
        出 = 运行源码('混沌 试\n盘古 启动\n    阴 名称 为 "天穹"\n    阳 输出 名称\n')
        self.assertEqual(出.strip(), "天穹")

    def test_存于获值(self):
        出 = 运行源码('盘古 启动\n    阳 长度 "天穹" 存于 长\n    阳 输出 长\n')
        self.assertEqual(出.strip(), "2")

    def test_入口之外亦可行(self):
        # 混沌注记与入口之外，顶层之句照常行
        出 = 运行源码('阳 输出 "顶层"\n')
        self.assertEqual(出.strip(), "顶层")


class 数术之试(unittest.TestCase):
    def test_四则与优先级(self):
        出 = 运行源码('盘古 启动\n    阴 甲 为 7 乘 6 加 1\n    阳 输出 甲\n')
        self.assertEqual(出.strip(), "43")

    def test_括号易序(self):
        出 = 运行源码('盘古 启动\n    阴 乙 为 (7 加 3) 除以 2\n    阳 输出 乙\n')
        self.assertEqual(出.strip(), "5.0")

    def test_幂与余(self):
        出 = 运行源码('盘古 启动\n    阳 输出 2 幂 10\n    阳 输出 17 余 5\n')
        self.assertEqual(出.split(), ["1024", "2"])

    def test_字串相加(self):
        出 = 运行源码('盘古 启动\n    阳 输出 "天" 加 "穹"\n')
        self.assertEqual(出.strip(), "天穹")

    def test_比较与真伪(self):
        出 = 运行源码('盘古 启动\n    阳 输出 3 大于 2\n    阳 输出 1 等于 2\n')
        self.assertEqual(出.split(), ["True", "False"])

    def test_且或非(self):
        出 = 运行源码('盘古 启动\n    阳 输出 太极 且 非 太极\n    阳 输出 太极 或 非 太极\n')
        self.assertEqual(出.split(), ["False", "True"])

    def test_管道(self):
        出 = 运行源码('盘古 启动\n    阴 长 为 "天穹" | 长度\n    阳 输出 长\n')
        self.assertEqual(出.strip(), "2")

    def test_管道带参(self):
        出 = 运行源码('盘古 启动\n    阳 输出 5 | 至大 3\n')
        self.assertEqual(出.strip(), "5")

    def test_表达式为参数(self):
        出 = 运行源码('盘古 启动\n    阳 输出 1 加 2 乘 3\n')
        self.assertEqual(出.strip(), "7")

    def test_逗号分隔参(self):
        出 = 运行源码('盘古 启动\n    阳 输出 至大(3, 9)\n')
        self.assertEqual(出.strip(), "9")

    def test_之取属性(self):
        出 = 运行源码('盘古 启动\n    阳 输出 "天穹" 之 upper()\n')
        self.assertEqual(出.strip(), "天穹")


class 牖户之试(unittest.TestCase):
    def test_库可引(self):
        from tianqiong.kunlun import you as 牖库
        for 名 in ("立牖", "匾额", "按钮", "书栏", "览栏", "书文",
                   "取文", "布画", "画线", "守牖"):
            self.assertTrue(callable(getattr(牖库, 名)))


class 律令之试(unittest.TestCase):
    def test_若与否则(self):
        出 = 运行源码(
            '盘古 启动\n'
            '    阴 甲 为 5\n'
            '    若 甲 大于 3\n'
            '        阳 输出 "大"\n'
            '    否则\n'
            '        阳 输出 "小"\n')
        self.assertEqual(出.strip(), "大")

    def test_遍历范围(self):
        出 = 运行源码(
            '盘古 启动\n'
            '    遍历 甲 于 范围(0, 3)\n'
            '        阳 输出 甲\n')
        self.assertEqual(出.split(), ["0", "1", "2"])

    def test_造化递归(self):
        出 = 运行源码(
            '盘古 启动\n'
            '    造化 菲波 以 数\n'
            '        若 数 小于 2\n'
            '            归一 数\n'
            '        否则\n'
            '            归一 菲波(数 减 1) 加 菲波(数 减 2)\n'
            '    阳 菲波 10 存于 果\n'
            '    阳 输出 果\n')
        self.assertEqual(出.strip(), "55")

    def test_周而复始(self):
        出 = 运行源码(
            '盘古 启动\n'
            '    阴 筹 为 0\n'
            '    周而复始 筹 小于 3\n'
            '        阳 输出 筹\n'
            '        阴 筹 为 筹 加 1\n')
        self.assertEqual(出.split(), ["0", "1", "2"])

    def test_归一无值(self):
        出 = 运行源码(
            '盘古 启动\n'
            '    造化 寒暄 以\n'
            '        阳 输出 "寒暄"\n'
            '        归一\n'
            '    阳 寒暄\n')
        self.assertEqual(出.strip(), "寒暄")


class 星辰之试(unittest.TestCase):
    def test_同耀并行(self):
        出 = 运行源码(
            '盘古 启动\n'
            '    造化 星职 以 名\n'
            '        阳 输出 名\n'
            '    阳 同耀 星职 "甲" 存于 甲星\n'
            '    阳 同耀 星职 "乙" 存于 乙星\n'
            '    阳 待星 甲星\n'
            '    阳 待星 乙星\n'
            '    阳 输出 "归位"\n')
        行们 = 出.split()
        self.assertEqual(行们[-1], "归位")
        self.assertCountEqual(行们[:-1], ["甲", "乙"])

    def test_锁可用(self):
        from tianqiong.kunlun import xingchen as 星辰库
        锁 = 星辰库.立锁()
        星辰库.持锁(锁)
        星辰库.释锁(锁)


class 玄武之试(unittest.TestCase):
    def test_铸印验印(self):
        出 = 运行源码(
            '盘古 启动\n'
            '    阳 铸印 "天穹" 存于 印\n'
            '    阳 验印 "天穹" 印 存于 真\n'
            '    阳 输出 真\n'
            '    阳 验印 "伪文" 印 存于 伪\n'
            '    阳 输出 伪\n')
        self.assertEqual(出.split(), ["True", "False"])

    def test_密押验押(self):
        出 = 运行源码(
            '盘古 启动\n'
            '    阳 密押 "文" "钥" 存于 押\n'
            '    阳 验押 "文" "钥" 押 存于 真\n'
            '    阳 输出 真\n')
        self.assertEqual(出.strip(), "True")

    def test_灵符天衍(self):
        from tianqiong.kunlun import xuanwu as 玄武库
        符 = 玄武库.灵符(8)
        self.assertEqual(len(符), 16)
        数 = 玄武库.天衍(1, 100)
        self.assertTrue(1 <= 数 <= 100)


class 四象之试(unittest.TestCase):
    def test_立定观化(self):
        出 = 运行源码(
            '盘古 启动\n'
            '    阳 立四象 存于 象\n'
            '    阳 定象 象 "名" "天穹"\n'
            '    阳 观象 象 "名" 存于 名\n'
            '    阳 输出 名\n')
        self.assertEqual(出.strip(), "天穹")

    def test_化解往返(self):
        出 = 运行源码(
            '盘古 启动\n'
            '    阳 立四象 存于 象\n'
            '    阳 定象 象 "数" 42\n'
            '    阳 化四象 象 存于 文\n'
            '    阳 解四象 文 存于 新\n'
            '    阳 观象 新 "数" 存于 数\n'
            '    阳 输出 数\n')
        self.assertEqual(出.strip(), "42")


class 公文之试(unittest.TestCase):
    def test_编译误公文(self):
        文 = 报编译误("试.天穹", 5, "未闻此句法")
        self.assertIn("天穹编译错误", 文)
        self.assertIn("第 5 行", 文)

    def test_语义未定义公文(self):
        try:
            运行源码('盘古 启动\n    阳 输出 乌有\n')
        except NameError as 误:
            文 = 化公文(误, "试.天穹")
            self.assertIn("语义未定义", 文)
            self.assertIn("「乌有」", 文)
        else:
            self.fail("当掷 NameError")


if __name__ == "__main__":
    unittest.main()
