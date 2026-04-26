from __future__ import annotations

import csv
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "results" / "visa_pcb" / "bayes_optimization_comparison.csv"
OUT_DIR = ROOT / "results" / "figures"
OUT_BASELINE = OUT_DIR / "13_朴素贝叶斯基准诊断信息图.png"
OUT_CODE = OUT_DIR / "14_贝叶斯优化过程代码体现图.png"

W, H = 1920, 1080
NAVY = "#003B73"
NAVY_DARK = "#08243D"
BLUE = "#004488"
BLUE2 = "#1B95C9"
PALE_BLUE = "#E8F5FB"
PALE_GREEN = "#E8F7EF"
PALE_ORANGE = "#FFF1E8"
PALE_GOLD = "#FFF7D8"
ORANGE = "#D95319"
RED = "#B22222"
GOLD = "#C99700"
GREEN = "#258A52"
INK = "#0F172A"
MUTED = "#64748B"
LINE = "#C7D5E3"
BG = "#F4F8FB"
WHITE = "#FFFFFF"
CODE_BG = "#0B1F33"
CODE_FG = "#E7F0FA"


def font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont:
    if mono:
        candidates = [r"C:\Windows\Fonts\consola.ttf", r"C:\Windows\Fonts\cour.ttf"]
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


def rounded(draw: ImageDraw.ImageDraw, box, fill=WHITE, outline=LINE, width=2, radius=24) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw: ImageDraw.ImageDraw, box, text: str, fnt, fill=INK) -> None:
    x1, y1, x2, y2 = box
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2 - 1), text, font=fnt, fill=fill)


def draw_header(draw: ImageDraw.ImageDraw, title: str, subtitle: str) -> None:
    draw.rectangle((0, 0, W, 128), fill=NAVY)
    draw.text((76, 30), title, font=font(42, True), fill=WHITE)
    draw.text((78, 86), subtitle, font=font(23), fill="#D4EBF8")
    draw.rounded_rectangle((1510, 39, 1840, 88), radius=24, fill="#0A4B82")
    center_text(draw, (1510, 39, 1840, 88), "HEU | PCB Bayes", font(18, True), WHITE)


def load_rows() -> list[dict[str, str]]:
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def row_by_stage(rows: list[dict[str, str]], stage: str) -> dict[str, str]:
    for row in rows:
        if row["Stage"] == stage:
            return row
    raise RuntimeError(f"{stage} not found")


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color="#8CA6BD") -> None:
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=color, width=3)
    if x2 >= x1:
        tip = [(x2, y2), (x2 - 14, y2 - 8), (x2 - 14, y2 + 8)]
    else:
        tip = [(x2, y2), (x2 + 14, y2 - 8), (x2 + 14, y2 + 8)]
    draw.polygon(tip, fill=color)


def metric_ring(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    label: str,
    value: float,
    note: str,
    color: str,
) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, WHITE, LINE, 2, 22)
    cx, cy = x1 + 76, y1 + 76
    r = 52
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline="#DDE8F2", width=14)
    draw.arc((cx - r, cy - r, cx + r, cy + r), start=-90, end=-90 + 360 * value, fill=color, width=14)
    center_text(draw, (cx - 48, cy - 24, cx + 48, cy + 24), f"{value:.3f}", font(21, True), color)
    draw.text((x1 + 150, y1 + 34), label, font=font(21, True), fill=INK)
    draw.text((x1 + 150, y1 + 72), note, font=font(17), fill=MUTED)


def definition_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    formula: str,
    meaning: str,
    color: str,
) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, WHITE, LINE, 2, 18)
    draw.ellipse((x1 + 18, y1 + 23, x1 + 38, y1 + 43), fill=color)
    draw.text((x1 + 50, y1 + 17), title, font=font(21, True), fill=INK)
    draw.text((x1 + 20, y1 + 58), formula, font=font(17, True), fill=color)
    draw.text((x1 + 20, y1 + 88), meaning, font=font(17), fill=MUTED)


def code_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    lines: list[str],
    accent: str = BLUE2,
) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, WHITE, LINE, 2, 20)
    draw.rounded_rectangle((x1 + 16, y1 + 16, x2 - 16, y1 + 54), radius=16, fill=accent)
    draw.text((x1 + 32, y1 + 24), title, font=font(19, True), fill=WHITE)
    code_area = (x1 + 16, y1 + 68, x2 - 16, y2 - 16)
    draw.rounded_rectangle(code_area, radius=14, fill=CODE_BG)
    ty = code_area[1] + 15
    for line in lines:
        draw.text((code_area[0] + 18, ty), line, font=font(17, mono=True), fill=CODE_FG)
        ty += 27


