# 中文注释：生成朴素贝叶斯基线结果的柱状图。
# 主要流程：整理基线模型指标，绘制适合放入 PPT 的对比图。
# 输出结果：帮助说明贝叶斯改进前后的性能差异。

# 行注释：这里启用较新的 Python 类型注解行为。
from __future__ import annotations

# 行注释：这里导入脚本后面需要用到的 Python 模块。
import csv
# 行注释：这里导入脚本后面需要用到的 Python 模块。
from pathlib import Path

# 行注释：这里导入脚本后面需要用到的 Python 模块。
import matplotlib.pyplot as plt
# 行注释：这里导入脚本后面需要用到的 Python 模块。
import numpy as np
# 行注释：这里导入脚本后面需要用到的 Python 模块。
from matplotlib import font_manager
# 行注释：这里导入脚本后面需要用到的 Python 模块。
from matplotlib.patches import FancyBboxPatch, Rectangle


# 行注释：这里设置 ROOT 的值，后续绘图或计算会用到。
ROOT = Path(r"C:\Users\19571\Desktop\研讨\PCB_Bayes_Project")
# 行注释：这里设置 CSV_PATH 的值，后续绘图或计算会用到。
CSV_PATH = ROOT / "results" / "visa_pcb" / "bayes_optimization_comparison.csv"
# 行注释：这里设置 OUT_DIR 的值，后续绘图或计算会用到。
OUT_DIR = ROOT / "results" / "figures"
# 行注释：这里设置 OUT 的值，后续绘图或计算会用到。
OUT = OUT_DIR / "13_朴素贝叶斯基准模型指标柱状图.png"

# 行注释：这里设置 NAVY 的值，后续绘图或计算会用到。
NAVY = "#003B73"
# 行注释：这里设置 BLUE 的值，后续绘图或计算会用到。
BLUE = "#004488"
# 行注释：这里设置 LIGHT_BLUE 的值，后续绘图或计算会用到。
LIGHT_BLUE = "#D9EEF8"
# 行注释：这里设置 ORANGE 的值，后续绘图或计算会用到。
ORANGE = "#D95319"
# 行注释：这里设置 RED 的值，后续绘图或计算会用到。
RED = "#B22222"
# 行注释：这里设置 GOLD 的值，后续绘图或计算会用到。
GOLD = "#C99700"
# 行注释：这里设置 INK 的值，后续绘图或计算会用到。
INK = "#0F172A"
# 行注释：这里设置 MUTED 的值，后续绘图或计算会用到。
MUTED = "#64748B"
# 行注释：这里设置 BG 的值，后续绘图或计算会用到。
BG = "#F4F8FB"
# 行注释：这里设置 LINE 的值，后续绘图或计算会用到。
LINE = "#C7D5E3"
# 行注释：这里设置 WHITE 的值，后续绘图或计算会用到。
WHITE = "#FFFFFF"


# 函数说明：设置 Matplotlib 中文字体，避免图表中文字乱码。
# 行注释：这里定义 use_chinese_font 函数。
def use_chinese_font() -> None:
    # 行注释：这里设置 candidates 的值，后续绘图或计算会用到。
    candidates = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        r"C:\Windows\Fonts\msyh.ttc",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        r"C:\Windows\Fonts\simhei.ttf",
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        r"C:\Windows\Fonts\simsun.ttc",
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for item in candidates:
        # 行注释：这里判断条件是否满足。
        if Path(item).exists():
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            font_manager.fontManager.addfont(item)
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            plt.rcParams["font.sans-serif"] = [font_manager.FontProperties(fname=item).get_name()]
            # 行注释：这里提前结束当前循环。
            break
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    plt.rcParams["axes.unicode_minus"] = False


# 函数说明：读取 Bayes-0 基线指标，用于基线柱状图。
# 行注释：这里定义 load_bayes0 函数。
def load_bayes0() -> dict[str, str]:
    # 行注释：这里用上下文管理器安全地打开或处理资源。
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        # 行注释：这里开始循环，逐个处理列表或数据项。
        for row in csv.DictReader(f):
            # 行注释：这里判断条件是否满足。
            if row["Stage"] == "Bayes-0":
                # 行注释：这里把结果返回给调用它的代码。
                return row
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    raise RuntimeError("Bayes-0 row not found.")


