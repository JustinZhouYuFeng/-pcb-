# 中文注释：生成项目总结与使用目的说明页。
# 主要流程：概括项目目标、方法链路、实验结果和实际应用价值。
# 输出结果：生成一页可直接放入演示文稿的项目总结图片。

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "image2_report_pages" / "16_project_summary_purpose.png"

W, H = 1920, 1080
NAVY = "#082A4A"
NAVY2 = "#003B73"
BLUE = "#0A57A3"
ORANGE = "#E87511"
GOLD = "#C99700"
GREEN = "#168A5B"
RED = "#C7372F"
INK = "#122033"
MUTED = "#5C6B7A"
LINE = "#BDD0E2"
BG = "#F6FAFD"
WHITE = "#FFFFFF"
PALE_BLUE = "#EAF5FF"
PALE_GOLD = "#FFF7E3"
PALE_GREEN = "#EAF8F1"
PALE_ORANGE = "#FFF0E2"


def fnt(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for item in candidates:
        if Path(item).exists():
            return ImageFont.truetype(item, size=size)
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for ch in text:
        if ch == "\n":
            lines.append(current)
            current = ""
            continue
        trial = current + ch
        if text_size(draw, trial, font)[0] <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    font: ImageFont.FreeTypeFont,
    fill: str,
    max_w: int,
    gap: int = 8,
) -> int:
    x, y = xy
    for line in wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=fill)
        y += text_size(draw, line, font)[1] + gap
    return y


def rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: str = WHITE,
    outline: str = LINE,
    width: int = 2,
    radius: int = 24,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color: str = BLUE, width: int = 4) -> None:
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    length = 16
    points = [
        (x2, y2),
        (x2 + length * math.cos(angle + math.pi * 0.82), y2 + length * math.sin(angle + math.pi * 0.82)),
        (x2 + length * math.cos(angle - math.pi * 0.82), y2 + length * math.sin(angle - math.pi * 0.82)),
    ]
    draw.polygon(points, fill=color)


def metric_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], value: str, label: str, color: str) -> None:
    rounded(draw, box, WHITE, "#CADAE8", 2, 18)
    x1, y1, _, _ = box
    draw.text((x1 + 26, y1 + 18), value, font=fnt(34, True), fill=color)
    draw.text((x1 + 27, y1 + 69), label, font=fnt(19), fill=MUTED)


