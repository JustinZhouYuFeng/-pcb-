# 中文注释：用 Python 生成贝叶斯报告中需要的中文信息图。
# 主要流程：使用 PIL 绘制标题、公式、流程和结果说明，形成统一视觉风格。
# 输出结果：保存为图片后插入 PPT 或报告页面。

# 行注释：这里启用较新的 Python 类型注解行为。
from __future__ import annotations

# 行注释：这里导入脚本后面需要用到的 Python 模块。
import csv
# 行注释：这里导入脚本后面需要用到的 Python 模块。
from pathlib import Path
# 行注释：这里导入脚本后面需要用到的 Python 模块。
from textwrap import wrap

# 行注释：这里导入脚本后面需要用到的 Python 模块。
from PIL import Image, ImageDraw, ImageFont


# 行注释：这里设置 ROOT 的值，后续绘图或计算会用到。
ROOT = Path(__file__).resolve().parents[2]
# 行注释：这里设置 CSV_PATH 的值，后续绘图或计算会用到。
CSV_PATH = ROOT / "results" / "visa_pcb" / "bayes_optimization_comparison.csv"
# 行注释：这里设置 OUT_DIR 的值，后续绘图或计算会用到。
OUT_DIR = ROOT / "results" / "figures"
# 行注释：这里设置 OUT_BASELINE 的值，后续绘图或计算会用到。
OUT_BASELINE = OUT_DIR / "13_朴素贝叶斯基准诊断信息图.png"
# 行注释：这里设置 OUT_CODE 的值，后续绘图或计算会用到。
OUT_CODE = OUT_DIR / "14_贝叶斯优化过程代码体现图.png"

# 行注释：这里设置 W, H 的值，后续绘图或计算会用到。
W, H = 1920, 1080
# 行注释：这里设置 NAVY 的值，后续绘图或计算会用到。
NAVY = "#003B73"
# 行注释：这里设置 NAVY_DARK 的值，后续绘图或计算会用到。
NAVY_DARK = "#08243D"
# 行注释：这里设置 BLUE 的值，后续绘图或计算会用到。
BLUE = "#004488"
# 行注释：这里设置 BLUE2 的值，后续绘图或计算会用到。
BLUE2 = "#1B95C9"
# 行注释：这里设置 PALE_BLUE 的值，后续绘图或计算会用到。
PALE_BLUE = "#E8F5FB"
# 行注释：这里设置 PALE_GREEN 的值，后续绘图或计算会用到。
PALE_GREEN = "#E8F7EF"
# 行注释：这里设置 PALE_ORANGE 的值，后续绘图或计算会用到。
PALE_ORANGE = "#FFF1E8"
# 行注释：这里设置 PALE_GOLD 的值，后续绘图或计算会用到。
PALE_GOLD = "#FFF7D8"
# 行注释：这里设置 ORANGE 的值，后续绘图或计算会用到。
ORANGE = "#D95319"
# 行注释：这里设置 RED 的值，后续绘图或计算会用到。
RED = "#B22222"
# 行注释：这里设置 GOLD 的值，后续绘图或计算会用到。
GOLD = "#C99700"
# 行注释：这里设置 GREEN 的值，后续绘图或计算会用到。
GREEN = "#258A52"
# 行注释：这里设置 INK 的值，后续绘图或计算会用到。
INK = "#0F172A"
# 行注释：这里设置 MUTED 的值，后续绘图或计算会用到。
MUTED = "#64748B"
# 行注释：这里设置 LINE 的值，后续绘图或计算会用到。
LINE = "#C7D5E3"
# 行注释：这里设置 BG 的值，后续绘图或计算会用到。
BG = "#F4F8FB"
# 行注释：这里设置 WHITE 的值，后续绘图或计算会用到。
WHITE = "#FFFFFF"
# 行注释：这里设置 CODE_BG 的值，后续绘图或计算会用到。
CODE_BG = "#0B1F33"
# 行注释：这里设置 CODE_FG 的值，后续绘图或计算会用到。
CODE_FG = "#E7F0FA"