# 函数说明：在 Matplotlib 图中画一张浅色卡片背景。
# 行注释：这里定义 card 函数。
def card(fig: plt.Figure, xywh: tuple[float, float, float, float], radius: float = 0.018) -> None:
    # 行注释：这里设置 x, y, w, h 的值，后续绘图或计算会用到。
    x, y, w, h = xywh
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fig.patches.append(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        FancyBboxPatch(
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            (x, y),
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            w,
            # 行注释：这里执行当前语句，推进这一小步逻辑。
            h,
            # 行注释：这里设置 transform 的值，后续绘图或计算会用到。
            transform=fig.transFigure,
            # 行注释：这里设置 boxstyle 的值，后续绘图或计算会用到。
            boxstyle=f"round,pad=0.006,rounding_size={radius}",
            # 行注释：这里设置 facecolor 的值，后续绘图或计算会用到。
            facecolor=WHITE,
            # 行注释：这里设置 edgecolor 的值，后续绘图或计算会用到。
            edgecolor=LINE,
            # 行注释：这里设置 linewidth 的值，后续绘图或计算会用到。
            linewidth=1.3,
            # 行注释：这里设置 zorder 的值，后续绘图或计算会用到。
            zorder=-5,
        # 行注释：这里结束当前多行参数、列表或代码结构。
        )
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )


