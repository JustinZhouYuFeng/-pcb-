# 中文注释：生成 PPT 中复用的基础视觉素材。
# 主要流程：绘制项目流程、数据说明、模型框架等图片资源。
# 输出结果：把素材集中保存，便于 PPT 构建脚本统一引用。

# 行注释：这里启用较新的 Python 类型注解行为。
from __future__ import annotations

# 行注释：这里导入脚本后面需要用到的 Python 模块。
import math
# 行注释：这里导入脚本后面需要用到的 Python 模块。
import random
# 行注释：这里导入脚本后面需要用到的 Python 模块。
from pathlib import Path

# 行注释：这里导入脚本后面需要用到的 Python 模块。
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# 行注释：这里设置 ROOT 的值，后续绘图或计算会用到。
ROOT = Path(r"C:\Users\19571\Desktop\研讨\PCB_Bayes_Project")
# 行注释：这里设置 OUT 的值，后续绘图或计算会用到。
OUT = ROOT / "ppt_materials" / "visa_pcb" / "polished"
# 行注释：这里设置 DATA 的值，后续绘图或计算会用到。
DATA = ROOT / "data" / "raw" / "visa"


# 行注释：这里设置 NAVY 的值，后续绘图或计算会用到。
NAVY = "#003B73"
# 行注释：这里设置 OCEAN 的值，后续绘图或计算会用到。
OCEAN = "#005A8D"
# 行注释：这里设置 CYAN 的值，后续绘图或计算会用到。
CYAN = "#28A9E0"
# 行注释：这里设置 GOLD 的值，后续绘图或计算会用到。
GOLD = "#C99700"
# 行注释：这里设置 INK 的值，后续绘图或计算会用到。
INK = "#0F172A"
# 行注释：这里设置 SLATE 的值，后续绘图或计算会用到。
SLATE = "#475569"
# 行注释：这里设置 LIGHT 的值，后续绘图或计算会用到。
LIGHT = "#F5F8FB"
# 行注释：这里设置 WHITE 的值，后续绘图或计算会用到。
WHITE = "#FFFFFF"
# 行注释：这里设置 ORANGE 的值，后续绘图或计算会用到。
ORANGE = "#D95319"


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


# 函数说明：计算文字宽高，帮助把文字放到合适位置。
# 行注释：这里定义 text_size 函数。
def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    box = draw.textbbox((0, 0), text, font=fnt)
    # 行注释：这里把结果返回给调用它的代码。
    return box[2] - box[0], box[3] - box[1]