def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    for y in range(160):
        ratio = y / 160
        draw.line((0, y, W, y), fill=(int(8 + ratio * 2), int(42 + ratio * 12), int(74 + ratio * 24)))
    draw.rectangle((0, 154, W, 160), fill="#F0A500")
    draw.text((56, 34), "项目总结：为什么用贝叶斯决策做 PCB 缺陷检测", font=fnt(46, True), fill=WHITE)
    draw.text((58, 98), "目的：把“是否有缺陷”的硬判断，转化为可解释、可调阈值、可评估风险的概率决策过程", font=fnt(25), fill="#D7ECFF")
    draw.text((1828, 40), "哈尔滨工程大学", font=fnt(26, True), fill=WHITE, anchor="ra")
    draw.text((1828, 82), "Pattern Recognition Seminar", font=fnt(21), fill="#D7ECFF", anchor="ra")
    draw.text((1828, 118), "周玉峰 2023080502", font=fnt(22, True), fill="#FFC44D", anchor="ra")

    rounded(draw, (54, 196, 1866, 326), fill=WHITE, outline="#9FC4E8", width=2, radius=22)
    draw.ellipse((92, 226, 164, 298), fill=NAVY2)
    draw.text((128, 261), "目", font=fnt(31, True), fill=WHITE, anchor="mm")
    draw.text((195, 218), "使用贝叶斯决策的目的", font=fnt(31, True), fill=NAVY2)
    draw_wrapped(
        draw,
        "在真实 PCB 质检中，缺陷样本少、误报和漏报代价不同。贝叶斯方法能够输出 P(缺陷|x)，再根据阈值 T 和损失函数选择风险最小的动作，而不是只给一个无法解释的标签。",
        (195, 263),
        fnt(24),
        INK,
        1585,
        8,
    )

    flow_y = 405
    nodes = [
        ("真实 PCB 图像", "normal / anomaly\n真实彩色样本", PALE_BLUE, BLUE),
        ("1318 维特征", "颜色、纹理、边缘\nLBP、HOG、GLCM", PALE_GOLD, GOLD),
        ("贝叶斯后验概率", "计算 P(缺陷|x)\n保留不确定性", PALE_GREEN, GREEN),
        ("阈值与风险决策", "调节 T\n权衡误报和漏报", PALE_ORANGE, ORANGE),
        ("可解释结果", "指标、曲线、混淆矩阵\n支撑汇报结论", "#EEF2FF", BLUE),
    ]
    x0, box_w, box_h, gap = 80, 300, 180, 70
    for i, (title, body, fill, color) in enumerate(nodes):
        x = x0 + i * (box_w + gap)
        rounded(draw, (x, flow_y, x + box_w, flow_y + box_h), fill=fill, outline="#AFC6D9", width=2, radius=20)
        draw.text((x + 24, flow_y + 24), f"{i + 1:02d}", font=fnt(25, True), fill=color)
        draw.text((x + 78, flow_y + 25), title, font=fnt(26, True), fill=INK)
        draw.line((x + 24, flow_y + 70, x + box_w - 24, flow_y + 70), fill="#D5E1EB", width=2)
        draw_wrapped(draw, body, (x + 24, flow_y + 92), fnt(21), MUTED, box_w - 48, 7)
        if i < len(nodes) - 1:
            arrow(draw, (x + box_w + 10, flow_y + box_h // 2), (x + box_w + gap - 18, flow_y + box_h // 2), "#88AFCB", 4)

    rounded(draw, (64, 645, 700, 915), fill=WHITE, outline=LINE, width=2, radius=22)
    draw.text((96, 678), "本项目解决什么问题？", font=fnt(30, True), fill=NAVY2)
    items = [
        ("缺陷样本少", "4013 张正常样本对 400 张缺陷样本，类别明显不均衡。"),
        ("判断要可解释", "输出 P(缺陷|x)，说明缺陷可能性，而不只是给标签。"),
        ("风险要可调", "通过阈值 T 权衡误报与漏报，适配不同质检代价。"),
    ]
    y = 732
    for title, body in items:
        draw.rounded_rectangle((96, y + 4, 108, y + 16), radius=4, fill=BLUE)
        draw.text((126, y - 2), title, font=fnt(23, True), fill=INK)
        draw_wrapped(draw, body, (126, y + 29), fnt(18), MUTED, 505, 4)
        y += 64

    rounded(draw, (744, 645, 1856, 915), fill=WHITE, outline=LINE, width=2, radius=22)
    draw.text((780, 678), "最终形成的结论", font=fnt(30, True), fill=NAVY2)
    conclusion = (
        "在贝叶斯框架内，PCA 降维、Gaussian 建模、Gamma 正则化和后验阈值优化共同提升了 PCB 缺陷检测效果。"
        "最优 Bayes-4 模型在测试集上 Accuracy=0.9184，F1=0.5424，AUC=0.8986。"
    )
    draw_wrapped(draw, conclusion, (780, 727), fnt(23), INK, 1015, 10)
    metric_card(draw, (790, 807, 1015, 876), "0.9184", "Accuracy", BLUE)
    metric_card(draw, (1040, 807, 1265, 876), "0.5424", "F1-score", ORANGE)
    metric_card(draw, (1290, 807, 1515, 876), "0.8986", "AUC", GREEN)
    metric_card(draw, (1540, 807, 1765, 876), "0.0432", "FPR", RED)

    rounded(draw, (64, 940, 1856, 1020), fill=NAVY2, outline=NAVY2, width=0, radius=18)
    draw.text((100, 963), "一句话总结：", font=fnt(27, True), fill="#FFD46B")
    draw_wrapped(
        draw,
        "本项目使用贝叶斯决策，是为了让 PCB 缺陷检测既能给出概率依据，又能根据质量风险调节判别阈值，从而实现可解释、可优化、可复现实验的检测流程。",
        (275, 958),
        fnt(24, True),
        WHITE,
        1510,
        6,
    )
    draw.rectangle((0, 1072, W, H), fill=BLUE)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, quality=96)
    print(OUT)


if __name__ == "__main__":
    main()
