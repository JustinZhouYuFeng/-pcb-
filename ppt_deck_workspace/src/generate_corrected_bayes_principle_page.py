# 中文注释：生成修正后的贝叶斯决策原理说明页。
# 主要流程：重新绘制公式、类条件分布、后验阈值和最小风险关系，避免概念表达不准确。
# 输出结果：生成用于替换原 PPT 中贝叶斯原理页的高清图片。

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "image2_report_pages" / "07_贝叶斯决策原理_条件概率到最小风险.png"

W, H = 1920, 1080
NAVY = "#003B73"
NAVY_DARK = "#07294A"
BLUE = "#0A57A3"
TEAL = "#006D78"
CYAN = "#00A5C8"
ORANGE = "#E87511"
GOLD = "#C58A00"
RED = "#D42020"
INK = "#152033"
MUTED = "#52606F"
LINE = "#B8CADC"
BG = "#F7FAFD"
WHITE = "#FFFFFF"
PALE_BLUE = "#EAF5FF"
PALE_TEAL = "#E8F8F6"
PALE_GOLD = "#FFF7E3"


# 函数说明：加载中文字体，保证图片里的中文能正常显示。
def font(size: int, bold: bool = False, formula: bool = False) -> ImageFont.FreeTypeFont:
    if formula:
        candidates = [
            r"C:\Windows\Fonts\cambria.ttc",
            r"C:\Windows\Fonts\ARIALUNI.TTF",
            r"C:\Windows\Fonts\msyh.ttc",
        ]
    else:
        candidates = [
            r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
            r"C:\Windows\Fonts\simhei.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ]
    for item in candidates:
        if Path(item).exists():
            return ImageFont.truetype(item, size=size)
    return ImageFont.load_default()


# 函数说明：计算一段文字的宽度，方便后续居中或换行。
def text_w(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


# 函数说明：把长句按最大宽度拆成多行，避免文字溢出。
def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for ch in text:
        if ch == "\n":
            lines.append(current)
            current = ""
            continue
        trial = current + ch
        if text_w(draw, trial, fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


# 函数说明：按多行方式绘制文字，保证中文说明不挤出卡片。
def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    size: int,
    fill: str,
    max_w: int,
    *,
    bold: bool = False,
    line_gap: int = 8,
) -> int:
    x, y = xy
    fnt = font(size, bold)
    for line in wrap_text(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += draw.textbbox((0, 0), line, font=fnt)[3] + line_gap
    return y


# 函数说明：绘制圆角矩形，作为信息卡片或内容面板。
def rounded(draw: ImageDraw.ImageDraw, box, fill=WHITE, outline=LINE, width=2, radius=24) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# 函数说明：把文字放在指定矩形区域正中间。
def center_text(draw: ImageDraw.ImageDraw, box, text: str, fnt, fill=INK) -> None:
    x1, y1, x2, y2 = box
    bb = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - 1), text, font=fnt, fill=fill)


# 函数说明：绘制小标题胶囊，用来标识页面分区。
def title_pill(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, text: str, color: str = NAVY) -> None:
    rounded(draw, (x, y, x + w, y + 50), fill=color, outline=color, radius=12)
    center_text(draw, (x, y, x + w, y + 50), text, font(25, True), WHITE)


# 函数说明：绘制一条带圆点的说明文字。
def bullet(draw: ImageDraw.ImageDraw, x: int, y: int, text: str, color: str = BLUE, size: int = 23, width: int = 470) -> int:
    draw.ellipse((x, y + 11, x + 11, y + 22), fill=color)
    return draw_wrapped(draw, text, (x + 26, y), size, INK, width - 26, line_gap=7) + 12


# 函数说明：绘制页面顶部标题栏和副标题。
def draw_header(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle((0, 0, W, 156), fill=NAVY_DARK)
    draw.rectangle((0, 152, W, 158), fill="#F0A500")
    draw.text((52, 28), "贝叶斯决策原理：从后验概率到最小风险", font=font(52, True), fill=WHITE)
    draw.text((54, 98), "先估计 P(类别|特征)，再按损失函数选择条件风险最小的动作", font=font(28), fill="#D7ECFF")
    draw.text((1828, 32), "哈尔滨工程大学", font=font(26, True), fill=WHITE, anchor="ra")
    draw.text((1828, 78), "HEU | Pattern Recognition Seminar", font=font(23), fill="#D7ECFF", anchor="ra")
    draw.text((1828, 116), "电子信息方向 · 模式识别", font=font(24, True), fill="#FFC44D", anchor="ra")


# 函数说明：绘制贝叶斯公式说明卡片。
def draw_formula_card(draw: ImageDraw.ImageDraw) -> None:
    panel = (20, 234, 578, 842)
    rounded(draw, panel, WHITE, "#9EB7CF", 2, 16)
    title_pill(draw, 55, 206, 485, "贝叶斯公式：由类条件分布得到后验")

    rounded(draw, (40, 290, 558, 438), fill="#F0F7FF", outline="#9BC5F2", radius=10)
    eq = "P(ωₖ|x) = p(x|ωₖ)P(ωₖ) / Σⱼ p(x|ωⱼ)P(ωⱼ)"
    center_text(draw, (54, 314, 544, 394), eq, font(33, formula=True), INK)
    center_text(draw, (54, 388, 544, 426), "后验 ∝ 似然 × 先验，再归一化", font(22, True), BLUE)

    y = 462
    y = bullet(draw, 44, y, "p(x|ωₖ)：在类别 ωₖ 下观察到特征 x 的类条件概率/概率密度", BLUE, 22, 500)
    y = bullet(draw, 44, y, "P(ωₖ)：类别 ωₖ 的先验概率，反映缺陷样本比例等先验信息", BLUE, 22, 500)
    y = bullet(draw, 44, y, "P(ωₖ|x)：看到特征 x 后属于类别 ωₖ 的后验概率", BLUE, 22, 500)

    rounded(draw, (40, 640, 558, 806), fill=WHITE, outline="#A9C0D7", width=2, radius=14)
    draw.text((72, 666), "ω₁ = normal（正常）", font=font(24, formula=True), fill=BLUE)
    draw.text((72, 712), "ω₂ = anomaly（缺陷）", font=font(24, formula=True), fill=ORANGE)
    draw.line((72, 762, 520, 762), fill="#D5E1EB", width=2)
    draw.text((72, 776), "x：1318 维图像特征向量（颜色/纹理/边缘/HOG/LBP）", font=font(20), fill=INK)


# 函数说明：计算一维高斯分布值，用于画类条件概率曲线。
def gaussian(x: float, mu: float, sigma: float) -> float:
    return math.exp(-((x - mu) ** 2) / (2 * sigma**2))


# 函数说明：把数学坐标转换成画布上的像素坐标。
def map_point(x: float, y: float, x0: int, y0: int, w: int, h: int) -> tuple[int, int]:
    return int(x0 + x * w), int(y0 + h - y * h)


# 函数说明：绘制类条件分布和阈值判别示意区域。
def draw_distribution_panel(draw: ImageDraw.ImageDraw) -> None:
    panel = (604, 234, 1296, 842)
    rounded(draw, panel, WHITE, "#9EB7CF", 2, 16)
    title_pill(draw, 662, 206, 528, "一维示意：类条件分布、后验阈值与误差")

    x0, y0, w, h = 642, 350, 600, 345
    draw.line((x0, y0 + h, x0 + w + 18, y0 + h), fill=INK, width=2)
    draw.line((x0, y0 + h, x0, y0 - 18), fill=INK, width=2)
    draw.polygon([(x0 + w + 18, y0 + h), (x0 + w, y0 + h - 8), (x0 + w, y0 + h + 8)], fill=INK)
    draw.polygon([(x0, y0 - 18), (x0 - 8, y0), (x0 + 8, y0)], fill=INK)
    draw.text((x0 - 20, y0 - 54), "概率密度", font=font(18), fill=INK)
    draw.text((x0 + w - 60, y0 + h + 18), "特征投影 z", font=font(21), fill=INK)

    xs = [i / 500 for i in range(501)]
    y1 = [0.86 * gaussian(x, 0.34, 0.12) for x in xs]
    y2 = [0.86 * gaussian(x, 0.68, 0.14) for x in xs]
    max_y = max(max(y1), max(y2))
    y1 = [v / max_y * 0.82 for v in y1]
    y2 = [v / max_y * 0.82 for v in y2]
    x_t = 0.51

    # 函数说明：把曲线下方区域转换成多边形，用于填充误判区域。
    def polygon_for(vals: list[float], start_pred) -> list[tuple[int, int]]:
        pts = [(x0 + int(xs[0] * w), y0 + h)]
        pts += [map_point(x, y, x0, y0, w, h) for x, y in zip(xs, vals) if start_pred(x)]
        selected = [x for x in xs if start_pred(x)]
        if selected:
            pts.append((x0 + int(selected[-1] * w), y0 + h))
        return pts

    blue_tail = polygon_for(y1, lambda x: x >= x_t)
    orange_tail = polygon_for(y2, lambda x: x < x_t)
    if len(blue_tail) > 2:
        draw.polygon(blue_tail, fill="#D4E8FF")
    if len(orange_tail) > 2:
        draw.polygon(orange_tail, fill="#FFE0BE")

    poly1 = [(x0, y0 + h)] + [map_point(x, y, x0, y0, w, h) for x, y in zip(xs, y1)] + [(x0 + w, y0 + h)]
    poly2 = [(x0, y0 + h)] + [map_point(x, y, x0, y0, w, h) for x, y in zip(xs, y2)] + [(x0 + w, y0 + h)]
    draw.polygon(poly1, fill="#EEF6FF")
    draw.polygon(poly2, fill="#FFF0E2")
    draw.line([map_point(x, y, x0, y0, w, h) for x, y in zip(xs, y1)], fill=BLUE, width=4)
    draw.line([map_point(x, y, x0, y0, w, h) for x, y in zip(xs, y2)], fill=ORANGE, width=4)

    xt_px = x0 + int(x_t * w)
    for yy in range(y0 - 10, y0 + h + 10, 18):
        draw.line((xt_px, yy, xt_px, yy + 10), fill=RED, width=2)
    draw.text((xt_px - 92, y0 - 58), "特征边界 x_T", font=font(22, True), fill=RED)
    draw.text((xt_px - 116, y0 - 28), "由后验阈值 T 映射而来", font=font(18), fill=RED)
    draw.polygon([(xt_px, y0 + h + 5), (xt_px - 7, y0 + h + 24), (xt_px + 7, y0 + h + 24)], fill=INK)

    draw.text((735, 386), "正常  ω₁", font=font(22, True), fill=BLUE)
    draw.text((740, 421), "p(z|ω₁)P(ω₁)", font=font(21, formula=True), fill=BLUE)
    draw.text((1060, 386), "缺陷  ω₂", font=font(22, True), fill=ORANGE)
    draw.text((1064, 421), "p(z|ω₂)P(ω₂)", font=font(21, formula=True), fill=ORANGE)
    draw.text((810, 737), "误报区域", font=font(20, True), fill=BLUE)
    draw.text((934, 737), "漏检区域", font=font(20, True), fill=ORANGE)
    draw.text((786, 770), "重叠区导致贝叶斯误差；大小取决于特征、先验和损失", font=font(22, True), fill=INK)
    draw.text((650, 812), "注：真实模型在 1318 维/PCA 特征空间中计算；此图只是一维投影示意。", font=font(18), fill=MUTED)


# 函数说明：绘制最小风险决策公式和判别规则。
def draw_risk_panel(draw: ImageDraw.ImageDraw) -> None:
    panel = (1321, 234, 1872, 842)
    rounded(draw, panel, WHITE, "#9EB7CF", 2, 16)
    title_pill(draw, 1465, 206, 220, "最小风险决策", TEAL)

    rounded(draw, (1343, 282, 1850, 394), fill=PALE_TEAL, outline="#71BEB4", radius=10)
    center_text(draw, (1350, 306, 1844, 372), "R(αᵢ|x) = Σⱼ λᵢⱼ P(ωⱼ|x)", font(34, formula=True), INK)

    y = 424
    y = bullet(draw, 1344, y, "αᵢ：采取的决策动作，如判为正常或判为缺陷", TEAL, 22, 485)
    y = bullet(draw, 1344, y, "λᵢⱼ：真实类别为 ωⱼ 时采取动作 αᵢ 的损失/代价", TEAL, 22, 485)
    y = bullet(draw, 1344, y, "R(αᵢ|x)：给定特征 x 时动作 αᵢ 的条件风险", TEAL, 22, 485)

    rounded(draw, (1343, 576, 1850, 668), fill=PALE_TEAL, outline="#71BEB4", radius=10)
    draw.text((1364, 598), "选择风险最小的动作：", font=font(23, True), fill=TEAL)
    draw.text((1604, 598), "α*(x)=arg minᵢ R(αᵢ|x)", font=font(29, formula=True), fill=INK)

    rounded(draw, (1343, 696, 1850, 816), fill=PALE_GOLD, outline="#E2B24B", radius=10)
    draw.text((1372, 720), "二分类常用写法", font=font(23, True), fill=GOLD)
    draw.text((1372, 758), "若 P(ω₂|x) ≥ T，则判为缺陷；否则判为正常", font=font(22, True), fill=INK)
    draw.text((1372, 790), "零正确损失时：T = C_FA / (C_FA + C_Miss)", font=font(22, True), fill=RED)


# 函数说明：绘制页面底部说明区。
def draw_footer(draw: ImageDraw.ImageDraw) -> None:
    rounded(draw, (24, 886, 1870, 1003), fill="#EEF7FF", outline="#8EC5F2", width=2, radius=14)
    draw.ellipse((150, 910, 224, 984), fill=NAVY)
    draw.text((187, 944), "i", font=font(52, True), fill=WHITE, anchor="mm")
    draw.text((260, 918), "更严谨的讲法：", font=font(31, True), fill=NAVY)
    draw.text((520, 921), "后验概率给出缺陷可能性；阈值 T 不是固定常数，理论上由误报代价 C_FA、漏检代价 C_Miss、先验和模型分布共同决定。", font=font(25), fill=INK)
    draw.text((520, 956), "实际实验中用验证集搜索 T，是对最小风险思想的经验化实现。", font=font(25), fill=INK)
    draw.rectangle((0, 1072, W, H), fill="#0A57A3")


# 函数说明：脚本入口，按顺序调用前面的函数生成最终文件。
def main() -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(draw)
    draw_formula_card(draw)
    draw_distribution_panel(draw)
    draw_risk_panel(draw)
    draw_footer(draw)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, quality=96)
    print(OUT)


if __name__ == "__main__":
    main()
