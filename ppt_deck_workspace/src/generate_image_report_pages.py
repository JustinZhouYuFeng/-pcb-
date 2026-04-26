from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
POLISHED = ROOT / "ppt_materials" / "visa_pcb" / "polished"
BASIC = ROOT / "ppt_materials" / "visa_pcb"
DATA = ROOT / "data" / "raw" / "visa"
OUT = ROOT / "image_report_pages"

W, H = 1920, 1080

NAVY = "#003B73"
NAVY2 = "#004488"
OCEAN = "#005A8D"
BLUE = "#2E5A88"
CYAN = "#28A9E0"
GOLD = "#C99700"
ORANGE = "#D95319"
RED = "#B22222"
INK = "#0F172A"
SLATE = "#475569"
MUTED = "#64748B"
LINE = "#CBD8E4"
BG = "#F5F8FB"
WHITE = "#FFFFFF"
PALE_BLUE = "#E7F4FB"
PALE_GOLD = "#FFF7DB"
PALE_ORANGE = "#FFF0E6"

try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:  # pragma: no cover
    RESAMPLE = Image.LANCZOS


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


def mono(size: int) -> ImageFont.FreeTypeFont:
    for item in [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf"]:
        if Path(item).exists():
            return ImageFont.truetype(item, size=size)
    return font(size)


def text_size(draw: ImageDraw.ImageDraw, value: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), value, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def wrapped_lines(draw: ImageDraw.ImageDraw, value: str, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for ch in value:
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
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    value: str,
    xy: tuple[int, int],
    size: int,
    fill: str,
    max_width: int,
    *,
    bold: bool = False,
    line_gap: int = 8,
    fnt: ImageFont.FreeTypeFont | None = None,
) -> int:
    x, y = xy
    fnt = fnt or font(size, bold)
    for line in wrapped_lines(draw, value, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += text_size(draw, line, fnt)[1] + line_gap
    return y


def make_canvas() -> Image.Image:
    return Image.new("RGB", (W, H), BG)


def add_shadow(base: Image.Image, rect: tuple[int, int, int, int], radius: int = 24, alpha: int = 38) -> None:
    x1, y1, x2, y2 = rect
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((x1 + 6, y1 + 8, x2 + 6, y2 + 8), radius=radius, fill=(0, 48, 90, alpha))
    layer = layer.filter(ImageFilter.GaussianBlur(8))
    base.alpha_composite(layer) if base.mode == "RGBA" else base.paste(Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB"))


def rounded(draw: ImageDraw.ImageDraw, box, fill=WHITE, outline=LINE, width=2, radius=24) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def header(draw: ImageDraw.ImageDraw, title: str, subtitle: str = "", tag: str = "HEU | Bayesian PCB Inspection") -> None:
    draw.rectangle((0, 0, W, 136), fill=NAVY)
    draw.text((76, 34), title, font=font(46, True), fill=WHITE)
    if subtitle:
        draw.text((78, 92), subtitle, font=font(23), fill="#CFE8F7")
    draw.rounded_rectangle((1490, 42, 1838, 92), radius=24, fill="#0A4B82")
    draw.text((1664, 67), tag, font=font(18, True), fill=WHITE, anchor="mm")


def footer(draw: ImageDraw.ImageDraw, page_no: int) -> None:
    draw.text((76, 1035), "哈尔滨工程大学 · 电子信息方向 · 模式识别课程研讨", font=font(16), fill="#6B7E8F")
    draw.text((1838, 1035), f"{page_no:02d}", font=font(18, True), fill=NAVY, anchor="ra")


def contain(path: Path, size: tuple[int, int], bg: str = WHITE) -> Image.Image:
    img = Image.open(path).convert("RGB")
    tw, th = size
    sw, sh = img.size
    scale = min(tw / sw, th / sh)
    new = img.resize((max(1, int(sw * scale)), max(1, int(sh * scale))), RESAMPLE)
    canvas = Image.new("RGB", size, bg)
    canvas.paste(new, ((tw - new.width) // 2, (th - new.height) // 2))
    return canvas


def cover(path: Path, size: tuple[int, int]) -> Image.Image:
    img = Image.open(path).convert("RGB")
    tw, th = size
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    new = img.resize((max(1, int(sw * scale)), max(1, int(sh * scale))), RESAMPLE)
    left = (new.width - tw) // 2
    top = (new.height - th) // 2
    return new.crop((left, top, left + tw, top + th))


def paste_card(base: Image.Image, box, img_path: Path, *, padding: int = 12, fit: str = "contain", bg: str = WHITE) -> None:
    draw = ImageDraw.Draw(base)
    rounded(draw, box, WHITE, LINE, 2, 18)
    x1, y1, x2, y2 = box
    size = (x2 - x1 - 2 * padding, y2 - y1 - 2 * padding)
    image = contain(img_path, size, bg) if fit == "contain" else cover(img_path, size)
    base.paste(image, (x1 + padding, y1 + padding))


def stat_card(draw: ImageDraw.ImageDraw, box, value: str, label: str, color: str) -> None:
    rounded(draw, box, WHITE, LINE, 2, 20)
    x1, y1, _, _ = box
    draw.text((x1 + 24, y1 + 20), value, font=font(38, True), fill=color)
    draw.text((x1 + 25, y1 + 73), label, font=font(19), fill=MUTED)


def bullet_list(draw: ImageDraw.ImageDraw, items: Iterable[str], x: int, y: int, width: int, *, dot: str = GOLD, size: int = 24, gap: int = 16) -> int:
    for item in items:
        draw.ellipse((x, y + 10, x + 10, y + 20), fill=dot)
        y = draw_wrapped(draw, item, (x + 25, y), size, SLATE, width - 25, line_gap=7)
        y += gap
    return y


def save(page_no: int, title: str, img: Image.Image) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{page_no:02d}_{title}.png"
    img.save(path, quality=95)
    return path


def page_01_cover() -> Path:
    bg = cover(POLISHED / "00_哈工程深蓝封面背景.png", (W, H))
    d = ImageDraw.Draw(bg)
    d.text((118, 112), "基于贝叶斯决策的", font=font(76, True), fill=WHITE)
    d.text((118, 205), "PCB 缺陷检测", font=font(96, True), fill=WHITE)
    d.rectangle((118, 323, 520, 333), fill=GOLD)
    d.text((118, 365), "VisA PCB 真实彩色图像 · normal / anomaly 二分类 · Bayes-only 优化", font=font(31), fill="#D9ECF7")
    d.text((118, 902), "项目流程汇报图册", font=font(32, True), fill=WHITE)
    d.text((118, 950), "电子信息方向 | 模式识别 | MATLAB 实验实现", font=font(23), fill="#CFE8F7")
    d.text((1600, 104), "哈尔滨工程大学", font=font(32, True), fill=WHITE, anchor="mm")
    d.text((1600, 148), "Harbin Engineering University", font=font(20), fill="#CFE8F7", anchor="mm")
    d.text((1600, 184), "大工至善 · 大学至真", font=font(21, True), fill="#F6D77D", anchor="mm")
    return save(1, "封面", bg)


def page_02_storyline() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "汇报主线：从真实图像到贝叶斯决策", "按老师评分点组织：数据、方法、参数、指标、对比、改进。")
    steps = [
        ("01", "数据集", "VisA PCB 真实彩色图像\nnormal / anomaly 二分类"),
        ("02", "特征", "每张图像提取 1318 维\n颜色、灰度、边缘、纹理、LBP、HOG"),
        ("03", "模型", "用贝叶斯公式得到\nP(缺陷|x) 后验概率"),
        ("04", "优化", "PCA 降维、Gamma 正则化\n后验阈值 T 寻优"),
        ("05", "评估", "Accuracy、Precision、Recall\nF1、IoU、AUC、FPR、FNR"),
    ]
    x0, y0, w, h, gap = 90, 280, 325, 300, 50
    for i, (num, title, body) in enumerate(steps):
        x = x0 + i * (w + gap)
        rounded(d, (x, y0, x + w, y0 + h), WHITE, LINE, 2, 28)
        d.ellipse((x + 28, y0 + 28, x + 90, y0 + 90), fill=[OCEAN, NAVY2, BLUE, GOLD, ORANGE][i])
        d.text((x + 59, y0 + 59), num, font=font(22, True), fill=WHITE, anchor="mm")
        d.text((x + 112, y0 + 42), title, font=font(31, True), fill=INK)
        d.line((x + 30, y0 + 118, x + w - 30, y0 + 118), fill="#DDE8F2", width=2)
        draw_wrapped(d, body, (x + 32, y0 + 150), 24, SLATE, w - 64, line_gap=12)
        if i < len(steps) - 1:
            d.line((x + w + 6, y0 + h // 2, x + w + gap - 10, y0 + h // 2), fill="#87AEC9", width=5)
            d.polygon([(x + w + gap - 10, y0 + h // 2), (x + w + gap - 28, y0 + h // 2 - 12), (x + w + gap - 28, y0 + h // 2 + 12)], fill="#87AEC9")
    rounded(d, (220, 735, 1700, 875), PALE_BLUE, "#9CCBE2", 2, 24)
    d.text((265, 770), "一句话逻辑", font=font(32, True), fill=NAVY)
    d.text((475, 773), "把 PCB 图片转为特征向量 x，利用贝叶斯后验概率 P(缺陷|x) 做最小风险判别，再通过参数优化证明性能提升。", font=font(27), fill=INK)
    footer(d, 2)
    return save(2, "汇报主线", img)


def page_03_dataset() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "数据集汇报：VisA PCB 真实彩色图像", "数据真实、类别不均衡、划分清晰，是后续评价指标选择的基础。")
    cards = [
        ("4413", "可用 PCB 图像总数", NAVY2),
        ("4013", "正常样本 normal", OCEAN),
        ("400", "缺陷样本 anomaly", ORANGE),
        ("4 类", "pcb1-pcb4 子集", GOLD),
        ("70/15/15", "训练/验证/测试", NAVY2),
    ]
    for i, item in enumerate(cards):
        stat_card(d, (80 + i * 350, 175, 405 + i * 350, 305), *item)
    rounded(d, (80, 350, 675, 970), WHITE, LINE, 2, 28)
    d.text((118, 390), "类别比例", font=font(34, True), fill=NAVY)
    center, radius, thick = (377, 610), 130, 47
    normal, anomaly = 4013, 400
    angle = 360 * normal / (normal + anomaly)
    box = (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)
    d.pieslice(box, -90, -90 + angle, fill=NAVY2)
    d.pieslice(box, -90 + angle, 270, fill=ORANGE)
    inner = (center[0] - radius + thick, center[1] - radius + thick, center[0] + radius - thick, center[1] + radius - thick)
    d.ellipse(inner, fill=WHITE)
    d.text(center, "4413", font=font(42, True), fill=INK, anchor="mm")
    d.text((center[0], center[1] + 44), "张图像", font=font(21), fill=MUTED, anchor="mm")
    d.rectangle((145, 785, 174, 814), fill=NAVY2)
    d.text((190, 783), "normal：4013 张，占 90.9%", font=font(25), fill=SLATE)
    d.rectangle((145, 835, 174, 864), fill=ORANGE)
    d.text((190, 833), "anomaly：400 张，占 9.1%", font=font(25), fill=SLATE)
    rounded(d, (720, 350, 1240, 970), WHITE, LINE, 2, 28)
    d.text((758, 390), "子集分布", font=font(34, True), fill=NAVY)
    x, y, cw, ch = 785, 520, 390, 280
    for i in range(6):
        yy = y + ch - i * ch / 5
        d.line((x, yy, x + cw, yy), fill="#E4ECF3", width=1)
    for i, subset in enumerate(["pcb1", "pcb2", "pcb3", "pcb4"]):
        bx = x + i * 96 + 20
        nh, ah = 255, 26
        d.rounded_rectangle((bx, y + ch - nh, bx + 30, y + ch), radius=6, fill=NAVY2)
        d.rounded_rectangle((bx + 38, y + ch - ah, bx + 68, y + ch), radius=6, fill=ORANGE)
        d.text((bx + 8, y + ch + 18), subset, font=font(18, True), fill=INK)
    d.line((x, y + ch, x + cw, y + ch), fill="#94A3B8", width=2)
    d.rectangle((790, 875, 815, 900), fill=NAVY2)
    d.text((830, 873), "正常样本", font=font(20), fill=SLATE)
    d.rectangle((940, 875, 965, 900), fill=ORANGE)
    d.text((980, 873), "缺陷样本", font=font(20), fill=SLATE)
    rounded(d, (1280, 350, 1835, 970), WHITE, LINE, 2, 28)
    d.text((1318, 390), "真实样本", font=font(34, True), fill=NAVY)
    sample_paths = [
        (DATA / "pcb1" / "Data" / "Images" / "Normal" / "0313.JPG", "正常 / pcb1", PALE_BLUE, NAVY),
        (DATA / "pcb1" / "Data" / "Images" / "Anomaly" / "000.JPG", "缺陷 / pcb1", PALE_ORANGE, ORANGE),
        (DATA / "pcb4" / "Data" / "Images" / "Anomaly" / "000.JPG", "缺陷 / pcb4", PALE_GOLD, "#805E00"),
    ]
    for idx, (p, label, tag_fill, tag_color) in enumerate(sample_paths):
        yy = 465 + idx * 160
        rounded(d, (1320, yy, 1795, yy + 128), "#FAFCFE", "#D7E2EC", 2, 18)
        if not p.exists():
            p = next((DATA / "pcb4" / "Data" / "Images" / "Anomaly").glob("*.JPG"))
        img.paste(cover(p, (175, 98)), (1338, yy + 15))
        d.rounded_rectangle((1540, yy + 22, 1715, yy + 58), radius=16, fill=tag_fill)
        d.text((1560, yy + 29), label, font=font(20, True), fill=tag_color)
        d.text((1540, yy + 78), "图像 → 1318维特征 x", font=font(20), fill=SLATE)
    rounded(d, (720, 995, 1835, 1050), PALE_BLUE, "#9CCBE2", 2, 18)
    d.text((750, 1012), "汇报重点：类别不均衡，因此后续不能只看准确率，要结合 F1、AUC、FPR/FNR 等指标。", font=font(23, True), fill=NAVY)
    footer(d, 3)
    return save(3, "数据集汇报界面", img)


def page_04_samples() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "任务定义：good / bad 二分类", "正常样本放一张，缺陷样本放两张，强调模型输出的是 P(缺陷|x)。")
    paste_card(img, (78, 165, 1840, 990), POLISHED / "14_正常与缺陷样本归类预览.png", padding=0, fit="contain", bg=BG)
    footer(d, 4)
    return save(4, "任务定义与样本", img)


def page_05_flowchart() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "项目流程：从图像到贝叶斯优化结果", "数据处理、特征工程、贝叶斯建模、参数反馈、指标汇报形成闭环。")
    paste_card(img, (78, 165, 1840, 990), POLISHED / "13_项目流程图.png", padding=0, fit="contain", bg=BG)
    footer(d, 5)
    return save(5, "项目流程图", img)


def page_06_feature_visual() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "特征提取：PCB 图像如何变成 1318 维向量", "贝叶斯模型不能直接读图片，因此先把图像转成结构化特征矩阵。")
    paste_card(img, (78, 165, 1840, 990), POLISHED / "12_图像特征提取过程可视化.png", padding=0, fit="contain", bg=BG)
    footer(d, 6)
    return save(6, "特征提取可视化", img)


def page_07_feature_matrix() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "特征矩阵：模型真正看到的是 X = 4413 × 1318", "每一行是一张图像，每一列是一类手工特征。")
    rounded(d, (90, 185, 1120, 955), WHITE, LINE, 2, 26)
    d.text((130, 225), "特征组成", font=font(36, True), fill=NAVY)
    rows = [
        ("颜色统计 RGB/HSV/Lab", "36", "均值、标准差、偏度、峰度，描述基板与元件颜色"),
        ("灰度统计", "8", "亮度、熵、分位数，描述整体明暗分布"),
        ("边缘密度", "2", "Canny 与 Sobel，捕捉走线和器件边缘"),
        ("GLCM 纹理", "4", "对比度、相关性、能量、同质性"),
        ("LBP 局部纹理", "944", "对局部划痕、污点、纹理异常较敏感"),
        ("HOG 梯度结构", "324", "描述方向梯度和结构轮廓"),
    ]
    y = 300
    d.text((135, y), "特征类别", font=font(24, True), fill=INK)
    d.text((500, y), "维度", font=font(24, True), fill=INK)
    d.text((630, y), "作用解释", font=font(24, True), fill=INK)
    y += 45
    d.line((130, y, 1080, y), fill=LINE, width=2)
    y += 22
    for name, dim, desc in rows:
        d.text((135, y), name, font=font(23, True), fill=INK)
        d.text((520, y), dim, font=font(23, True), fill=ORANGE, anchor="ra")
        draw_wrapped(d, desc, (630, y), 21, SLATE, 420, line_gap=5)
        y += 82
    rounded(d, (1180, 185, 1830, 955), PALE_BLUE, "#9CCBE2", 2, 26)
    d.text((1225, 230), "数据形态", font=font(36, True), fill=NAVY)
    d.text((1225, 305), "X ∈ R^(4413×1318)", font=font(46, True), fill=NAVY2)
    d.text((1225, 375), "Y ∈ {normal, anomaly}", font=font(34, True), fill=ORANGE)
    bullet_list(
        d,
        [
            "标准化只用训练集均值和方差，防止数据泄漏。",
            "PCA 在训练集上学习方向，再映射验证集和测试集。",
            "贝叶斯模型估计 p(x|ω)，再输出 P(缺陷|x)。",
            "最后由阈值 T 把概率变成 normal / anomaly 标签。",
        ],
        1228,
        470,
        545,
        dot=GOLD,
        size=25,
        gap=18,
    )
    footer(d, 7)
    return save(7, "特征矩阵说明", img)


def page_08_bayes_theory() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "贝叶斯决策：从后验概率到缺陷判别", "核心不是直接给标签，而是先得到 P(缺陷|x)，再做最小风险决策。")
    rounded(d, (90, 185, 760, 955), WHITE, LINE, 2, 26)
    d.text((130, 230), "核心公式", font=font(36, True), fill=NAVY)
    rounded(d, (135, 305, 710, 395), PALE_BLUE, "#9CCBE2", 2, 18)
    d.text((422, 350), "P(ωₖ|x)= p(x|ωₖ)P(ωₖ) / Σⱼp(x|ωⱼ)P(ωⱼ)", font=font(24, True), fill=NAVY, anchor="mm")
    rounded(d, (135, 430, 710, 520), PALE_GOLD, "#EAD18B", 2, 18)
    d.text((422, 475), "若 P(缺陷|x) ≥ T，则判为缺陷；否则判为正常", font=font(24, True), fill="#6B4E00", anchor="mm")
    bullet_list(
        d,
        [
            "ω₁：normal，ω₂：anomaly。",
            "T 是后验概率阈值，控制误报和漏报。",
            "如果漏检代价更高，可以调低阈值；如果误报代价更高，可以调高阈值。",
        ],
        135,
        590,
        535,
        dot=CYAN,
        size=24,
        gap=20,
    )
    paste_card(img, (815, 185, 1830, 955), POLISHED / "09_一维概率分布与贝叶斯误差.png", padding=16, fit="contain")
    footer(d, 8)
    return save(8, "贝叶斯决策原理", img)


def page_09_code() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "贝叶斯模型核心代码：训练、后验概率、阈值决策", "这一页用于讲清楚 MATLAB 中 Bayes-0 到 Bayes-4 的实现逻辑。")
    rounded(d, (80, 175, 1160, 980), "#102033", "#28465F", 2, 20)
    d.rectangle((80, 175, 1160, 225), fill="#0B1828")
    d.text((108, 190), "MATLAB 核心代码", font=font(22, True), fill="#E8F2FA")
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
    y = 255
    for line in code.splitlines():
        d.text((110, y), line, font=mono(24), fill="#E8F2FA")
        y += 34
    rounded(d, (1210, 175, 1835, 980), WHITE, LINE, 2, 20)
    d.text((1250, 225), "讲解口径", font=font(36, True), fill=NAVY)
    bullet_list(
        d,
        [
            "PCA 先把 1318 维高维特征压缩到更稳定的低维空间。",
            "fitcdiscr 的 Gamma 是正则化参数，用来稳定协方差估计。",
            "predict 返回每一类后验分数，取 anomaly 对应列得到 P(缺陷|x)。",
            "阈值 T 把概率输出转成最终标签，是贝叶斯风险控制的一部分。",
        ],
        1250,
        310,
        520,
        dot=GOLD,
        size=25,
        gap=20,
    )
    footer(d, 9)
    return save(9, "贝叶斯模型代码展示", img)


def page_10_optimization() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "Bayes-only 优化路径：不换模型，只优化贝叶斯决策", "对比对象是 Bayes-0 到 Bayes-4，而不是 CNN、BP、Kmeans。")
    rounded(d, (90, 185, 630, 955), WHITE, LINE, 2, 26)
    d.text((130, 225), "五个阶段", font=font(36, True), fill=NAVY)
    stages = [
        ("Bayes-0", "原始朴素贝叶斯"),
        ("Bayes-1", "PCA 降维优化"),
        ("Bayes-2", "高斯建模优化"),
        ("Bayes-3", "Gamma 正则化优化"),
        ("Bayes-4", "后验阈值优化"),
    ]
    y = 300
    for i, (a, b) in enumerate(stages):
        fill = PALE_GOLD if i == 4 else PALE_BLUE
        outline = "#EAD18B" if i == 4 else "#B6D9EA"
        rounded(d, (130, y, 590, y + 88), fill, outline, 2, 18)
        d.text((155, y + 28), a, font=font(24, True), fill=NAVY if i < 4 else "#6B4E00")
        d.text((300, y + 30), b, font=font(23), fill=INK)
        y += 112
    paste_card(img, (675, 185, 1830, 955), POLISHED / "03_贝叶斯优化迭代趋势.png", padding=16, fit="contain")
    footer(d, 10)
    return save(10, "贝叶斯优化路径", img)


def page_11_parameters() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "参数分析：PCA 维度 × Gamma 正则化", "用验证集 F1 选择关键参数，证明调参过程是科学的。")
    paste_card(img, (80, 175, 1120, 980), POLISHED / "05_主成分维度与正则化参数热力图.png", padding=16, fit="contain")
    rounded(d, (1170, 175, 1835, 980), WHITE, LINE, 2, 24)
    d.text((1210, 225), "图怎么讲", font=font(36, True), fill=NAVY)
    bullet_list(
        d,
        [
            "纵轴是 PCA 维度：过低会丢信息，过高会引入噪声和冗余。",
            "横轴是 Gamma：控制协方差估计的正则化强度。",
            "颜色越深表示验证集 F1 越高。",
            "金色框对应当前最佳参数区域。",
        ],
        1210,
        310,
        560,
        dot=GOLD,
        size=26,
        gap=22,
    )
    rounded(d, (1210, 735, 1795, 885), PALE_BLUE, "#9CCBE2", 2, 20)
    draw_wrapped(d, "汇报句式：我先固定评价指标为 F1，再在验证集上同时搜索 PCA 维度和 Gamma，最后只在测试集上汇报最终性能。", (1240, 770), 24, NAVY, 520, bold=True, line_gap=10)
    footer(d, 11)
    return save(11, "参数热力图", img)


