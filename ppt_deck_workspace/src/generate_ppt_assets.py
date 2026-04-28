# 中文注释：生成 PPT 中复用的基础视觉素材。
# 主要流程：绘制项目流程、数据说明、模型框架等图片资源。
# 输出结果：把素材集中保存，便于 PPT 构建脚本统一引用。

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(r"C:\Users\19571\Desktop\研讨\PCB_Bayes_Project")
OUT = ROOT / "ppt_materials" / "visa_pcb" / "polished"
DATA = ROOT / "data" / "raw" / "visa"


NAVY = "#003B73"
OCEAN = "#005A8D"
CYAN = "#28A9E0"
GOLD = "#C99700"
INK = "#0F172A"
SLATE = "#475569"
LIGHT = "#F5F8FB"
WHITE = "#FFFFFF"
ORANGE = "#D95319"


# 函数说明：加载中文字体，保证图片里的中文能正常显示。
def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for item in candidates:
        if item and Path(item).exists():
            return ImageFont.truetype(item, size=size)
    return ImageFont.load_default()


# 函数说明：计算文字宽高，帮助把文字放到合适位置。
def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


# 函数说明：按多行方式绘制文字，保证中文说明不挤出卡片。
def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    fnt: ImageFont.FreeTypeFont,
    fill: str,
    max_width: int,
    line_gap: int = 8,
) -> int:
    x, y = xy
    lines: list[str] = []
    current = ""
    for ch in text:
        if ch == "\n":
            lines.append(current)
            current = ""
            continue
        test = current + ch
        if text_size(draw, test, fnt)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += text_size(draw, line, fnt)[1] + line_gap
    return y


# 函数说明：绘制圆角信息卡片，统一页面视觉样式。
def rounded_card(draw: ImageDraw.ImageDraw, box, fill, outline="#D7DEE7", width=2, radius=28):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# 函数说明：生成 PPT 封面背景图。
def cover_background() -> None:
    w, h = 1920, 1080
    img = Image.new("RGB", (w, h), NAVY)
    px = img.load()
    top = (0, 35, 73)
    bottom = (0, 91, 141)
    for y in range(h):
        t = y / (h - 1)
        for x in range(w):
            vignette = 1 - 0.18 * ((x - w * 0.52) ** 2 / (w * w) + (y - h * 0.42) ** 2 / (h * h))
            r = int((top[0] * (1 - t) + bottom[0] * t) * vignette)
            g = int((top[1] * (1 - t) + bottom[1] * t) * vignette)
            b = int((top[2] * (1 - t) + bottom[2] * t) * vignette)
            px[x, y] = (max(0, r), max(0, g), max(0, b))

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)

    # Subtle engineering grid.
    for x in range(0, w, 64):
        d.line((x, 0, x, h), fill=(255, 255, 255, 18), width=1)
    for y in range(0, h, 64):
        d.line((0, y, w, y), fill=(255, 255, 255, 14), width=1)

    # Ocean-wave / signal traces.
    for i, color in enumerate([(40, 169, 224, 92), (255, 255, 255, 54), (201, 151, 0, 80)]):
        points = []
        for x in range(-80, w + 160, 28):
            y = 720 + i * 55 + math.sin(x / 150 + i * 0.9) * 42
            points.append((x, y))
        d.line(points, fill=color, width=5 if i == 0 else 3)

    # Circuit board traces and nodes.
    rng = random.Random(42)
    for _ in range(38):
        x = rng.randint(1080, 1860)
        y = rng.randint(120, 880)
        length = rng.randint(80, 230)
        elbow = rng.randint(-90, 90)
        color = (255, 255, 255, rng.randint(28, 70))
        d.line((x, y, x - length, y, x - length, y + elbow), fill=color, width=3)
        d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(40, 169, 224, 100))
        d.ellipse((x - length - 6, y + elbow - 6, x - length + 6, y + elbow + 6), fill=(201, 151, 0, 120))

    d.text((1250, 118), "HEU", font=font(210, True), fill=(255, 255, 255, 28))
    d.text((1260, 320), "Harbin Engineering University", font=font(34), fill=(255, 255, 255, 78))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img.save(OUT / "00_哈工程深蓝封面背景.png", quality=95)


