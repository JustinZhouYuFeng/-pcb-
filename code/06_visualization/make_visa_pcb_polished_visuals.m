% 中文注释：生成排版更精细的 PCB 实验结果展示图。
% 主要流程：读取实验结果，绘制优化对比、混淆矩阵、ROC 等适合汇报的图表。
% 输出结果：保存到 ppt_materials 目录，作为最终演示文稿的主要图片来源。

% 函数说明：生成最终汇报使用的高质量 PCB 实验图表。
% 行注释：这里开始定义 make_visa_pcb_polished_visuals 函数。
function make_visa_pcb_polished_visuals(featuresFile, bayesResultsFile, optimizationResultsFile, cfg)
%MAKE_VISA_PCB_POLISHED_VISUALS Create Chinese PPT-ready comparison figures.

% 行注释：这里从磁盘读取前面步骤保存的数据文件。
S = load(featuresFile);
% 行注释：这里从磁盘读取前面步骤保存的数据文件。
B = load(bayesResultsFile);
% 行注释：这里从磁盘读取前面步骤保存的数据文件。
O = load(optimizationResultsFile);

% 行注释：这里计算或设置 figDir，供后续步骤使用。
figDir = fullfile(cfg.projectRoot, "results", "figures");
% 行注释：这里计算或设置 pptDir，供后续步骤使用。
pptDir = fullfile(cfg.projectRoot, "ppt_materials", "visa_pcb", "polished");
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(figDir);
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(pptDir);

% 行注释：这里计算或设置 theme，供后续步骤使用。
theme = pcb_theme();
% 行注释：这里执行当前语句，完成这一小步处理。
setup_chinese_style(theme);

% 行注释：这里执行当前语句，完成这一小步处理。
make_polished_dataset_overview(S, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_feature_extraction_pipeline(S, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_metrics_horizontal(O.rows, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_metrics_vertical(O.rows, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_error_tradeoff(O.rows, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_parameter_heatmaps(B.valRows, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_threshold_tradeoff(B.valRows, B.bestSpec, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_posterior_density_risk(S, B, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_summary_dashboard(O.rows, B.valRows, B.bestSpec, figDir, pptDir, theme);

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Polished Chinese figures saved to: %s\n", pptDir);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：集中定义配色、字体和线条风格，保证整套图表视觉一致。
% 行注释：这里开始定义 pcb_theme 函数。
function theme = pcb_theme()
% 行注释：这里执行当前语句，完成这一小步处理。
theme.font = 'Microsoft YaHei';
% 行注释：这里执行当前语句，完成这一小步处理。
theme.bg = [1 1 1];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.panel = [1 1 1];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.text = [0.10 0.12 0.16];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.muted = [0.45 0.48 0.54];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.grid = [0.90 0.91 0.93];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.deepBlue = hex2rgb("#004488");
% 行注释：这里执行当前语句，完成这一小步处理。
theme.blue = hex2rgb("#2E5A88");
% 行注释：这里执行当前语句，完成这一小步处理。
theme.lightBlue = [0.72 0.84 0.93];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.gray = hex2rgb("#CCCCCC");
% 行注释：这里执行当前语句，完成这一小步处理。
theme.lightGray = [0.91 0.92 0.94];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.orange = hex2rgb("#D95319");
% 行注释：这里执行当前语句，完成这一小步处理。
theme.orangeRed = hex2rgb("#E4572E");
% 行注释：这里执行当前语句，完成这一小步处理。
theme.darkRed = hex2rgb("#B22222");
% 行注释：这里执行当前语句，完成这一小步处理。
theme.gold = [0.96 0.68 0.16];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.green = [0.20 0.56 0.36];
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：设置 MATLAB 默认字体，避免中文标题或标签乱码。
% 行注释：这里开始定义 setup_chinese_style 函数。
function setup_chinese_style(theme)
% 行注释：这里执行当前语句，完成这一小步处理。
set(groot, 'DefaultAxesFontName', theme.font);
% 行注释：这里执行当前语句，完成这一小步处理。
set(groot, 'DefaultTextFontName', theme.font);
% 行注释：这里执行当前语句，完成这一小步处理。
set(groot, 'DefaultLegendFontName', theme.font);
% 行注释：这里执行当前语句，完成这一小步处理。
set(groot, 'DefaultColorbarFontName', theme.font);
% 行注释：这里执行当前语句，完成这一小步处理。
set(groot, 'DefaultAxesTickDir', 'out');
% 行注释：这里执行当前语句，完成这一小步处理。
set(groot, 'DefaultFigureColor', theme.bg);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：绘制数据集概览图，说明 PCB1 到 PCB4 的样本组成。
% 行注释：这里开始定义 make_polished_dataset_overview 函数。
function make_polished_dataset_overview(S, figDir, pptDir, theme)
% 行注释：这里计算或设置 T，供后续步骤使用。
T = table(string(S.PCBSubset), categorical(string(S.Y), ["normal", "anomaly"]), ...
    'VariableNames', {'PCBSubset', 'Label'});
% 行注释：这里计算或设置 G，供后续步骤使用。
G = groupsummary(T, ["PCBSubset", "Label"]);

% 行注释：这里计算或设置 subsets，供后续步骤使用。
subsets = unique(string(G.PCBSubset), "stable");
% 行注释：这里计算或设置 normalCounts，供后续步骤使用。
normalCounts = zeros(numel(subsets), 1);
% 行注释：这里计算或设置 anomalyCounts，供后续步骤使用。
anomalyCounts = zeros(numel(subsets), 1);
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(subsets)
    % 行注释：这里执行当前语句，完成这一小步处理。
    normalCounts(i) = G.GroupCount(G.PCBSubset == subsets(i) & G.Label == "normal");
    % 行注释：这里执行当前语句，完成这一小步处理。
    anomalyCounts(i) = G.GroupCount(G.PCBSubset == subsets(i) & G.Label == "anomaly");
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 1180 620]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里计算或设置 b，供后续步骤使用。
b = bar(ax, categorical(subsets), [normalCounts, anomalyCounts], 'grouped', 'BarWidth', 0.72);
% 行注释：这里执行当前语句，完成这一小步处理。
b(1).FaceColor = theme.deepBlue;
% 行注释：这里执行当前语句，完成这一小步处理。
b(2).FaceColor = theme.orangeRed;
% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax, theme);
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "图像数量");
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax, "VisA 真实 PCB 数据集样本组成", 'FontWeight', 'bold');
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, ["正常样本", "缺陷样本"], 'Location', 'northoutside', ...
    'Orientation', 'horizontal', 'Box', 'off', 'FontSize', 12);
% 行注释：这里调整坐标轴、网格或绘图状态。
ylim(ax, [0 max(normalCounts) * 1.18]);
% 行注释：这里执行当前语句，完成这一小步处理。
add_bar_labels(ax, b, 0);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "01_数据集样本组成.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：绘制从原图到特征向量的特征提取流程图。
% 行注释：这里开始定义 make_feature_extraction_pipeline 函数。
function make_feature_extraction_pipeline(S, figDir, pptDir, theme)
% 行注释：这里计算或设置 idx，供后续步骤使用。
idx = select_feature_sample(S);
% 行注释：这里计算或设置 raw，供后续步骤使用。
raw = imread(S.ImagePath(idx));
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if size(raw, 3) == 1
    % 行注释：这里计算或设置 raw，供后续步骤使用。
    raw = repmat(raw, 1, 1, 3);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 img，供后续步骤使用。
img = im2double(imresize(raw, [256 256]));
% 行注释：这里计算或设置 gray，供后续步骤使用。
gray = rgb2gray(img);
% 行注释：这里计算或设置 grayEq，供后续步骤使用。
grayEq = adapthisteq(gray);
% 行注释：这里计算或设置 edgeMap，供后续步骤使用。
edgeMap = edge(grayEq, "Canny");
% 行注释：这里计算或设置 gradMag，供后续步骤使用。
gradMag = imgradient(grayEq);
% 行注释：这里计算或设置 gradMag，供后续步骤使用。
gradMag = mat2gray(gradMag);

% 行注释：这里计算或设置 featureVector，供后续步骤使用。
featureVector = double(S.X(idx, :));
% 行注释：这里计算或设置 featureNames，供后续步骤使用。
featureNames = string(S.featureNames(:));
% 行注释：这里计算或设置 groupNames，供后续步骤使用。
groupNames = ["颜色统计", "灰度统计", "边缘密度", "GLCM纹理", "LBP纹理", "HOG梯度"];
% 行注释：这里计算或设置 groupDims，供后续步骤使用。
groupDims = [36, 8, 2, 4, 944, 324];
% 行注释：这里计算或设置 groupColors，供后续步骤使用。
groupColors = [
    % 行注释：这里执行当前语句，完成这一小步处理。
    theme.deepBlue
    % 行注释：这里执行当前语句，完成这一小步处理。
    theme.lightBlue
    % 行注释：这里执行当前语句，完成这一小步处理。
    theme.green
    % 行注释：这里执行当前语句，完成这一小步处理。
    theme.gold
    % 行注释：这里执行当前语句，完成这一小步处理。
    theme.orangeRed
    % 行注释：这里执行当前语句，完成这一小步处理。
    theme.darkRed
% 行注释：这里结束当前多行参数、列表或结构。
];

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [80 60 1600 980]);
% 行注释：这里执行当前语句，完成这一小步处理。
tiledlayout(fig, 3, 4, 'TileSpacing', 'compact', 'Padding', 'compact');

% 行注释：这里计算或设置 ax1，供后续步骤使用。
ax1 = nexttile(1);
% 行注释：这里执行当前语句，完成这一小步处理。
imshow(raw, 'Parent', ax1);
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax1, "1 原始彩色图像", 'FontWeight', 'bold', 'Color', theme.text);

% 行注释：这里计算或设置 ax2，供后续步骤使用。
ax2 = nexttile(2);
% 行注释：这里执行当前语句，完成这一小步处理。
imshow(img, 'Parent', ax2);
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax2, "2 尺寸统一 256×256", 'FontWeight', 'bold', 'Color', theme.text);