def draw_baseline_page(rows: list[dict[str, str]]) -> None:
    row = row_by_stage(rows, "Bayes-0")
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "Bayes-0 原始朴素贝叶斯：基准效果诊断",
        "无 PCA、无协方差建模、无阈值优化；默认以 P(bad|x) >= 0.5 判为缺陷",
    )

    # Decision logic.
    rounded(draw, (78, 158, 1140, 380), WHITE, LINE, 2, 24)
    draw.text((108, 186), "朴素贝叶斯判决逻辑", font=font(30, True), fill=INK)
    draw.text((108, 230), "把一张 PCB 图像表示为特征向量 x，分别计算它属于正常类和缺陷类的后验概率。", font=font(21), fill=MUTED)
    nodes = [
        ((120, 284, 280, 342), "PCB 图像", "真实彩色样本", PALE_BLUE),
        ((340, 284, 535, 342), "1318 维特征", "颜色/纹理/HOG/LBP", PALE_GOLD),
        ((600, 258, 835, 318), "P(good|x)", "正常后验概率", PALE_GREEN),
        ((600, 326, 835, 366), "P(bad|x)", "缺陷后验概率", PALE_ORANGE),
        ((910, 284, 1078, 342), "阈值 0.5", "后验概率判决", "#EEF6FF"),
    ]
    for box, title, subtitle, fill in nodes:
        rounded(draw, box, fill, "#AFC4D5", 2, 18)
        center_text(draw, (box[0], box[1] + 5, box[2], box[1] + 34), title, font(20, True), INK)
        center_text(draw, (box[0], box[1] + 30, box[2], box[3] - 4), subtitle, font(15), MUTED)
    draw_arrow(draw, (280, 313), (338, 313))
    draw_arrow(draw, (535, 313), (598, 288))
    draw_arrow(draw, (535, 313), (598, 345))
    draw_arrow(draw, (835, 288), (908, 313))
    draw_arrow(draw, (835, 345), (908, 313))
    draw.text((108, 350), "公式：P(ωk|x) ∝ P(ωk) · ∏ p(xi|ωk)，其中“朴素”指条件独立假设。", font=font(20, True), fill=NAVY)

    # Confusion matrix.
    rounded(draw, (1180, 158, 1842, 380), WHITE, LINE, 2, 24)
    draw.text((1212, 186), "混淆矩阵：模型把样本判成了什么", font=font(28, True), fill=INK)
    draw.text((1214, 228), "行是真实类别，列是预测类别；normal/anomaly 二分类。", font=font(19), fill=MUTED)
    cm_x, cm_y, cell = 1282, 260, 76
    cm = [[int(row["TN"]), int(row["FP"])], [int(row["FN"]), int(row["TP"])]]
    labels_x = ["预测正常", "预测缺陷"]
    labels_y = ["真实正常", "真实缺陷"]
    for j, label in enumerate(labels_x):
        center_text(draw, (cm_x + j * cell, cm_y - 30, cm_x + (j + 1) * cell, cm_y - 2), label, font(16), INK)
    for i, label in enumerate(labels_y):
        draw.text((cm_x - 94, cm_y + i * cell + 24), label, font=font(16), fill=INK)
    maxv = max(max(cm[0]), max(cm[1]))
    for i in range(2):
        for j in range(2):
            v = cm[i][j]
            intensity = int(235 - 150 * v / maxv)
            fill = f"#{intensity:02x}{intensity + 12:02x}{min(255, intensity + 35):02x}"
            if i == 0 and j == 0:
                fill = "#173F78"
            draw.rectangle((cm_x + j * cell, cm_y + i * cell, cm_x + (j + 1) * cell, cm_y + (i + 1) * cell), fill=fill)
            center_text(
                draw,
                (cm_x + j * cell, cm_y + i * cell, cm_x + (j + 1) * cell, cm_y + (i + 1) * cell),
                str(v),
                font(26, True),
                WHITE if v > maxv * 0.5 else INK,
            )
    draw.text((1505, 272), f"FP={int(row['FP'])}：正常板被误判为缺陷", font=font(18), fill=ORANGE)
    draw.text((1505, 315), f"FN={int(row['FN'])}：缺陷板被误判为正常", font=font(18), fill=RED)
    draw.text((1505, 348), "FN 在质检中更危险，后续可用阈值/风险控制。", font=font(16), fill=MUTED)

    # Metric rings.
    metrics = [
        ("Accuracy 准确率", float(row["TestAccuracy"]), "整体判对比例", BLUE),
        ("Precision 精确率", float(row["TestPrecision"]), "预测缺陷中真缺陷比例", ORANGE),
        ("Recall 召回率", float(row["TestRecall"]), "真实缺陷被检出比例", BLUE),
        ("F1 值", float(row["TestF1"]), "精确率与召回率的平衡", RED),
        ("AUC", float(row["TestAUC"]), "不固定阈值的排序能力", GREEN),
        ("IoU", float(row["TestIoU"]), "缺陷类集合重合程度", GOLD),
    ]
    draw.text((78, 416), "基准指标快照", font=font(30, True), fill=INK)
    for i, metric in enumerate(metrics):
        x = 78 + (i % 3) * 600
        y = 462 + (i // 3) * 150
        metric_ring(draw, (x, y, x + 552, y + 126), *metric)

    # Error tradeoff.
    rounded(draw, (78, 752, 1842, 830), PALE_GOLD, "#DDBD52", 2, 20)
    draw.text((110, 774), "错误率解释", font=font(23, True), fill=INK)
    draw.text((282, 774), f"FPR 误报率 = {float(row['TestFPR']):.3f}：正常板被判为缺陷，增加复检成本。", font=font(21), fill=ORANGE)
    draw.text((980, 774), f"FNR 漏报率 = {float(row['TestFNR']):.3f}：缺陷板被判为正常，带来质量风险。", font=font(21), fill=RED)

    definitions = [
        ("Accuracy", "(TP+TN)/(TP+FP+TN+FN)", "所有样本中判对的比例。", BLUE),
        ("Precision", "TP/(TP+FP)", "判为缺陷的样本里，真正缺陷占比。", ORANGE),
        ("Recall", "TP/(TP+FN)", "真实缺陷中，被成功检出的比例。", BLUE),
        ("F1-score", "2PR/(P+R)", "精确率和召回率的调和平均。", RED),
        ("FPR", "FP/(FP+TN)", "正常样本被误报为缺陷的比例。", ORANGE),
        ("FNR", "FN/(FN+TP)", "缺陷样本被漏判为正常的比例。", RED),
        ("IoU", "TP/(TP+FP+FN)", "缺陷类预测集合与真实集合重合度。", GOLD),
        ("AUC", "ROC 曲线下面积", "衡量后验概率对两类样本的排序能力。", GREEN),
    ]
    for i, item in enumerate(definitions):
        x = 78 + (i % 4) * 450
        y = 858 + (i // 4) * 96
        definition_card(draw, (x, y, x + 410, y + 78), *item)

    draw.text((78, 1040), "结论：Bayes-0 的 AUC 尚可，但 Precision、F1、IoU 偏低，说明原始朴素贝叶斯有概率排序基础，但直接判决质量不足。", font=font(20, True), fill=NAVY)
    img.save(OUT_BASELINE, quality=95)


def stage_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    stage: str,
    title: str,
    detail: str,
    f1: float,
    auc: float,
    fill: str,
) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, fill, "#AFC4D5", 2, 20)
    draw.text((x1 + 20, y1 + 18), stage, font=font(23, True), fill=NAVY)
    draw.text((x1 + 20, y1 + 54), title, font=font(18, True), fill=INK)
    draw.text((x1 + 20, y1 + 84), detail, font=font(15), fill=MUTED)
    draw.text((x1 + 20, y2 - 40), f"F1={f1:.3f}  AUC={auc:.3f}", font=font(17, True), fill=BLUE)