# 函数说明：加载中文字体，保证图片里的中文能正常显示。
# 行注释：这里定义 font 函数。
def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    # 行注释：这里判断条件是否满足。
    if mono:
        # 行注释：这里设置 candidates 的值，后续绘图或计算会用到。
        candidates = [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf"]
    # 行注释：这里处理其他情况。
    else:
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


# 函数说明：绘制圆角矩形，作为信息卡片或内容面板。
# 行注释：这里定义 rounded 函数。
def rounded(draw: ImageDraw.ImageDraw, box, fill=WHITE, outline=LINE, width=2, radius=24) -> None:
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# 函数说明：把文字放在指定矩形区域正中间。
# 行注释：这里定义 center_text 函数。
def center_text(draw: ImageDraw.ImageDraw, box, text: str, fnt, fill=INK) -> None:
    # 行注释：这里设置 x1, y1, x2, y2 的值，后续绘图或计算会用到。
    x1, y1, x2, y2 = box
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    bbox = draw.textbbox((0, 0), text, font=fnt)
    # 行注释：这里设置 tw, th 的值，后续绘图或计算会用到。
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - 1), text, font=fnt, fill=fill)


# 函数说明：绘制页面顶部标题栏和副标题。
# 行注释：这里定义 draw_header 函数。
def draw_header(draw: ImageDraw.ImageDraw, title: str, subtitle: str) -> None:
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rectangle((0, 0, W, 128), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((76, 30), title, font=font(42, True), fill=WHITE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((78, 86), subtitle, font=font(23), fill="#D4EBF8")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rounded_rectangle((1510, 39, 1840, 88), radius=24, fill="#0A4B82")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    center_text(draw, (1510, 39, 1840, 88), "HEU | PCB Bayes", font(18, True), WHITE)


# 函数说明：读取实验结果 CSV，供图表页面使用。
# 行注释：这里定义 load_rows 函数。
def load_rows() -> list[dict[str, str]]:
    # 行注释：这里用上下文管理器安全地打开或处理资源。
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        # 行注释：这里把结果返回给调用它的代码。
        return list(csv.DictReader(f))


# 函数说明：根据阶段名称取出对应实验结果。
# 行注释：这里定义 row_by_stage 函数。
def row_by_stage(rows: list[dict[str, str]], stage: str) -> dict[str, str]:
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for row in rows:
        # 行注释：这里判断条件是否满足。
        if row["Stage"] == stage:
            # 行注释：这里把结果返回给调用它的代码。
            return row
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    raise RuntimeError(f"{stage} not found")


# 函数说明：绘制箭头，表示流程方向或信息关系。
# 行注释：这里定义 draw_arrow 函数。
def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color="#8CA6BD") -> None:
    # 行注释：这里设置 x1, y1 的值，后续绘图或计算会用到。
    x1, y1 = start
    # 行注释：这里设置 x2, y2 的值，后续绘图或计算会用到。
    x2, y2 = end
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.line((x1, y1, x2, y2), fill=color, width=3)
    # 行注释：这里判断条件是否满足。
    if x2 >= x1:
        # 行注释：这里设置 tip 的值，后续绘图或计算会用到。
        tip = [(x2, y2), (x2 - 14, y2 - 8), (x2 - 14, y2 + 8)]
    # 行注释：这里处理其他情况。
    else:
        # 行注释：这里设置 tip 的值，后续绘图或计算会用到。
        tip = [(x2, y2), (x2 + 14, y2 - 8), (x2 + 14, y2 + 8)]
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.polygon(tip, fill=color)


# 函数说明：绘制环形指标图，突出准确率、召回率等关键数值。
# 行注释：这里定义 metric_ring 函数。
def metric_ring(
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw: ImageDraw.ImageDraw,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    box: tuple[int, int, int, int],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    label: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    value: float,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    note: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    color: str,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> None:
    # 行注释：这里设置 x1, y1, x2, y2 的值，后续绘图或计算会用到。
    x1, y1, x2, y2 = box
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, box, WHITE, LINE, 2, 22)
    # 行注释：这里设置 cx, cy 的值，后续绘图或计算会用到。
    cx, cy = x1 + 76, y1 + 76
    # 行注释：这里设置 r 的值，后续绘图或计算会用到。
    r = 52
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline="#DDE8F2", width=14)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.arc((cx - r, cy - r, cx + r, cy + r), start=-90, end=-90 + 360 * value, fill=color, width=14)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    center_text(draw, (cx - 48, cy - 24, cx + 48, cy + 24), f"{value:.3f}", font(21, True), color)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 150, y1 + 34), label, font=font(21, True), fill=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 150, y1 + 72), note, font=font(17), fill=MUTED)