% 行注释：这里计算或设置 ax3，供后续步骤使用。
ax3 = nexttile(3);
% 行注释：这里执行当前语句，完成这一小步处理。
imshow(grayEq, 'Parent', ax3);
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax3, "3 灰度增强", 'FontWeight', 'bold', 'Color', theme.text);

% 行注释：这里计算或设置 ax4，供后续步骤使用。
ax4 = nexttile(4);
% 行注释：这里执行当前语句，完成这一小步处理。
imshow(edgeMap, 'Parent', ax4);
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax4, "4 Canny 边缘响应", 'FontWeight', 'bold', 'Color', theme.text);

% 行注释：这里计算或设置 ax5，供后续步骤使用。
ax5 = nexttile(5, [1 2]);
% 行注释：这里计算或设置 b，供后续步骤使用。
b = barh(ax5, 1:numel(groupNames), groupDims, 0.62);
% 行注释：这里执行当前语句，完成这一小步处理。
b.FaceColor = 'flat';
% 行注释：这里执行当前语句，完成这一小步处理。
b.CData = groupColors;
% 行注释：这里执行当前语句，完成这一小步处理。
b.EdgeColor = 'none';
% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax5, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
ax5.YDir = 'reverse';
% 行注释：这里执行当前语句，完成这一小步处理。
ax5.YTick = 1:numel(groupNames);
% 行注释：这里执行当前语句，完成这一小步处理。
ax5.YTickLabel = groupNames;
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax5, "维度数量");
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax5, "5 六类手工特征组成（共 1318 维）", 'FontWeight', 'bold');
% 行注释：这里调整坐标轴、网格或绘图状态。
xlim(ax5, [0 1020]);
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(groupDims)
    % 行注释：这里给图表添加标题、标签或说明文字。
    text(ax5, groupDims(i) + 18, i, string(groupDims(i)) + "维", ...
        'VerticalAlignment', 'middle', 'FontWeight', 'bold', ...
        'Color', theme.text, 'FontSize', 11);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 ax6，供后续步骤使用。
ax6 = nexttile(7, [1 2]);
% 行注释：这里计算或设置 displayVec，供后续步骤使用。
displayVec = normalize_vector_for_display(featureVector);
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
imagesc(ax6, repmat(displayVec, 24, 1), [0 1]);
% 行注释：这里执行当前语句，完成这一小步处理。
colormap(ax6, blue_colormap());
% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax6, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
ax6.YTick = [];
% 行注释：这里执行当前语句，完成这一小步处理。
ax6.XTick = [1, 50, 994, 1318];
% 行注释：这里执行当前语句，完成这一小步处理。
ax6.XTickLabel = ["1", "50", "994", "1318"];
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax6, "特征编号");
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax6, "6 当前图像的 1318 维特征向量可视化", 'FontWeight', 'bold');
% 行注释：这里计算或设置 boundaries，供后续步骤使用。
boundaries = cumsum(groupDims);
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(boundaries)-1
    % 行注释：这里执行当前语句，完成这一小步处理。
    xline(ax6, boundaries(i) + 0.5, '-', 'Color', [1 1 1], ...
        'LineWidth', 1.4, 'HandleVisibility', 'off');
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax6, 25, -2.2, "统计特征 50维", ...
    'HorizontalAlignment', 'center', 'FontSize', 10, ...
    'FontWeight', 'bold', 'Color', theme.text, 'Clipping', 'off');
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax6, 522, -2.2, "LBP纹理 944维", ...
    'HorizontalAlignment', 'center', 'FontSize', 10, ...
    'FontWeight', 'bold', 'Color', theme.text, 'Clipping', 'off');
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax6, 1156, -2.2, "HOG梯度 324维", ...
    'HorizontalAlignment', 'center', 'FontSize', 10, ...
    'FontWeight', 'bold', 'Color', theme.text, 'Clipping', 'off');