def page_12_threshold() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "阈值与风险：为什么不是固定 0.5", "后验概率阈值 T 决定误报和漏报的权衡。")
    paste_card(img, (80, 175, 945, 980), POLISHED / "06_后验概率阈值决策曲线.png", padding=16, fit="contain")
    paste_card(img, (985, 175, 1835, 980), POLISHED / "11_贝叶斯风险与损失函数.png", padding=16, fit="contain")
    footer(d, 12)
    return save(12, "阈值风险权衡", img)


def page_13_metrics() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "核心指标横向对比：优化后到底提升在哪里", "用多指标说明结果，避免类别不均衡下 Accuracy 误导。")
    paste_card(img, (80, 175, 1080, 980), POLISHED / "02_五大指标横向对比.png", padding=16, fit="contain")
    rounded(d, (1130, 175, 1835, 980), WHITE, LINE, 2, 24)
    d.text((1170, 225), "最终 Bayes-4", font=font(36, True), fill=NAVY)
    stats = [("0.918", "Accuracy", NAVY2), ("0.542", "F1-score", ORANGE), ("0.899", "AUC", OCEAN), ("0.372", "IoU", GOLD)]
    for i, (v, lab, col) in enumerate(stats):
        x = 1170 + (i % 2) * 310
        y = 300 + (i // 2) * 150
        stat_card(d, (x, y, x + 275, y + 120), v, lab, col)
    bullet_list(
        d,
        [
            "Bayes-0 的 F1 低，说明原始朴素贝叶斯对缺陷类识别不足。",
            "Bayes-4 提高了精确率，减少把正常 PCB 误报为缺陷的情况。",
            "AUC 保持较高，说明后验概率排序能力较稳定。",
        ],
        1170,
        655,
        560,
        dot=CYAN,
        size=25,
        gap=20,
    )
    footer(d, 13)
    return save(13, "核心指标对比", img)


def page_14_errors() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "误报与漏报：质量检测里最需要解释的权衡", "FPR 表示误报，FNR 表示漏检；二者决定真实应用风险。")
    paste_card(img, (80, 175, 985, 980), POLISHED / "04_误报率与漏报率权衡.png", padding=16, fit="contain")
    paste_card(img, (1030, 175, 1835, 980), BASIC / "基础图_贝叶斯混淆矩阵.png", padding=16, fit="contain")
    footer(d, 14)
    return save(14, "误报漏报与混淆矩阵", img)


