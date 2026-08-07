"""天地：运行环境。内建诸名，皆化中文。"""

from __future__ import annotations


def 筑天地() -> dict:
    """筑一方天地：exec 所用的全局命名空间。"""
    from .kunlun import you as 牖库
    from .kunlun import xingchen as 星辰库
    from .kunlun import xuanwu as 玄武库
    from .kunlun import sixiang as 四象库

    天地 = {
        "__name__": "__main__",
        "__builtins__": __builtins__,
        # 出入
        "输出": print,
        "输入": input,
        # 度量
        "长度": len,
        "范围": range,
        "枚举": enumerate,
        "拉链": zip,
        # 五行（类型）
        "整数": int,
        "小数": float,
        "文": str,
        "真伪": bool,
        "列表": list,
        "元组": tuple,
        "集": set,
        "典": dict,
        "类属": type,
        "是否": isinstance,
        # 文卷
        "开卷": open,
        # 杂项
        "排序": sorted,
        "逆转": reversed,
        "求和": sum,
        "至大": max,
        "至小": min,
        "绝对": abs,
        "四舍五入": round,
        "化文": str,
        "化整": int,
        # 昆仑·牖（窗棂之道，tkinter 薄壳）
        "立牖": 牖库.立牖,
        "匾额": 牖库.匾额,
        "按钮": 牖库.按钮,
        "书栏": 牖库.书栏,
        "览栏": 牖库.览栏,
        "书文": 牖库.书文,
        "取文": 牖库.取文,
        "布画": 牖库.布画,
        "画线": 牖库.画线,
        "守牖": 牖库.守牖,
        # 昆仑·星辰（同耀并行，threading 薄壳）
        "同耀": 星辰库.同耀,
        "待星": 星辰库.待星,
        "安歇": 星辰库.安歇,
        "立锁": 星辰库.立锁,
        "持锁": 星辰库.持锁,
        "释锁": 星辰库.释锁,
        # 昆仑·玄武（安全印验，hashlib/hmac 薄壳）
        "铸印": 玄武库.铸印,
        "验印": 玄武库.验印,
        "密押": 玄武库.密押,
        "验押": 玄武库.验押,
        "灵符": 玄武库.灵符,
        "天衍": 玄武库.天衍,
        # 昆仑·四象（配置键值，json 薄壳）
        "立四象": 四象库.立四象,
        "观象": 四象库.观象,
        "定象": 四象库.定象,
        "化四象": 四象库.化文,
        "解四象": 四象库.解文,
        "存四象": 四象库.存象,
        "载四象": 四象库.载象,
        # 太极/太初 已由语法层直译
    }
    return 天地
