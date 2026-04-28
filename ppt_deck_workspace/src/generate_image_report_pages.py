# 中文注释：批量生成项目图文报告页面。
# 主要流程：读取实验素材，按固定画布尺寸绘制多页中文说明图。
# 输出结果：生成 image2_report_pages 目录中的汇报图片页面。

# 行注释：这里启用较新的 Python 类型注解行为。
from __future__ import annotations

# 行注释：这里导入脚本后面需要用到的 Python 模块。
import math
# 行注释：这里导入脚本后面需要用到的 Python 模块。
from pathlib import Path
# 行注释：这里导入脚本后面需要用到的 Python 模块。
from typing import Iterable

# 行注释：这里导入脚本后面需要用到的 Python 模块。
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# 行注释：这里设置 ROOT 的值，后续绘图或计算会用到。
ROOT = Path(__file__).resolve().parents[2]
# 行注释：这里设置 POLISHED 的值，后续绘图或计算会用到。
POLISHED = ROOT / "ppt_materials" / "visa_pcb" / "polished"
# 行注释：这里设置 BASIC 的值，后续绘图或计算会用到。
BASIC = ROOT / "ppt_materials" / "visa_pcb"
# 行注释：这里设置 DATA 的值，后续绘图或计算会用到。
DATA = ROOT / "data" / "raw" / "visa"
# 行注释：这里设置 OUT 的值，后续绘图或计算会用到。
OUT = ROOT / "image_report_pages"

# 行注释：这里设置 W, H 的值，后续绘图或计算会用到。
W, H = 1920, 1080

# 行注释：这里设置 NAVY 的值，后续绘图或计算会用到。
NAVY = "#003B73"
# 行注释：这里设置 NAVY2 的值，后续绘图或计算会用到。
NAVY2 = "#004488"
# 行注释：这里设置 OCEAN 的值，后续绘图或计算会用到。
OCEAN = "#005A8D"
# 行注释：这里设置 BLUE 的值，后续绘图或计算会用到。
BLUE = "#2E5A88"
# 行注释：这里设置 CYAN 的值，后续绘图或计算会用到。
CYAN = "#28A9E0"
# 行注释：这里设置 GOLD 的值，后续绘图或计算会用到。
GOLD = "#C99700"
# 行注释：这里设置 ORANGE 的值，后续绘图或计算会用到。
ORANGE = "#D95319"
# 行注释：这里设置 RED 的值，后续绘图或计算会用到。
RED = "#B22222"
# 行注释：这里设置 INK 的值，后续绘图或计算会用到。
INK = "#0F172A"
# 行注释：这里设置 SLATE 的值，后续绘图或计算会用到。
SLATE = "#475569"
# 行注释：这里设置 MUTED 的值，后续绘图或计算会用到。
MUTED = "#64748B"
# 行注释：这里设置 LINE 的值，后续绘图或计算会用到。
LINE = "#CBD8E4"
# 行注释：这里设置 BG 的值，后续绘图或计算会用到。
BG = "#F5F8FB"
# 行注释：这里设置 WHITE 的值，后续绘图或计算会用到。
WHITE = "#FFFFFF"
# 行注释：这里设置 PALE_BLUE 的值，后续绘图或计算会用到。
PALE_BLUE = "#E7F4FB"
# 行注释：这里设置 PALE_GOLD 的值，后续绘图或计算会用到。
PALE_GOLD = "#FFF7DB"
# 行注释：这里设置 PALE_ORANGE 的值，后续绘图或计算会用到。
PALE_ORANGE = "#FFF0E6"

# 行注释：这里尝试执行可能因为环境差异而失败的代码。
try:
    # 行注释：这里设置 RESAMPLE 的值，后续绘图或计算会用到。
    RESAMPLE = Image.Resampling.LANCZOS
# 行注释：这里处理上面 try 捕获到的异常情况。
except AttributeError:  # pragma: no cover
    # 行注释：这里设置 RESAMPLE 的值，后续绘图或计算会用到。
    RESAMPLE = Image.LANCZOS


# 函数说明：加载中文字体，保证图片里的中文能正常显示。
# 行注释：这里定义 font 函数。
def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    # 行注释：这里设置 candidates 的值，后续绘图或计算会用到。
    candidates = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        r"C:\Windows\Fonts\simhei.ttf",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        r"C:\Windows\Fonts\arial.ttf",
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for item in candidates:
        # 行注释：这里判断条件是否满足。
        if item and Path(item).exists():
            # 行注释：这里把结果返回给调用它的代码。
            return ImageFont.truetype(item, size=size)
    # 行注释：这里把结果返回给调用它的代码。
    return ImageFont.load_default()