% 行注释：这里计算或设置 ax7，供后续步骤使用。
ax7 = nexttile(9, [1 2]);
% 行注释：这里调整坐标轴、网格或绘图状态。
axis(ax7, 'off');
% 行注释：这里计算或设置 labelText，供后续步骤使用。
labelText = label_to_chinese_single(string(S.Y(idx)));
% 行注释：这里计算或设置 sampleText，供后续步骤使用。
sampleText = strjoin([
    % 行注释：这里执行当前语句，完成这一小步处理。
    "7 输出形式：特征矩阵 X"
    % 行注释：这里执行当前语句，完成这一小步处理。
    ""
    % 行注释：这里执行当前语句，完成这一小步处理。
    "X 的大小：" + string(size(S.X, 1)) + " × " + string(size(S.X, 2))
    % 行注释：这里执行当前语句，完成这一小步处理。
    "第 i 行：第 i 张电路板图像"
    % 行注释：这里执行当前语句，完成这一小步处理。
    "第 j 列：第 j 个手工特征"
    % 行注释：这里执行当前语句，完成这一小步处理。
    "当前示例：" + labelText + " / " + string(S.PCBSubset(idx))
    % 行注释：这里执行当前语句，完成这一小步处理。
    ""
    % 行注释：这里执行当前语句，完成这一小步处理。
    "同时保存：标签 Y、数据划分 Split、图像路径 ImagePath"
% 行注释：这里结束当前多行参数、列表或结构。
], newline);
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax7, 0.02, 0.92, sampleText, 'Units', 'normalized', ...
    'VerticalAlignment', 'top', 'FontName', theme.font, ...
    'FontSize', 14, 'FontWeight', 'bold', 'Color', theme.text, ...
    'BackgroundColor', [0.97 0.98 1.00], 'EdgeColor', theme.lightGray, ...
    'Margin', 12, 'Interpreter', 'none');

% 行注释：这里计算或设置 ax8，供后续步骤使用。
ax8 = nexttile(11, [1 2]);
% 行注释：这里调整坐标轴、网格或绘图状态。
axis(ax8, 'off');
% 行注释：这里计算或设置 exampleText，供后续步骤使用。
exampleText = strjoin([
    % 行注释：这里执行当前语句，完成这一小步处理。
    "8 单个特征值示例"
    % 行注释：这里执行当前语句，完成这一小步处理。
    ""
    % 行注释：这里执行当前语句，完成这一小步处理。
    "红色通道均值 rgb_r_mean：" + format_value(feature_value(featureVector, featureNames, "rgb_r_mean"))
    % 行注释：这里执行当前语句，完成这一小步处理。
    "灰度熵 gray_entropy：" + format_value(feature_value(featureVector, featureNames, "gray_entropy"))
    % 行注释：这里执行当前语句，完成这一小步处理。
    "Canny 边缘密度：" + format_value(feature_value(featureVector, featureNames, "edge_density_canny"))
    % 行注释：这里执行当前语句，完成这一小步处理。
    "GLCM 对比度：" + format_value(feature_value(featureVector, featureNames, "glcm_contrast"))
    % 行注释：这里执行当前语句，完成这一小步处理。
    ""
    % 行注释：这里执行当前语句，完成这一小步处理。
    "这些数值共同组成一行 1318 维向量，随后进入标准化、PCA 与贝叶斯建模。"
% 行注释：这里结束当前多行参数、列表或结构。
], newline);
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax8, 0.02, 0.92, exampleText, 'Units', 'normalized', ...
    'VerticalAlignment', 'top', 'FontName', theme.font, ...
    'FontSize', 14, 'FontWeight', 'bold', 'Color', theme.text, ...
    'BackgroundColor', [1.00 0.98 0.93], 'EdgeColor', theme.gold, ...
    'Margin', 12, 'Interpreter', 'none');

% 行注释：这里执行当前语句，完成这一小步处理。
sgtitle(fig, "电路板图像从原始图片到 1318 维特征数据的转换过程", ...
    'FontWeight', 'bold', 'FontSize', 22, 'Color', theme.text, ...
    'FontName', theme.font);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "12_图像特征提取过程可视化.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：从数据集中挑一张稳定的样例图，用于展示特征提取效果。
% 行注释：这里开始定义 select_feature_sample 函数。
function idx = select_feature_sample(S)
% 行注释：这里计算或设置 candidateIdx，供后续步骤使用。
candidateIdx = [find(string(S.Y) == "anomaly"); find(string(S.Y) == "normal")];
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(candidateIdx)
    % 行注释：这里开始尝试执行可能出错的代码。
    try
        % 行注释：这里执行当前语句，完成这一小步处理。
        imread(S.ImagePath(candidateIdx(i)));
        % 行注释：这里计算或设置 idx，供后续步骤使用。
        idx = candidateIdx(i);
        % 行注释：这里提前返回，结束当前函数的后续执行。
        return;
    % 行注释：如果 try 中出错，这里负责兜底处理。
    catch
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里执行当前语句，完成这一小步处理。
error("No readable sample image found for feature visualization.");
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：把特征向量缩放到适合画图的范围。
% 行注释：这里开始定义 normalize_vector_for_display 函数。
function displayVec = normalize_vector_for_display(featureVector)
% 行注释：这里计算或设置 v，供后续步骤使用。
v = double(featureVector(:)');
% 行注释：这里执行当前语句，完成这一小步处理。
v(~isfinite(v)) = 0;
% 行注释：这里计算或设置 lo，供后续步骤使用。
lo = prctile(v, 1);
% 行注释：这里计算或设置 hi，供后续步骤使用。
hi = prctile(v, 99);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if abs(hi - lo) < eps
    % 行注释：这里计算或设置 displayVec，供后续步骤使用。
    displayVec = zeros(size(v));
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里计算或设置 v，供后续步骤使用。
    v = min(max(v, lo), hi);
    % 行注释：这里计算或设置 displayVec，供后续步骤使用。
    displayVec = (v - lo) ./ (hi - lo);
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：按特征名查找对应数值，便于在图中标出关键特征。
% 行注释：这里开始定义 feature_value 函数。
function value = feature_value(featureVector, featureNames, featureName)
% 行注释：这里计算或设置 idx，供后续步骤使用。
idx = find(featureNames == string(featureName), 1);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if isempty(idx)
    % 行注释：这里计算或设置 value，供后续步骤使用。
    value = NaN;
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里计算或设置 value，供后续步骤使用。
    value = featureVector(idx);
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：把数值转成适合展示的短文本。
% 行注释：这里开始定义 format_value 函数。
function textValue = format_value(value)
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if isnan(value)
    % 行注释：这里计算或设置 textValue，供后续步骤使用。
    textValue = "NaN";
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里计算或设置 textValue，供后续步骤使用。
    textValue = string(sprintf("%.4f", value));
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：把英文类别标签转换成中文显示。
% 行注释：这里开始定义 label_to_chinese_single 函数。
function label = label_to_chinese_single(label)
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if label == "normal"
    % 行注释：这里计算或设置 label，供后续步骤使用。
    label = "正常样本";
% 行注释：如果前面的条件不满足，这里继续检查另一个条件。
elseif label == "anomaly"
    % 行注释：这里计算或设置 label，供后续步骤使用。
    label = "缺陷样本";
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：生成横向指标柱状图。
% 行注释：这里开始定义 make_metrics_horizontal 函数。
function make_metrics_horizontal(R, figDir, pptDir, theme)
% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 1120 680]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里执行当前语句，完成这一小步处理。
draw_metrics_horizontal(ax, R, theme, true);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "02_五大指标横向对比.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：在指定坐标轴上绘制横向指标柱状图。
% 行注释：这里开始定义 draw_metrics_horizontal 函数。
function draw_metrics_horizontal(ax, R, theme, showTitle)
% 行注释：这里计算或设置 metricNames，供后续步骤使用。
metricNames = ["准确率", "精确率", "召回率", "F1值", "AUC"];
% 行注释：这里计算或设置 baseline，供后续步骤使用。
baseline = [R.TestAccuracy(1), R.TestPrecision(1), R.TestRecall(1), R.TestF1(1), R.TestAUC(1)];
% 行注释：这里计算或设置 optimized，供后续步骤使用。
optimized = [R.TestAccuracy(end), R.TestPrecision(end), R.TestRecall(end), R.TestF1(end), R.TestAUC(end)];
% 行注释：这里计算或设置 data，供后续步骤使用。
data = [baseline(:), optimized(:)];

