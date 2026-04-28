# 中文注释：生成项目总结与使用目的说明页。
# 主要流程：概括项目目标、方法链路、实验结果和实际应用价值。
# 输出结果：生成一页可直接放入演示文稿的项目总结图片。

# 行注释：这里启用较新的 Python 类型注解行为。
from __future__ import annotations

# 行注释：这里导入脚本后面需要用到的 Python 模块。
import math
# 行注释：这里导入脚本后面需要用到的 Python 模块。
from pathlib import Path

# 行注释：这里导入脚本后面需要用到的 Python 模块。
from PIL import Image, ImageDraw, ImageFont


# 行注释：这里设置 ROOT 的值，后续绘图或计算会用到。
ROOT = Path(__file__).resolve().parents[2]
# 行注释：这里设置 OUT 的值，后续绘图或计算会用到。
OUT = ROOT / "image2_report_pages" / "16_project_summary_purpose.png"

# 行注释：这里设置 W, H 的值，后续绘图或计算会用到。
W, H = 1920, 1080
# 行注释：这里设置 NAVY 的值，后续绘图或计算会用到。
NAVY = "#082A4A"
# 行注释：这里设置 NAVY2 的值，后续绘图或计算会用到。
NAVY2 = "#003B73"
# 行注释：这里设置 BLUE 的值，后续绘图或计算会用到。
BLUE = "#0A57A3"
# 行注释：这里设置 ORANGE 的值，后续绘图或计算会用到。
ORANGE = "#E87511"
# 行注释：这里设置 GOLD 的值，后续绘图或计算会用到。
GOLD = "#C99700"
# 行注释：这里设置 GREEN 的值，后续绘图或计算会用到。
GREEN = "#168A5B"
# 行注释：这里设置 RED 的值，后续绘图或计算会用到。
RED = "#C7372F"
# 行注释：这里设置 INK 的值，后续绘图或计算会用到。
INK = "#122033"
# 行注释：这里设置 MUTED 的值，后续绘图或计算会用到。
MUTED = "#5C6B7A"
# 行注释：这里设置 LINE 的值，后续绘图或计算会用到。
LINE = "#BDD0E2"
# 行注释：这里设置 BG 的值，后续绘图或计算会用到。
BG = "#F6FAFD"
# 行注释：这里设置 WHITE 的值，后续绘图或计算会用到。
WHITE = "#FFFFFF"
# 行注释：这里设置 PALE_BLUE 的值，后续绘图或计算会用到。
PALE_BLUE = "#EAF5FF"
# 行注释：这里设置 PALE_GOLD 的值，后续绘图或计算会用到。
PALE_GOLD = "#FFF7E3"
# 行注释：这里设置 PALE_GREEN 的值，后续绘图或计算会用到。
PALE_GREEN = "#EAF8F1"
# 行注释：这里设置 PALE_ORANGE 的值，后续绘图或计算会用到。
PALE_ORANGE = "#FFF0E2"


