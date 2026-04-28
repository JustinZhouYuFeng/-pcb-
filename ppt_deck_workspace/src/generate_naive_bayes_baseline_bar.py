# 中文注释：生成朴素贝叶斯基线结果的柱状图。
# 主要流程：整理基线模型指标，绘制适合放入 PPT 的对比图。
# 输出结果：帮助说明贝叶斯改进前后的性能差异。

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle


ROOT = Path(r"C:\Users\19571\Desktop\研讨\PCB_Bayes_Project")
CSV_PATH = ROOT / "results" / "visa_pcb" / "bayes_optimization_comparison.csv"
OUT_DIR = ROOT / "results" / "figures"
OUT = OUT_DIR / "13_朴素贝叶斯基准模型指标柱状图.png"

NAVY = "#003B73"
BLUE = "#004488"
LIGHT_BLUE = "#D9EEF8"
ORANGE = "#D95319"
RED = "#B22222"
GOLD = "#C99700"
INK = "#0F172A"
MUTED = "#64748B"
BG = "#F4F8FB"
LINE = "#C7D5E3"
WHITE = "#FFFFFF"


# 函数说明：设置 Matplotlib 中文字体，避免图表中文字乱码。
def use_chinese_font() -> None:
    candidates = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\simhei.ttf",
        r"C:\Windows\Fonts\simsun.ttc",
    ]
    for item in candidates:
        if Path(item).exists():
            font_manager.fontManager.addfont(item)
            plt.rcParams["font.sans-serif"] = [font_manager.FontProperties(fname=item).get_name()]
            break
    plt.rcParams["axes.unicode_minus"] = False


# 函数说明：读取 Bayes-0 基线指标，用于基线柱状图。
def load_bayes0() -> dict[str, str]:
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row["Stage"] == "Bayes-0":
                return row
    raise RuntimeError("Bayes-0 row not found.")


# 函数说明：在 Matplotlib 图中画一张浅色卡片背景。
def card(fig: plt.Figure, xywh: tuple[float, float, float, float], radius: float = 0.018) -> None:
    x, y, w, h = xywh
    fig.patches.append(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            transform=fig.transFigure,
            boxstyle=f"round,pad=0.006,rounding_size={radius}",
            facecolor=WHITE,
            edgecolor=LINE,
            linewidth=1.3,
            zorder=-5,
        )
    )