# 函数说明：加载等宽字体，用来绘制代码片段和矩阵示意。
# 行注释：这里定义 mono 函数。
def mono(size: int) -> ImageFont.FreeTypeFont:
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for item in [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf"]:
        # 行注释：这里判断条件是否满足。
        if Path(item).exists():
            # 行注释：这里把结果返回给调用它的代码。
            return ImageFont.truetype(item, size=size)
    # 行注释：这里把结果返回给调用它的代码。
    return font(size)


# 函数说明：计算文字宽高，帮助把文字放到合适位置。
# 行注释：这里定义 text_size 函数。
def text_size(draw: ImageDraw.ImageDraw, value: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    box = draw.textbbox((0, 0), value, font=fnt)
    # 行注释：这里把结果返回给调用它的代码。
    return box[2] - box[0], box[3] - box[1]


# 函数说明：把长句按最大宽度拆成多行，避免文字溢出。
# 行注释：这里定义 wrapped_lines 函数。
def wrapped_lines(draw: ImageDraw.ImageDraw, value: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    lines: list[str] = []
    # 行注释：这里设置 current 的值，后续绘图或计算会用到。
    current = ""
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for ch in value:
        # 行注释：这里判断条件是否满足。
        if ch == "\n":
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            lines.append(current)
            # 行注释：这里设置 current 的值，后续绘图或计算会用到。
            current = ""
            # 行注释：这里跳过本轮循环，进入下一项。
            continue
        # 行注释：这里设置 test 的值，后续绘图或计算会用到。
        test = current + ch
        # 行注释：这里判断条件是否满足。
        if text_size(draw, test, fnt)[0] <= max_width:
            # 行注释：这里设置 current 的值，后续绘图或计算会用到。
            current = test
        # 行注释：这里处理其他情况。
        else:
            # 行注释：这里判断条件是否满足。
            if current:
                # 行注释：这里执行当前语句，推进这一小步逻辑。
                lines.append(current)
            # 行注释：这里设置 current 的值，后续绘图或计算会用到。
            current = ch
    # 行注释：这里判断条件是否满足。
    if current:
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        lines.append(current)
    # 行注释：这里把结果返回给调用它的代码。
    return lines


# 函数说明：按多行方式绘制文字，保证中文说明不挤出卡片。
# 行注释：这里定义 draw_wrapped 函数。
def draw_wrapped(
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw: ImageDraw.ImageDraw,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    value: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    xy: tuple[int, int],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    size: int,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fill: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    max_width: int,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    *,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    bold: bool = False,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    line_gap: int = 8,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fnt: ImageFont.FreeTypeFont | None = None,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> int:
    # 行注释：这里设置 x, y 的值，后续绘图或计算会用到。
    x, y = xy
    # 行注释：这里设置 fnt 的值，后续绘图或计算会用到。
    fnt = fnt or font(size, bold)
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for line in wrapped_lines(draw, value, fnt, max_width):
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.text((x, y), line, font=fnt, fill=fill)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        y += text_size(draw, line, fnt)[1] + line_gap
    # 行注释：这里把结果返回给调用它的代码。
    return y


# 函数说明：创建统一尺寸和背景色的页面画布。
# 行注释：这里定义 make_canvas 函数。
def make_canvas() -> Image.Image:
    # 行注释：这里把结果返回给调用它的代码。
    return Image.new("RGB", (W, H), BG)


# 函数说明：给卡片区域加柔和阴影，让页面层次更清楚。
# 行注释：这里定义 add_shadow 函数。
def add_shadow(base: Image.Image, rect: tuple[int, int, int, int], radius: int = 24, alpha: int = 38) -> None:
    # 行注释：这里设置 x1, y1, x2, y2 的值，后续绘图或计算会用到。
    x1, y1, x2, y2 = rect
    # 行注释：这里创建新的图片画布。
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(layer)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rounded_rectangle((x1 + 6, y1 + 8, x2 + 6, y2 + 8), radius=radius, fill=(0, 48, 90, alpha))
    # 行注释：这里设置 layer 的值，后续绘图或计算会用到。
    layer = layer.filter(ImageFilter.GaussianBlur(8))
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    base.alpha_composite(layer) if base.mode == "RGBA" else base.paste(Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB"))


# 函数说明：绘制圆角矩形，作为信息卡片或内容面板。
# 行注释：这里定义 rounded 函数。
def rounded(draw: ImageDraw.ImageDraw, box, fill=WHITE, outline=LINE, width=2, radius=24) -> None:
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# 函数说明：绘制页面顶部标题栏和副标题。
# 行注释：这里定义 header 函数。
def header(draw: ImageDraw.ImageDraw, title: str, subtitle: str = "", tag: str = "HEU | Bayesian PCB Inspection") -> None:
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rectangle((0, 0, W, 136), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((76, 34), title, font=font(46, True), fill=WHITE)
    # 行注释：这里判断条件是否满足。
    if subtitle:
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.text((78, 92), subtitle, font=font(23), fill="#CFE8F7")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rounded_rectangle((1490, 42, 1838, 92), radius=24, fill="#0A4B82")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((1664, 67), tag, font=font(18, True), fill=WHITE, anchor="mm")


# 函数说明：绘制页脚和页码信息。
# 行注释：这里定义 footer 函数。
def footer(draw: ImageDraw.ImageDraw, page_no: int) -> None:
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((76, 1035), "哈尔滨工程大学 · 电子信息方向 · 模式识别课程研讨", font=font(16), fill="#6B7E8F")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((1838, 1035), f"{page_no:02d}", font=font(18, True), fill=NAVY, anchor="ra")


# 函数说明：把图片完整放入目标区域，必要时留白。
# 行注释：这里定义 contain 函数。
def contain(path: Path, size: tuple[int, int], bg: str = WHITE) -> Image.Image:
    # 行注释：这里读取一张图片并准备处理。
    img = Image.open(path).convert("RGB")
    # 行注释：这里设置 tw, th 的值，后续绘图或计算会用到。
    tw, th = size
    # 行注释：这里设置 sw, sh 的值，后续绘图或计算会用到。
    sw, sh = img.size
    # 行注释：这里设置 scale 的值，后续绘图或计算会用到。
    scale = min(tw / sw, th / sh)
    # 行注释：这里设置 new 的值，后续绘图或计算会用到。
    new = img.resize((max(1, int(sw * scale)), max(1, int(sh * scale))), RESAMPLE)
    # 行注释：这里创建新的图片画布。
    canvas = Image.new("RGB", size, bg)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    canvas.paste(new, ((tw - new.width) // 2, (th - new.height) // 2))
    # 行注释：这里把结果返回给调用它的代码。
    return canvas


# 函数说明：把图片按目标区域裁剪填满，用于样本展示。
# 行注释：这里定义 cover 函数。
def cover(path: Path, size: tuple[int, int]) -> Image.Image:
    # 行注释：这里读取一张图片并准备处理。
    img = Image.open(path).convert("RGB")
    # 行注释：这里设置 tw, th 的值，后续绘图或计算会用到。
    tw, th = size
    # 行注释：这里设置 sw, sh 的值，后续绘图或计算会用到。
    sw, sh = img.size
    # 行注释：这里设置 scale 的值，后续绘图或计算会用到。
    scale = max(tw / sw, th / sh)
    # 行注释：这里设置 new 的值，后续绘图或计算会用到。
    new = img.resize((max(1, int(sw * scale)), max(1, int(sh * scale))), RESAMPLE)
    # 行注释：这里设置 left 的值，后续绘图或计算会用到。
    left = (new.width - tw) // 2
    # 行注释：这里设置 top 的值，后续绘图或计算会用到。
    top = (new.height - th) // 2
    # 行注释：这里把结果返回给调用它的代码。
    return new.crop((left, top, left + tw, top + th))


# 函数说明：把图片贴进卡片区域，并自动处理缩放和留白。
# 行注释：这里定义 paste_card 函数。
def paste_card(base: Image.Image, box, img_path: Path, *, padding: int = 12, fit: str = "contain", bg: str = WHITE) -> None:
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    draw = ImageDraw.Draw(base)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, box, WHITE, LINE, 2, 18)
    # 行注释：这里设置 x1, y1, x2, y2 的值，后续绘图或计算会用到。
    x1, y1, x2, y2 = box
    # 行注释：这里设置 size 的值，后续绘图或计算会用到。
    size = (x2 - x1 - 2 * padding, y2 - y1 - 2 * padding)
    # 行注释：这里设置 image 的值，后续绘图或计算会用到。
    image = contain(img_path, size, bg) if fit == "contain" else cover(img_path, size)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    base.paste(image, (x1 + padding, y1 + padding))


# 函数说明：绘制统计数字卡片。
# 行注释：这里定义 stat_card 函数。
def stat_card(draw: ImageDraw.ImageDraw, box, value: str, label: str, color: str) -> None:
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, box, WHITE, LINE, 2, 20)
    # 行注释：这里设置 x1, y1, _, _ 的值，后续绘图或计算会用到。
    x1, y1, _, _ = box
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 24, y1 + 20), value, font=font(38, True), fill=color)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 25, y1 + 73), label, font=font(19), fill=MUTED)


# 函数说明：绘制多条项目符号说明。
# 行注释：这里定义 bullet_list 函数。
def bullet_list(draw: ImageDraw.ImageDraw, items: Iterable[str], x: int, y: int, width: int, *, dot: str = GOLD, size: int = 24, gap: int = 16) -> int:
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for item in items:
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.ellipse((x, y + 10, x + 10, y + 20), fill=dot)
        # 行注释：这里设置 y 的值，后续绘图或计算会用到。
        y = draw_wrapped(draw, item, (x + 25, y), size, SLATE, width - 25, line_gap=7)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        y += gap
    # 行注释：这里把结果返回给调用它的代码。
    return y


# 函数说明：按页码和标题保存生成的图片。
# 行注释：这里定义 save 函数。
def save(page_no: int, title: str, img: Image.Image) -> Path:
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    OUT.mkdir(parents=True, exist_ok=True)
    # 行注释：这里设置 path 的值，后续绘图或计算会用到。
    path = OUT / f"{page_no:02d}_{title}.png"
    # 行注释：这里把生成的图片或文件保存到磁盘。
    img.save(path, quality=95)
    # 行注释：这里把结果返回给调用它的代码。
    return path


# 函数说明：生成第 1 页封面。
# 行注释：这里定义 page_01_cover 函数。
def page_01_cover() -> Path:
    # 行注释：这里设置 bg 的值，后续绘图或计算会用到。
    bg = cover(POLISHED / "00_哈工程深蓝封面背景.png", (W, H))
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(bg)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((118, 112), "基于贝叶斯决策的", font=font(76, True), fill=WHITE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((118, 205), "PCB 缺陷检测", font=font(96, True), fill=WHITE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rectangle((118, 323, 520, 333), fill=GOLD)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((118, 365), "VisA PCB 真实彩色图像 · normal / anomaly 二分类 · Bayes-only 优化", font=font(31), fill="#D9ECF7")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((118, 902), "项目流程汇报图册", font=font(32, True), fill=WHITE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((118, 950), "电子信息方向 | 模式识别 | MATLAB 实验实现", font=font(23), fill="#CFE8F7")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1600, 104), "哈尔滨工程大学", font=font(32, True), fill=WHITE, anchor="mm")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1600, 148), "Harbin Engineering University", font=font(20), fill="#CFE8F7", anchor="mm")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1600, 184), "大工至善 · 大学至真", font=font(21, True), fill="#F6D77D", anchor="mm")
    # 行注释：这里把结果返回给调用它的代码。
    return save(1, "封面", bg)