% 行注释：这里计算或设置 b，供后续步骤使用。
b = barh(ax, data, 'grouped', 'BarWidth', 0.72);
% 行注释：这里执行当前语句，完成这一小步处理。
b(1).FaceColor = theme.gray;
% 行注释：这里执行当前语句，完成这一小步处理。
b(1).EdgeColor = 'none';
% 行注释：这里执行当前语句，完成这一小步处理。
b(2).FaceColor = theme.deepBlue;
% 行注释：这里执行当前语句，完成这一小步处理。
b(2).EdgeColor = 'none';

% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax, theme);
% 行注释：这里调整坐标轴、网格或绘图状态。
grid(ax, 'off');
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YTick = 1:numel(metricNames);
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YTickLabel = metricNames;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YDir = 'reverse';
% 行注释：这里调整坐标轴、网格或绘图状态。
xlim(ax, [0 1.18]);
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "指标得分");
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, ["基准模型", "优化后"], 'Location', 'southoutside', ...
    'Orientation', 'horizontal', 'Box', 'off', 'FontSize', 12);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if showTitle
    % 行注释：这里给图表添加标题、标签或说明文字。
    title(ax, "五大指标横向对比：基准模型 vs 优化后", 'FontWeight', 'bold');
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里给图表添加标题、标签或说明文字。
    title(ax, "核心指标对比", 'FontWeight', 'bold');
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里执行当前语句，完成这一小步处理。
annotate_barh_values(ax, b, 3);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：生成竖向指标柱状图。
% 行注释：这里开始定义 make_metrics_vertical 函数。
function make_metrics_vertical(R, figDir, pptDir, theme)
% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 1160 650]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里执行当前语句，完成这一小步处理。
draw_metrics_vertical(ax, R, theme, true);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "03_贝叶斯优化迭代趋势.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：在指定坐标轴上绘制竖向指标柱状图。
% 行注释：这里开始定义 draw_metrics_vertical 函数。
function draw_metrics_vertical(ax, R, theme, showTitle)
% 行注释：这里计算或设置 x，供后续步骤使用。
x = 1:height(R);
% 行注释：这里计算或设置 labels，供后续步骤使用。
labels = "Bayes-" + string(0:height(R)-1);
% 行注释：这里调整坐标轴、网格或绘图状态。
hold(ax, 'on');

% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for y = 0.2:0.1:1.0
    % 行注释：这里执行当前语句，完成这一小步处理。
    yline(ax, y, '-', 'Color', theme.grid, 'LineWidth', 0.7, ...
        'HandleVisibility', 'off');
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, R.TestF1, '-o', 'LineWidth', 2.0, 'MarkerSize', 7, ...
    'MarkerFaceColor', theme.darkRed, 'MarkerEdgeColor', 'w', ...
    'Color', theme.darkRed, 'DisplayName', "F1值");
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, R.TestAUC, '--*', 'LineWidth', 2.0, 'MarkerSize', 8, ...
    'Color', theme.deepBlue, 'DisplayName', "AUC");

% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax, theme);
% 行注释：这里调整坐标轴、网格或绘图状态。
grid(ax, 'off');
% 行注释：这里执行当前语句，完成这一小步处理。
ax.XTick = x;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.XTickLabel = labels;
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "优化迭代阶段");
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "性能得分");
% 行注释：这里调整坐标轴、网格或绘图状态。
ylim(ax, [0.25 0.98]);
% 行注释：这里调整坐标轴、网格或绘图状态。
xlim(ax, [0.75 height(R) + 0.75]);
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, 'Location', 'northoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if showTitle
    % 行注释：这里给图表添加标题、标签或说明文字。
    title(ax, "纵向趋势：贝叶斯模型逐步优化", 'FontWeight', 'bold');
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里给图表添加标题、标签或说明文字。
    title(ax, "优化趋势", 'FontWeight', 'bold');
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 targetX，供后续步骤使用。
targetX = x(end);
% 行注释：这里计算或设置 targetY，供后续步骤使用。
targetY = R.TestF1(end);
% 行注释：这里计算或设置 shadowText，供后续步骤使用。
shadowText = sprintf("最终优化结果\nF1=%.3f  AUC=%.3f", R.TestF1(end), R.TestAUC(end));
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax, targetX - 0.02, targetY + 0.055, shadowText, ...
    'FontSize', 11, 'FontWeight', 'bold', 'Color', [0.55 0.55 0.55], ...
    'BackgroundColor', [0.74 0.74 0.74], 'Margin', 5, ...
    'HorizontalAlignment', 'right', 'Clipping', 'on');
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax, targetX - 0.05, targetY + 0.075, shadowText, ...
    'FontSize', 11, 'FontWeight', 'bold', 'Color', theme.text, ...
    'BackgroundColor', [1 1 1], 'EdgeColor', theme.lightGray, ...
    'LineWidth', 1.0, 'Margin', 5, 'HorizontalAlignment', 'right', ...
    'Clipping', 'on');
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：生成漏检率和误报率的权衡图。
% 行注释：这里开始定义 make_error_tradeoff 函数。
function make_error_tradeoff(R, figDir, pptDir, theme)
% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 1160 650]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里执行当前语句，完成这一小步处理。
draw_error_tradeoff(ax, R, theme, true);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "04_误报率与漏报率权衡.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：在指定坐标轴上画误报/漏检权衡曲线。
% 行注释：这里开始定义 draw_error_tradeoff 函数。
function draw_error_tradeoff(ax, R, theme, showTitle)
% 行注释：这里计算或设置 x，供后续步骤使用。
x = 1:height(R);
% 行注释：这里计算或设置 labels，供后续步骤使用。
labels = "Bayes-" + string(0:height(R)-1);
% 行注释：这里计算或设置 fpr，供后续步骤使用。
fpr = R.TestFPR(:);
% 行注释：这里计算或设置 fnr，供后续步骤使用。
fnr = R.TestFNR(:);
% 行注释：这里计算或设置 balanceX，供后续步骤使用。
balanceX = find_balance_x(x(:), fpr, fnr);

% 行注释：这里调整坐标轴、网格或绘图状态。
hold(ax, 'on');
% 行注释：这里执行当前语句，完成这一小步处理。
yyaxis(ax, 'left');
% 行注释：这里计算或设置 p1，供后续步骤使用。
p1 = plot(ax, x, fpr, '-o', 'Color', theme.deepBlue, ...
    'MarkerFaceColor', theme.deepBlue, 'MarkerEdgeColor', 'w', ...
    'LineWidth', 2.2, 'MarkerSize', 7, 'DisplayName', "误报率 (FPR)");
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "误报率 (FPR)");
% 行注释：这里调整坐标轴、网格或绘图状态。
ylim(ax, [0 0.55]);

