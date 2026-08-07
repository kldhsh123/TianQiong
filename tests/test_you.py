"""牖户之试：以虚拟显示器起真窗，验昆仑·牖之行。

直行此卷（python tests/test_you.py）而无显示器时，二试皆跳过，
是常态，非过失。Windows 桌面直行则真窗自起。
"""

import os
import unittest


@unittest.skipUnless(os.environ.get("DISPLAY"), "无显示器，牖不可立")
class 牖户实测(unittest.TestCase):
    def test_立牖布件(self):
        from tianqiong.kunlun import you as 牖库

        牖 = 牖库.立牖("试验之窗", 320, 240)
        牖库.匾额(牖, "试验")
        栏 = 牖库.书栏(牖)
        览 = 牖库.览栏(牖)
        牖库.书文(栏, "栏中之文")
        牖库.书文(览, "览中之文")
        self.assertEqual(牖库.取文(栏), "栏中之文")
        self.assertEqual(牖库.取文(览), "览中之文")
        画 = 牖库.布画(牖, 100, 80)
        牖库.画线(画, 0, 0, 100, 80, "朱", 2)
        牖.update()  # 起一轮事件循环即阖，不入 mainloop
        牖.destroy()

    def test_天穹脚本驱牖(self):
        from tianqiong.yufa import 语法分析
        from tianqiong.tian_di import 筑天地

        源码 = (
            "混沌 牖试\n"
            "盘古 启动\n"
            '    阳 立牖 "脚本之窗" 200 150 存于 牖\n'
            '    阳 匾额 牖 "脚本所立"\n'
            "    阳 书栏 牖 20 存于 栏\n"
            '    阳 书文 栏 "自天穹来"\n'
            "    阳 取文 栏 存于 文\n"
            "    阳 输出 文\n"
        )
        天地 = 筑天地()
        import io
        from contextlib import redirect_stdout
        缓冲 = io.StringIO()
        with redirect_stdout(缓冲):
            exec(compile(语法分析(源码), "牖试.天穹", "exec"), 天地)
        self.assertEqual(缓冲.getvalue().strip(), "自天穹来")


if __name__ == "__main__":
    unittest.main()