# 函数说明：按多行方式绘制文字，保证中文说明不挤出卡片。
# 行注释：这里定义 draw_wrapped 函数。
def draw_wrapped(
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw: ImageDraw.ImageDraw,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    text: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    xy: tuple[int, int],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fnt: ImageFont.FreeTypeFont,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fill: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    max_width: int,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    line_gap: int = 8,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> int:
    # 行注释：这里设置 x, y 的值，后续绘图或计算会用到。
    x, y = xy
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    lines: list[str] = []
    # 行注释：这里设置 current 的值，后续绘图或计算会用到。
    current = ""
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for ch in text:
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
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for line in lines:
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.text((x, y), line, font=fnt, fill=fill)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        y += text_size(draw, line, fnt)[1] + line_gap
    # 行注释：这里把结果返回给调用它的代码。
    return y


# 函数说明：绘制圆角信息卡片，统一页面视觉样式。
# 行注释：这里定义 rounded_card 函数。
def rounded_card(draw: ImageDraw.ImageDraw, box, fill, outline="#D7DEE7", width=2, radius=28):
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# 函数说明：生成 PPT 封面背景图。
# 行注释：这里定义 cover_background 函数。
def cover_background() -> None:
    # 行注释：这里设置 w, h 的值，后续绘图或计算会用到。
    w, h = 1920, 1080
    # 行注释：这里创建新的图片画布。
    img = Image.new("RGB", (w, h), NAVY)
    # 行注释：这里设置 px 的值，后续绘图或计算会用到。
    px = img.load()
    # 行注释：这里设置 top 的值，后续绘图或计算会用到。
    top = (0, 35, 73)
    # 行注释：这里设置 bottom 的值，后续绘图或计算会用到。
    bottom = (0, 91, 141)
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for y in range(h):
        # 行注释：这里设置 t 的值，后续绘图或计算会用到。
        t = y / (h - 1)
        # 行注释：这里开始循环，逐个处理列表或数据项。
        for x in range(w):
            # 行注释：这里设置 vignette 的值，后续绘图或计算会用到。
            vignette = 1 - 0.18 * ((x - w * 0.52) ** 2 / (w * w) + (y - h * 0.42) ** 2 / (h * h))
            # 行注释：这里设置 r 的值，后续绘图或计算会用到。
            r = int((top[0] * (1 - t) + bottom[0] * t) * vignette)
            # 行注释：这里设置 g 的值，后续绘图或计算会用到。
            g = int((top[1] * (1 - t) + bottom[1] * t) * vignette)
            # 行注释：这里设置 b 的值，后续绘图或计算会用到。
            b = int((top[2] * (1 - t) + bottom[2] * t) * vignette)
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            px[x, y] = (max(0, r), max(0, g), max(0, b))

    # 行注释：这里创建新的图片画布。
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(overlay)

    # Subtle engineering grid.
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for x in range(0, w, 64):
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.line((x, 0, x, h), fill=(255, 255, 255, 18), width=1)
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for y in range(0, h, 64):
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.line((0, y, w, y), fill=(255, 255, 255, 14), width=1)

    # Ocean-wave / signal traces.
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, color in enumerate([(40, 169, 224, 92), (255, 255, 255, 54), (201, 151, 0, 80)]):
        # 行注释：这里设置 points 的值，后续绘图或计算会用到。
        points = []
        # 行注释：这里开始循环，逐个处理列表或数据项。
        for x in range(-80, w + 160, 28):
            # 行注释：这里设置 y 的值，后续绘图或计算会用到。
            y = 720 + i * 55 + math.sin(x / 150 + i * 0.9) * 42
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            points.append((x, y))
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.line(points, fill=color, width=5 if i == 0 else 3)

    # Circuit board traces and nodes.
    # 行注释：这里设置 rng 的值，后续绘图或计算会用到。
    rng = random.Random(42)
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for _ in range(38):
        # 行注释：这里设置 x 的值，后续绘图或计算会用到。
        x = rng.randint(1080, 1860)
        # 行注释：这里设置 y 的值，后续绘图或计算会用到。
        y = rng.randint(120, 880)
        # 行注释：这里设置 length 的值，后续绘图或计算会用到。
        length = rng.randint(80, 230)
        # 行注释：这里设置 elbow 的值，后续绘图或计算会用到。
        elbow = rng.randint(-90, 90)
        # 行注释：这里设置 color 的值，后续绘图或计算会用到。
        color = (255, 255, 255, rng.randint(28, 70))
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.line((x, y, x - length, y, x - length, y + elbow), fill=color, width=3)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(40, 169, 224, 100))
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d.ellipse((x - length - 6, y + elbow - 6, x - length + 6, y + elbow + 6), fill=(201, 151, 0, 120))

    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1250, 118), "HEU", font=font(210, True), fill=(255, 255, 255, 28))
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((1260, 320), "Harbin Engineering University", font=font(34), fill=(255, 255, 255, 78))

    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    # 行注释：这里把生成的图片或文件保存到磁盘。
    img.save(OUT / "00_哈工程深蓝封面背景.png", quality=95)


# 函数说明：绘制箭头，表示流程方向或信息关系。
# 行注释：这里定义 draw_arrow 函数。
def draw_arrow(draw: ImageDraw.ImageDraw, start, end, color=OCEAN, width=5):
    # 行注释：这里设置 x1, y1 的值，后续绘图或计算会用到。
    x1, y1 = start
    # 行注释：这里设置 x2, y2 的值，后续绘图或计算会用到。
    x2, y2 = end
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    # 行注释：这里设置 ang 的值，后续绘图或计算会用到。
    ang = math.atan2(y2 - y1, x2 - x1)
    # 行注释：这里设置 size 的值，后续绘图或计算会用到。
    size = 18
    # 行注释：这里设置 p1 的值，后续绘图或计算会用到。
    p1 = (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45))
    # 行注释：这里设置 p2 的值，后续绘图或计算会用到。
    p2 = (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45))
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.polygon([end, p1, p2], fill=color)