# 函数说明：绘制概念解释卡片，帮助读者理解术语。
# 行注释：这里定义 definition_card 函数。
def definition_card(
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw: ImageDraw.ImageDraw,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    box: tuple[int, int, int, int],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    title: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    formula: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    meaning: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    color: str,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> None:
    # 行注释：这里设置 x1, y1, x2, y2 的值，后续绘图或计算会用到。
    x1, y1, x2, y2 = box
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, box, WHITE, LINE, 2, 18)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.ellipse((x1 + 18, y1 + 23, x1 + 38, y1 + 43), fill=color)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 50, y1 + 17), title, font=font(21, True), fill=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 20, y1 + 58), formula, font=font(17, True), fill=color)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 20, y1 + 88), meaning, font=font(17), fill=MUTED)


# 函数说明：绘制代码展示框，让实现思路更容易读。
# 行注释：这里定义 code_box 函数。
def code_box(
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw: ImageDraw.ImageDraw,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    box: tuple[int, int, int, int],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    title: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    lines: list[str],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    accent: str = BLUE2,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> None:
    # 行注释：这里设置 x1, y1, x2, y2 的值，后续绘图或计算会用到。
    x1, y1, x2, y2 = box
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, box, WHITE, LINE, 2, 20)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rounded_rectangle((x1 + 16, y1 + 16, x2 - 16, y1 + 54), radius=16, fill=accent)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 32, y1 + 24), title, font=font(19, True), fill=WHITE)
    # 行注释：这里设置 code_area 的值，后续绘图或计算会用到。
    code_area = (x1 + 16, y1 + 68, x2 - 16, y2 - 16)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rounded_rectangle(code_area, radius=14, fill=CODE_BG)
    # 行注释：这里设置 ty 的值，后续绘图或计算会用到。
    ty = code_area[1] + 15
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for line in lines:
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.text((code_area[0] + 18, ty), line, font=font(17, mono=True), fill=CODE_FG)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ty += 27


