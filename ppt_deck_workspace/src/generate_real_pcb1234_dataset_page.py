# 中文注释：生成真实 PCB1 到 PCB4 数据集说明页。
# 主要流程：展示四个 PCB 子集的样本来源、类别含义和项目使用方式。
# 输出结果：形成可直接插入汇报的单页图片。

# 行注释：这里启用较新的 Python 类型注解行为。
from __future__ import annotations

# 行注释：这里导入脚本后面需要用到的 Python 模块。
from pathlib import Path

# 行注释：这里导入脚本后面需要用到的 Python 模块。
import numpy as np
# 行注释：这里导入脚本后面需要用到的 Python 模块。
from PIL import Image, ImageDraw, ImageFont


# 行注释：这里设置 ROOT 的值，后续绘图或计算会用到。
ROOT = Path(r"C:\Users\19571\Desktop\研讨\PCB_Bayes_Project")
# 行注释：这里设置 DATA 的值，后续绘图或计算会用到。
DATA = ROOT / "data" / "raw" / "visa"
# 行注释：这里设置 OUT_DIR 的值，后续绘图或计算会用到。
OUT_DIR = ROOT / "image2_report_pages"
# 行注释：这里设置 OUT 的值，后续绘图或计算会用到。
OUT = OUT_DIR / "03_数据集采集_真实PCB1234正常缺陷对照.png"

# 行注释：这里设置 W, H 的值，后续绘图或计算会用到。
W, H = 1920, 1080
# 行注释：这里设置 NAVY 的值，后续绘图或计算会用到。
NAVY = "#003B73"
# 行注释：这里设置 NAVY_DARK 的值，后续绘图或计算会用到。
NAVY_DARK = "#08243D"
# 行注释：这里设置 BLUE 的值，后续绘图或计算会用到。
BLUE = "#004488"
# 行注释：这里设置 CYAN 的值，后续绘图或计算会用到。
CYAN = "#1B95C9"
# 行注释：这里设置 ORANGE 的值，后续绘图或计算会用到。
ORANGE = "#D95319"
# 行注释：这里设置 GOLD 的值，后续绘图或计算会用到。
GOLD = "#C99700"
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
# 行注释：这里设置 PALE_BLUE 的值，后续绘图或计算会用到。
PALE_BLUE = "#E8F5FB"
# 行注释：这里设置 PALE_ORANGE 的值，后续绘图或计算会用到。
PALE_ORANGE = "#FFF1E8"
# 行注释：这里设置 PALE_GOLD 的值，后续绘图或计算会用到。
PALE_GOLD = "#FFF7D8"

# 行注释：这里尝试执行可能因为环境差异而失败的代码。
try:
    # 行注释：这里设置 RESAMPLE 的值，后续绘图或计算会用到。
    RESAMPLE = Image.Resampling.LANCZOS
# 行注释：这里处理上面 try 捕获到的异常情况。
except AttributeError:
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
        if Path(item).exists():
            # 行注释：这里把结果返回给调用它的代码。
            return ImageFont.truetype(item, size=size)
    # 行注释：这里把结果返回给调用它的代码。
    return ImageFont.load_default()


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
    radius: int = 22,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> None:
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


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
    # 行注释：这里设置 new_size 的值，后续绘图或计算会用到。
    new_size = (max(1, int(sw * scale)), max(1, int(sh * scale)))
    # 行注释：这里设置 resized 的值，后续绘图或计算会用到。
    resized = img.resize(new_size, RESAMPLE)
    # 行注释：这里设置 left 的值，后续绘图或计算会用到。
    left = (resized.width - tw) // 2
    # 行注释：这里设置 top 的值，后续绘图或计算会用到。
    top = (resized.height - th) // 2
    # 行注释：这里把结果返回给调用它的代码。
    return resized.crop((left, top, left + tw, top + th))


