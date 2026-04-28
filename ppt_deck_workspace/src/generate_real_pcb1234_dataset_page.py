# 中文注释：生成真实 PCB1 到 PCB4 数据集说明页。
# 主要流程：展示四个 PCB 子集的样本来源、类别含义和项目使用方式。
# 输出结果：形成可直接插入汇报的单页图片。

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"C:\Users\19571\Desktop\研讨\PCB_Bayes_Project")
DATA = ROOT / "data" / "raw" / "visa"
OUT_DIR = ROOT / "image2_report_pages"
OUT = OUT_DIR / "03_数据集采集_真实PCB1234正常缺陷对照.png"

W, H = 1920, 1080
NAVY = "#003B73"
NAVY_DARK = "#08243D"
BLUE = "#004488"
CYAN = "#1B95C9"
ORANGE = "#D95319"
GOLD = "#C99700"
INK = "#0F172A"
MUTED = "#64748B"
LINE = "#C7D5E3"
BG = "#F4F8FB"
WHITE = "#FFFFFF"
PALE_BLUE = "#E8F5FB"
PALE_ORANGE = "#FFF1E8"
PALE_GOLD = "#FFF7D8"

try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE = Image.LANCZOS


# 函数说明：加载中文字体，保证图片里的中文能正常显示。
def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    for item in candidates:
        if Path(item).exists():
            return ImageFont.truetype(item, size=size)
    return ImageFont.load_default()


# 函数说明：绘制圆角矩形，作为信息卡片或内容面板。
def rounded(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: str = WHITE,
    outline: str = LINE,
    width: int = 2,
    radius: int = 22,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# 函数说明：把图片按目标区域裁剪填满，用于样本展示。
def cover(path: Path, size: tuple[int, int]) -> Image.Image:
    img = Image.open(path).convert("RGB")
    tw, th = size
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    new_size = (max(1, int(sw * scale)), max(1, int(sh * scale)))
    resized = img.resize(new_size, RESAMPLE)
    left = (resized.width - tw) // 2
    top = (resized.height - th) // 2
    return resized.crop((left, top, left + tw, top + th))


# 函数说明：把图片完整放入目标区域，必要时留白。
def contain(path: Path, size: tuple[int, int]) -> Image.Image:
    img = Image.open(path).convert("RGB")
    img = crop_pcb_region(img)
    tw, th = size
    sw, sh = img.size
    scale = min(tw / sw, th / sh)
    new_size = (max(1, int(sw * scale)), max(1, int(sh * scale)))
    resized = img.resize(new_size, RESAMPLE)
    canvas = Image.new("RGB", size, WHITE)
    left = (tw - resized.width) // 2
    top = (th - resized.height) // 2
    canvas.paste(resized, (left, top))
    return canvas


# 函数说明：裁剪 PCB 图像的有效区域，减少无关边框干扰。
def crop_pcb_region(img: Image.Image) -> Image.Image:
    arr = np.asarray(img).astype(np.int16)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mask = (b > 70) & (b > r + 20) & (b > g - 10)
    ys, xs = np.where(mask)
    if len(xs) < 200:
        return img

    x1, x2 = int(xs.min()), int(xs.max())
    y1, y2 = int(ys.min()), int(ys.max())
    bw, bh = x2 - x1 + 1, y2 - y1 + 1
    pad_x = max(50, int(bw * 0.20))
    pad_y = max(50, int(bh * 0.25))
    x1 = max(0, x1 - pad_x)
    x2 = min(img.width, x2 + pad_x)
    y1 = max(0, y1 - pad_y)
    y2 = min(img.height, y2 + pad_y)
    return img.crop((x1, y1, x2, y2))


# 函数说明：按子集和标签找到一张代表性样本图。
def sample_path(subset: str, label: str, preferred: str) -> Path:
    folder = DATA / subset / "Data" / "Images" / label
    preferred_path = folder / preferred
    if preferred_path.exists():
        return preferred_path
    files = sorted(folder.glob("*.JPG"))
    if not files:
        raise FileNotFoundError(f"No JPG images found in {folder}")
    return files[0]


# 函数说明：在指定区域居中绘制文字。
def text_center(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    text_font: ImageFont.FreeTypeFont,
    fill: str,
) -> None:
    x1, y1, x2, y2 = box
    bbox = draw.textbbox((0, 0), text, font=text_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - 1), text, font=text_font, fill=fill)


# 函数说明：绘制小标签，用来标注正常或缺陷类别。
def draw_tag(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    label: str,
    fill: str,
    color: str,
    width: int = 120,
) -> None:
    draw.rounded_rectangle((x, y, x + width, y + 38), radius=19, fill=fill)
    text_center(draw, (x, y, x + width, y + 38), label, font(19, True), color)