% 行注释：这里执行当前语句，完成这一小步处理。
yyaxis(ax, 'right');
% 行注释：这里计算或设置 p2，供后续步骤使用。
p2 = plot(ax, x, fnr, '-s', 'Color', theme.orangeRed, ...
    'MarkerFaceColor', theme.orangeRed, 'MarkerEdgeColor', 'w', ...
    'LineWidth', 2.2, 'MarkerSize', 7, 'DisplayName', "漏报率 (FNR)");
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "漏报率 (FNR)");
% 行注释：这里调整坐标轴、网格或绘图状态。
ylim(ax, [0 0.55]);

% 行注释：这里计算或设置 eerLine，供后续步骤使用。
eerLine = xline(ax, balanceX, '--', ...
    'Color', [0.18 0.18 0.20], 'LineWidth', 1.5, ...
    'HandleVisibility', 'off');
% 行注释：这里执行当前语句，完成这一小步处理。
eerLine.HandleVisibility = 'off';

% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YAxis(1).Color = theme.deepBlue;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YAxis(2).Color = theme.orangeRed;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.XTick = x;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.XTickLabel = labels;
% 行注释：这里调整坐标轴、网格或绘图状态。
xlim(ax, [0.75 height(R) + 0.25]);
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "优化迭代阶段");
% 行注释：这里执行当前语句，完成这一小步处理。
yyaxis(ax, 'left');
% 行注释：这里计算或设置 xText，供后续步骤使用。
xText = min(balanceX + 0.12, height(R) - 0.35);
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax, xText, 0.50, "等价错误率 (EER) 平衡点", ...
    'Color', [0.18 0.18 0.20], 'FontSize', 11, 'FontWeight', 'bold', ...
    'BackgroundColor', [1 1 1], 'EdgeColor', theme.lightGray, ...
    'Margin', 4);
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, [p1 p2], 'Location', 'northoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if showTitle
    % 行注释：这里给图表添加标题、标签或说明文字。
    title(ax, "误报率与漏报率权衡", 'FontWeight', 'bold');
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里给图表添加标题、标签或说明文字。
    title(ax, "错误率权衡", 'FontWeight', 'bold');
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：生成 PCA 维数和正则化参数的性能热力图。
% 行注释：这里开始定义 make_parameter_heatmaps 函数。
function make_parameter_heatmaps(valRows, figDir, pptDir, theme)
% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 1040 690]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里执行当前语句，完成这一小步处理。
draw_parameter_heatmap(ax, valRows, theme, true);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "05_主成分维度与正则化参数热力图.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：在指定坐标轴上绘制参数组合热力图。
% 行注释：这里开始定义 draw_parameter_heatmap 函数。
function draw_parameter_heatmap(ax, valRows, theme, showTitle)
% 行注释：这里计算或设置 R，供后续步骤使用。
R = valRows(string(valRows.ModelName) == "RegularizedGaussianLDA", :);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if isempty(R)
    % 行注释：这里给图表添加标题、标签或说明文字。
    text(ax, 0.5, 0.5, "没有可用的正则化贝叶斯调参结果", ...
        'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    % 行注释：这里调整坐标轴、网格或绘图状态。
    axis(ax, 'off');
    % 行注释：这里提前返回，结束当前函数的后续执行。
    return;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 dims，供后续步骤使用。
dims = unique(R.PCADim, "stable");
% 行注释：这里计算或设置 gammas，供后续步骤使用。
gammas = unique(R.Gamma, "stable");
% 行注释：这里计算或设置 f1Grid，供后续步骤使用。
f1Grid = nan(numel(dims), numel(gammas));
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for d = 1:numel(dims)
    % 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
    for g = 1:numel(gammas)
        % 行注释：这里计算或设置 idx，供后续步骤使用。
        idx = R.PCADim == dims(d) & abs(R.Gamma - gammas(g)) < 1e-12;
        % 行注释：这里计算或设置 subset，供后续步骤使用。
        subset = R(idx, :);
        % 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
        if ~isempty(subset)
            % 行注释：这里计算或设置 占位输出, bestIdx，供后续步骤使用。
            [~, bestIdx] = max(subset.f1);
            % 行注释：这里执行当前语句，完成这一小步处理。
            f1Grid(d, g) = subset.f1(bestIdx);
        % 行注释：这里结束当前的 if、for 或函数代码块。
        end
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 X, Y，供后续步骤使用。
[X, Y] = meshgrid(1:numel(gammas), 1:numel(dims));
% 行注释：这里计算或设置 Xi, Yi，供后续步骤使用。
[Xi, Yi] = meshgrid(linspace(1, numel(gammas), 240), linspace(1, numel(dims), 240));
% 行注释：这里计算或设置 Zi，供后续步骤使用。
Zi = interp2(X, Y, f1Grid, Xi, Yi, 'linear');

% 行注释：这里执行当前语句，完成这一小步处理。
contourf(ax, Xi, Yi, Zi, 28, 'LineStyle', 'none');
% 行注释：这里执行当前语句，完成这一小步处理。
shading(ax, 'interp');
% 行注释：这里执行当前语句，完成这一小步处理。
colormap(ax, blue_colormap());
% 行注释：这里计算或设置 cb，供后续步骤使用。
cb = colorbar(ax);
% 行注释：这里执行当前语句，完成这一小步处理。
cb.Box = 'off';
% 行注释：这里执行当前语句，完成这一小步处理。
cb.Label.String = "F1得分";
% 行注释：这里执行当前语句，完成这一小步处理。
cb.Label.FontName = theme.font;
% 行注释：这里执行当前语句，完成这一小步处理。
cb.Label.FontSize = 12;
% 行注释：这里执行当前语句，完成这一小步处理。
clim(ax, [max(0, min(f1Grid(:), [], 'omitnan') - 0.03), 1.0]);

% 行注释：这里计算或设置 bestValue, bestLinearIdx，供后续步骤使用。
[bestValue, bestLinearIdx] = max(f1Grid(:), [], 'omitnan');
% 行注释：这里计算或设置 bestDimIdx, bestGammaIdx，供后续步骤使用。
[bestDimIdx, bestGammaIdx] = ind2sub(size(f1Grid), bestLinearIdx);
% 行注释：这里执行当前语句，完成这一小步处理。
rectangle(ax, 'Position', [bestGammaIdx - 0.5, bestDimIdx - 0.5, 1, 1], ...
    'EdgeColor', theme.gold, 'LineWidth', 3.0);
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax, min(bestGammaIdx + 0.18, numel(gammas) - 0.05), ...
    max(bestDimIdx - 0.32, 0.68), sprintf("最优参数\nF1=%.3f", bestValue), ...
    'Color', theme.text, 'FontWeight', 'bold', 'FontSize', 11, ...
    'BackgroundColor', [1.00 0.96 0.84], 'EdgeColor', theme.gold, ...
    'Margin', 4);

% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
ax.XTick = 1:numel(gammas);
% 行注释：这里执行当前语句，完成这一小步处理。
ax.XTickLabel = string(gammas);
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YTick = 1:numel(dims);
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YTickLabel = string(dims);
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YDir = 'normal';
% 行注释：这里调整坐标轴、网格或绘图状态。
xlim(ax, [0.5 numel(gammas) + 0.5]);
% 行注释：这里调整坐标轴、网格或绘图状态。
ylim(ax, [0.5 numel(dims) + 0.5]);
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "正则化参数 \gamma", 'Interpreter', 'tex');
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "PCA 特征维度");
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if showTitle
    % 行注释：这里给图表添加标题、标签或说明文字。
    title(ax, "参数热力图：PCA 维度 × 正则化参数", 'FontWeight', 'bold');
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里给图表添加标题、标签或说明文字。
    title(ax, "参数热力图", 'FontWeight', 'bold');
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：生成阈值变化对召回率、误报率等指标的影响图。
% 行注释：这里开始定义 make_threshold_tradeoff 函数。
function make_threshold_tradeoff(valRows, bestSpec, figDir, pptDir, theme)
% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 760 760]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里执行当前语句，完成这一小步处理。
draw_threshold_tradeoff(ax, valRows, bestSpec, theme, true);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "06_后验概率阈值决策曲线.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：在指定坐标轴上绘制阈值权衡曲线。
% 行注释：这里开始定义 draw_threshold_tradeoff 函数。
function draw_threshold_tradeoff(ax, valRows, bestSpec, theme, showTitle)
% 行注释：这里计算或设置 R，供后续步骤使用。
R = threshold_rows(valRows, bestSpec);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if isempty(R)
    % 行注释：这里给图表添加标题、标签或说明文字。
    text(ax, 0.5, 0.5, "没有可用的阈值实验结果", ...
        'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    % 行注释：这里调整坐标轴、网格或绘图状态。
    axis(ax, 'off');
    % 行注释：这里提前返回，结束当前函数的后续执行。
    return;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 x，供后续步骤使用。
x = R.Threshold(:);
% 行注释：这里计算或设置 precision，供后续步骤使用。
precision = R.precision(:);
% 行注释：这里计算或设置 recall，供后续步骤使用。
recall = R.recall(:);
% 行注释：这里计算或设置 f1，供后续步骤使用。
f1 = R.f1(:);
% 行注释：这里计算或设置 upper，供后续步骤使用。
upper = max(precision, recall);
% 行注释：这里计算或设置 lower，供后续步骤使用。
lower = min(precision, recall);

% 行注释：这里调整坐标轴、网格或绘图状态。
hold(ax, 'on');
% 行注释：这里执行当前语句，完成这一小步处理。
fill(ax, [x; flipud(x)], [upper; flipud(lower)], [0.72 0.72 0.74], ...
    'FaceAlpha', 0.22, 'EdgeColor', 'none', 'HandleVisibility', 'off');
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, precision, '-o', 'Color', theme.deepBlue, ...
    'MarkerFaceColor', theme.deepBlue, 'MarkerEdgeColor', 'w', ...
    'LineWidth', 2.0, 'DisplayName', "精确率");
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, recall, '-s', 'Color', theme.orangeRed, ...
    'MarkerFaceColor', theme.orangeRed, 'MarkerEdgeColor', 'w', ...
    'LineWidth', 2.0, 'DisplayName', "召回率");
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, f1, '-^', 'Color', theme.darkRed, ...
    'MarkerFaceColor', theme.darkRed, 'MarkerEdgeColor', 'w', ...
    'LineWidth', 2.2, 'DisplayName', "F1值");

% 行注释：这里计算或设置 占位输出, bestIdx，供后续步骤使用。
[~, bestIdx] = max(f1);
% 行注释：这里计算或设置 bestThreshold，供后续步骤使用。
bestThreshold = x(bestIdx);
% 行注释：这里计算或设置 bestLine，供后续步骤使用。
bestLine = xline(ax, bestThreshold, '--', ...
    'Color', theme.darkRed, 'LineWidth', 2.0, ...
    'HandleVisibility', 'off');
% 行注释：这里执行当前语句，完成这一小步处理。
bestLine.HandleVisibility = 'off';
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax, min(bestThreshold + 0.025, 0.82), 0.93, "推荐决策阈值", ...
    'Color', theme.darkRed, 'FontSize', 11, 'FontWeight', 'bold', ...
    'BackgroundColor', [1 1 1], 'Margin', 4);

% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax, theme);
% 行注释：这里调整坐标轴、网格或绘图状态。
axis(ax, [0 1 0 1]);
% 行注释：这里调整坐标轴、网格或绘图状态。
axis(ax, 'square');
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "后验概率分类阈值");
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "指标得分");
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, 'Location', 'southoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if showTitle
    % 行注释：这里给图表添加标题、标签或说明文字。
    title(ax, "阈值决策曲线：精确率、召回率与 F1 权衡", 'FontWeight', 'bold');
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里给图表添加标题、标签或说明文字。
    title(ax, "阈值权衡", 'FontWeight', 'bold');
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：绘制后验概率分布与风险解释图。
% 行注释：这里开始定义 make_posterior_density_risk 函数。
function make_posterior_density_risk(S, B, figDir, pptDir, theme)
% 行注释：这里计算或设置 testMask，供后续步骤使用。
testMask = string(S.Split) == "test";
% 行注释：这里计算或设置 X，供后续步骤使用。
X = double(S.X(testMask, :));
% 行注释：这里计算或设置 Y，供后续步骤使用。
Y = categorical(string(S.Y(testMask)), ["normal", "anomaly"]);

% 行注释：这里计算或设置 XZ，供后续步骤使用。
XZ = (X - B.prepBase.mu) ./ B.prepBase.sigma;
% 行注释：这里执行当前语句，完成这一小步处理。
XZ(~isfinite(XZ)) = 0;
% 行注释：这里计算或设置 XP，供后续步骤使用。
XP = XZ * B.prep.coeff(:, 1:B.prep.pcaDim);
% 行注释：这里用训练好的模型预测标签或概率分数。
[~, score] = predict(B.bestModel, XP);
% 行注释：这里计算或设置 scoreAnomaly，供后续步骤使用。
scoreAnomaly = positive_score(B.bestModel, score);
% 行注释：这里计算或设置 scoreAnomaly，供后续步骤使用。
scoreAnomaly = max(0, min(1, scoreAnomaly));

% 行注释：这里计算或设置 normalScores，供后续步骤使用。
normalScores = scoreAnomaly(Y == "normal");
% 行注释：这里计算或设置 anomalyScores，供后续步骤使用。
anomalyScores = scoreAnomaly(Y == "anomaly");
% 行注释：这里计算或设置 x，供后续步骤使用。
x = linspace(0, 1, 500);

% 行注释：这里计算或设置 pdfNormal，供后续步骤使用。
pdfNormal = posterior_density(normalScores, x);
% 行注释：这里计算或设置 pdfAnomaly，供后续步骤使用。
pdfAnomaly = posterior_density(anomalyScores, x);
% 行注释：这里计算或设置 densityNormal，供后续步骤使用。
densityNormal = pdfNormal ./ max(pdfNormal);
% 行注释：这里计算或设置 densityAnomaly，供后续步骤使用。
densityAnomaly = pdfAnomaly ./ max(pdfAnomaly);
% 行注释：这里执行当前语句，完成这一小步处理。
densityNormal(~isfinite(densityNormal)) = 0;
% 行注释：这里执行当前语句，完成这一小步处理。
densityAnomaly(~isfinite(densityAnomaly)) = 0;
% 行注释：这里计算或设置 overlapPdf，供后续步骤使用。
overlapPdf = min(densityNormal, densityAnomaly);

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 1160 660]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里调整坐标轴、网格或绘图状态。
hold(ax, 'on');