# 函数说明：生成第 2 页项目主线说明。
# 行注释：这里定义 page_02_storyline 函数。
def page_02_storyline() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "汇报主线：从真实图像到贝叶斯决策", "按老师评分点组织：数据、方法、参数、指标、对比、改进。")
    # 行注释：这里设置 steps 的值，后续绘图或计算会用到。
    steps = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("01", "数据集", "VisA PCB 真实彩色图像\nnormal / anomaly 二分类"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("02", "特征", "每张图像提取 1318 维\n颜色、灰度、边缘、纹理、LBP、HOG"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("03", "模型", "用贝叶斯公式得到\nP(缺陷|x) 后验概率"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("04", "优化", "PCA 降维、Gamma 正则化\n后验阈值 T 寻优"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("05", "评估", "Accuracy、Precision、Recall\nF1、IoU、AUC、FPR、FNR"),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里设置 x0, y0, w, h, gap 的值，后续绘图或计算会用到。
    x0, y0, w, h, gap = 90, 280, 325, 300, 50
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, (num, title, body) in enumerate(steps):
        # 行注释：这里设置 x 的值，后续绘图或计算会用到。
        x = x0 + i * (w + gap)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        rounded(d, (x, y0, x + w, y0 + h), WHITE, LINE, 2, 28)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d.ellipse((x + 28, y0 + 28, x + 90, y0 + 90), fill=[OCEAN, NAVY2, BLUE, GOLD, ORANGE][i])
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((x + 59, y0 + 59), num, font=font(22, True), fill=WHITE, anchor="mm")
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((x + 112, y0 + 42), title, font=font(31, True), fill=INK)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.line((x + 30, y0 + 118, x + w - 30, y0 + 118), fill="#DDE8F2", width=2)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw_wrapped(d, body, (x + 32, y0 + 150), 24, SLATE, w - 64, line_gap=12)
        # 行注释：这里判断条件是否满足。
        if i < len(steps) - 1:
            # 行注释：这里在图片画布上绘制文字、线条或形状。
            d.line((x + w + 6, y0 + h // 2, x + w + gap - 10, y0 + h // 2), fill="#87AEC9", width=5)
            # 行注释：这里在图片画布上绘制文字、线条或形状。
            d.polygon([(x + w + gap - 10, y0 + h // 2), (x + w + gap - 28, y0 + h // 2 - 12), (x + w + gap - 28, y0 + h // 2 + 12)], fill="#87AEC9")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (220, 735, 1700, 875), PALE_BLUE, "#9CCBE2", 2, 24)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((265, 770), "一句话逻辑", font=font(32, True), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((475, 773), "把 PCB 图片转为特征向量 x，利用贝叶斯后验概率 P(缺陷|x) 做最小风险判别，再通过参数优化证明性能提升。", font=font(27), fill=INK)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 2)
    # 行注释：这里把结果返回给调用它的代码。
    return save(2, "汇报主线", img)


# 函数说明：生成第 3 页数据集介绍。
# 行注释：这里定义 page_03_dataset 函数。
def page_03_dataset() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "数据集汇报：VisA PCB 真实彩色图像", "数据真实、类别不均衡、划分清晰，是后续评价指标选择的基础。")
    # 行注释：这里设置 cards 的值，后续绘图或计算会用到。
    cards = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("4413", "可用 PCB 图像总数", NAVY2),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("4013", "正常样本 normal", OCEAN),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("400", "缺陷样本 anomaly", ORANGE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("4 类", "pcb1-pcb4 子集", GOLD),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("70/15/15", "训练/验证/测试", NAVY2),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, item in enumerate(cards):
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        stat_card(d, (80 + i * 350, 175, 405 + i * 350, 305), *item)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (80, 350, 675, 970), WHITE, LINE, 2, 28)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((118, 390), "类别比例", font=font(34, True), fill=NAVY)
    # 行注释：这里设置 center, radius, thick 的值，后续绘图或计算会用到。
    center, radius, thick = (377, 610), 130, 47
    # 行注释：这里设置 normal, anomaly 的值，后续绘图或计算会用到。
    normal, anomaly = 4013, 400
    # 行注释：这里设置 angle 的值，后续绘图或计算会用到。
    angle = 360 * normal / (normal + anomaly)
    # 行注释：这里设置 box 的值，后续绘图或计算会用到。
    box = (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    d.pieslice(box, -90, -90 + angle, fill=NAVY2)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    d.pieslice(box, -90 + angle, 270, fill=ORANGE)
    # 行注释：这里设置 inner 的值，后续绘图或计算会用到。
    inner = (center[0] - radius + thick, center[1] - radius + thick, center[0] + radius - thick, center[1] + radius - thick)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    d.ellipse(inner, fill=WHITE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text(center, "4413", font=font(42, True), fill=INK, anchor="mm")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((center[0], center[1] + 44), "张图像", font=font(21), fill=MUTED, anchor="mm")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rectangle((145, 785, 174, 814), fill=NAVY2)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((190, 783), "normal：4013 张，占 90.9%", font=font(25), fill=SLATE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rectangle((145, 835, 174, 864), fill=ORANGE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((190, 833), "anomaly：400 张，占 9.1%", font=font(25), fill=SLATE)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (720, 350, 1240, 970), WHITE, LINE, 2, 28)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((758, 390), "子集分布", font=font(34, True), fill=NAVY)
    # 行注释：这里设置 x, y, cw, ch 的值，后续绘图或计算会用到。
    x, y, cw, ch = 785, 520, 390, 280
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i in range(6):
        # 行注释：这里设置 yy 的值，后续绘图或计算会用到。
        yy = y + ch - i * ch / 5
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.line((x, yy, x + cw, yy), fill="#E4ECF3", width=1)
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, subset in enumerate(["pcb1", "pcb2", "pcb3", "pcb4"]):
        # 行注释：这里设置 bx 的值，后续绘图或计算会用到。
        bx = x + i * 96 + 20
        # 行注释：这里设置 nh, ah 的值，后续绘图或计算会用到。
        nh, ah = 255, 26
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.rounded_rectangle((bx, y + ch - nh, bx + 30, y + ch), radius=6, fill=NAVY2)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.rounded_rectangle((bx + 38, y + ch - ah, bx + 68, y + ch), radius=6, fill=ORANGE)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((bx + 8, y + ch + 18), subset, font=font(18, True), fill=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.line((x, y + ch, x + cw, y + ch), fill="#94A3B8", width=2)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rectangle((790, 875, 815, 900), fill=NAVY2)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((830, 873), "正常样本", font=font(20), fill=SLATE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rectangle((940, 875, 965, 900), fill=ORANGE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((980, 873), "缺陷样本", font=font(20), fill=SLATE)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (1280, 350, 1835, 970), WHITE, LINE, 2, 28)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1318, 390), "真实样本", font=font(34, True), fill=NAVY)
    # 行注释：这里设置 sample_paths 的值，后续绘图或计算会用到。
    sample_paths = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (DATA / "pcb1" / "Data" / "Images" / "Normal" / "0313.JPG", "正常 / pcb1", PALE_BLUE, NAVY),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (DATA / "pcb1" / "Data" / "Images" / "Anomaly" / "000.JPG", "缺陷 / pcb1", PALE_ORANGE, ORANGE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (DATA / "pcb4" / "Data" / "Images" / "Anomaly" / "000.JPG", "缺陷 / pcb4", PALE_GOLD, "#805E00"),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for idx, (p, label, tag_fill, tag_color) in enumerate(sample_paths):
        # 行注释：这里设置 yy 的值，后续绘图或计算会用到。
        yy = 465 + idx * 160
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        rounded(d, (1320, yy, 1795, yy + 128), "#FAFCFE", "#D7E2EC", 2, 18)
        # 行注释：这里判断条件是否满足。
        if not p.exists():
            # 行注释：这里设置 p 的值，后续绘图或计算会用到。
            p = next((DATA / "pcb4" / "Data" / "Images" / "Anomaly").glob("*.JPG"))
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        img.paste(cover(p, (175, 98)), (1338, yy + 15))
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.rounded_rectangle((1540, yy + 22, 1715, yy + 58), radius=16, fill=tag_fill)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((1560, yy + 29), label, font=font(20, True), fill=tag_color)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((1540, yy + 78), "图像 → 1318维特征 x", font=font(20), fill=SLATE)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (720, 995, 1835, 1050), PALE_BLUE, "#9CCBE2", 2, 18)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((750, 1012), "汇报重点：类别不均衡，因此后续不能只看准确率，要结合 F1、AUC、FPR/FNR 等指标。", font=font(23, True), fill=NAVY)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 3)
    # 行注释：这里把结果返回给调用它的代码。
    return save(3, "数据集汇报界面", img)


# 函数说明：生成第 4 页样本展示。
# 行注释：这里定义 page_04_samples 函数。
def page_04_samples() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "任务定义：good / bad 二分类", "正常样本放一张，缺陷样本放两张，强调模型输出的是 P(缺陷|x)。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (78, 165, 1840, 990), POLISHED / "14_正常与缺陷样本归类预览.png", padding=0, fit="contain", bg=BG)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 4)
    # 行注释：这里把结果返回给调用它的代码。
    return save(4, "任务定义与样本", img)


# 函数说明：生成第 5 页项目流程图。
# 行注释：这里定义 page_05_flowchart 函数。
def page_05_flowchart() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "项目流程：从图像到贝叶斯优化结果", "数据处理、特征工程、贝叶斯建模、参数反馈、指标汇报形成闭环。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (78, 165, 1840, 990), POLISHED / "13_项目流程图.png", padding=0, fit="contain", bg=BG)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 5)
    # 行注释：这里把结果返回给调用它的代码。
    return save(5, "项目流程图", img)


# 函数说明：生成第 6 页特征提取可视化。
# 行注释：这里定义 page_06_feature_visual 函数。
def page_06_feature_visual() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "特征提取：PCB 图像如何变成 1318 维向量", "贝叶斯模型不能直接读图片，因此先把图像转成结构化特征矩阵。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (78, 165, 1840, 990), POLISHED / "12_图像特征提取过程可视化.png", padding=0, fit="contain", bg=BG)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 6)
    # 行注释：这里把结果返回给调用它的代码。
    return save(6, "特征提取可视化", img)


# 函数说明：生成第 7 页特征矩阵说明。
# 行注释：这里定义 page_07_feature_matrix 函数。
def page_07_feature_matrix() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "特征矩阵：模型真正看到的是 X = 4413 × 1318", "每一行是一张图像，每一列是一类手工特征。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (90, 185, 1120, 955), WHITE, LINE, 2, 26)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((130, 225), "特征组成", font=font(36, True), fill=NAVY)
    # 行注释：这里设置 rows 的值，后续绘图或计算会用到。
    rows = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("颜色统计 RGB/HSV/Lab", "36", "均值、标准差、偏度、峰度，描述基板与元件颜色"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("灰度统计", "8", "亮度、熵、分位数，描述整体明暗分布"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("边缘密度", "2", "Canny 与 Sobel，捕捉走线和器件边缘"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("GLCM 纹理", "4", "对比度、相关性、能量、同质性"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("LBP 局部纹理", "944", "对局部划痕、污点、纹理异常较敏感"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("HOG 梯度结构", "324", "描述方向梯度和结构轮廓"),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里设置 y 的值，后续绘图或计算会用到。
    y = 300
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((135, y), "特征类别", font=font(24, True), fill=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((500, y), "维度", font=font(24, True), fill=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((630, y), "作用解释", font=font(24, True), fill=INK)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    y += 45
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.line((130, y, 1080, y), fill=LINE, width=2)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    y += 22
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for name, dim, desc in rows:
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((135, y), name, font=font(23, True), fill=INK)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((520, y), dim, font=font(23, True), fill=ORANGE, anchor="ra")
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw_wrapped(d, desc, (630, y), 21, SLATE, 420, line_gap=5)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        y += 82
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (1180, 185, 1830, 955), PALE_BLUE, "#9CCBE2", 2, 26)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1225, 230), "数据形态", font=font(36, True), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1225, 305), "X ∈ R^(4413×1318)", font=font(46, True), fill=NAVY2)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1225, 375), "Y ∈ {normal, anomaly}", font=font(34, True), fill=ORANGE)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    bullet_list(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "标准化只用训练集均值和方差，防止数据泄漏。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "PCA 在训练集上学习方向，再映射验证集和测试集。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "贝叶斯模型估计 p(x|ω)，再输出 P(缺陷|x)。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "最后由阈值 T 把概率变成 normal / anomaly 标签。",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        1228,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        470,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        545,
        # 行注释：这里设置 dot 的值，后续绘图或计算会用到。
        dot=GOLD,
        # 行注释：这里设置 size 的值，后续绘图或计算会用到。
        size=25,
        # 行注释：这里设置 gap 的值，后续绘图或计算会用到。
        gap=18,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 7)
    # 行注释：这里把结果返回给调用它的代码。
    return save(7, "特征矩阵说明", img)


# 函数说明：生成第 8 页贝叶斯理论说明。
# 行注释：这里定义 page_08_bayes_theory 函数。
def page_08_bayes_theory() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "贝叶斯决策：从后验概率到缺陷判别", "核心不是直接给标签，而是先得到 P(缺陷|x)，再做最小风险决策。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (90, 185, 760, 955), WHITE, LINE, 2, 26)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((130, 230), "核心公式", font=font(36, True), fill=NAVY)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (135, 305, 710, 395), PALE_BLUE, "#9CCBE2", 2, 18)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((422, 350), "P(ωₖ|x)= p(x|ωₖ)P(ωₖ) / Σⱼp(x|ωⱼ)P(ωⱼ)", font=font(24, True), fill=NAVY, anchor="mm")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (135, 430, 710, 520), PALE_GOLD, "#EAD18B", 2, 18)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((422, 475), "若 P(缺陷|x) ≥ T，则判为缺陷；否则判为正常", font=font(24, True), fill="#6B4E00", anchor="mm")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    bullet_list(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "ω₁：normal，ω₂：anomaly。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "T 是后验概率阈值，控制误报和漏报。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "如果漏检代价更高，可以调低阈值；如果误报代价更高，可以调高阈值。",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        135,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        590,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        535,
        # 行注释：这里设置 dot 的值，后续绘图或计算会用到。
        dot=CYAN,
        # 行注释：这里设置 size 的值，后续绘图或计算会用到。
        size=24,
        # 行注释：这里设置 gap 的值，后续绘图或计算会用到。
        gap=20,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (815, 185, 1830, 955), POLISHED / "09_一维概率分布与贝叶斯误差.png", padding=16, fit="contain")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 8)
    # 行注释：这里把结果返回给调用它的代码。
    return save(8, "贝叶斯决策原理", img)


# 函数说明：生成第 9 页代码实现说明。
# 行注释：这里定义 page_09_code 函数。
def page_09_code() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "贝叶斯模型核心代码：训练、后验概率、阈值决策", "这一页用于讲清楚 MATLAB 中 Bayes-0 到 Bayes-4 的实现逻辑。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (80, 175, 1160, 980), "#102033", "#28465F", 2, 20)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rectangle((80, 175, 1160, 225), fill="#0B1828")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((108, 190), "MATLAB 核心代码", font=font(22, True), fill="#E8F2FA")
    # 行注释：这里设置 code 的值，后续绘图或计算会用到。
    code = """% 1. PCA 降维
[coeff, ~, ~, ~, explained] = pca(XTrainZ);
XTrainP = XTrainZ * coeff(:, 1:pcaDim);
XValP   = XValZ   * coeff(:, 1:pcaDim);

% 2. 贝叶斯建模：朴素贝叶斯 / 高斯判别 / 正则化判别
model = fitcdiscr(XTrainP, YTrain, ...
    'DiscrimType', 'linear', ...
    'Gamma', gamma, ...
    'Prior', 'uniform');

% 3. 输出缺陷类后验概率
[~, scoreVal] = predict(model, XValP);
classNames = string(model.ClassNames);
posCol = find(classNames == "anomaly", 1);
pBadVal = scoreVal(:, posCol);

% 4. 阈值决策：P(缺陷|x) >= T 判为缺陷
yPred = repmat("normal", numel(pBadVal), 1);
yPred(pBadVal >= T) = "anomaly";"""
    # 行注释：这里设置 y 的值，后续绘图或计算会用到。
    y = 255
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for line in code.splitlines():
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((110, y), line, font=mono(24), fill="#E8F2FA")
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        y += 34
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (1210, 175, 1835, 980), WHITE, LINE, 2, 20)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1250, 225), "讲解口径", font=font(36, True), fill=NAVY)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    bullet_list(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "PCA 先把 1318 维高维特征压缩到更稳定的低维空间。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "fitcdiscr 的 Gamma 是正则化参数，用来稳定协方差估计。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "predict 返回每一类后验分数，取 anomaly 对应列得到 P(缺陷|x)。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "阈值 T 把概率输出转成最终标签，是贝叶斯风险控制的一部分。",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        1250,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        310,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        520,
        # 行注释：这里设置 dot 的值，后续绘图或计算会用到。
        dot=GOLD,
        # 行注释：这里设置 size 的值，后续绘图或计算会用到。
        size=25,
        # 行注释：这里设置 gap 的值，后续绘图或计算会用到。
        gap=20,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 9)
    # 行注释：这里把结果返回给调用它的代码。
    return save(9, "贝叶斯模型代码展示", img)


# 函数说明：生成第 10 页优化阶段对比。
# 行注释：这里定义 page_10_optimization 函数。
def page_10_optimization() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "Bayes-only 优化路径：不换模型，只优化贝叶斯决策", "对比对象是 Bayes-0 到 Bayes-4，而不是 CNN、BP、Kmeans。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (90, 185, 630, 955), WHITE, LINE, 2, 26)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((130, 225), "五个阶段", font=font(36, True), fill=NAVY)
    # 行注释：这里设置 stages 的值，后续绘图或计算会用到。
    stages = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Bayes-0", "原始朴素贝叶斯"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Bayes-1", "PCA 降维优化"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Bayes-2", "高斯建模优化"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Bayes-3", "Gamma 正则化优化"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Bayes-4", "后验阈值优化"),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里设置 y 的值，后续绘图或计算会用到。
    y = 300
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, (a, b) in enumerate(stages):
        # 行注释：这里设置 fill 的值，后续绘图或计算会用到。
        fill = PALE_GOLD if i == 4 else PALE_BLUE
        # 行注释：这里设置 outline 的值，后续绘图或计算会用到。
        outline = "#EAD18B" if i == 4 else "#B6D9EA"
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        rounded(d, (130, y, 590, y + 88), fill, outline, 2, 18)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((155, y + 28), a, font=font(24, True), fill=NAVY if i < 4 else "#6B4E00")
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((300, y + 30), b, font=font(23), fill=INK)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        y += 112
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (675, 185, 1830, 955), POLISHED / "03_贝叶斯优化迭代趋势.png", padding=16, fit="contain")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 10)
    # 行注释：这里把结果返回给调用它的代码。
    return save(10, "贝叶斯优化路径", img)


# 函数说明：生成第 11 页参数分析。
# 行注释：这里定义 page_11_parameters 函数。
def page_11_parameters() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "参数分析：PCA 维度 × Gamma 正则化", "用验证集 F1 选择关键参数，证明调参过程是科学的。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (80, 175, 1120, 980), POLISHED / "05_主成分维度与正则化参数热力图.png", padding=16, fit="contain")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (1170, 175, 1835, 980), WHITE, LINE, 2, 24)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1210, 225), "图怎么讲", font=font(36, True), fill=NAVY)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    bullet_list(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "纵轴是 PCA 维度：过低会丢信息，过高会引入噪声和冗余。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "横轴是 Gamma：控制协方差估计的正则化强度。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "颜色越深表示验证集 F1 越高。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "金色框对应当前最佳参数区域。",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        1210,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        310,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        560,
        # 行注释：这里设置 dot 的值，后续绘图或计算会用到。
        dot=GOLD,
        # 行注释：这里设置 size 的值，后续绘图或计算会用到。
        size=26,
        # 行注释：这里设置 gap 的值，后续绘图或计算会用到。
        gap=22,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (1210, 735, 1795, 885), PALE_BLUE, "#9CCBE2", 2, 20)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_wrapped(d, "汇报句式：我先固定评价指标为 F1，再在验证集上同时搜索 PCA 维度和 Gamma，最后只在测试集上汇报最终性能。", (1240, 770), 24, NAVY, 520, bold=True, line_gap=10)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 11)
    # 行注释：这里把结果返回给调用它的代码。
    return save(11, "参数热力图", img)


# 函数说明：生成第 12 页阈值分析。
# 行注释：这里定义 page_12_threshold 函数。
def page_12_threshold() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "阈值与风险：为什么不是固定 0.5", "后验概率阈值 T 决定误报和漏报的权衡。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (80, 175, 945, 980), POLISHED / "06_后验概率阈值决策曲线.png", padding=16, fit="contain")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (985, 175, 1835, 980), POLISHED / "11_贝叶斯风险与损失函数.png", padding=16, fit="contain")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 12)
    # 行注释：这里把结果返回给调用它的代码。
    return save(12, "阈值风险权衡", img)


# 函数说明：生成第 13 页模型指标总结。
# 行注释：这里定义 page_13_metrics 函数。
def page_13_metrics() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "核心指标横向对比：优化后到底提升在哪里", "用多指标说明结果，避免类别不均衡下 Accuracy 误导。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (80, 175, 1080, 980), POLISHED / "02_五大指标横向对比.png", padding=16, fit="contain")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (1130, 175, 1835, 980), WHITE, LINE, 2, 24)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1170, 225), "最终 Bayes-4", font=font(36, True), fill=NAVY)
    # 行注释：这里设置 stats 的值，后续绘图或计算会用到。
    stats = [("0.918", "Accuracy", NAVY2), ("0.542", "F1-score", ORANGE), ("0.899", "AUC", OCEAN), ("0.372", "IoU", GOLD)]
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, (v, lab, col) in enumerate(stats):
        # 行注释：这里设置 x 的值，后续绘图或计算会用到。
        x = 1170 + (i % 2) * 310
        # 行注释：这里设置 y 的值，后续绘图或计算会用到。
        y = 300 + (i // 2) * 150
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        stat_card(d, (x, y, x + 275, y + 120), v, lab, col)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    bullet_list(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "Bayes-0 的 F1 低，说明原始朴素贝叶斯对缺陷类识别不足。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "Bayes-4 提高了精确率，减少把正常 PCB 误报为缺陷的情况。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "AUC 保持较高，说明后验概率排序能力较稳定。",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        1170,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        655,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        560,
        # 行注释：这里设置 dot 的值，后续绘图或计算会用到。
        dot=CYAN,
        # 行注释：这里设置 size 的值，后续绘图或计算会用到。
        size=25,
        # 行注释：这里设置 gap 的值，后续绘图或计算会用到。
        gap=20,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 13)
    # 行注释：这里把结果返回给调用它的代码。
    return save(13, "核心指标对比", img)


# 函数说明：生成第 14 页误报和漏检分析。
# 行注释：这里定义 page_14_errors 函数。
def page_14_errors() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "误报与漏报：质量检测里最需要解释的权衡", "FPR 表示误报，FNR 表示漏检；二者决定真实应用风险。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (80, 175, 985, 980), POLISHED / "04_误报率与漏报率权衡.png", padding=16, fit="contain")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (1030, 175, 1835, 980), BASIC / "基础图_贝叶斯混淆矩阵.png", padding=16, fit="contain")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 14)
    # 行注释：这里把结果返回给调用它的代码。
    return save(14, "误报漏报与混淆矩阵", img)


# 函数说明：生成第 15 页项目总结。
# 行注释：这里定义 page_15_summary 函数。
def page_15_summary() -> Path:
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = make_canvas()
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    header(d, "总结：贝叶斯方案的价值与边界", "用可解释概率决策完成 PCB 缺陷识别，但也要主动说明方法局限。")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    paste_card(img, (80, 170, 980, 985), POLISHED / "08_贝叶斯优化性能评估仪表盘.png", padding=16, fit="contain")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (1025, 170, 1835, 985), WHITE, LINE, 2, 24)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1070, 220), "可以强调的贡献", font=font(34, True), fill=NAVY)
    # 行注释：这里设置 y 的值，后续绘图或计算会用到。
    y = bullet_list(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "选用真实彩色 PCB 图像，贴近电子信息质量检测场景。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "构建 1318 维手工特征，并解释颜色、纹理、边缘、梯度的物理含义。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "在贝叶斯框架内完成 PCA、Gamma、阈值三类优化。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "使用多指标和多图表完成横向、纵向、参数、风险可视化。",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        1070,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        285,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        660,
        # 行注释：这里设置 dot 的值，后续绘图或计算会用到。
        dot=GOLD,
        # 行注释：这里设置 size 的值，后续绘图或计算会用到。
        size=24,
        # 行注释：这里设置 gap 的值，后续绘图或计算会用到。
        gap=16,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1070, y + 10), "主动承认的不足", font=font(34, True), fill=ORANGE)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    bullet_list(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "贝叶斯依赖手工特征，难以自动学习复杂空间拓扑结构。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "缺陷样本少且类别不均衡，precision 与 recall 存在权衡。",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "当前是图像级识别，不是像素级缺陷分割。",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        1070,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        y + 78,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        660,
        # 行注释：这里设置 dot 的值，后续绘图或计算会用到。
        dot=CYAN,
        # 行注释：这里设置 size 的值，后续绘图或计算会用到。
        size=24,
        # 行注释：这里设置 gap 的值，后续绘图或计算会用到。
        gap=16,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    footer(d, 15)
    # 行注释：这里把结果返回给调用它的代码。
    return save(15, "总结与反思", img)


# 函数说明：把多张报告页缩略图拼成一张总览图。
# 行注释：这里定义 make_contact_sheet 函数。
def make_contact_sheet(paths: list[Path]) -> Path:
    # 行注释：这里设置 thumb_w, thumb_h 的值，后续绘图或计算会用到。
    thumb_w, thumb_h = 384, 216
    # 行注释：这里设置 cols 的值，后续绘图或计算会用到。
    cols = 3
    # 行注释：这里设置 rows 的值，后续绘图或计算会用到。
    rows = math.ceil(len(paths) / cols)
    # 行注释：这里设置 margin 的值，后续绘图或计算会用到。
    margin = 26
    # 行注释：这里设置 label_h 的值，后续绘图或计算会用到。
    label_h = 32
    # 行注释：这里创建新的图片画布。
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * margin, rows * (thumb_h + label_h) + (rows + 1) * margin), BG)
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(sheet)
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for idx, p in enumerate(paths):
        # 行注释：这里读取一张图片并准备处理。
        im = Image.open(p).convert("RGB").resize((thumb_w, thumb_h), RESAMPLE)
        # 行注释：这里设置 r, c 的值，后续绘图或计算会用到。
        r, c = divmod(idx, cols)
        # 行注释：这里设置 x 的值，后续绘图或计算会用到。
        x = margin + c * (thumb_w + margin)
        # 行注释：这里设置 y 的值，后续绘图或计算会用到。
        y = margin + r * (thumb_h + label_h + margin)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((x, y), f"{idx + 1:02d}  {p.name}", font=font(18), fill=NAVY)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        sheet.paste(im, (x, y + label_h))
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.rectangle((x, y + label_h, x + thumb_w - 1, y + label_h + thumb_h - 1), outline=LINE, width=2)
    # 行注释：这里设置 out 的值，后续绘图或计算会用到。
    out = OUT / "00_全部图片页总览.png"
    # 行注释：这里把生成的图片或文件保存到磁盘。
    sheet.save(out, quality=95)
    # 行注释：这里把结果返回给调用它的代码。
    return out


# 函数说明：脚本入口，按顺序调用前面的函数生成最终文件。
# 行注释：这里定义 main 函数。
def main() -> None:
    # 行注释：这里设置 paths 的值，后续绘图或计算会用到。
    paths = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_01_cover(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_02_storyline(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_03_dataset(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_04_samples(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_05_flowchart(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_06_feature_visual(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_07_feature_matrix(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_08_bayes_theory(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_09_code(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_10_optimization(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_11_parameters(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_12_threshold(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_13_metrics(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_14_errors(),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        page_15_summary(),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里设置 contact 的值，后续绘图或计算会用到。
    contact = make_contact_sheet(paths)
    # 行注释：这里在终端输出生成结果或进度信息。
    print("Generated image report pages:")
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for p in paths:
        # 行注释：这里在终端输出生成结果或进度信息。
        print(p)
    # 行注释：这里在终端输出生成结果或进度信息。
    print(contact)


# 行注释：这里判断脚本是否被直接运行。
if __name__ == "__main__":
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    main()