# 函数说明：绘制单张样本图及其文字说明。
def draw_sample(
    base: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    img_path: Path,
    tag: str,
    tag_fill: str,
    tag_color: str,
    caption: str,
) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, WHITE, "#B8CAD9", 2, 18)
    draw_tag(draw, x1 + 16, y1 + 14, tag, tag_fill, tag_color, 128)

    draw.text((x1 + 158, y1 + 20), caption, font=font(17), fill=MUTED)

    image_box = (x1 + 16, y1 + 60, x2 - 16, y2 - 16)
    thumb = contain(img_path, (image_box[2] - image_box[0], image_box[3] - image_box[1]))
    base.paste(thumb, (image_box[0], image_box[1]))
    draw.rectangle(image_box, outline="#FFFFFF", width=2)


# 函数说明：绘制一个 PCB 子集卡片，展示正常/缺陷样本。
def draw_subset_card(
    base: Image.Image,
    draw: ImageDraw.ImageDraw,
    subset: str,
    box: tuple[int, int, int, int],
    normal_img: Path,
    anomaly_img: Path,
) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, WHITE, LINE, 2, 24)

    draw.text((x1 + 24, y1 + 20), subset.upper(), font=font(32, True), fill=NAVY)
    draw.text((x1 + 132, y1 + 31), "真实拍摄样本：正常 / 缺陷成对展示", font=font(20), fill=MUTED)
    draw.line((x1 + 24, y1 + 70, x2 - 24, y1 + 70), fill="#E4EDF5", width=2)

    inner_y = y1 + 88
    sample_w = (x2 - x1 - 66) // 2
    left_box = (x1 + 22, inner_y, x1 + 22 + sample_w, y2 - 22)
    right_box = (x1 + 44 + sample_w, inner_y, x2 - 22, y2 - 22)

    draw_sample(
        base,
        draw,
        left_box,
        normal_img,
        "正常",
        PALE_BLUE,
        BLUE,
        f"good 类 / {subset}",
    )
    draw_sample(
        base,
        draw,
        right_box,
        anomaly_img,
        "缺陷",
        PALE_ORANGE,
        ORANGE,
        f"bad 类 / {subset}",
    )


# 函数说明：绘制数据统计卡片。
def draw_stat_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], value: str, label: str, color: str) -> None:
    rounded(draw, box, WHITE, LINE, 2, 18)
    x1, y1, _, _ = box
    draw.text((x1 + 24, y1 + 17), value, font=font(32, True), fill=color)
    draw.text((x1 + 25, y1 + 61), label, font=font(18), fill=MUTED)


# 函数说明：脚本入口，按顺序调用前面的函数生成最终文件。
def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    d.rectangle((0, 0, W, 126), fill=NAVY)
    d.text((76, 30), "数据集采集：VisA PCB1-4 真实图像样本", font=font(44, True), fill=WHITE)
    d.text(
        (78, 86),
        "每个 PCB 子集均包含 normal 与 anomaly，最终统一映射为 good / bad 二分类任务",
        font=font(23),
        fill="#D4EBF8",
    )
    d.rounded_rectangle((1508, 39, 1838, 88), radius=24, fill="#0A4B82")
    text_center(d, (1508, 39, 1838, 88), "HEU | PCB Dataset", font(18, True), WHITE)

    stats = [
        ("4413", "可用真实图像总数", BLUE),
        ("4013", "normal 正常样本", CYAN),
        ("400", "anomaly 缺陷样本", ORANGE),
        ("PCB1-4", "四类电子模块子集", GOLD),
        ("70/15/15", "训练/验证/测试划分", BLUE),
    ]
    for i, (value, label, color) in enumerate(stats):
        x = 78 + i * 350
        draw_stat_card(d, (x, 150, x + 318, 248), value, label, color)

    choices = {
        "pcb1": ("0313.JPG", "000.JPG"),
        "pcb2": ("0000.JPG", "000.JPG"),
        "pcb3": ("0000.JPG", "000.JPG"),
        "pcb4": ("0000.JPG", "000.JPG"),
    }
    layout = {
        "pcb1": (76, 278, 930, 615),
        "pcb2": (990, 278, 1844, 615),
        "pcb3": (76, 638, 930, 975),
        "pcb4": (990, 638, 1844, 975),
    }

    for subset, box in layout.items():
        normal_file, anomaly_file = choices[subset]
        normal = sample_path(subset, "Normal", normal_file)
        anomaly = sample_path(subset, "Anomaly", anomaly_file)
        draw_subset_card(img, d, subset, box, normal, anomaly)

    rounded(d, (236, 1003, 1684, 1052), PALE_GOLD, "#E1C463", 2, 16)
    text_center(
        d,
        (236, 1003, 1684, 1052),
        "汇报口径：真实彩色 PCB 图像 → 1318 维手工特征 → 贝叶斯后验概率 P(bad|x) → good / bad 判决",
        font(22, True),
        NAVY_DARK,
    )

    img.save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    main()