% 行注释：这里执行当前语句，完成这一小步处理。
fill(ax, [x, fliplr(x)], [densityNormal, zeros(size(densityNormal))], ...
    theme.deepBlue, 'FaceAlpha', 0.18, 'EdgeColor', 'none', ...
    'DisplayName', "正常样本后验密度");
% 行注释：这里执行当前语句，完成这一小步处理。
fill(ax, [x, fliplr(x)], [densityAnomaly, zeros(size(densityAnomaly))], ...
    theme.orangeRed, 'FaceAlpha', 0.20, 'EdgeColor', 'none', ...
    'DisplayName', "缺陷样本后验密度");
% 行注释：这里执行当前语句，完成这一小步处理。
area(ax, x, overlapPdf, 'FaceColor', [0.42 0.43 0.46], ...
    'FaceAlpha', 0.42, 'EdgeColor', 'none', ...
    'DisplayName', "重叠区域 / 期望误差");

% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, densityNormal, 'Color', theme.deepBlue, 'LineWidth', 2.4, ...
    'HandleVisibility', 'off');
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, densityAnomaly, 'Color', theme.orangeRed, 'LineWidth', 2.4, ...
    'HandleVisibility', 'off');

% 行注释：这里计算或设置 threshold，供后续步骤使用。
threshold = B.bestSpec.Threshold;
% 行注释：这里计算或设置 db，供后续步骤使用。
db = xline(ax, threshold, '--', "决策阈值  T = " + string(threshold), ...
    'Color', theme.darkRed, 'LineWidth', 2.0);
% 行注释：这里执行当前语句，完成这一小步处理。
db.LabelVerticalAlignment = 'middle';
% 行注释：这里执行当前语句，完成这一小步处理。
db.LabelHorizontalAlignment = 'left';
% 行注释：这里执行当前语句，完成这一小步处理。
db.FontWeight = 'bold';
% 行注释：这里执行当前语句，完成这一小步处理。
db.HandleVisibility = 'off';

% 行注释：这里计算或设置 maxOverlap, maxIdx，供后续步骤使用。
[maxOverlap, maxIdx] = max(overlapPdf);
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax, x(maxIdx) + 0.02, maxOverlap * 1.12, ...
    "贝叶斯误差风险区", 'Color', theme.text, ...
    'FontSize', 12, 'FontWeight', 'bold');
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax, 0.05, 0.92, "判为正常区域", 'Color', theme.deepBlue, ...
    'FontWeight', 'bold', 'FontSize', 12);
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax, min(0.78, threshold + 0.07), 0.78, "判为缺陷区域", ...
    'Color', theme.orangeRed, 'FontWeight', 'bold', 'FontSize', 12);

% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax, theme);
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "后验概率  P(缺陷 | x)");
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "归一化密度");
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax, "后验概率分布、决策阈值与误判重叠区", 'FontWeight', 'bold');
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, 'Location', 'northoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
% 行注释：这里调整坐标轴、网格或绘图状态。
xlim(ax, [0 1]);
% 行注释：这里调整坐标轴、网格或绘图状态。
ylim(ax, [0 1.18]);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "07_后验概率分布与误判风险.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：生成汇总仪表盘，把关键指标和结论放在一张图里。
% 行注释：这里开始定义 make_summary_dashboard 函数。
function make_summary_dashboard(R, valRows, bestSpec, figDir, pptDir, theme)
% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 1450 900]);
% 行注释：这里计算或设置 t，供后续步骤使用。
t = tiledlayout(fig, 2, 2, 'TileSpacing', 'compact', 'Padding', 'compact');

% 行注释：这里计算或设置 ax1，供后续步骤使用。
ax1 = nexttile(t, 1);
% 行注释：这里执行当前语句，完成这一小步处理。
draw_metrics_vertical(ax1, R, theme, false);

% 行注释：这里计算或设置 ax2，供后续步骤使用。
ax2 = nexttile(t, 2);
% 行注释：这里执行当前语句，完成这一小步处理。
draw_threshold_tradeoff(ax2, valRows, bestSpec, theme, false);

% 行注释：这里计算或设置 ax3，供后续步骤使用。
ax3 = nexttile(t, 3);
% 行注释：这里执行当前语句，完成这一小步处理。
draw_parameter_heatmap(ax3, valRows, theme, false);

% 行注释：这里计算或设置 ax4，供后续步骤使用。
ax4 = nexttile(t, 4);
% 行注释：这里执行当前语句，完成这一小步处理。
draw_metrics_horizontal(ax4, R, theme, false);

% 行注释：这里执行当前语句，完成这一小步处理。
sgtitle(fig, "基于贝叶斯优化的 PCB 缺陷检测系统性能评估", ...
    'FontWeight', 'bold', 'FontSize', 21, 'Color', theme.text, ...
    'FontName', theme.font);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "08_贝叶斯优化性能评估仪表盘.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：把一组阈值逐个试一遍，记录每个阈值对应的评价结果。
% 行注释：这里开始定义 threshold_rows 函数。
function R = threshold_rows(valRows, bestSpec)
% 行注释：这里计算或设置 mask，供后续步骤使用。
mask = string(valRows.ModelName) == string(bestSpec.ModelName) & valRows.PCADim == bestSpec.PCADim;
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if isnan(bestSpec.Gamma)
    % 行注释：这里计算或设置 mask，供后续步骤使用。
    mask = mask & isnan(valRows.Gamma);
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里计算或设置 mask，供后续步骤使用。
    mask = mask & abs(valRows.Gamma - bestSpec.Gamma) < 1e-12;
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里计算或设置 R，供后续步骤使用。
R = sortrows(valRows(mask, :), "Threshold");
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：用样本分数估计概率密度，用于展示后验分布形状。
% 行注释：这里开始定义 posterior_density 函数。
function density = posterior_density(samples, x)
% 行注释：这里计算或设置 samples，供后续步骤使用。
samples = samples(:);
% 行注释：这里计算或设置 samples，供后续步骤使用。
samples = samples(isfinite(samples));
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if numel(samples) < 3 || numel(unique(samples)) < 2
    % 行注释：这里计算或设置 mu，供后续步骤使用。
    mu = mean(samples, 'omitnan');
    % 行注释：这里计算或设置 sigma，供后续步骤使用。
    sigma = max(std(samples, 0, 'omitnan'), 0.05);
    % 行注释：这里计算或设置 density，供后续步骤使用。
    density = normpdf(x, mu, sigma);
    % 行注释：这里提前返回，结束当前函数的后续执行。
    return;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里开始尝试执行可能出错的代码。
try
    % 行注释：这里计算或设置 density，供后续步骤使用。
    density = ksdensity(samples, x, 'Support', [0 1], ...
        'BoundaryCorrection', 'reflection');