def page_15_summary() -> Path:
    img = make_canvas()
    d = ImageDraw.Draw(img)
    header(d, "总结：贝叶斯方案的价值与边界", "用可解释概率决策完成 PCB 缺陷识别，但也要主动说明方法局限。")
    paste_card(img, (80, 170, 980, 985), POLISHED / "08_贝叶斯优化性能评估仪表盘.png", padding=16, fit="contain")
    rounded(d, (1025, 170, 1835, 985), WHITE, LINE, 2, 24)
    d.text((1070, 220), "可以强调的贡献", font=font(34, True), fill=NAVY)
    y = bullet_list(
        d,
        [
            "选用真实彩色 PCB 图像，贴近电子信息质量检测场景。",
            "构建 1318 维手工特征，并解释颜色、纹理、边缘、梯度的物理含义。",
            "在贝叶斯框架内完成 PCA、Gamma、阈值三类优化。",
            "使用多指标和多图表完成横向、纵向、参数、风险可视化。",
        ],
        1070,
        285,
        660,
        dot=GOLD,
        size=24,
        gap=16,
    )
    d.text((1070, y + 10), "主动承认的不足", font=font(34, True), fill=ORANGE)
    bullet_list(
        d,
        [
            "贝叶斯依赖手工特征，难以自动学习复杂空间拓扑结构。",
            "缺陷样本少且类别不均衡，precision 与 recall 存在权衡。",
            "当前是图像级识别，不是像素级缺陷分割。",
        ],
        1070,
        y + 78,
        660,
        dot=CYAN,
        size=24,
        gap=16,
    )
    footer(d, 15)
    return save(15, "总结与反思", img)