# 函数说明：生成项目整体流程图。
# 行注释：这里定义 project_flowchart 函数。
def project_flowchart() -> None:
    # 行注释：这里设置 w, h 的值，后续绘图或计算会用到。
    w, h = 1920, 1080
    # 行注释：这里创建新的图片画布。
    img = Image.new("RGB", (w, h), LIGHT)
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)

    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rectangle((0, 0, w, 150), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((92, 45), "项目流程总览：基于贝叶斯决策的 PCB 缺陷检测", font=font(48, True), fill=WHITE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((92, 106), "哈尔滨工程大学电子信息方向课程研讨 | VisA PCB 真实图像 | good / bad 二分类", font=font(24), fill="#CFE8F7")

    # 行注释：这里设置 stages 的值，后续绘图或计算会用到。
    stages = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("01", "数据获取", "VisA PCB 真实彩色图像\npcb1 - pcb4 共 4 类子集\n正常 4013 张，缺陷 400 张"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("02", "数据处理", "标签映射为 good / bad\n训练集、验证集、测试集划分\n灰度增强与尺寸归一化"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("03", "特征工程", "每张图像提取 1318 维向量\n颜色、灰度、边缘、纹理\nLBP 局部纹理 + HOG 梯度"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("04", "贝叶斯优化", "由 P(ω|x) 输出缺陷概率\nPCA 降维、高斯建模\n协方差正则化与阈值寻优"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("05", "结果评估", "Accuracy / Precision / Recall\nF1 / IoU / AUC / FPR / FNR\n横向对比、趋势与热力图"),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]

    # 行注释：这里设置 positions 的值，后续绘图或计算会用到。
    positions = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (100, 260, 500, 320),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (710, 260, 500, 320),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (1320, 260, 500, 320),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (390, 660, 520, 290),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (1030, 660, 520, 290),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里设置 colors 的值，后续绘图或计算会用到。
    colors = [OCEAN, "#2563A7", "#2E5A88", "#0B5D78", "#004488"]
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, ((num, title, body), (x, y, card_w, card_h)) in enumerate(zip(stages, positions)):
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        rounded_card(d, (x, y, x + card_w, y + card_h), WHITE, outline="#C7D3DF", width=2, radius=32)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d.ellipse((x + 28, y + 28, x + 92, y + 92), fill=colors[i])
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((x + 44, y + 43), num, font=font(22, True), fill=WHITE)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((x + 112, y + 37), title, font=font(34, True), fill=INK)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.line((x + 34, y + 120, x + card_w - 34, y + 120), fill="#DCE6EF", width=2)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw_wrapped(d, body, (x + 34, y + 150), font(25), SLATE, card_w - 68, line_gap=11)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.rectangle((x, y + card_h - 10, x + card_w, y + card_h), fill=colors[i])

    # 行注释：这里设置 arrow_pairs 的值，后续绘图或计算会用到。
    arrow_pairs = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ((600, 420), (700, 420)),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ((1210, 420), (1310, 420)),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ((1570, 590), (870, 650)),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ((910, 805), (1020, 805)),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for start, end in arrow_pairs:
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw_arrow(d, start, end, color="#7DA9C8", width=5)

    # Feedback loop
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    d.arc((250, 590, 1670, 1010), start=200, end=340, fill=GOLD, width=5)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_arrow(d, (1535, 902), (1565, 865), color=GOLD, width=5)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((520, 988), "参数分析与阈值反馈：PCA 维度、正则化 γ、后验概率阈值共同决定最终风险", font=font(25, True), fill="#6B4E00")

    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rounded_rectangle((140, 930, 1780, 1032), radius=26, fill="#E7F4FB", outline="#9CCBE2", width=2)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((188, 962), "核心思想", font=font(30, True), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((335, 965), "把 PCB 图像转化为特征向量 x，用后验概率 P(缺陷|x) 做最小风险决策，并用可解释指标验证优化是否有效。", font=font(26), fill=INK)

    # 行注释：这里把生成的图片或文件保存到磁盘。
    img.save(OUT / "13_项目流程图.png", quality=95)


# 函数说明：读取图片并等比例缩放到指定大小。
# 行注释：这里定义 load_fit 函数。
def load_fit(path: Path, size: tuple[int, int]) -> Image.Image:
    # 行注释：这里读取一张图片并准备处理。
    img = Image.open(path).convert("RGB")
    # 行注释：这里设置 target_w, target_h 的值，后续绘图或计算会用到。
    target_w, target_h = size
    # 行注释：这里设置 src_w, src_h 的值，后续绘图或计算会用到。
    src_w, src_h = img.size
    # 行注释：这里设置 scale 的值，后续绘图或计算会用到。
    scale = max(target_w / src_w, target_h / src_h)
    # 行注释：这里设置 new 的值，后续绘图或计算会用到。
    new = img.resize((int(src_w * scale), int(src_h * scale)), Image.Resampling.LANCZOS)
    # 行注释：这里设置 left 的值，后续绘图或计算会用到。
    left = (new.width - target_w) // 2
    # 行注释：这里设置 top 的值，后续绘图或计算会用到。
    top = (new.height - target_h) // 2
    # 行注释：这里把结果返回给调用它的代码。
    return new.crop((left, top, left + target_w, top + target_h))


# 函数说明：生成正常样本和缺陷样本的对比图。
# 行注释：这里定义 sample_comparison 函数。
def sample_comparison() -> None:
    # 行注释：这里设置 w, h 的值，后续绘图或计算会用到。
    w, h = 1920, 1080
    # 行注释：这里创建新的图片画布。
    img = Image.new("RGB", (w, h), LIGHT)
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rectangle((0, 0, w, 120), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((80, 35), "VisA PCB 真实图像样本归类预览", font=font(44, True), fill=WHITE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((80, 86), "按类别重新排布：左侧为正常样本，右侧为缺陷样本，避免 PPT 中样本顺序混乱", font=font(22), fill="#CFE8F7")

    # 行注释：这里设置 normal 的值，后续绘图或计算会用到。
    normal = DATA / "pcb1" / "Data" / "Images" / "Normal" / "0313.JPG"
    # 行注释：这里设置 anomaly_a 的值，后续绘图或计算会用到。
    anomaly_a = DATA / "pcb1" / "Data" / "Images" / "Anomaly" / "000.JPG"
    # 行注释：这里设置 anomaly_b 的值，后续绘图或计算会用到。
    anomaly_b = DATA / "pcb4" / "Data" / "Images" / "Anomaly" / "012.JPG"
    # 行注释：这里判断条件是否满足。
    if not anomaly_b.exists():
        # 行注释：这里设置 anomaly_b 的值，后续绘图或计算会用到。
        anomaly_b = DATA / "pcb4" / "Data" / "Images" / "Anomaly" / "000.JPG"

    # Left large normal image.
    # 行注释：这里设置 left_box 的值，后续绘图或计算会用到。
    left_box = (90, 190, 875, 900)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded_card(d, left_box, WHITE, "#BFD1DF", 2, 28)
    # 行注释：这里设置 normal_img 的值，后续绘图或计算会用到。
    normal_img = load_fit(normal, (725, 480))
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    img.paste(normal_img, (120, 270))
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rounded_rectangle((120, 218, 350, 262), radius=18, fill="#E7F4FB")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((144, 226), "正常样本 / pcb1", font=font(24, True), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((120, 775), "目标：学习良品 PCB 的颜色、纹理、边缘与结构统计分布", font=font(25), fill=SLATE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((120, 820), "决策含义：P(缺陷|x) 低于阈值，判为正常", font=font(25, True), fill=NAVY)

    # 行注释：这里设置 right_x 的值，后续绘图或计算会用到。
    right_x = 1010
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for idx, (p, label, y0) in enumerate(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            (anomaly_a, "缺陷样本 1 / pcb1", 190),
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            (anomaly_b, "缺陷样本 2 / pcb4", 555),
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ]
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ):
        # 行注释：这里设置 box 的值，后续绘图或计算会用到。
        box = (right_x, y0, 1825, y0 + 345)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        rounded_card(d, box, WHITE, "#BFD1DF", 2, 28)
        # 行注释：这里设置 crop 的值，后续绘图或计算会用到。
        crop = load_fit(p, (440, 250))
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        img.paste(crop, (right_x + 28, y0 + 70))
        # 行注释：这里设置 tag_fill 的值，后续绘图或计算会用到。
        tag_fill = "#FFF0E6" if idx == 0 else "#FFF7DB"
        # 行注释：这里设置 tag_color 的值，后续绘图或计算会用到。
        tag_color = ORANGE if idx == 0 else "#805E00"
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.rounded_rectangle((right_x + 28, y0 + 22, right_x + 280, y0 + 62), radius=17, fill=tag_fill)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((right_x + 50, y0 + 29), label, font=font(22, True), fill=tag_color)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((right_x + 505, y0 + 92), "异常纹理 / 局部结构变化", font=font(26, True), fill=INK)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw_wrapped(
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            d,
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "特征向量在后验概率中更接近缺陷类分布",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            (right_x + 505, y0 + 142),
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            font(22),
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            SLATE,
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            265,
            # 行注释：这里设置 line_gap 的值，后续绘图或计算会用到。
            line_gap=8,
        # 行注释：这里结束当前多行参数、列表或代码结构。
        )
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        d.text((right_x + 505, y0 + 236), "输出：P(缺陷|x)", font=font(28, True), fill=tag_color)

    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rounded_rectangle((300, 940, 1620, 1018), radius=24, fill="#FFFFFF", outline="#C7D3DF", width=2)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((350, 960), "说明：本页只展示分类任务中的样本组织方式；模型实际输入不是图片本身，而是由图片提取得到的 1318 维特征向量。", font=font(25), fill=INK)

    # 行注释：这里把生成的图片或文件保存到磁盘。
    img.save(OUT / "14_正常与缺陷样本归类预览.png", quality=95)


# 行注释：这里判断脚本是否被直接运行。
if __name__ == "__main__":
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    OUT.mkdir(parents=True, exist_ok=True)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    cover_background()
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    project_flowchart()
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    sample_comparison()
    # 行注释：这里在终端输出生成结果或进度信息。
    print("Generated PPT assets:")
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for name in [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "00_哈工程深蓝封面背景.png",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "13_项目流程图.png",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "14_正常与缺陷样本归类预览.png",
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]:
        # 行注释：这里在终端输出生成结果或进度信息。
        print(OUT / name)