# 函数说明：生成基础贝叶斯实验结果说明页。
# 行注释：这里定义 draw_baseline_page 函数。
def draw_baseline_page(rows: list[dict[str, str]]) -> None:
    # 行注释：这里设置 row 的值，后续绘图或计算会用到。
    row = row_by_stage(rows, "Bayes-0")
    # 行注释：这里创建新的图片画布。
    img = Image.new("RGB", (W, H), BG)
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    draw = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_header(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "Bayes-0 原始朴素贝叶斯：基准效果诊断",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "无 PCA、无协方差建模、无阈值优化；默认以 P(bad|x) >= 0.5 判为缺陷",
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )

    # Decision logic.
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, (78, 158, 1140, 380), WHITE, LINE, 2, 24)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((108, 186), "朴素贝叶斯判决逻辑", font=font(30, True), fill=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((108, 230), "把一张 PCB 图像表示为特征向量 x，分别计算它属于正常类和缺陷类的后验概率。", font=font(21), fill=MUTED)
    # 行注释：这里设置 nodes 的值，后续绘图或计算会用到。
    nodes = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ((120, 284, 280, 342), "PCB 图像", "真实彩色样本", PALE_BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ((340, 284, 535, 342), "1318 维特征", "颜色/纹理/HOG/LBP", PALE_GOLD),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ((600, 258, 835, 318), "P(good|x)", "正常后验概率", PALE_GREEN),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ((600, 326, 835, 366), "P(bad|x)", "缺陷后验概率", PALE_ORANGE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ((910, 284, 1078, 342), "阈值 0.5", "后验概率判决", "#EEF6FF"),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for box, title, subtitle, fill in nodes:
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        rounded(draw, box, fill, "#AFC4D5", 2, 18)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        center_text(draw, (box[0], box[1] + 5, box[2], box[1] + 34), title, font(20, True), INK)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        center_text(draw, (box[0], box[1] + 30, box[2], box[3] - 4), subtitle, font(15), MUTED)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_arrow(draw, (280, 313), (338, 313))
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_arrow(draw, (535, 313), (598, 288))
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_arrow(draw, (535, 313), (598, 345))
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_arrow(draw, (835, 288), (908, 313))
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_arrow(draw, (835, 345), (908, 313))
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((108, 350), "公式：P(ωk|x) ∝ P(ωk) · ∏ p(xi|ωk)，其中“朴素”指条件独立假设。", font=font(20, True), fill=NAVY)

    # Confusion matrix.
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, (1180, 158, 1842, 380), WHITE, LINE, 2, 24)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((1212, 186), "混淆矩阵：模型把样本判成了什么", font=font(28, True), fill=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((1214, 228), "行是真实类别，列是预测类别；normal/anomaly 二分类。", font=font(19), fill=MUTED)
    # 行注释：这里设置 cm_x, cm_y, cell 的值，后续绘图或计算会用到。
    cm_x, cm_y, cell = 1282, 260, 76
    # 行注释：这里设置 cm 的值，后续绘图或计算会用到。
    cm = [[int(row["TN"]), int(row["FP"])], [int(row["FN"]), int(row["TP"])]]
    # 行注释：这里设置 labels_x 的值，后续绘图或计算会用到。
    labels_x = ["预测正常", "预测缺陷"]
    # 行注释：这里设置 labels_y 的值，后续绘图或计算会用到。
    labels_y = ["真实正常", "真实缺陷"]
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for j, label in enumerate(labels_x):
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        center_text(draw, (cm_x + j * cell, cm_y - 30, cm_x + (j + 1) * cell, cm_y - 2), label, font(16), INK)
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, label in enumerate(labels_y):
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.text((cm_x - 94, cm_y + i * cell + 24), label, font=font(16), fill=INK)
    # 行注释：这里设置 maxv 的值，后续绘图或计算会用到。
    maxv = max(max(cm[0]), max(cm[1]))
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i in range(2):
        # 行注释：这里开始循环，逐个处理列表或数据项。
        for j in range(2):
            # 行注释：这里设置 v 的值，后续绘图或计算会用到。
            v = cm[i][j]
            # 行注释：这里设置 intensity 的值，后续绘图或计算会用到。
            intensity = int(235 - 150 * v / maxv)
            # 行注释：这里设置 fill 的值，后续绘图或计算会用到。
            fill = f"#{intensity:02x}{intensity + 12:02x}{min(255, intensity + 35):02x}"
            # 行注释：这里判断条件是否满足。
            if i == 0 and j == 0:
                # 行注释：这里设置 fill 的值，后续绘图或计算会用到。
                fill = "#173F78"
            # 行注释：这里在图片画布上绘制文字、线条或形状。
            draw.rectangle((cm_x + j * cell, cm_y + i * cell, cm_x + (j + 1) * cell, cm_y + (i + 1) * cell), fill=fill)
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            center_text(
                # 行注释：这里执行当前语句，推进这一小步逻辑。
                draw,
                # 行注释：这里执行当前语句，推进这一小步逻辑。
                (cm_x + j * cell, cm_y + i * cell, cm_x + (j + 1) * cell, cm_y + (i + 1) * cell),
                # 行注释：这里执行当前语句，推进这一小步逻辑。
                str(v),
                # 行注释：这里执行当前语句，推进这一小步逻辑。
                font(26, True),
                # 行注释：这里执行当前语句，推进这一小步逻辑。
                WHITE if v > maxv * 0.5 else INK,
            # 行注释：这里结束当前多行参数、列表或代码结构。
            )
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((1505, 272), f"FP={int(row['FP'])}：正常板被误判为缺陷", font=font(18), fill=ORANGE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((1505, 315), f"FN={int(row['FN'])}：缺陷板被误判为正常", font=font(18), fill=RED)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((1505, 348), "FN 在质检中更危险，后续可用阈值/风险控制。", font=font(16), fill=MUTED)

    # Metric rings.
    # 行注释：这里设置 metrics 的值，后续绘图或计算会用到。
    metrics = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Accuracy 准确率", float(row["TestAccuracy"]), "整体判对比例", BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Precision 精确率", float(row["TestPrecision"]), "预测缺陷中真缺陷比例", ORANGE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Recall 召回率", float(row["TestRecall"]), "真实缺陷被检出比例", BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("F1 值", float(row["TestF1"]), "精确率与召回率的平衡", RED),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("AUC", float(row["TestAUC"]), "不固定阈值的排序能力", GREEN),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("IoU", float(row["TestIoU"]), "缺陷类集合重合程度", GOLD),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((78, 416), "基准指标快照", font=font(30, True), fill=INK)
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, metric in enumerate(metrics):
        # 行注释：这里设置 x 的值，后续绘图或计算会用到。
        x = 78 + (i % 3) * 600
        # 行注释：这里设置 y 的值，后续绘图或计算会用到。
        y = 462 + (i // 3) * 150
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        metric_ring(draw, (x, y, x + 552, y + 126), *metric)

    # Error tradeoff.
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, (78, 752, 1842, 830), PALE_GOLD, "#DDBD52", 2, 20)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((110, 774), "错误率解释", font=font(23, True), fill=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((282, 774), f"FPR 误报率 = {float(row['TestFPR']):.3f}：正常板被判为缺陷，增加复检成本。", font=font(21), fill=ORANGE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((980, 774), f"FNR 漏报率 = {float(row['TestFNR']):.3f}：缺陷板被判为正常，带来质量风险。", font=font(21), fill=RED)

    # 行注释：这里设置 definitions 的值，后续绘图或计算会用到。
    definitions = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Accuracy", "(TP+TN)/(TP+FP+TN+FN)", "所有样本中判对的比例。", BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Precision", "TP/(TP+FP)", "判为缺陷的样本里，真正缺陷占比。", ORANGE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Recall", "TP/(TP+FN)", "真实缺陷中，被成功检出的比例。", BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("F1-score", "2PR/(P+R)", "精确率和召回率的调和平均。", RED),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("FPR", "FP/(FP+TN)", "正常样本被误报为缺陷的比例。", ORANGE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("FNR", "FN/(FN+TP)", "缺陷样本被漏判为正常的比例。", RED),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("IoU", "TP/(TP+FP+FN)", "缺陷类预测集合与真实集合重合度。", GOLD),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("AUC", "ROC 曲线下面积", "衡量后验概率对两类样本的排序能力。", GREEN),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, item in enumerate(definitions):
        # 行注释：这里设置 x 的值，后续绘图或计算会用到。
        x = 78 + (i % 4) * 450
        # 行注释：这里设置 y 的值，后续绘图或计算会用到。
        y = 858 + (i // 4) * 96
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        definition_card(draw, (x, y, x + 410, y + 78), *item)

    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((78, 1040), "结论：Bayes-0 的 AUC 尚可，但 Precision、F1、IoU 偏低，说明原始朴素贝叶斯有概率排序基础，但直接判决质量不足。", font=font(20, True), fill=NAVY)
    # 行注释：这里把生成的图片或文件保存到磁盘。
    img.save(OUT_BASELINE, quality=95)


# 函数说明：绘制模型优化阶段卡片。
# 行注释：这里定义 stage_card 函数。
def stage_card(
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw: ImageDraw.ImageDraw,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    box: tuple[int, int, int, int],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    stage: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    title: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    detail: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    f1: float,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    auc: float,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fill: str,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> None:
    # 行注释：这里设置 x1, y1, x2, y2 的值，后续绘图或计算会用到。
    x1, y1, x2, y2 = box
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, box, fill, "#AFC4D5", 2, 20)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 20, y1 + 18), stage, font=font(23, True), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 20, y1 + 54), title, font=font(18, True), fill=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 20, y1 + 84), detail, font=font(15), fill=MUTED)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 20, y2 - 40), f"F1={f1:.3f}  AUC={auc:.3f}", font=font(17, True), fill=BLUE)


# 函数说明：绘制参数说明卡片。
# 行注释：这里定义 param_card 函数。
def param_card(draw: ImageDraw.ImageDraw, box, title: str, value: str, detail: str, color: str) -> None:
    # 行注释：这里设置 x1, y1, x2, y2 的值，后续绘图或计算会用到。
    x1, y1, x2, y2 = box
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, box, WHITE, LINE, 2, 18)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 18, y1 + 14), title, font=font(19, True), fill=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 18, y1 + 47), value, font=font(24, True), fill=color)
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for idx, line in enumerate(wrap(detail, width=20)):
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        draw.text((x1 + 18, y1 + 86 + idx * 24), line, font=font(16), fill=MUTED)