# 函数说明：绘制箭头，表示流程方向或信息关系。
def draw_arrow(draw: ImageDraw.ImageDraw, start, end, color=OCEAN, width=5):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 18
    p1 = (x2 - size * math.cos(ang - 0.45), y2 - size * math.sin(ang - 0.45))
    p2 = (x2 - size * math.cos(ang + 0.45), y2 - size * math.sin(ang + 0.45))
    draw.polygon([end, p1, p2], fill=color)


# 函数说明：生成项目整体流程图。
def project_flowchart() -> None:
    w, h = 1920, 1080
    img = Image.new("RGB", (w, h), LIGHT)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, w, 150), fill=NAVY)
    d.text((92, 45), "项目流程总览：基于贝叶斯决策的 PCB 缺陷检测", font=font(48, True), fill=WHITE)
    d.text((92, 106), "哈尔滨工程大学电子信息方向课程研讨 | VisA PCB 真实图像 | good / bad 二分类", font=font(24), fill="#CFE8F7")

    stages = [
        ("01", "数据获取", "VisA PCB 真实彩色图像\npcb1 - pcb4 共 4 类子集\n正常 4013 张，缺陷 400 张"),
        ("02", "数据处理", "标签映射为 good / bad\n训练集、验证集、测试集划分\n灰度增强与尺寸归一化"),
        ("03", "特征工程", "每张图像提取 1318 维向量\n颜色、灰度、边缘、纹理\nLBP 局部纹理 + HOG 梯度"),
        ("04", "贝叶斯优化", "由 P(ω|x) 输出缺陷概率\nPCA 降维、高斯建模\n协方差正则化与阈值寻优"),
        ("05", "结果评估", "Accuracy / Precision / Recall\nF1 / IoU / AUC / FPR / FNR\n横向对比、趋势与热力图"),
    ]

    positions = [
        (100, 260, 500, 320),
        (710, 260, 500, 320),
        (1320, 260, 500, 320),
        (390, 660, 520, 290),
        (1030, 660, 520, 290),
    ]
    colors = [OCEAN, "#2563A7", "#2E5A88", "#0B5D78", "#004488"]
    for i, ((num, title, body), (x, y, card_w, card_h)) in enumerate(zip(stages, positions)):
        rounded_card(d, (x, y, x + card_w, y + card_h), WHITE, outline="#C7D3DF", width=2, radius=32)
        d.ellipse((x + 28, y + 28, x + 92, y + 92), fill=colors[i])
        d.text((x + 44, y + 43), num, font=font(22, True), fill=WHITE)
        d.text((x + 112, y + 37), title, font=font(34, True), fill=INK)
        d.line((x + 34, y + 120, x + card_w - 34, y + 120), fill="#DCE6EF", width=2)
        draw_wrapped(d, body, (x + 34, y + 150), font(25), SLATE, card_w - 68, line_gap=11)
        d.rectangle((x, y + card_h - 10, x + card_w, y + card_h), fill=colors[i])

    arrow_pairs = [
        ((600, 420), (700, 420)),
        ((1210, 420), (1310, 420)),
        ((1570, 590), (870, 650)),
        ((910, 805), (1020, 805)),
    ]
    for start, end in arrow_pairs:
        draw_arrow(d, start, end, color="#7DA9C8", width=5)

    # Feedback loop
    d.arc((250, 590, 1670, 1010), start=200, end=340, fill=GOLD, width=5)
    draw_arrow(d, (1535, 902), (1565, 865), color=GOLD, width=5)
    d.text((520, 988), "参数分析与阈值反馈：PCA 维度、正则化 γ、后验概率阈值共同决定最终风险", font=font(25, True), fill="#6B4E00")

    d.rounded_rectangle((140, 930, 1780, 1032), radius=26, fill="#E7F4FB", outline="#9CCBE2", width=2)
    d.text((188, 962), "核心思想", font=font(30, True), fill=NAVY)
    d.text((335, 965), "把 PCB 图像转化为特征向量 x，用后验概率 P(缺陷|x) 做最小风险决策，并用可解释指标验证优化是否有效。", font=font(26), fill=INK)

    img.save(OUT / "13_项目流程图.png", quality=95)