# 函数说明：脚本入口，按顺序调用前面的函数生成最终文件。
def main() -> None:
    use_chinese_font()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    row = load_bayes0()

    metrics = [
        ("准确率 Accuracy", float(row["TestAccuracy"]), BLUE),
        ("精确率 Precision", float(row["TestPrecision"]), BLUE),
        ("召回率 Recall", float(row["TestRecall"]), BLUE),
        ("特异度 Specificity", float(row["TestSpecificity"]), BLUE),
        ("F1 值", float(row["TestF1"]), BLUE),
        ("IoU", float(row["TestIoU"]), BLUE),
        ("AUC", float(row["TestAUC"]), BLUE),
        ("误报率 FPR", float(row["TestFPR"]), ORANGE),
        ("漏报率 FNR", float(row["TestFNR"]), RED),
    ]

    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=BG)

    # Header band
    fig.patches.append(Rectangle((0, 0.885), 1, 0.115, transform=fig.transFigure, facecolor=NAVY, edgecolor="none"))
    fig.text(0.055, 0.943, "Bayes-0 原始朴素贝叶斯决策效果", fontsize=28, fontweight="bold", color=WHITE, va="center")
    fig.text(
        0.055,
        0.902,
        "无 PCA、无高斯相关建模、无阈值优化；默认以 P(bad|x) ≥ 0.5 判为缺陷",
        fontsize=15,
        color="#D4EBF8",
        va="center",
    )
    fig.text(
        0.853,
        0.943,
        "HEU | PCB Bayes",
        fontsize=13,
        color=WHITE,
        ha="center",
        va="center",
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.55,rounding_size=1.3", facecolor="#0A4B82", edgecolor="none"),
    )

    # Left: main bar chart
    card(fig, (0.055, 0.105, 0.615, 0.735))
    ax = fig.add_axes([0.12, 0.165, 0.505, 0.62], facecolor=WHITE)
    labels = [item[0] for item in metrics]
    values = np.array([item[1] for item in metrics])
    colors = [item[2] for item in metrics]
    y = np.arange(len(labels))

    bars = ax.barh(y, values, color=colors, alpha=0.93, height=0.56)
    ax.set_xlim(0, 1.0)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=12, color=INK)
    ax.invert_yaxis()
    ax.set_title("测试集各项指标", loc="left", fontsize=18, fontweight="bold", color=INK, pad=18)
    ax.grid(axis="x", color="#E5EDF5", linewidth=1.0)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#AABBCD")
    ax.tick_params(axis="x", colors=MUTED, labelsize=11)
    ax.tick_params(axis="y", length=0)

    for bar, value in zip(bars, values):
        x = min(value + 0.018, 0.94)
        ax.text(x, bar.get_y() + bar.get_height() / 2, f"{value:.3f}", va="center", ha="left", fontsize=11.5, color=INK)

    fig.text(
        0.096,
        0.124,
        "读图重点：AUC 尚可，但 Precision、F1、IoU 偏低；说明模型能给出一定排序能力，直接 0.5 判决时缺陷识别质量仍不足。",
        fontsize=12.5,
        color=MUTED,
    )

    # Right: confusion matrix and diagnosis cards
    card(fig, (0.705, 0.565, 0.24, 0.275))
    fig.text(0.728, 0.803, "混淆矩阵", fontsize=18, fontweight="bold", color=INK)
    fig.text(0.728, 0.775, "测试集：normal / anomaly 二分类", fontsize=11.5, color=MUTED)

    ax_cm = fig.add_axes([0.735, 0.602, 0.18, 0.145])
    cm = np.array([[int(row["TN"]), int(row["FP"])], [int(row["FN"]), int(row["TP"])]])
    ax_cm.imshow(cm, cmap="Blues", vmin=0, vmax=cm.max())
    ax_cm.set_xticks([0, 1], ["预测正常", "预测缺陷"], fontsize=10)
    ax_cm.set_yticks([0, 1], ["真实正常", "真实缺陷"], fontsize=10)
    ax_cm.tick_params(length=0)
    for i in range(2):
        for j in range(2):
            color = WHITE if cm[i, j] > cm.max() * 0.52 else INK
            ax_cm.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=16, fontweight="bold", color=color)
    for spine in ax_cm.spines.values():
        spine.set_visible(False)

    card(fig, (0.705, 0.355, 0.24, 0.175))
    fig.text(0.728, 0.49, "关键问题", fontsize=18, fontweight="bold", color=INK)
    fig.text(0.728, 0.455, f"误报 FP = {int(row['FP'])}，正常板被判缺陷较多", fontsize=12.2, color=MUTED)
    fig.text(0.728, 0.422, f"漏报 FN = {int(row['FN'])}，缺陷板仍有漏检风险", fontsize=12.2, color=MUTED)
    fig.text(0.728, 0.389, "后续优化应压低错误率并提升 F1/IoU", fontsize=12.2, color=MUTED)

    card(fig, (0.705, 0.105, 0.24, 0.215))
    fig.text(0.728, 0.278, "用于过渡到优化", fontsize=18, fontweight="bold", color=INK)
    fig.text(0.728, 0.239, "1. PCA：降低冗余特征干扰", fontsize=12.2, color=MUTED)
    fig.text(0.728, 0.204, "2. 高斯建模：表达特征相关性", fontsize=12.2, color=MUTED)
    fig.text(0.728, 0.169, "3. 阈值/风险：调节误报与漏报", fontsize=12.2, color=MUTED)

    fig.savefig(OUT, dpi=120, facecolor=BG)
    plt.close(fig)
    print(OUT)


if __name__ == "__main__":
    main()
