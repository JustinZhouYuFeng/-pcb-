// 中文注释：根据项目结果和图片素材生成哈尔滨工程大学汇报 PPT。
// 主要流程：定义版式、加载图像素材、组织章节页面并导出 pptx 文件。
// 注意事项：本脚本关注演示文稿排版，不改变 MATLAB 实验结果。

import fs from "node:fs";
import path from "node:path";
import {
  Presentation,
  PresentationFile,
  row,
  column,
  grid,
  layers,
  panel,
  text,
  image,
  shape,
  rule,
  fill,
  hug,
  fixed,
  wrap,
  grow,
  fr,
  auto,
} from "@oai/artifact-tool";

const W = 1920;
const H = 1080;

const ROOT = "C:/Users/19571/Desktop/研讨/PCB_Bayes_Project";
const MATERIAL = `${ROOT}/ppt_materials/visa_pcb`;
const POLISHED = `${MATERIAL}/polished`;
const WORKSPACE = `${ROOT}/ppt_deck_workspace`;
const OUTPUT = `${WORKSPACE}/output/output.pptx`;
const PREVIEW_DIR = `${WORKSPACE}/scratch/previews`;

const C = {
  navy: "#003B73",
  navy2: "#004488",
  ocean: "#005A8D",
  blue: "#2E5A88",
  cyan: "#28A9E0",
  gold: "#C99700",
  ink: "#0F172A",
  slate: "#475569",
  muted: "#64748B",
  line: "#CBD8E4",
  bg: "#F5F8FB",
  white: "#FFFFFF",
  orange: "#D95319",
  red: "#B22222",
  paleBlue: "#E7F4FB",
  paleGold: "#FFF7DB",
};

// 函数说明：拼接精修版素材路径，方便后面插入 PPT。
function asset(name) {
  return `${POLISHED}/${name}`;
}

// 函数说明：拼接基础素材路径，作为没有精修图时的备用来源。
function basicAsset(name) {
  return `${MATERIAL}/${name}`;
}

// 函数说明：把 PNG 图片读成 data URL，供 PPT 工具直接嵌入。
function pngDataUrl(filePath) {
  const bytes = fs.readFileSync(filePath);
  return `data:image/png;base64,${bytes.toString("base64")}`;
}

// 函数说明：把图片路径和显示参数包装成 PPT 可用的图片对象。
function bitmap(filePath, opts = {}) {
  return image({
    dataUrl: pngDataUrl(filePath),
    contentType: "image/png",
    width: opts.width ?? fill,
    height: opts.height ?? fill,
    fit: opts.fit ?? "contain",
    alt: opts.alt ?? path.basename(filePath),
    name: opts.name,
  });
}

// 函数说明：合并默认文字样式和自定义样式，减少重复配置。
function baseStyle(style = {}) {
  return {
    fontFamily: "Microsoft YaHei",
    color: C.ink,
    ...style,
  };
}

// 函数说明：创建普通文本组件，并套用统一字体和颜色。
function tx(value, opts = {}) {
  return text(value, {
    width: opts.width ?? fill,
    height: opts.height ?? hug,
    ...opts,
    style: baseStyle(opts.style),
  });
}

// 函数说明：创建代码样式文本组件，用于展示脚本片段。
function codeText(value, opts = {}) {
  return text(value, {
    width: opts.width ?? fill,
    height: opts.height ?? hug,
    ...opts,
    style: {
      fontFamily: "Consolas",
      fontSize: 22,
      color: "#E8F2FA",
      lineSpacing: 1.16,
      ...opts.style,
    },
  });
}

// 函数说明：绘制一条带圆点的说明文字。
function bullet(lines, opts = {}) {
  return column(
    {
      width: opts.width ?? fill,
      height: opts.height ?? hug,
      gap: opts.gap ?? 12,
      ...opts,
    },
    lines.map((line) =>
      row(
        { width: fill, height: hug, gap: 12, align: "start" },
        [
          shape({
            width: fixed(9),
            height: fixed(9),
            fill: opts.dotColor ?? C.gold,
            line: { width: 0, fill: opts.dotColor ?? C.gold },
            borderRadius: "rounded-full",
          }),
          tx(line, {
            width: fill,
            style: {
              fontSize: opts.fontSize ?? 26,
              color: opts.color ?? C.slate,
              lineSpacing: 1.18,
            },
          }),
        ],
      ),
    ),
  );
}