# 函数说明：生成代码流程说明页。
# 行注释：这里定义 draw_code_page 函数。
def draw_code_page(rows: list[dict[str, str]]) -> None:
    # 行注释：这里创建新的图片画布。
    img = Image.new("RGB", (W, H), BG)
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    draw = ImageDraw.Draw(img)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_header(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "贝叶斯优化过程：代码如何体现",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "优化没有跳出贝叶斯框架，而是在特征空间、概率建模和决策阈值三层逐步改进",
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )

    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, (78, 156, 1842, 246), PALE_BLUE, "#A8D4E8", 2, 24)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((112, 180), "主代码文件", font=font(24, True), fill=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((270, 181), "code/03_bayes_model/run_visa_bayes_optimization_comparison.m", font=font(21, mono=True), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((112, 216), "核心思想：同一训练/验证/测试划分下，依次叠加 PCA、协方差建模、正则化和后验阈值，再用同一套指标评价。", font=font(19), fill=MUTED)

    # Code boxes.
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    code_box(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (78, 280, 570, 488),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "1. 只用训练集统计量做标准化",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "[XTrainZ, prepBase] = standardize_train(XTrain);",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "XValZ  = standardize_apply(XVal,  prepBase);",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "XTestZ = standardize_apply(XTest, prepBase);",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        BLUE2,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    code_box(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (612, 280, 1104, 488),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "2. PCA 压缩特征空间",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "[coeff, ~] = pca(XTrainZ);",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "bestDim = 80;",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "XTrainP = XTrainZ * coeff(:,1:bestDim);",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "XTestP  = XTestZ  * coeff(:,1:bestDim);",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        GOLD,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    code_box(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (1146, 280, 1842, 488),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "3. 贝叶斯概率建模逐步增强",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "fitcnb(..., 'DistributionNames','normal')",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "fitcdiscr(..., 'DiscrimType','pseudoQuadratic')",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "fitcdiscr(..., 'DiscrimType','linear', 'Gamma',0.1)",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ORANGE,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    code_box(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (78, 520, 870, 720),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "4. 输出缺陷后验概率 P(bad|x)",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "[~, scoreRaw] = predict(model, XTest);",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "scoreAnomaly = positive_score(model, scoreRaw);",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "testMetrics = classification_metrics(YTest, pred, scoreAnomaly, 'anomaly');",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        GREEN,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    code_box(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (912, 520, 1842, 720),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "5. 阈值优化体现最小风险思想",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        [
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "bestThreshold = 0.75;",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "labels = repmat('normal', numel(scoreAnomaly), 1);",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "labels(scoreAnomaly >= threshold) = 'anomaly';",
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            "yPred = categorical(labels, ['normal','anomaly']);",
        # 行注释：这里结束当前多行参数、列表或代码结构。
        ],
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        RED,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )

    # Parameter meaning.
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((78, 752), "关键参数含义", font=font(28, True), fill=INK)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    param_card(draw, (78, 790, 408, 936), "PCA 维度 bestDim", "80", "从 1318 维手工特征中保留主要变化方向，降低冗余与噪声。", BLUE)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    param_card(draw, (438, 790, 768, 936), "Gamma 正则化", "0.1", "约束协方差估计，避免高维小样本下矩阵不稳定。", ORANGE)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    param_card(draw, (798, 790, 1128, 936), "后验阈值 Threshold", "0.75", "控制 P(bad|x) 多大时判为缺陷，用来平衡误报和漏报。", RED)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    param_card(draw, (1158, 790, 1488, 936), "Prior = uniform", "均匀先验", "避免训练集中正常样本过多导致模型天然偏向 normal。", GREEN)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    param_card(draw, (1518, 790, 1842, 936), "DiscrimType", "决策面形式", "pseudoQuadratic/linear 表示不同高斯判别边界。", GOLD)

    # Stage timeline.
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((78, 965), "优化阶段对应关系", font=font(25, True), fill=INK)
    # 行注释：这里设置 stage_colors 的值，后续绘图或计算会用到。
    stage_colors = [WHITE, PALE_BLUE, PALE_GOLD, PALE_GREEN, PALE_ORANGE]
    # 行注释：这里设置 stage_titles 的值，后续绘图或计算会用到。
    stage_titles = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Bayes-0", "原始朴素贝叶斯", "全特征 + 默认阈值"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Bayes-1", "PCA 优化", "80 维主成分"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Bayes-2", "高斯建模", "协方差相关性"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Bayes-3", "正则化", "Gamma=0.1"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("Bayes-4", "阈值优化", "Threshold=0.75"),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里设置 x 的值，后续绘图或计算会用到。
    x = 310
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, (stage, title, detail) in enumerate(stage_titles):
        # 行注释：这里设置 row 的值，后续绘图或计算会用到。
        row = row_by_stage(rows, stage)
        # 行注释：这里设置 box 的值，后续绘图或计算会用到。
        box = (x + i * 300, 955, x + i * 300 + 260, 1060)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        stage_card(draw, box, stage, title, detail, float(row["TestF1"]), float(row["TestAUC"]), stage_colors[i])
        # 行注释：这里判断条件是否满足。
        if i < 4:
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            draw_arrow(draw, (box[2] + 4, 1008), (box[2] + 36, 1008))

    # 行注释：这里把生成的图片或文件保存到磁盘。
    img.save(OUT_CODE, quality=95)


# 函数说明：脚本入口，按顺序调用前面的函数生成最终文件。
# 行注释：这里定义 main 函数。
def main() -> None:
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # 行注释：这里设置 rows 的值，后续绘图或计算会用到。
    rows = load_rows()
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_baseline_page(rows)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_code_page(rows)
    # 行注释：这里在终端输出生成结果或进度信息。
    print(OUT_BASELINE)
    # 行注释：这里在终端输出生成结果或进度信息。
    print(OUT_CODE)


# 行注释：这里判断脚本是否被直接运行。
if __name__ == "__main__":
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    main()