# 函数说明：读取图片并等比例缩放到指定大小。
def load_fit(path: Path, size: tuple[int, int]) -> Image.Image:
    img = Image.open(path).convert("RGB")
    target_w, target_h = size
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new = img.resize((int(src_w * scale), int(src_h * scale)), Image.Resampling.LANCZOS)
    left = (new.width - target_w) // 2
    top = (new.height - target_h) // 2
    return new.crop((left, top, left + target_w, top + target_h))


# 函数说明：生成正常样本和缺陷样本的对比图。
def sample_comparison() -> None:
    w, h = 1920, 1080
    img = Image.new("RGB", (w, h), LIGHT)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, w, 120), fill=NAVY)
    d.text((80, 35), "VisA PCB 真实图像样本归类预览", font=font(44, True), fill=WHITE)
    d.text((80, 86), "按类别重新排布：左侧为正常样本，右侧为缺陷样本，避免 PPT 中样本顺序混乱", font=font(22), fill="#CFE8F7")

    normal = DATA / "pcb1" / "Data" / "Images" / "Normal" / "0313.JPG"
    anomaly_a = DATA / "pcb1" / "Data" / "Images" / "Anomaly" / "000.JPG"
    anomaly_b = DATA / "pcb4" / "Data" / "Images" / "Anomaly" / "012.JPG"
    if not anomaly_b.exists():
        anomaly_b = DATA / "pcb4" / "Data" / "Images" / "Anomaly" / "000.JPG"

    # Left large normal image.
    left_box = (90, 190, 875, 900)
    rounded_card(d, left_box, WHITE, "#BFD1DF", 2, 28)
    normal_img = load_fit(normal, (725, 480))
    img.paste(normal_img, (120, 270))
    d.rounded_rectangle((120, 218, 350, 262), radius=18, fill="#E7F4FB")
    d.text((144, 226), "正常样本 / pcb1", font=font(24, True), fill=NAVY)
    d.text((120, 775), "目标：学习良品 PCB 的颜色、纹理、边缘与结构统计分布", font=font(25), fill=SLATE)
    d.text((120, 820), "决策含义：P(缺陷|x) 低于阈值，判为正常", font=font(25, True), fill=NAVY)

    right_x = 1010
    for idx, (p, label, y0) in enumerate(
        [
            (anomaly_a, "缺陷样本 1 / pcb1", 190),
            (anomaly_b, "缺陷样本 2 / pcb4", 555),
        ]
    ):
        box = (right_x, y0, 1825, y0 + 345)
        rounded_card(d, box, WHITE, "#BFD1DF", 2, 28)
        crop = load_fit(p, (440, 250))
        img.paste(crop, (right_x + 28, y0 + 70))
        tag_fill = "#FFF0E6" if idx == 0 else "#FFF7DB"
        tag_color = ORANGE if idx == 0 else "#805E00"
        d.rounded_rectangle((right_x + 28, y0 + 22, right_x + 280, y0 + 62), radius=17, fill=tag_fill)
        d.text((right_x + 50, y0 + 29), label, font=font(22, True), fill=tag_color)
        d.text((right_x + 505, y0 + 92), "异常纹理 / 局部结构变化", font=font(26, True), fill=INK)
        draw_wrapped(
            d,
            "特征向量在后验概率中更接近缺陷类分布",
            (right_x + 505, y0 + 142),
            font(22),
            SLATE,
            265,
            line_gap=8,
        )
        d.text((right_x + 505, y0 + 236), "输出：P(缺陷|x)", font=font(28, True), fill=tag_color)

    d.rounded_rectangle((300, 940, 1620, 1018), radius=24, fill="#FFFFFF", outline="#C7D3DF", width=2)
    d.text((350, 960), "说明：本页只展示分类任务中的样本组织方式；模型实际输入不是图片本身，而是由图片提取得到的 1318 维特征向量。", font=font(25), fill=INK)

    img.save(OUT / "14_正常与缺陷样本归类预览.png", quality=95)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    cover_background()
    project_flowchart()
    sample_comparison()
    print("Generated PPT assets:")
    for name in [
        "00_哈工程深蓝封面背景.png",
        "13_项目流程图.png",
        "14_正常与缺陷样本归类预览.png",
    ]:
        print(OUT / name)