# 函数说明：加载中文字体，供标题、正文和数字使用。
# 行注释：这里定义 fnt 函数。
def fnt(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
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
        if Path(item).exists():
            # 行注释：这里把结果返回给调用它的代码。
            return ImageFont.truetype(item, size=size)
    # 行注释：这里把结果返回给调用它的代码。
    return ImageFont.load_default()


# 函数说明：计算文字宽高，帮助把文字放到合适位置。
# 行注释：这里定义 text_size 函数。
def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    box = draw.textbbox((0, 0), text, font=font)
    # 行注释：这里把结果返回给调用它的代码。
    return box[2] - box[0], box[3] - box[1]


# 函数说明：把长句按最大宽度拆成多行，避免文字溢出。
# 行注释：这里定义 wrap 函数。
def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
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
        # 行注释：这里设置 trial 的值，后续绘图或计算会用到。
        trial = current + ch
        # 行注释：这里判断条件是否满足。
        if text_size(draw, trial, font)[0] <= max_w:
            # 行注释：这里设置 current 的值，后续绘图或计算会用到。
            current = trial
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
    text: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    xy: tuple[int, int],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    font: ImageFont.FreeTypeFont,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fill: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    max_w: int,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    gap: int = 8,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> int:
    # 行注释：这里设置 x, y 的值，后续绘图或计算会用到。
    x, y = xy
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for line in wrap(draw, text, font, max_w):
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.text((x, y), line, font=font, fill=fill)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        y += text_size(draw, line, font)[1] + gap
    # 行注释：这里把结果返回给调用它的代码。
    return y


# 函数说明：绘制圆角矩形，作为信息卡片或内容面板。
# 行注释：这里定义 rounded 函数。
def rounded(
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw: ImageDraw.ImageDraw,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    box: tuple[int, int, int, int],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fill: str = WHITE,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    outline: str = LINE,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    width: int = 2,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    radius: int = 24,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> None:
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# 函数说明：绘制箭头，表示流程方向或信息关系。
# 行注释：这里定义 arrow 函数。
def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str = BLUE, width: int = 4) -> None:
    # 行注释：这里设置 x1, y1 的值，后续绘图或计算会用到。
    x1, y1 = start
    # 行注释：这里设置 x2, y2 的值，后续绘图或计算会用到。
    x2, y2 = end
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    # 行注释：这里设置 angle 的值，后续绘图或计算会用到。
    angle = math.atan2(y2 - y1, x2 - x1)
    # 行注释：这里设置 length 的值，后续绘图或计算会用到。
    length = 16
    # 行注释：这里设置 points 的值，后续绘图或计算会用到。
    points = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (x2, y2),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (x2 + length * math.cos(angle + math.pi * 0.82), y2 + length * math.sin(angle + math.pi * 0.82)),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (x2 + length * math.cos(angle - math.pi * 0.82), y2 + length * math.sin(angle - math.pi * 0.82)),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.polygon(points, fill=color)


# 函数说明：绘制单个指标卡片。
# 行注释：这里定义 metric_card 函数。
def metric_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], value: str, label: str, color: str) -> None:
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, box, WHITE, "#CADAE8", 2, 18)
    # 行注释：这里设置 x1, y1, _, _ 的值，后续绘图或计算会用到。
    x1, y1, _, _ = box
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 26, y1 + 18), value, font=fnt(34, True), fill=color)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 27, y1 + 69), label, font=fnt(19), fill=MUTED)


