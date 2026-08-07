"""昆仑·牖：天穹窗棂之道（tkinter 薄壳）。

凡牖皆有柄，柄即 tkinter 组件。诸令皆以中文为名，
所包者，tkinter 也。薄，是特性。
"""

from __future__ import annotations


def _库():
    try:
        import tkinter as tk
        return tk
    except ImportError as 失:
        raise RuntimeError("牖户之库未具（此机无 tkinter）") from 失


def 立牖(题: str = "天穹", 宽: int = 480, 高: int = 320):
    """立一主牖（tk.Tk）。"""
    tk = _库()
    牖 = tk.Tk()
    牖.title(str(题))
    牖.geometry(f"{int(宽)}x{int(高)}")
    return 牖


def 匾额(牖, 文: str, 字号: int = 14):
    """牖上立一匾额（tk.Label）。"""
    tk = _库()
    匾 = tk.Label(牖, text=str(文), font=("TkDefaultFont", int(字号)))
    匾.pack(padx=8, pady=8)
    return 匾


def 按钮(牖, 文: str, 令=None):
    """牖上置一按钮（tk.Button）。令：按之所行。"""
    tk = _库()
    钮 = tk.Button(牖, text=str(文), command=令)
    钮.pack(padx=8, pady=8)
    return 钮


def 书栏(牖, 宽: int = 40):
    """牖上开一书栏（tk.Entry）。"""
    tk = _库()
    栏 = tk.Entry(牖, width=int(宽))
    栏.pack(padx=8, pady=8)
    return 栏


def 览栏(牖, 宽: int = 60, 高: int = 10):
    """牖上开一览栏（tk.Text）。"""
    tk = _库()
    栏 = tk.Text(牖, width=int(宽), height=int(高))
    栏.pack(padx=8, pady=8)
    return 栏


def 书文(栏, 文: str) -> None:
    """于览栏之末添文；于书栏则置其文。"""
    tk = _库()
    if isinstance(栏, tk.Text):
        栏.insert("end", str(文))
    else:
        栏.delete(0, "end")
        栏.insert(0, str(文))


def 取文(栏) -> str:
    """取书栏/览栏之文。"""
    tk = _库()
    if isinstance(栏, tk.Text):
        return 栏.get("1.0", "end").rstrip("\n")
    return 栏.get()


def 布画(牖, 宽: int = 480, 高: int = 320, 底: str = "白"):
    """牖上布一画（tk.Canvas）。"""
    tk = _库()
    色表 = {"白": "white", "玄": "black", "朱": "red", "青": "blue", "翠": "green"}
    画 = tk.Canvas(牖, width=int(宽), height=int(高),
                   bg=色表.get(str(底), str(底)))
    画.pack(padx=8, pady=8)
    return 画


def 画线(画, 甲x, 甲y, 乙x, 乙y, 色: str = "玄", 粗: int = 2) -> None:
    """画上引线（Canvas.create_line）。"""
    色表 = {"白": "white", "玄": "black", "朱": "red", "青": "blue", "翠": "green"}
    画.create_line(甲x, 甲y, 乙x, 乙y,
                   fill=色表.get(str(色), str(色)), width=int(粗))


def 守牖(牖) -> None:
    """守牖不离，直至牖阖（mainloop）。"""
    牖.mainloop()