// 函数说明：创建一个关键数字卡片，用来突出样本量或模型指标。
function statCard(value, label, accent = C.navy2) {
  return panel(
    {
      width: fill,
      height: fixed(132),
      fill: C.white,
      line: { style: "solid", width: 1, fill: C.line },
      borderRadius: "rounded-lg",
      padding: { x: 24, y: 18 },
    },
    column({ width: fill, height: fill, gap: 6 }, [
      tx(value, { style: { fontSize: 42, bold: true, color: accent } }),
      tx(label, { style: { fontSize: 20, color: C.muted } }),
    ]),
  );
}

// 函数说明：绘制页脚和页码信息。
function footer(slideNo) {
  return row(
    { width: fill, height: hug, align: "center", justify: "between" },
    [
      tx("哈尔滨工程大学 · 电子信息方向 · 模式识别课程研讨", {
        width: wrap(860),
        style: { fontSize: 15, color: "#6B7E8F" },
      }),
      tx(String(slideNo).padStart(2, "0"), {
        width: fixed(48),
        style: { fontSize: 16, bold: true, color: C.ocean, alignment: "right" },
      }),
    ],
  );
}

// 函数说明：生成带统一标题栏和页脚的标准幻灯片。
function titledSlide(p, slideNo, title, subtitle, main, opts = {}) {
  const slide = p.slides.add();
  const bg = opts.bg ?? C.bg;
  slide.compose(
    layers({ width: fill, height: fill }, [
      shape({ width: fill, height: fill, fill: bg, line: { width: 0, fill: bg } }),
      column(
        {
          width: fill,
          height: fill,
          padding: { x: 76, top: 46, bottom: 34 },
          gap: 22,
        },
        [
          row({ width: fill, height: hug, justify: "between", align: "start" }, [
            column({ width: fill, height: hug, gap: 8 }, [
              tx(title, {
                name: `slide-${slideNo}-title`,
                width: wrap(1340),
                style: { fontSize: opts.titleSize ?? 44, bold: true, color: C.ink, lineSpacing: 1.05 },
              }),
              subtitle
                ? tx(subtitle, {
                    width: wrap(1280),
                    style: { fontSize: opts.subtitleSize ?? 21, color: C.slate, lineSpacing: 1.18 },
                  })
                : rule({ width: fixed(210), stroke: C.gold, weight: 5 }),
            ]),
            panel(
              {
                width: fixed(300),
                height: fixed(58),
                fill: opts.badgeFill ?? C.navy,
                line: { width: 0, fill: opts.badgeFill ?? C.navy },
                borderRadius: "rounded-full",
                padding: { x: 22, y: 13 },
              },
              tx(opts.badge ?? "Bayesian PCB Inspection", {
                width: fill,
                style: { fontSize: 17, bold: true, color: C.white, alignment: "center" },
              }),
            ),
          ]),
          main,
          footer(slideNo),
        ],
      ),
    ]),
    { frame: { left: 0, top: 0, width: W, height: H }, baseUnit: 8 },
  );
  return slide;
}

// 函数说明：生成带边框和留白的图片面板。
function imagePanel(name, h = fill, fit = "contain") {
  return panel(
    {
      width: fill,
      height: h,
      fill: C.white,
      line: { style: "solid", width: 1, fill: C.line },
      borderRadius: "rounded-lg",
      padding: 10,
    },
    bitmap(asset(name), { width: fill, height: fill, fit, alt: name }),
  );
}

// 函数说明：生成铺满主要区域的图片页。
function plainImage(name, fit = "contain") {
  return bitmap(asset(name), { width: fill, height: fill, fit, alt: name });
}