# 函数说明：把图片完整放入目标区域，必要时留白。
# 行注释：这里定义 contain 函数。
def contain(path: Path, size: tuple[int, int]) -> Image.Image:
    # 行注释：这里读取一张图片并准备处理。
    img = Image.open(path).convert("RGB")
    # 行注释：这里设置 img 的值，后续绘图或计算会用到。
    img = crop_pcb_region(img)
    # 行注释：这里设置 tw, th 的值，后续绘图或计算会用到。
    tw, th = size
    # 行注释：这里设置 sw, sh 的值，后续绘图或计算会用到。
    sw, sh = img.size
    # 行注释：这里设置 scale 的值，后续绘图或计算会用到。
    scale = min(tw / sw, th / sh)
    # 行注释：这里设置 new_size 的值，后续绘图或计算会用到。
    new_size = (max(1, int(sw * scale)), max(1, int(sh * scale)))
    # 行注释：这里设置 resized 的值，后续绘图或计算会用到。
    resized = img.resize(new_size, RESAMPLE)
    # 行注释：这里创建新的图片画布。
    canvas = Image.new("RGB", size, WHITE)
    # 行注释：这里设置 left 的值，后续绘图或计算会用到。
    left = (tw - resized.width) // 2
    # 行注释：这里设置 top 的值，后续绘图或计算会用到。
    top = (th - resized.height) // 2
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    canvas.paste(resized, (left, top))
    # 行注释：这里把结果返回给调用它的代码。
    return canvas


# 函数说明：裁剪 PCB 图像的有效区域，减少无关边框干扰。
# 行注释：这里定义 crop_pcb_region 函数。
def crop_pcb_region(img: Image.Image) -> Image.Image:
    # 行注释：这里设置 arr 的值，后续绘图或计算会用到。
    arr = np.asarray(img).astype(np.int16)
    # 行注释：这里设置 r, g, b 的值，后续绘图或计算会用到。
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    # 行注释：这里设置 mask 的值，后续绘图或计算会用到。
    mask = (b > 70) & (b > r + 20) & (b > g - 10)
    # 行注释：这里设置 ys, xs 的值，后续绘图或计算会用到。
    ys, xs = np.where(mask)
    # 行注释：这里判断条件是否满足。
    if len(xs) < 200:
        # 行注释：这里把结果返回给调用它的代码。
        return img

    # 行注释：这里设置 x1, x2 的值，后续绘图或计算会用到。
    x1, x2 = int(xs.min()), int(xs.max())
    # 行注释：这里设置 y1, y2 的值，后续绘图或计算会用到。
    y1, y2 = int(ys.min()), int(ys.max())
    # 行注释：这里设置 bw, bh 的值，后续绘图或计算会用到。
    bw, bh = x2 - x1 + 1, y2 - y1 + 1
    # 行注释：这里设置 pad_x 的值，后续绘图或计算会用到。
    pad_x = max(50, int(bw * 0.20))
    # 行注释：这里设置 pad_y 的值，后续绘图或计算会用到。
    pad_y = max(50, int(bh * 0.25))
    # 行注释：这里设置 x1 的值，后续绘图或计算会用到。
    x1 = max(0, x1 - pad_x)
    # 行注释：这里设置 x2 的值，后续绘图或计算会用到。
    x2 = min(img.width, x2 + pad_x)
    # 行注释：这里设置 y1 的值，后续绘图或计算会用到。
    y1 = max(0, y1 - pad_y)
    # 行注释：这里设置 y2 的值，后续绘图或计算会用到。
    y2 = min(img.height, y2 + pad_y)
    # 行注释：这里把结果返回给调用它的代码。
    return img.crop((x1, y1, x2, y2))


# 函数说明：按子集和标签找到一张代表性样本图。
# 行注释：这里定义 sample_path 函数。
def sample_path(subset: str, label: str, preferred: str) -> Path:
    # 行注释：这里设置 folder 的值，后续绘图或计算会用到。
    folder = DATA / subset / "Data" / "Images" / label
    # 行注释：这里设置 preferred_path 的值，后续绘图或计算会用到。
    preferred_path = folder / preferred
    # 行注释：这里判断条件是否满足。
    if preferred_path.exists():
        # 行注释：这里把结果返回给调用它的代码。
        return preferred_path
    # 行注释：这里设置 files 的值，后续绘图或计算会用到。
    files = sorted(folder.glob("*.JPG"))
    # 行注释：这里判断条件是否满足。
    if not files:
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        raise FileNotFoundError(f"No JPG images found in {folder}")
    # 行注释：这里把结果返回给调用它的代码。
    return files[0]