% 行注释：如果 try 中出错，这里负责兜底处理。
catch
    % 行注释：这里计算或设置 density，供后续步骤使用。
    density = ksdensity(samples, x);
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里执行当前语句，完成这一小步处理。
density(~isfinite(density)) = 0;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：从模型输出的多列概率中取出“缺陷”这一类的概率。
% 行注释：这里开始定义 positive_score 函数。
function scoreAnomaly = positive_score(model, score)
% 行注释：这里计算或设置 classNames，供后续步骤使用。
classNames = string(model.ClassNames);
% 行注释：这里计算或设置 posCol，供后续步骤使用。
posCol = find(classNames == "anomaly", 1);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if isempty(posCol)
    % 行注释：这里执行当前语句，完成这一小步处理。
    error("The model does not contain an anomaly class.");
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里计算或设置 scoreAnomaly，供后续步骤使用。
scoreAnomaly = score(:, posCol);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：寻找误报率和漏检率接近平衡的位置。
% 行注释：这里开始定义 find_balance_x 函数。
function xBalance = find_balance_x(x, fpr, fnr)
% 行注释：这里计算或设置 diffValue，供后续步骤使用。
diffValue = fpr - fnr;
% 行注释：这里计算或设置 crossIdx，供后续步骤使用。
crossIdx = find(diffValue(1:end-1) .* diffValue(2:end) <= 0, 1);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if ~isempty(crossIdx)
    % 行注释：这里计算或设置 x1，供后续步骤使用。
    x1 = x(crossIdx);
    % 行注释：这里计算或设置 x2，供后续步骤使用。
    x2 = x(crossIdx + 1);
    % 行注释：这里计算或设置 d1，供后续步骤使用。
    d1 = diffValue(crossIdx);
    % 行注释：这里计算或设置 d2，供后续步骤使用。
    d2 = diffValue(crossIdx + 1);
    % 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
    if abs(d2 - d1) < eps
        % 行注释：这里计算或设置 xBalance，供后续步骤使用。
        xBalance = x1;
    % 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
    else
        % 行注释：这里计算或设置 xBalance，供后续步骤使用。
        xBalance = x1 + (0 - d1) * (x2 - x1) / (d2 - d1);
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里计算或设置 占位输出, idx，供后续步骤使用。
    [~, idx] = min(abs(diffValue));
    % 行注释：这里计算或设置 xBalance，供后续步骤使用。
    xBalance = x(idx);
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：统一设置图表坐标轴的视觉样式。
% 行注释：这里开始定义 style_axes 函数。
function style_axes(ax, theme)
% 行注释：这里执行当前语句，完成这一小步处理。
ax.Color = theme.panel;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.FontName = theme.font;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.FontSize = 12;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.LineWidth = 1.0;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.XColor = theme.text;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YColor = theme.text;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.GridColor = theme.grid;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.GridAlpha = 0.35;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.MinorGridAlpha = 0.15;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.TickDir = 'out';
% 行注释：这里执行当前语句，完成这一小步处理。
ax.Layer = 'top';
% 行注释：这里调整坐标轴、网格或绘图状态。
grid(ax, 'off');
% 行注释：这里执行当前语句，完成这一小步处理。
box(ax, 'off');
% 行注释：这里执行当前语句，完成这一小步处理。
set(ax, 'LooseInset', get(ax, 'TightInset'));
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：给横向柱状图添加数值标签。
% 行注释：这里开始定义 annotate_barh_values 函数。
function annotate_barh_values(~, bars, decimals)
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(bars)
    % 行注释：这里计算或设置 xtips，供后续步骤使用。
    xtips = bars(i).YEndPoints;
    % 行注释：这里计算或设置 ytips，供后续步骤使用。
    ytips = bars(i).XEndPoints;
    % 行注释：这里计算或设置 values，供后续步骤使用。
    values = bars(i).YData;
    % 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
    for j = 1:numel(values)
        % 行注释：这里给图表添加标题、标签或说明文字。
        text(xtips(j) + 0.014, ytips(j), sprintf("%.*f", decimals, values(j)), ...
            'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle', ...
            'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.14 0.16 0.20]);
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：给柱状图添加数值标签。
% 行注释：这里开始定义 add_bar_labels 函数。
function add_bar_labels(~, bars, decimals)
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(bars)
    % 行注释：这里计算或设置 xtips，供后续步骤使用。
    xtips = bars(i).XEndPoints;
    % 行注释：这里计算或设置 ytips，供后续步骤使用。
    ytips = bars(i).YEndPoints;
    % 行注释：这里计算或设置 values，供后续步骤使用。
    values = bars(i).YData;
    % 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
    for j = 1:numel(values)
        % 行注释：这里给图表添加标题、标签或说明文字。
        text(xtips(j), ytips(j), sprintf("%.*f", decimals, values(j)), ...
            'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', ...
            'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.12 0.14 0.18]);
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：生成蓝色渐变色图，用于热力图。
% 行注释：这里开始定义 blue_colormap 函数。
function cmap = blue_colormap()
% 行注释：这里计算或设置 anchors，供后续步骤使用。
anchors = [
    % 行注释：这里执行当前语句，完成这一小步处理。
    1.00 1.00 1.00
    % 行注释：这里执行当前语句，完成这一小步处理。
    0.82 0.91 0.97
    % 行注释：这里执行当前语句，完成这一小步处理。
    0.48 0.70 0.86
    % 行注释：这里执行当前语句，完成这一小步处理。
    0.16 0.42 0.66
    % 行注释：这里执行当前语句，完成这一小步处理。
    0.00 0.18 0.36
% 行注释：这里结束当前多行参数、列表或结构。
];
% 行注释：这里计算或设置 x，供后续步骤使用。
x = linspace(0, 1, size(anchors, 1));
% 行注释：这里计算或设置 xi，供后续步骤使用。
xi = linspace(0, 1, 256);
% 行注释：这里计算或设置 cmap，供后续步骤使用。
cmap = interp1(x, anchors, xi);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：把十六进制颜色转换成绘图函数需要的 RGB 数值。
% 行注释：这里开始定义 hex2rgb 函数。
function rgb = hex2rgb(hex)
% 行注释：这里计算或设置 hex，供后续步骤使用。
hex = erase(string(hex), "#");
% 行注释：这里计算或设置 rgb，供后续步骤使用。
rgb = sscanf(hex, "%2x%2x%2x", [1 3]) / 255;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：把同一张图同时保存到结果目录和 PPT 素材目录。
% 行注释：这里开始定义 export_to_both 函数。
function export_to_both(fig, figDir, pptDir, fileName)
% 行注释：这里执行当前语句，完成这一小步处理。
hide_axes_toolbars(fig);
% 行注释：这里执行当前语句，完成这一小步处理。
exportgraphics(fig, fullfile(figDir, fileName), 'Resolution', 300);
% 行注释：这里执行当前语句，完成这一小步处理。
exportgraphics(fig, fullfile(pptDir, fileName), 'Resolution', 300);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：隐藏 MATLAB 图窗工具条，让导出的图片更干净。
% 行注释：这里开始定义 hide_axes_toolbars 函数。
function hide_axes_toolbars(fig)
% 行注释：这里计算或设置 axesList，供后续步骤使用。
axesList = findall(fig, 'Type', 'axes');
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(axesList)
    % 行注释：这里开始尝试执行可能出错的代码。
    try
        % 行注释：这里执行当前语句，完成这一小步处理。
        axesList(i).Toolbar.Visible = 'off';
    % 行注释：如果 try 中出错，这里负责兜底处理。
    catch
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
    % 行注释：这里开始尝试执行可能出错的代码。
    try
        % 行注释：这里执行当前语句，完成这一小步处理。
        disableDefaultInteractivity(axesList(i));
    % 行注释：如果 try 中出错，这里负责兜底处理。
    catch
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end