// 函数说明：添加封面页，展示项目题目、身份信息和关键指标。
function addCover(p) {
  const slide = p.slides.add();
  slide.compose(
    layers({ width: fill, height: fill }, [
      image({
        name: "cover-background",
        dataUrl: pngDataUrl(asset("00_哈工程深蓝封面背景.png")),
        contentType: "image/png",
        width: fill,
        height: fill,
        fit: "cover",
        alt: "哈工程深蓝工程风背景",
      }),
      column(
        {
          width: fill,
          height: fill,
          padding: { x: 118, top: 94, bottom: 74 },
          justify: "between",
        },
        [
          row({ width: fill, height: hug, justify: "between", align: "start" }, [
            column({ width: wrap(1180), height: hug, gap: 16 }, [
              tx("基于贝叶斯决策的 PCB 缺陷检测", {
                width: wrap(1180),
                style: { fontSize: 78, bold: true, color: C.white, lineSpacing: 1.04 },
              }),
              rule({ width: fixed(360), stroke: C.gold, weight: 7 }),
              tx("VisA PCB 真实彩色图像 · normal / anomaly 二分类 · Bayes-only 优化对比", {
                width: wrap(1040),
                style: { fontSize: 28, color: "#D9ECF7", lineSpacing: 1.2 },
              }),
            ]),
            column({ width: fixed(440), height: hug, gap: 10, align: "end" }, [
              tx("哈尔滨工程大学", {
                width: fill,
                style: { fontSize: 34, bold: true, color: C.white, alignment: "right" },
              }),
              tx("Harbin Engineering University", {
                width: fill,
                style: { fontSize: 18, color: "#B9D7EA", alignment: "right" },
              }),
              tx("大工至善 · 大学至真", {
                width: fill,
                style: { fontSize: 20, bold: true, color: "#F6D77D", alignment: "right" },
              }),
            ]),
          ]),
          row({ width: fill, height: hug, justify: "between", align: "end" }, [
            column({ width: wrap(760), height: hug, gap: 10 }, [
              tx("课程研讨汇报", {
                width: wrap(420),
                style: { fontSize: 28, bold: true, color: C.white },
              }),
              tx("电子信息方向 | 模式识别 | MATLAB 实验实现", {
                width: wrap(760),
                style: { fontSize: 22, color: "#CFE8F7" },
              }),
            ]),
            panel(
              {
                width: fixed(470),
                height: fixed(86),
                fill: "rgba(255,255,255,0.12)",
                line: { width: 1, fill: "rgba(255,255,255,0.22)" },
                borderRadius: "rounded-lg",
                padding: { x: 24, y: 18 },
              },
              tx("主题：用可解释的贝叶斯后验概率完成 PCB 良品 / 缺陷判别，并通过参数优化提升检测性能。", {
                style: { fontSize: 20, color: C.white, lineSpacing: 1.18 },
              }),
            ),
          ]),
        ],
      ),
    ]),
    { frame: { left: 0, top: 0, width: W, height: H }, baseUnit: 8 },
  );
}