# 函数说明：在指定区域居中绘制文字。
# 行注释：这里定义 text_center 函数。
def text_center(
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw: ImageDraw.ImageDraw,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    box: tuple[int, int, int, int],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    text: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    text_font: ImageFont.FreeTypeFont,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fill: str,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> None:
    # 行注释：这里设置 x1, y1, x2, y2 的值，后续绘图或计算会用到。
    x1, y1, x2, y2 = box
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    bbox = draw.textbbox((0, 0), text, font=text_font)
    # 行注释：这里设置 tw 的值，后续绘图或计算会用到。
    tw = bbox[2] - bbox[0]
    # 行注释：这里设置 th 的值，后续绘图或计算会用到。
    th = bbox[3] - bbox[1]
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - 1), text, font=text_font, fill=fill)


# 函数说明：绘制小标签，用来标注正常或缺陷类别。
# 行注释：这里定义 draw_tag 函数。
def draw_tag(
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw: ImageDraw.ImageDraw,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    x: int,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    y: int,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    label: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fill: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    color: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    width: int = 120,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> None:
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rounded_rectangle((x, y, x + width, y + 38), radius=19, fill=fill)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    text_center(draw, (x, y, x + width, y + 38), label, font(19, True), color)


# 函数说明：绘制单张样本图及其文字说明。
# 行注释：这里定义 draw_sample 函数。
def draw_sample(
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    base: Image.Image,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw: ImageDraw.ImageDraw,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    box: tuple[int, int, int, int],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    img_path: Path,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    tag: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    tag_fill: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    tag_color: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    caption: str,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> None:
    # 行注释：这里设置 x1, y1, x2, y2 的值，后续绘图或计算会用到。
    x1, y1, x2, y2 = box
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, box, WHITE, "#B8CAD9", 2, 18)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_tag(draw, x1 + 16, y1 + 14, tag, tag_fill, tag_color, 128)

    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 158, y1 + 20), caption, font=font(17), fill=MUTED)

    # 行注释：这里设置 image_box 的值，后续绘图或计算会用到。
    image_box = (x1 + 16, y1 + 60, x2 - 16, y2 - 16)
    # 行注释：这里设置 thumb 的值，后续绘图或计算会用到。
    thumb = contain(img_path, (image_box[2] - image_box[0], image_box[3] - image_box[1]))
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    base.paste(thumb, (image_box[0], image_box[1]))
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.rectangle(image_box, outline="#FFFFFF", width=2)


# 函数说明：绘制一个 PCB 子集卡片，展示正常/缺陷样本。
# 行注释：这里定义 draw_subset_card 函数。
def draw_subset_card(
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    base: Image.Image,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw: ImageDraw.ImageDraw,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    subset: str,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    box: tuple[int, int, int, int],
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    normal_img: Path,
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    anomaly_img: Path,
# 行注释：这里结束当前多行参数、列表或代码结构。
) -> None:
    # 行注释：这里设置 x1, y1, x2, y2 的值，后续绘图或计算会用到。
    x1, y1, x2, y2 = box
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, box, WHITE, LINE, 2, 24)

    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 24, y1 + 20), subset.upper(), font=font(32, True), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 132, y1 + 31), "真实拍摄样本：正常 / 缺陷成对展示", font=font(20), fill=MUTED)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.line((x1 + 24, y1 + 70, x2 - 24, y1 + 70), fill="#E4EDF5", width=2)

    # 行注释：这里设置 inner_y 的值，后续绘图或计算会用到。
    inner_y = y1 + 88
    # 行注释：这里设置 sample_w 的值，后续绘图或计算会用到。
    sample_w = (x2 - x1 - 66) // 2
    # 行注释：这里设置 left_box 的值，后续绘图或计算会用到。
    left_box = (x1 + 22, inner_y, x1 + 22 + sample_w, y2 - 22)
    # 行注释：这里设置 right_box 的值，后续绘图或计算会用到。
    right_box = (x1 + 44 + sample_w, inner_y, x2 - 22, y2 - 22)

    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_sample(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        base,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        left_box,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        normal_img,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "正常",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        PALE_BLUE,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        BLUE,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        f"good 类 / {subset}",
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    draw_sample(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        base,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        right_box,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        anomaly_img,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "缺陷",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        PALE_ORANGE,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ORANGE,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        f"bad 类 / {subset}",
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )


# 函数说明：绘制数据统计卡片。
# 行注释：这里定义 draw_stat_card 函数。
def draw_stat_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], value: str, label: str, color: str) -> None:
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(draw, box, WHITE, LINE, 2, 18)
    # 行注释：这里设置 x1, y1, _, _ 的值，后续绘图或计算会用到。
    x1, y1, _, _ = box
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 24, y1 + 17), value, font=font(32, True), fill=color)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    draw.text((x1 + 25, y1 + 61), label, font=font(18), fill=MUTED)