def make_contact_sheet(paths: list[Path]) -> Path:
    thumb_w, thumb_h = 384, 216
    cols = 3
    rows = math.ceil(len(paths) / cols)
    margin = 26
    label_h = 32
    sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * margin, rows * (thumb_h + label_h) + (rows + 1) * margin), BG)
    d = ImageDraw.Draw(sheet)
    for idx, p in enumerate(paths):
        im = Image.open(p).convert("RGB").resize((thumb_w, thumb_h), RESAMPLE)
        r, c = divmod(idx, cols)
        x = margin + c * (thumb_w + margin)
        y = margin + r * (thumb_h + label_h + margin)
        d.text((x, y), f"{idx + 1:02d}  {p.name}", font=font(18), fill=NAVY)
        sheet.paste(im, (x, y + label_h))
        d.rectangle((x, y + label_h, x + thumb_w - 1, y + label_h + thumb_h - 1), outline=LINE, width=2)
    out = OUT / "00_全部图片页总览.png"
    sheet.save(out, quality=95)
    return out


def main() -> None:
    paths = [
        page_01_cover(),
        page_02_storyline(),
        page_03_dataset(),
        page_04_samples(),
        page_05_flowchart(),
        page_06_feature_visual(),
        page_07_feature_matrix(),
        page_08_bayes_theory(),
        page_09_code(),
        page_10_optimization(),
        page_11_parameters(),
        page_12_threshold(),
        page_13_metrics(),
        page_14_errors(),
        page_15_summary(),
    ]
    contact = make_contact_sheet(paths)
    print("Generated image report pages:")
    for p in paths:
        print(p)
    print(contact)


if __name__ == "__main__":
    main()