# 函数说明：脚本入口，按顺序调用前面的函数生成最终文件。
# 行注释：这里定义 main 函数。
def main() -> None:
    # 行注释：这里创建新的图片画布。
    img = Image.new("RGB", (W, H), BG)
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    draw = ImageDraw.Draw(img)

    # 行注释：这里开始循环，逐个处理列表或数据项。
    for y in range(160):
        # 行注释：这里设置 ratio 的值，后续绘图或计算会用到。
        ratio = y / 160
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.line((0, y, W, y), fill=(int(8 + ratio * 2), int(42 + ratio * 12), int(74 + ratio * 24)))
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rectangle((0, 154, W, 160), fill="#F0A500")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((56, 34), "项目总结：为什么用贝叶斯决策做 PCB 缺陷检测", font=fnt(46, True), fill=WHITE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((58, 98), "目的：把“是否有缺陷”的硬判断，转化为可解释、可调阈值、可评估风险的概率决策过程", font=fnt(25), fill="#D7ECFF")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((1828, 40), "哈尔滨工程大学", font=fnt(26, True), fill=WHITE, anchor="ra")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((1828, 82), "Pattern Recognition Seminar", font=fnt(21), fill="#D7ECFF", anchor="ra")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((1828, 118), "周玉峰 2023080502", font=fnt(22, True), fill="#FFC44D", anchor="ra")

    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, (54, 196, 1866, 326), fill=WHITE, outline="#9FC4E8", width=2, radius=22)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.ellipse((92, 226, 164, 298), fill=NAVY2)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((128, 261), "目", font=fnt(31, True), fill=WHITE, anchor="mm")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((195, 218), "使用贝叶斯决策的目的", font=fnt(31, True), fill=NAVY2)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_wrapped(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "在真实 PCB 质检中，缺陷样本少、误报和漏报代价不同。贝叶斯方法能够输出 P(缺陷|x)，再根据阈值 T 和损失函数选择风险最小的动作，而不是只给一个无法解释的标签。",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (195, 263),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        fnt(24),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        INK,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        1585,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        8,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )

    # 行注释：这里设置 flow_y 的值，后续绘图或计算会用到。
    flow_y = 405
    # 行注释：这里设置 nodes 的值，后续绘图或计算会用到。
    nodes = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("真实 PCB 图像", "normal / anomaly\n真实彩色样本", PALE_BLUE, BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("1318 维特征", "颜色、纹理、边缘\nLBP、HOG、GLCM", PALE_GOLD, GOLD),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("贝叶斯后验概率", "计算 P(缺陷|x)\n保留不确定性", PALE_GREEN, GREEN),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("阈值与风险决策", "调节 T\n权衡误报和漏报", PALE_ORANGE, ORANGE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("可解释结果", "指标、曲线、混淆矩阵\n支撑汇报结论", "#EEF2FF", BLUE),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里设置 x0, box_w, box_h, gap 的值，后续绘图或计算会用到。
    x0, box_w, box_h, gap = 80, 300, 180, 70
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, (title, body, fill, color) in enumerate(nodes):
        # 行注释：这里设置 x 的值，后续绘图或计算会用到。
        x = x0 + i * (box_w + gap)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        rounded(draw, (x, flow_y, x + box_w, flow_y + box_h), fill=fill, outline="#AFC6D9", width=2, radius=20)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.text((x + 24, flow_y + 24), f"{i + 1:02d}", font=fnt(25, True), fill=color)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.text((x + 78, flow_y + 25), title, font=fnt(26, True), fill=INK)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.line((x + 24, flow_y + 70, x + box_w - 24, flow_y + 70), fill="#D5E1EB", width=2)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw_wrapped(draw, body, (x + 24, flow_y + 92), fnt(21), MUTED, box_w - 48, 7)
        # 行注释：这里判断条件是否满足。
        if i < len(nodes) - 1:
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            arrow(draw, (x + box_w + 10, flow_y + box_h // 2), (x + box_w + gap - 18, flow_y + box_h // 2), "#88AFCB", 4)

    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, (64, 645, 700, 915), fill=WHITE, outline=LINE, width=2, radius=22)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((96, 678), "本项目解决什么问题？", font=fnt(30, True), fill=NAVY2)
    # 行注释：这里设置 items 的值，后续绘图或计算会用到。
    items = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("缺陷样本少", "4013 张正常样本对 400 张缺陷样本，类别明显不均衡。"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("判断要可解释", "输出 P(缺陷|x)，说明缺陷可能性，而不只是给标签。"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("风险要可调", "通过阈值 T 权衡误报与漏报，适配不同质检代价。"),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里设置 y 的值，后续绘图或计算会用到。
    y = 732
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for title, body in items:
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.rounded_rectangle((96, y + 4, 108, y + 16), radius=4, fill=BLUE)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.text((126, y - 2), title, font=fnt(23, True), fill=INK)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw_wrapped(draw, body, (126, y + 29), fnt(18), MUTED, 505, 4)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        y += 64

    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, (744, 645, 1856, 915), fill=WHITE, outline=LINE, width=2, radius=22)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((780, 678), "最终形成的结论", font=fnt(30, True), fill=NAVY2)
    # 行注释：这里设置 conclusion 的值，后续绘图或计算会用到。
    conclusion = (
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "在贝叶斯框架内，PCA 降维、Gaussian 建模、Gamma 正则化和后验阈值优化共同提升了 PCB 缺陷检测效果。"
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "最优 Bayes-4 模型在测试集上 Accuracy=0.9184，F1=0.5424，AUC=0.8986。"
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_wrapped(draw, conclusion, (780, 727), fnt(23), INK, 1015, 10)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    metric_card(draw, (790, 807, 1015, 876), "0.9184", "Accuracy", BLUE)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    metric_card(draw, (1040, 807, 1265, 876), "0.5424", "F1-score", ORANGE)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    metric_card(draw, (1290, 807, 1515, 876), "0.8986", "AUC", GREEN)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    metric_card(draw, (1540, 807, 1765, 876), "0.0432", "FPR", RED)

    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, (64, 940, 1856, 1020), fill=NAVY2, outline=NAVY2, width=0, radius=18)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((100, 963), "一句话总结：", font=fnt(27, True), fill="#FFD46B")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_wrapped(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "本项目使用贝叶斯决策，是为了让 PCB 缺陷检测既能给出概率依据，又能根据质量风险调节判别阈值，从而实现可解释、可优化、可复现实验的检测流程。",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (275, 958),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        fnt(24, True),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        WHITE,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        1510,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        6,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rectangle((0, 1072, W, H), fill=BLUE)

    # 行注释：这里执行当前语句，推进这一小步逻辑。
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # 行注释：这里把生成的图片或文件保存到磁盘。
    img.save(OUT, quality=96)
    # 行注释：这里在终端输出生成结果或进度信息。
    print(OUT)


# 行注释：这里判断脚本是否被直接运行。
if __name__ == "__main__":
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    main()