# 函数说明：脚本入口，按顺序调用前面的函数生成最终文件。
# 行注释：这里定义 main 函数。
def main() -> None:
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # 行注释：这里创建新的图片画布。
    img = Image.new("RGB", (W, H), BG)
    # 行注释：这里创建绘图对象，后面用它画文字和形状。
    d = ImageDraw.Draw(img)

    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rectangle((0, 0, W, 126), fill=NAVY)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text((76, 30), "数据集采集：VisA PCB1-4 真实图像样本", font=font(44, True), fill=WHITE)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.text(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (78, 86),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "每个 PCB 子集均包含 normal 与 anomaly，最终统一映射为 good / bad 二分类任务",
        # 行注释：这里设置 font 的值，后续绘图或计算会用到。
        font=font(23),
        # 行注释：这里设置 fill 的值，后续绘图或计算会用到。
        fill="#D4EBF8",
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    d.rounded_rectangle((1508, 39, 1838, 88), radius=24, fill="#0A4B82")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    text_center(d, (1508, 39, 1838, 88), "HEU | PCB Dataset", font(18, True), WHITE)

    # 行注释：这里设置 stats 的值，后续绘图或计算会用到。
    stats = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("4413", "可用真实图像总数", BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("4013", "normal 正常样本", CYAN),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("400", "anomaly 缺陷样本", ORANGE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("PCB1-4", "四类电子模块子集", GOLD),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("70/15/15", "训练/验证/测试划分", BLUE),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i, (value, label, color) in enumerate(stats):
        # 行注释：这里设置 x 的值，后续绘图或计算会用到。
        x = 78 + i * 350
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw_stat_card(d, (x, 150, x + 318, 248), value, label, color)

    # 行注释：这里设置 choices 的值，后续绘图或计算会用到。
    choices = {
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "pcb1": ("0313.JPG", "000.JPG"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "pcb2": ("0000.JPG", "000.JPG"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "pcb3": ("0000.JPG", "000.JPG"),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "pcb4": ("0000.JPG", "000.JPG"),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    }
    # 行注释：这里设置 layout 的值，后续绘图或计算会用到。
    layout = {
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "pcb1": (76, 278, 930, 615),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "pcb2": (990, 278, 1844, 615),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "pcb3": (76, 638, 930, 975),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "pcb4": (990, 638, 1844, 975),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    }

    # 行注释：这里开始循环，逐个处理列表或数据项。
    for subset, box in layout.items():
        # 行注释：这里设置 normal_file, anomaly_file 的值，后续绘图或计算会用到。
        normal_file, anomaly_file = choices[subset]
        # 行注释：这里设置 normal 的值，后续绘图或计算会用到。
        normal = sample_path(subset, "Normal", normal_file)
        # 行注释：这里设置 anomaly 的值，后续绘图或计算会用到。
        anomaly = sample_path(subset, "Anomaly", anomaly_file)
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        draw_subset_card(img, d, subset, box, normal, anomaly)

    # 行注释：这里执行当前语句，推进这一小步逻辑。
    rounded(d, (236, 1003, 1684, 1052), PALE_GOLD, "#E1C463", 2, 16)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    text_center(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        d,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        (236, 1003, 1684, 1052),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "汇报口径：真实彩色 PCB 图像 → 1318 维手工特征 → 贝叶斯后验概率 P(bad|x) → good / bad 判决",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        font(22, True),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        NAVY_DARK,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )

    # 行注释：这里把生成的图片或文件保存到磁盘。
    img.save(OUT, quality=95)
    # 行注释：这里在终端输出生成结果或进度信息。
    print(OUT)


# 行注释：这里判断脚本是否被直接运行。
if __name__ == "__main__":
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    main()