# 函数说明：脚本入口，按顺序调用前面的函数生成最终文件。
# 行注释：这里定义 main 函数。
def main() -> None:
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    use_chinese_font()
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # 行注释：这里设置 row 的值，后续绘图或计算会用到。
    row = load_bayes0()

    # 行注释：这里设置 metrics 的值，后续绘图或计算会用到。
    metrics = [
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("准确率 Accuracy", float(row["TestAccuracy"]), BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("精确率 Precision", float(row["TestPrecision"]), BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("召回率 Recall", float(row["TestRecall"]), BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("特异度 Specificity", float(row["TestSpecificity"]), BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("F1 值", float(row["TestF1"]), BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("IoU", float(row["TestIoU"]), BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("AUC", float(row["TestAUC"]), BLUE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("误报率 FPR", float(row["TestFPR"]), ORANGE),
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        ("漏报率 FNR", float(row["TestFNR"]), RED),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    ]

    # 行注释：这里设置 fig 的值，后续绘图或计算会用到。
    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=BG)

    # Header band
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fig.patches.append(Rectangle((0, 0.885), 1, 0.115, transform=fig.transFigure, facecolor=NAVY, edgecolor="none"))
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(0.055, 0.943, "Bayes-0 原始朴素贝叶斯决策效果", fontsize=28, fontweight="bold", color=WHITE, va="center")
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        0.055,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        0.902,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "无 PCA、无高斯相关建模、无阈值优化；默认以 P(bad|x) ≥ 0.5 判为缺陷",
        # 行注释：这里设置 fontsize 的值，后续绘图或计算会用到。
        fontsize=15,
        # 行注释：这里设置 color 的值，后续绘图或计算会用到。
        color="#D4EBF8",
        # 行注释：这里设置 va 的值，后续绘图或计算会用到。
        va="center",
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        0.853,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        0.943,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "HEU | PCB Bayes",
        # 行注释：这里设置 fontsize 的值，后续绘图或计算会用到。
        fontsize=13,
        # 行注释：这里设置 color 的值，后续绘图或计算会用到。
        color=WHITE,
        # 行注释：这里设置 ha 的值，后续绘图或计算会用到。
        ha="center",
        # 行注释：这里设置 va 的值，后续绘图或计算会用到。
        va="center",
        # 行注释：这里设置 fontweight 的值，后续绘图或计算会用到。
        fontweight="bold",
        # 行注释：这里设置 bbox 的值，后续绘图或计算会用到。
        bbox=dict(boxstyle="round,pad=0.55,rounding_size=1.3", facecolor="#0A4B82", edgecolor="none"),
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )

    # Left: main bar chart
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    card(fig, (0.055, 0.105, 0.615, 0.735))
    # 行注释：这里设置 ax 的值，后续绘图或计算会用到。
    ax = fig.add_axes([0.12, 0.165, 0.505, 0.62], facecolor=WHITE)
    # 行注释：这里设置 labels 的值，后续绘图或计算会用到。
    labels = [item[0] for item in metrics]
    # 行注释：这里设置 values 的值，后续绘图或计算会用到。
    values = np.array([item[1] for item in metrics])
    # 行注释：这里设置 colors 的值，后续绘图或计算会用到。
    colors = [item[2] for item in metrics]
    # 行注释：这里设置 y 的值，后续绘图或计算会用到。
    y = np.arange(len(labels))

    # 行注释：这里设置 bars 的值，后续绘图或计算会用到。
    bars = ax.barh(y, values, color=colors, alpha=0.93, height=0.56)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax.set_xlim(0, 1.0)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax.set_yticks(y)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax.set_yticklabels(labels, fontsize=12, color=INK)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax.invert_yaxis()
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax.set_title("测试集各项指标", loc="left", fontsize=18, fontweight="bold", color=INK, pad=18)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax.grid(axis="x", color="#E5EDF5", linewidth=1.0)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax.set_axisbelow(True)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax.spines[["top", "right", "left"]].set_visible(False)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax.spines["bottom"].set_color("#AABBCD")
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax.tick_params(axis="x", colors=MUTED, labelsize=11)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax.tick_params(axis="y", length=0)

    # 行注释：这里开始循环，逐个处理列表或数据项。
    for bar, value in zip(bars, values):
        # 行注释：这里设置 x 的值，后续绘图或计算会用到。
        x = min(value + 0.018, 0.94)
        # 行注释：这里在图片画布上绘制文字、线条或形状。
        ax.text(x, bar.get_y() + bar.get_height() / 2, f"{value:.3f}", va="center", ha="left", fontsize=11.5, color=INK)

    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        0.096,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        0.124,
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        "读图重点：AUC 尚可，但 Precision、F1、IoU 偏低；说明模型能给出一定排序能力，直接 0.5 判决时缺陷识别质量仍不足。",
        # 行注释：这里设置 fontsize 的值，后续绘图或计算会用到。
        fontsize=12.5,
        # 行注释：这里设置 color 的值，后续绘图或计算会用到。
        color=MUTED,
    # 行注释：这里结束当前多行参数、列表或代码结构。
    )

    # Right: confusion matrix and diagnosis cards
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    card(fig, (0.705, 0.565, 0.24, 0.275))
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(0.728, 0.803, "混淆矩阵", fontsize=18, fontweight="bold", color=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(0.728, 0.775, "测试集：normal / anomaly 二分类", fontsize=11.5, color=MUTED)

    # 行注释：这里设置 ax_cm 的值，后续绘图或计算会用到。
    ax_cm = fig.add_axes([0.735, 0.602, 0.18, 0.145])
    # 行注释：这里设置 cm 的值，后续绘图或计算会用到。
    cm = np.array([[int(row["TN"]), int(row["FP"])], [int(row["FN"]), int(row["TP"])]])
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax_cm.imshow(cm, cmap="Blues", vmin=0, vmax=cm.max())
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax_cm.set_xticks([0, 1], ["预测正常", "预测缺陷"], fontsize=10)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax_cm.set_yticks([0, 1], ["真实正常", "真实缺陷"], fontsize=10)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    ax_cm.tick_params(length=0)
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for i in range(2):
        # 行注释：这里开始循环，逐个处理列表或数据项。
        for j in range(2):
            # 行注释：这里设置 color 的值，后续绘图或计算会用到。
            color = WHITE if cm[i, j] > cm.max() * 0.52 else INK
            # 行注释：这里在图片画布上绘制文字、线条或形状。
            ax_cm.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=16, fontweight="bold", color=color)
    # 行注释：这里开始循环，逐个处理列表或数据项。
    for spine in ax_cm.spines.values():
        # 行注释：这里执行当前语句，推进这一小步逻辑。
        spine.set_visible(False)

    # 行注释：这里执行当前语句，推进这一小步逻辑。
    card(fig, (0.705, 0.355, 0.24, 0.175))
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(0.728, 0.49, "关键问题", fontsize=18, fontweight="bold", color=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(0.728, 0.455, f"误报 FP = {int(row['FP'])}，正常板被判缺陷较多", fontsize=12.2, color=MUTED)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(0.728, 0.422, f"漏报 FN = {int(row['FN'])}，缺陷板仍有漏检风险", fontsize=12.2, color=MUTED)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(0.728, 0.389, "后续优化应压低错误率并提升 F1/IoU", fontsize=12.2, color=MUTED)

    # 行注释：这里执行当前语句，推进这一小步逻辑。
    card(fig, (0.705, 0.105, 0.24, 0.215))
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(0.728, 0.278, "用于过渡到优化", fontsize=18, fontweight="bold", color=INK)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(0.728, 0.239, "1. PCA：降低冗余特征干扰", fontsize=12.2, color=MUTED)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(0.728, 0.204, "2. 高斯建模：表达特征相关性", fontsize=12.2, color=MUTED)
    # 行注释：这里在图片画布上绘制文字、线条或形状。
    fig.text(0.728, 0.169, "3. 阈值/风险：调节误报与漏报", fontsize=12.2, color=MUTED)

    # 行注释：这里执行当前语句，推进这一小步逻辑。
    fig.savefig(OUT, dpi=120, facecolor=BG)
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    plt.close(fig)
    # 行注释：这里在终端输出生成结果或进度信息。
    print(OUT)


# 行注释：这里判断脚本是否被直接运行。
if __name__ == "__main__":
    # 行注释：这里执行当前语句，推进这一小步逻辑。
    main()