def param_card(draw: ImageDraw.ImageDraw, box, title: str, value: str, detail: str, color: str) -> None:
    x1, y1, x2, y2 = box
    rounded(draw, box, WHITE, LINE, 2, 18)
    draw.text((x1 + 18, y1 + 14), title, font=font(19, True), fill=INK)
    draw.text((x1 + 18, y1 + 47), value, font=font(24, True), fill=color)
    for idx, line in enumerate(wrap(detail, width=20)):
        draw.text((x1 + 18, y1 + 86 + idx * 24), line, font=font(16), fill=MUTED)


def draw_code_page(rows: list[dict[str, str]]) -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_header(
        draw,
        "贝叶斯优化过程：代码如何体现",
        "优化没有跳出贝叶斯框架，而是在特征空间、概率建模和决策阈值三层逐步改进",
    )

    rounded(draw, (78, 156, 1842, 246), PALE_BLUE, "#A8D4E8", 2, 24)
    draw.text((112, 180), "主代码文件", font=font(24, True), fill=INK)
    draw.text((270, 181), "code/03_bayes_model/run_visa_bayes_optimization_comparison.m", font=font(21, mono=True), fill=NAVY)
    draw.text((112, 216), "核心思想：同一训练/验证/测试划分下，依次叠加 PCA、协方差建模、正则化和后验阈值，再用同一套指标评价。", font=font(19), fill=MUTED)

    # Code boxes.
    code_box(
        draw,
        (78, 280, 570, 488),
        "1. 只用训练集统计量做标准化",
        [
            "[XTrainZ, prepBase] = standardize_train(XTrain);",
            "XValZ  = standardize_apply(XVal,  prepBase);",
            "XTestZ = standardize_apply(XTest, prepBase);",
        ],
        BLUE2,
    )
    code_box(
        draw,
        (612, 280, 1104, 488),
        "2. PCA 压缩特征空间",
        [
            "[coeff, ~] = pca(XTrainZ);",
            "bestDim = 80;",
            "XTrainP = XTrainZ * coeff(:,1:bestDim);",
            "XTestP  = XTestZ  * coeff(:,1:bestDim);",
        ],
        GOLD,
    )
    code_box(
        draw,
        (1146, 280, 1842, 488),
        "3. 贝叶斯概率建模逐步增强",
        [
            "fitcnb(..., 'DistributionNames','normal')",
            "fitcdiscr(..., 'DiscrimType','pseudoQuadratic')",
            "fitcdiscr(..., 'DiscrimType','linear', 'Gamma',0.1)",
        ],
        ORANGE,
    )
    code_box(
        draw,
        (78, 520, 870, 720),
        "4. 输出缺陷后验概率 P(bad|x)",
        [
            "[~, scoreRaw] = predict(model, XTest);",
            "scoreAnomaly = positive_score(model, scoreRaw);",
            "testMetrics = classification_metrics(YTest, pred, scoreAnomaly, 'anomaly');",
        ],
        GREEN,
    )
    code_box(
        draw,
        (912, 520, 1842, 720),
        "5. 阈值优化体现最小风险思想",
        [
            "bestThreshold = 0.75;",
            "labels = repmat('normal', numel(scoreAnomaly), 1);",
            "labels(scoreAnomaly >= threshold) = 'anomaly';",
            "yPred = categorical(labels, ['normal','anomaly']);",
        ],
        RED,
    )

    # Parameter meaning.
    draw.text((78, 752), "关键参数含义", font=font(28, True), fill=INK)
    param_card(draw, (78, 790, 408, 936), "PCA 维度 bestDim", "80", "从 1318 维手工特征中保留主要变化方向，降低冗余与噪声。", BLUE)
    param_card(draw, (438, 790, 768, 936), "Gamma 正则化", "0.1", "约束协方差估计，避免高维小样本下矩阵不稳定。", ORANGE)
    param_card(draw, (798, 790, 1128, 936), "后验阈值 Threshold", "0.75", "控制 P(bad|x) 多大时判为缺陷，用来平衡误报和漏报。", RED)
    param_card(draw, (1158, 790, 1488, 936), "Prior = uniform", "均匀先验", "避免训练集中正常样本过多导致模型天然偏向 normal。", GREEN)
    param_card(draw, (1518, 790, 1842, 936), "DiscrimType", "决策面形式", "pseudoQuadratic/linear 表示不同高斯判别边界。", GOLD)

    # Stage timeline.
    draw.text((78, 965), "优化阶段对应关系", font=font(25, True), fill=INK)
    stage_colors = [WHITE, PALE_BLUE, PALE_GOLD, PALE_GREEN, PALE_ORANGE]
    stage_titles = [
        ("Bayes-0", "原始朴素贝叶斯", "全特征 + 默认阈值"),
        ("Bayes-1", "PCA 优化", "80 维主成分"),
        ("Bayes-2", "高斯建模", "协方差相关性"),
        ("Bayes-3", "正则化", "Gamma=0.1"),
        ("Bayes-4", "阈值优化", "Threshold=0.75"),
    ]
    x = 310
    for i, (stage, title, detail) in enumerate(stage_titles):
        row = row_by_stage(rows, stage)
        box = (x + i * 300, 955, x + i * 300 + 260, 1060)
        stage_card(draw, box, stage, title, detail, float(row["TestF1"]), float(row["TestAUC"]), stage_colors[i])
        if i < 4:
            draw_arrow(draw, (box[2] + 4, 1008), (box[2] + 36, 1008))

    img.save(OUT_CODE, quality=95)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    draw_baseline_page(rows)
    draw_code_page(rows)
    print(OUT_BASELINE)
    print(OUT_CODE)


if __name__ == "__main__":
    main()