// 函数说明：按顺序组装所有 PPT 页面，形成完整演示文稿。
function addAllSlides(p) {
  addCover(p);

  titledSlide(
    p,
    2,
    "选题定位：电子信息场景下的可解释视觉检测",
    "不是单纯做一个分类器，而是把“电路板质量检测”转化为模式识别中的概率决策问题。",
    grid(
      { width: fill, height: fill, columns: [fr(0.95), fr(1.05)], columnGap: 34, alignItems: "stretch" },
      [
        panel(
          { width: fill, height: fill, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 34, y: 28 } },
          column({ width: fill, height: fill, gap: 22 }, [
            tx("为什么契合电子信息？", { style: { fontSize: 36, bold: true, color: C.navy } }),
            bullet(
              [
                "PCB 是电子系统的基础载体，缺陷会直接影响电气连接、可靠性与整机质量。",
                "真实彩色图像比黑白模板图更接近工业视觉检测中的光照、反光和纹理变化。",
                "贝叶斯决策能输出 P(缺陷|x)，适合解释“为什么判为缺陷”和“阈值如何影响风险”。",
              ],
              { fontSize: 28, gap: 18, dotColor: C.cyan },
            ),
            panel(
              { width: fill, height: hug, fill: C.paleBlue, line: { width: 1, fill: "#9CCBE2" }, borderRadius: "rounded-lg", padding: { x: 24, y: 18 } },
              tx("哈工程元素：以“三海一核”的工程应用气质为背景，强调可靠、可解释、可落地的检测流程。", {
                style: { fontSize: 25, bold: true, color: C.navy, lineSpacing: 1.2 },
              }),
            ),
          ]),
        ),
        grid({ width: fill, height: fill, columns: [fr(1), fr(1)], rows: [fr(1), fr(1)], columnGap: 22, rowGap: 22 }, [
          statCard("4413", "VisA PCB 可用图像", C.navy2),
          statCard("1318维", "每张图像的手工特征", C.ocean),
          statCard("5个阶段", "Bayes-0 → Bayes-4 优化", C.gold),
          statCard("8类指标", "Accuracy/F1/AUC/FPR/FNR 等", C.orange),
        ]),
      ],
    ),
  );

  titledSlide(
    p,
    3,
    "任务定义：真实 PCB 图像的 good / bad 二分类",
    "按类别重新组织样本：正常样本作为 good，缺陷样本作为 bad；模型输出后验概率 P(缺陷|x)。",
    imagePanel("14_正常与缺陷样本归类预览.png", fill, "contain"),
  );

  titledSlide(
    p,
    4,
    "数据集组成与划分：先把实验对象讲清楚",
    "VisA PCB 子集包含 pcb1 - pcb4，类别分布不均衡，因此结果不能只看 Accuracy。",
    grid({ width: fill, height: fill, columns: [fr(1.15), fr(0.85)], columnGap: 30 }, [
      imagePanel("01_数据集样本组成.png", fill, "contain"),
      column({ width: fill, height: fill, gap: 18 }, [
        statCard("4013", "正常样本 normal", C.navy),
        statCard("400", "缺陷样本 anomaly", C.orange),
        statCard("70 / 15 / 15", "训练 / 验证 / 测试划分", C.ocean),
        panel(
          { width: fill, height: fill, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 26, y: 22 } },
          bullet(
            [
              "训练集只负责估计标准化参数、PCA方向和贝叶斯模型。",
              "验证集用于选择 PCA 维度、Gamma 和后验阈值。",
              "测试集只在最后评估，避免参数选择污染结果。",
            ],
            { fontSize: 23, gap: 13, dotColor: C.gold },
          ),
        ),
      ]),
    ]),
  );

  titledSlide(
    p,
    5,
    "技术路线：从图像到贝叶斯优化结果",
    "流程图不追求复杂，重点展示每一步输入输出，以及参数反馈如何形成最终方案。",
    imagePanel("13_项目流程图.png", fill, "contain"),
  );

  titledSlide(
    p,
    6,
    "特征提取：PCB 图像如何变成 1318 维数据",
    "贝叶斯分类器不直接理解图片，需要先把图像转成可计算的特征向量 x。",
    imagePanel("12_图像特征提取过程可视化.png", fill, "contain"),
  );

  titledSlide(
    p,
    7,
    "特征矩阵：模型真正看到的是 X ∈ R^(4413×1318)",
    "每一行是一张 PCB 图像，每一列是一种统计或纹理特征；标签 Y 为 normal / anomaly。",
    grid({ width: fill, height: fill, columns: [fr(1.08), fr(0.92)], columnGap: 30 }, [
      panel(
        { width: fill, height: fill, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 32, y: 26 } },
        column({ width: fill, height: fill, gap: 16 }, [
          row({ width: fill, height: hug, justify: "between" }, [
            tx("特征类别", { width: fixed(260), style: { fontSize: 26, bold: true, color: C.navy } }),
            tx("维度", { width: fixed(110), style: { fontSize: 26, bold: true, color: C.navy, alignment: "right" } }),
            tx("作用", { width: fill, style: { fontSize: 26, bold: true, color: C.navy } }),
          ]),
          rule({ width: fill, stroke: C.line, weight: 2 }),
          ...[
            ["颜色统计 RGB/HSV/Lab", "36", "描述焊盘、基板、元件颜色与光照差异"],
            ["灰度统计", "8", "描述亮度分布、熵和分位数"],
            ["边缘密度", "2", "捕捉走线、器件边界和结构突变"],
            ["GLCM 纹理", "4", "度量对比度、相关性、能量和同质性"],
            ["LBP 局部纹理", "944", "描述局部纹理模式，敏感于划痕、污染、缺件"],
            ["HOG 梯度结构", "324", "描述方向梯度和整体结构轮廓"],
          ].map(([a, b, c]) =>
            row({ width: fill, height: hug, gap: 22, align: "start" }, [
              tx(a, { width: fixed(285), style: { fontSize: 22, bold: true, color: C.ink } }),
              tx(b, { width: fixed(80), style: { fontSize: 22, bold: true, color: C.orange, alignment: "right" } }),
              tx(c, { width: fill, style: { fontSize: 21, color: C.slate, lineSpacing: 1.16 } }),
            ]),
          ),
        ]),
      ),
      panel(
        { width: fill, height: fill, fill: C.paleBlue, line: { width: 1, fill: "#9CCBE2" }, borderRadius: "rounded-lg", padding: { x: 30, y: 28 } },
        column({ width: fill, height: fill, gap: 20 }, [
          tx("数据呈现方式", { style: { fontSize: 32, bold: true, color: C.navy } }),
          tx("X = [x₁; x₂; ...; xₙ]", { style: { fontSize: 42, bold: true, color: C.navy2 } }),
          tx("xᵢ = [颜色, 灰度, 边缘, GLCM, LBP, HOG]", { style: { fontSize: 24, color: C.ink } }),
          bullet(
            [
              "标准化后进入 PCA，减少 1318 维特征中的冗余。",
              "贝叶斯模型估计各类别条件概率分布 p(x|ω)。",
              "后验概率 P(缺陷|x) 作为最终判别依据。",
            ],
            { fontSize: 24, gap: 16, dotColor: C.gold },
          ),
        ]),
      ),
    ]),
  );

  titledSlide(
    p,
    8,
    "贝叶斯决策基础：从条件概率到最小风险",
    "PCB 检测中最有解释性的量不是一个硬标签，而是后验概率和由阈值控制的风险。",
    grid({ width: fill, height: fill, columns: [fr(0.9), fr(1.1)], columnGap: 30 }, [
      panel(
        { width: fill, height: fill, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 32, y: 28 } },
        column({ width: fill, height: fill, gap: 22 }, [
          tx("核心公式", { style: { fontSize: 34, bold: true, color: C.navy } }),
          panel(
            { width: fill, height: hug, fill: C.paleBlue, line: { width: 1, fill: "#9CCBE2" }, borderRadius: "rounded-lg", padding: { x: 24, y: 18 } },
            tx("P(ωₖ|x) = p(x|ωₖ)P(ωₖ) / Σⱼ p(x|ωⱼ)P(ωⱼ)", {
              style: { fontSize: 27, bold: true, color: C.navy, alignment: "center" },
            }),
          ),
          panel(
            { width: fill, height: hug, fill: C.paleGold, line: { width: 1, fill: "#EAD18B" }, borderRadius: "rounded-lg", padding: { x: 24, y: 18 } },
            tx("R(αᵢ|x) = Σⱼ λᵢⱼ P(ωⱼ|x)，选择风险最小的动作", {
              style: { fontSize: 25, bold: true, color: "#6B4E00", alignment: "center" },
            }),
          ),
          bullet(
            [
              "ω₁：normal；ω₂：anomaly。",
              "如果 P(缺陷|x) ≥ T，则判为缺陷。",
              "T 越低越敏感，召回率通常升高；T 越高越保守，误报率通常降低。",
            ],
            { fontSize: 24, gap: 14, dotColor: C.cyan },
          ),
        ]),
      ),
      imagePanel("09_一维概率分布与贝叶斯误差.png", fill, "contain"),
    ]),
  );

  titledSlide(
    p,
    9,
    "贝叶斯模型核心代码 1：训练模型并输出后验概率",
    "这一页对应“从 X 到 P(缺陷|x)”的关键实现，是讲清贝叶斯模型最重要的过渡页。",
    grid({ width: fill, height: fill, columns: [fr(1.2), fr(0.8)], columnGap: 28 }, [
      panel(
        { width: fill, height: fill, fill: "#102033", line: { width: 1, fill: "#28465F" }, borderRadius: "rounded-lg", padding: { x: 28, y: 24 } },
        codeText(`% 1. 标准化：只用训练集估计均值和方差
prep.mu = mean(XTrain, 1, 'omitnan');
prep.sigma = std(XTrain, 0, 1, 'omitnan');
XTrainZ = (XTrain - prep.mu) ./ prep.sigma;
XTestZ  = (XTest  - prep.mu) ./ prep.sigma;

% 2. PCA：将 1318 维特征压缩到 pcaDim 维
[coeff, ~, ~, ~, explained] = pca(XTrainZ);
XTrainP = XTrainZ * coeff(:, 1:pcaDim);
XTestP  = XTestZ  * coeff(:, 1:pcaDim);

% 3. 原始朴素贝叶斯：估计 p(x|ω) 并输出后验概率
model = fitcnb(XTrainP, YTrain, ...
    'DistributionNames', 'normal', ...
    'Prior', 'uniform');

[~, score] = predict(model, XTestP);
posCol = string(model.ClassNames) == "anomaly";
pBad = score(:, posCol);  % pBad = P(缺陷 | x)`, { style: { fontSize: 22 } }),
      ),
      panel(
        { width: fill, height: fill, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 30, y: 26 } },
        column({ width: fill, height: fill, gap: 20 }, [
          tx("讲解口径", { style: { fontSize: 32, bold: true, color: C.navy } }),
          bullet(
            [
              "标准化参数不能从测试集估计，否则会数据泄漏。",
              "PCA 的作用是把高维、强相关的手工特征压缩成较稳定的低维表示。",
              "MATLAB 的 predict 返回每一类的后验分数，缺陷类对应列就是 P(缺陷|x)。",
              "这一版仍是 Bayes-0/Bayes-1，独立性假设较强，因此后续继续优化。",
            ],
            { fontSize: 24, gap: 16, dotColor: C.gold },
          ),
        ]),
      ),
    ]),
  );

  titledSlide(
    p,
    10,
    "贝叶斯核心代码 2：Gamma 与阈值优化",
    "优化不是换成别的模型，而是在贝叶斯框架内改进特征空间、协方差估计和决策阈值。",
    grid({ width: fill, height: fill, columns: [fr(1.18), fr(0.82)], columnGap: 28 }, [
      panel(
        { width: fill, height: fill, fill: "#102033", line: { width: 1, fill: "#28465F" }, borderRadius: "rounded-lg", padding: { x: 28, y: 24 } },
        codeText(`% 参数网格：只在验证集上选择
cfg.pcaDims = [10 20 40 80 120];
cfg.bayesGammas = [0 0.1 0.3 0.6 0.9];
cfg.decisionThresholds = 0.20:0.05:0.80;

for d = cfg.pcaDims
    XTrainP = XTrainZ * coeff(:, 1:d);
    XValP   = XValZ   * coeff(:, 1:d);

    for gamma = cfg.bayesGammas
        model = fitcdiscr(XTrainP, YTrain, ...
            'DiscrimType', 'linear', ...
            'Gamma', gamma, ...
            'Prior', 'uniform');

        [~, scoreVal] = predict(model, XValP);
        pBadVal = positive_score(model, scoreVal);

        for T = cfg.decisionThresholds
            yPred = threshold_predict(pBadVal, T);
            metrics = classification_metrics( ...
                YVal, yPred, pBadVal, "anomaly");
        end
    end
end`, { style: { fontSize: 22 } }),
      ),
      column({ width: fill, height: fill, gap: 18 }, [
        panel(
          { width: fill, height: hug, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 28, y: 22 } },
          column({ width: fill, height: hug, gap: 12 }, [
            tx("Bayes-2", { style: { fontSize: 30, bold: true, color: C.blue } }),
            tx("高斯判别建模：弱化朴素贝叶斯独立性假设，考虑特征间相关结构。", { style: { fontSize: 22, color: C.slate, lineSpacing: 1.18 } }),
          ]),
        ),
        panel(
          { width: fill, height: hug, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 28, y: 22 } },
          column({ width: fill, height: hug, gap: 12 }, [
            tx("Bayes-3", { style: { fontSize: 30, bold: true, color: C.ocean } }),
            tx("Gamma 正则化：让协方差估计更稳，降低高维小样本下的过拟合风险。", { style: { fontSize: 22, color: C.slate, lineSpacing: 1.18 } }),
          ]),
        ),
        panel(
          { width: fill, height: fill, fill: C.paleGold, line: { width: 1, fill: "#EAD18B" }, borderRadius: "rounded-lg", padding: { x: 28, y: 22 } },
          column({ width: fill, height: fill, gap: 12 }, [
            tx("Bayes-4", { style: { fontSize: 30, bold: true, color: "#6B4E00" } }),
            tx("后验阈值 T=0.75：把“概率输出”转成更适合质量检测的决策规则。", { style: { fontSize: 22, bold: true, color: "#6B4E00", lineSpacing: 1.18 } }),
            tx("本质：不是只追求准确率，而是在误报、漏报、F1 和 AUC 之间做风险权衡。", { style: { fontSize: 21, color: C.slate, lineSpacing: 1.18 } }),
          ]),
        ),
      ]),
    ]),
  );

  titledSlide(
    p,
    11,
    "二维后验概率决策面：贝叶斯在特征空间中的判别方式",
    "把高维特征投影到二维后，可以直观看到后验概率区域和决策边界。",
    grid({ width: fill, height: fill, columns: [fr(1.06), fr(0.94)], columnGap: 30 }, [
      imagePanel("10_二维后验概率决策面.png", fill, "contain"),
      panel(
        { width: fill, height: fill, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 30, y: 28 } },
        column({ width: fill, height: fill, gap: 18 }, [
          tx("这张图怎么讲", { style: { fontSize: 32, bold: true, color: C.navy } }),
          bullet(
            [
              "背景色表示后验概率区域，颜色越接近缺陷类，P(缺陷|x) 越高。",
              "黑色边界对应 P(normal|x) = P(anomaly|x)，是理论上的概率分界线。",
              "散点混杂说明手工特征并不能完美分开真实 PCB 缺陷，这是贝叶斯检测的难点。",
              "后续阈值 T 不是画在二维边界上，而是作用在 P(缺陷|x) 的一维概率输出上。",
            ],
            { fontSize: 24, gap: 15, dotColor: C.cyan },
          ),
        ]),
      ),
    ]),
  );

  titledSlide(
    p,
    12,
    "Bayes-only 优化路径：从 Bayes-0 到 Bayes-4",
    "对比对象不是 CNN、Kmeans 或 BP，而是同一贝叶斯框架下的逐步优化版本。",
    grid({ width: fill, height: fill, columns: [fr(0.76), fr(1.24)], columnGap: 30 }, [
      panel(
        { width: fill, height: fill, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 28, y: 24 } },
        column({ width: fill, height: fill, gap: 15 }, [
          tx("五个阶段", { style: { fontSize: 32, bold: true, color: C.navy } }),
          ...[
            ["Bayes-0", "原始朴素贝叶斯"],
            ["Bayes-1", "PCA 降维优化"],
            ["Bayes-2", "高斯建模优化"],
            ["Bayes-3", "Gamma 正则化优化"],
            ["Bayes-4", "后验阈值优化"],
          ].map(([id, desc]) =>
            panel(
              { width: fill, height: fixed(78), fill: id === "Bayes-4" ? C.paleGold : C.paleBlue, line: { width: 1, fill: id === "Bayes-4" ? "#EAD18B" : "#B6D9EA" }, borderRadius: "rounded-lg", padding: { x: 18, y: 12 } },
              row({ width: fill, height: fill, gap: 16, align: "center" }, [
                tx(id, { width: fixed(120), style: { fontSize: 23, bold: true, color: id === "Bayes-4" ? "#6B4E00" : C.navy } }),
                tx(desc, { width: fill, style: { fontSize: 22, color: C.ink } }),
              ]),
            ),
          ),
        ]),
      ),
      imagePanel("03_贝叶斯优化迭代趋势.png", fill, "contain"),
    ]),
  );

  titledSlide(
    p,
    13,
    "参数分析：PCA 维度 × 正则化 Gamma",
    "这页对应老师要求的“关键参数变化对性能的影响”，展示调参不是拍脑袋选的。",
    grid({ width: fill, height: fill, columns: [fr(1.12), fr(0.88)], columnGap: 30 }, [
      imagePanel("05_主成分维度与正则化参数热力图.png", fill, "contain"),
      panel(
        { width: fill, height: fill, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 30, y: 28 } },
        column({ width: fill, height: fill, gap: 20 }, [
          tx("读图方式", { style: { fontSize: 32, bold: true, color: C.navy } }),
          bullet(
            [
              "纵轴：PCA 保留的特征维度，维度过低会丢信息，过高会带来冗余和噪声。",
              "横轴：正则化参数 γ，用来控制协方差估计的平滑程度。",
              "颜色：验证集 F1 值，越深说明 precision 和 recall 的综合表现越好。",
              "金色框：当前验证集下的最优参数区域。",
            ],
            { fontSize: 24, gap: 15, dotColor: C.gold },
          ),
          panel(
            { width: fill, height: hug, fill: C.paleBlue, line: { width: 1, fill: "#9CCBE2" }, borderRadius: "rounded-lg", padding: { x: 22, y: 18 } },
            tx("汇报句式：我不是单看准确率，而是用验证集 F1 选择 PCA 维度和 Gamma，再在测试集上报告最终结果。", {
              style: { fontSize: 22, bold: true, color: C.navy, lineSpacing: 1.18 },
            }),
          ),
        ]),
      ),
    ]),
  );

  titledSlide(
    p,
    14,
    "阈值与风险：为什么不是固定 0.5",
    "在质量检测中，阈值 T 决定误报与漏报的权衡，因此它本身就是贝叶斯决策的一部分。",
    grid({ width: fill, height: fill, columns: [fr(1), fr(1)], columnGap: 28 }, [
      imagePanel("06_后验概率阈值决策曲线.png", fill, "contain"),
      imagePanel("11_贝叶斯风险与损失函数.png", fill, "contain"),
    ]),
  );

  titledSlide(
    p,
    15,
    "核心指标横向对比：优化后到底提升在哪里",
    "用 Accuracy、Precision、Recall、F1、AUC 同时说明性能，避免单指标误导。",
    grid({ width: fill, height: fill, columns: [fr(1.05), fr(0.95)], columnGap: 30 }, [
      imagePanel("02_五大指标横向对比.png", fill, "contain"),
      panel(
        { width: fill, height: fill, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 30, y: 28 } },
        column({ width: fill, height: fill, gap: 18 }, [
          tx("测试集结果摘要", { style: { fontSize: 32, bold: true, color: C.navy } }),
          grid({ width: fill, height: hug, columns: [fr(1), fr(1)], columnGap: 16, rowGap: 16 }, [
            statCard("0.918", "Accuracy", C.navy2),
            statCard("0.542", "F1-score", C.orange),
            statCard("0.899", "AUC", C.ocean),
            statCard("0.372", "IoU", C.gold),
          ]),
          bullet(
            [
              "Bayes-0 的 Accuracy 不低，但 F1 很低，说明类别不均衡下有明显误导。",
              "Bayes-4 通过阈值优化提高 precision，减少把正常 PCB 误判为缺陷的情况。",
              "AUC 保持较高，说明后验排序能力较稳定。",
            ],
            { fontSize: 23, gap: 14, dotColor: C.cyan },
          ),
        ]),
      ),
    ]),
  );

  titledSlide(
    p,
    16,
    "误报与漏报：质量检测里最需要解释的权衡",
    "FPR 表示正常被误判为缺陷；FNR 表示缺陷被漏检。两者共同决定实际质检风险。",
    grid({ width: fill, height: fill, columns: [fr(1.1), fr(0.9)], columnGap: 30 }, [
      imagePanel("04_误报率与漏报率权衡.png", fill, "contain"),
      panel(
        {
          width: fill,
          height: fill,
          fill: C.white,
          line: { style: "solid", width: 1, fill: C.line },
          borderRadius: "rounded-lg",
          padding: 10,
        },
        bitmap(basicAsset("基础图_贝叶斯混淆矩阵.png"), {
          width: fill,
          height: fill,
          fit: "contain",
          alt: "贝叶斯混淆矩阵",
        }),
      ),
    ]),
  );

  titledSlide(
    p,
    17,
    "综合仪表盘：一页回答性能问题",
    "把趋势、阈值、参数热力图和核心指标放在同一页，适合作为答辩总结页。",
    imagePanel("08_贝叶斯优化性能评估仪表盘.png", fill, "contain"),
  );

  titledSlide(
    p,
    18,
    "结论与反思：贝叶斯方案的价值和边界",
    "最终方案不是为了证明贝叶斯一定优于深度学习，而是完整展示概率决策、参数优化和可解释评估。",
    grid({ width: fill, height: fill, columns: [fr(1), fr(1)], columnGap: 30 }, [
      panel(
        { width: fill, height: fill, fill: C.white, line: { width: 1, fill: C.line }, borderRadius: "rounded-lg", padding: { x: 32, y: 28 } },
        column({ width: fill, height: fill, gap: 18 }, [
          tx("可以强调的贡献", { style: { fontSize: 32, bold: true, color: C.navy } }),
          bullet(
            [
              "选用真实彩色 PCB 图像，任务场景更贴近电子信息方向。",
              "构建 1318 维手工特征，并解释每类特征的物理含义。",
              "在贝叶斯框架内做 PCA、Gamma、阈值三类优化。",
              "用多指标与多图表说明性能，满足课程研讨的完整实验要求。",
            ],
            { fontSize: 25, gap: 16, dotColor: C.gold },
          ),
        ]),
      ),
      panel(
        { width: fill, height: fill, fill: C.paleBlue, line: { width: 1, fill: "#9CCBE2" }, borderRadius: "rounded-lg", padding: { x: 32, y: 28 } },
        column({ width: fill, height: fill, gap: 18 }, [
          tx("需要主动承认的不足", { style: { fontSize: 32, bold: true, color: C.navy } }),
          bullet(
            [
              "贝叶斯依赖手工特征，难以自动学习复杂空间拓扑结构。",
              "真实缺陷样本少，类别不均衡导致 recall 与 precision 存在明显权衡。",
              "当前做的是图像级识别，不是像素级缺陷分割。",
              "后续可加入代价敏感贝叶斯、局部区域特征或更精细的异常定位。",
            ],
            { fontSize: 25, gap: 16, dotColor: C.cyan },
          ),
          rule({ width: fill, stroke: "#9CCBE2", weight: 2 }),
          tx("参考：VisA Visual Anomaly Dataset；哈尔滨工程大学校训与“三海一核”办学特色官方资料。", {
            style: { fontSize: 18, color: C.slate, lineSpacing: 1.2 },
          }),
        ]),
      ),
    ]),
  );
}

async function saveBlob(blob, outPath) {
  const bytes = Buffer.from(await blob.arrayBuffer());
  fs.mkdirSync(path.dirname(outPath), { recursive: true });
  fs.writeFileSync(outPath, bytes);
}

async function main() {
  fs.mkdirSync(path.dirname(OUTPUT), { recursive: true });
  fs.mkdirSync(PREVIEW_DIR, { recursive: true });
  const p = Presentation.create({ slideSize: { width: W, height: H } });
  addAllSlides(p);

  const pptxBlob = await PresentationFile.exportPptx(p);
  await pptxBlob.save(OUTPUT);

  for (let i = 0; i < p.slides.count; i += 1) {
    const slide = p.slides.getItem(i);
    const png = await slide.export({ format: "png" });
    await saveBlob(png, `${PREVIEW_DIR}/slide_${String(i + 1).padStart(2, "0")}.png`);
  }

  console.log(`PPTX: ${OUTPUT}`);
  console.log(`Previews: ${PREVIEW_DIR}`);
  console.log(`Slides: ${p.slides.count}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
