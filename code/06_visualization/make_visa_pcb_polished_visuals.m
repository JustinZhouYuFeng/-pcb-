function make_visa_pcb_polished_visuals(featuresFile, bayesResultsFile, optimizationResultsFile, cfg)
%MAKE_VISA_PCB_POLISHED_VISUALS Create Chinese PPT-ready comparison figures.

S = load(featuresFile);
B = load(bayesResultsFile);
O = load(optimizationResultsFile);

figDir = fullfile(cfg.projectRoot, "results", "figures");
pptDir = fullfile(cfg.projectRoot, "ppt_materials", "visa_pcb", "polished");
ensure_dir(figDir);
ensure_dir(pptDir);

theme = pcb_theme();
setup_chinese_style(theme);

make_polished_dataset_overview(S, figDir, pptDir, theme);
make_feature_extraction_pipeline(S, figDir, pptDir, theme);
make_metrics_horizontal(O.rows, figDir, pptDir, theme);
make_metrics_vertical(O.rows, figDir, pptDir, theme);
make_error_tradeoff(O.rows, figDir, pptDir, theme);
make_parameter_heatmaps(B.valRows, figDir, pptDir, theme);
make_threshold_tradeoff(B.valRows, B.bestSpec, figDir, pptDir, theme);
make_posterior_density_risk(S, B, figDir, pptDir, theme);
make_summary_dashboard(O.rows, B.valRows, B.bestSpec, figDir, pptDir, theme);

fprintf("Polished Chinese figures saved to: %s\n", pptDir);
end

function theme = pcb_theme()
theme.font = 'Microsoft YaHei';
theme.bg = [1 1 1];
theme.panel = [1 1 1];
theme.text = [0.10 0.12 0.16];
theme.muted = [0.45 0.48 0.54];
theme.grid = [0.90 0.91 0.93];
theme.deepBlue = hex2rgb("#004488");
theme.blue = hex2rgb("#2E5A88");
theme.lightBlue = [0.72 0.84 0.93];
theme.gray = hex2rgb("#CCCCCC");
theme.lightGray = [0.91 0.92 0.94];
theme.orange = hex2rgb("#D95319");
theme.orangeRed = hex2rgb("#E4572E");
theme.darkRed = hex2rgb("#B22222");
theme.gold = [0.96 0.68 0.16];
theme.green = [0.20 0.56 0.36];
end

function setup_chinese_style(theme)
set(groot, 'DefaultAxesFontName', theme.font);
set(groot, 'DefaultTextFontName', theme.font);
set(groot, 'DefaultLegendFontName', theme.font);
set(groot, 'DefaultColorbarFontName', theme.font);
set(groot, 'DefaultAxesTickDir', 'out');
set(groot, 'DefaultFigureColor', theme.bg);
end

function make_polished_dataset_overview(S, figDir, pptDir, theme)
T = table(string(S.PCBSubset), categorical(string(S.Y), ["normal", "anomaly"]), ...
    'VariableNames', {'PCBSubset', 'Label'});
G = groupsummary(T, ["PCBSubset", "Label"]);

subsets = unique(string(G.PCBSubset), "stable");
normalCounts = zeros(numel(subsets), 1);
anomalyCounts = zeros(numel(subsets), 1);
for i = 1:numel(subsets)
    normalCounts(i) = G.GroupCount(G.PCBSubset == subsets(i) & G.Label == "normal");
    anomalyCounts(i) = G.GroupCount(G.PCBSubset == subsets(i) & G.Label == "anomaly");
end

fig = figure('Color', theme.bg, 'Position', [100 100 1180 620]);
ax = axes(fig);
b = bar(ax, categorical(subsets), [normalCounts, anomalyCounts], 'grouped', 'BarWidth', 0.72);
b(1).FaceColor = theme.deepBlue;
b(2).FaceColor = theme.orangeRed;
style_axes(ax, theme);
ylabel(ax, "图像数量");
title(ax, "VisA 真实 PCB 数据集样本组成", 'FontWeight', 'bold');
legend(ax, ["正常样本", "缺陷样本"], 'Location', 'northoutside', ...
    'Orientation', 'horizontal', 'Box', 'off', 'FontSize', 12);
ylim(ax, [0 max(normalCounts) * 1.18]);
add_bar_labels(ax, b, 0);
export_to_both(fig, figDir, pptDir, "01_数据集样本组成.png");
close(fig);
end

function make_feature_extraction_pipeline(S, figDir, pptDir, theme)
idx = select_feature_sample(S);
raw = imread(S.ImagePath(idx));
if size(raw, 3) == 1
    raw = repmat(raw, 1, 1, 3);
end

img = im2double(imresize(raw, [256 256]));
gray = rgb2gray(img);
grayEq = adapthisteq(gray);
edgeMap = edge(grayEq, "Canny");
gradMag = imgradient(grayEq);
gradMag = mat2gray(gradMag);

featureVector = double(S.X(idx, :));
featureNames = string(S.featureNames(:));
groupNames = ["颜色统计", "灰度统计", "边缘密度", "GLCM纹理", "LBP纹理", "HOG梯度"];
groupDims = [36, 8, 2, 4, 944, 324];
groupColors = [
    theme.deepBlue
    theme.lightBlue
    theme.green
    theme.gold
    theme.orangeRed
    theme.darkRed
];

fig = figure('Color', theme.bg, 'Position', [80 60 1600 980]);
tiledlayout(fig, 3, 4, 'TileSpacing', 'compact', 'Padding', 'compact');

ax1 = nexttile(1);
imshow(raw, 'Parent', ax1);
title(ax1, "1 原始彩色图像", 'FontWeight', 'bold', 'Color', theme.text);

ax2 = nexttile(2);
imshow(img, 'Parent', ax2);
title(ax2, "2 尺寸统一 256×256", 'FontWeight', 'bold', 'Color', theme.text);

ax3 = nexttile(3);
imshow(grayEq, 'Parent', ax3);
title(ax3, "3 灰度增强", 'FontWeight', 'bold', 'Color', theme.text);

ax4 = nexttile(4);
imshow(edgeMap, 'Parent', ax4);
title(ax4, "4 Canny 边缘响应", 'FontWeight', 'bold', 'Color', theme.text);

ax5 = nexttile(5, [1 2]);
b = barh(ax5, 1:numel(groupNames), groupDims, 0.62);
b.FaceColor = 'flat';
b.CData = groupColors;
b.EdgeColor = 'none';
style_axes(ax5, theme);
ax5.YDir = 'reverse';
ax5.YTick = 1:numel(groupNames);
ax5.YTickLabel = groupNames;
xlabel(ax5, "维度数量");
title(ax5, "5 六类手工特征组成（共 1318 维）", 'FontWeight', 'bold');
xlim(ax5, [0 1020]);
for i = 1:numel(groupDims)
    text(ax5, groupDims(i) + 18, i, string(groupDims(i)) + "维", ...
        'VerticalAlignment', 'middle', 'FontWeight', 'bold', ...
        'Color', theme.text, 'FontSize', 11);
end

ax6 = nexttile(7, [1 2]);
displayVec = normalize_vector_for_display(featureVector);
imagesc(ax6, repmat(displayVec, 24, 1), [0 1]);
colormap(ax6, blue_colormap());
style_axes(ax6, theme);
ax6.YTick = [];
ax6.XTick = [1, 50, 994, 1318];
ax6.XTickLabel = ["1", "50", "994", "1318"];
xlabel(ax6, "特征编号");
title(ax6, "6 当前图像的 1318 维特征向量可视化", 'FontWeight', 'bold');
boundaries = cumsum(groupDims);
for i = 1:numel(boundaries)-1
    xline(ax6, boundaries(i) + 0.5, '-', 'Color', [1 1 1], ...
        'LineWidth', 1.4, 'HandleVisibility', 'off');
end
text(ax6, 25, -2.2, "统计特征 50维", ...
    'HorizontalAlignment', 'center', 'FontSize', 10, ...
    'FontWeight', 'bold', 'Color', theme.text, 'Clipping', 'off');
text(ax6, 522, -2.2, "LBP纹理 944维", ...
    'HorizontalAlignment', 'center', 'FontSize', 10, ...
    'FontWeight', 'bold', 'Color', theme.text, 'Clipping', 'off');
text(ax6, 1156, -2.2, "HOG梯度 324维", ...
    'HorizontalAlignment', 'center', 'FontSize', 10, ...
    'FontWeight', 'bold', 'Color', theme.text, 'Clipping', 'off');

ax7 = nexttile(9, [1 2]);
axis(ax7, 'off');
labelText = label_to_chinese_single(string(S.Y(idx)));
sampleText = strjoin([
    "7 输出形式：特征矩阵 X"
    ""
    "X 的大小：" + string(size(S.X, 1)) + " × " + string(size(S.X, 2))
    "第 i 行：第 i 张电路板图像"
    "第 j 列：第 j 个手工特征"
    "当前示例：" + labelText + " / " + string(S.PCBSubset(idx))
    ""
    "同时保存：标签 Y、数据划分 Split、图像路径 ImagePath"
], newline);
text(ax7, 0.02, 0.92, sampleText, 'Units', 'normalized', ...
    'VerticalAlignment', 'top', 'FontName', theme.font, ...
    'FontSize', 14, 'FontWeight', 'bold', 'Color', theme.text, ...
    'BackgroundColor', [0.97 0.98 1.00], 'EdgeColor', theme.lightGray, ...
    'Margin', 12, 'Interpreter', 'none');

ax8 = nexttile(11, [1 2]);
axis(ax8, 'off');
exampleText = strjoin([
    "8 单个特征值示例"
    ""
    "红色通道均值 rgb_r_mean：" + format_value(feature_value(featureVector, featureNames, "rgb_r_mean"))
    "灰度熵 gray_entropy：" + format_value(feature_value(featureVector, featureNames, "gray_entropy"))
    "Canny 边缘密度：" + format_value(feature_value(featureVector, featureNames, "edge_density_canny"))
    "GLCM 对比度：" + format_value(feature_value(featureVector, featureNames, "glcm_contrast"))
    ""
    "这些数值共同组成一行 1318 维向量，随后进入标准化、PCA 与贝叶斯建模。"
], newline);
text(ax8, 0.02, 0.92, exampleText, 'Units', 'normalized', ...
    'VerticalAlignment', 'top', 'FontName', theme.font, ...
    'FontSize', 14, 'FontWeight', 'bold', 'Color', theme.text, ...
    'BackgroundColor', [1.00 0.98 0.93], 'EdgeColor', theme.gold, ...
    'Margin', 12, 'Interpreter', 'none');

sgtitle(fig, "电路板图像从原始图片到 1318 维特征数据的转换过程", ...
    'FontWeight', 'bold', 'FontSize', 22, 'Color', theme.text, ...
    'FontName', theme.font);
export_to_both(fig, figDir, pptDir, "12_图像特征提取过程可视化.png");
close(fig);
end

function idx = select_feature_sample(S)
candidateIdx = [find(string(S.Y) == "anomaly"); find(string(S.Y) == "normal")];
for i = 1:numel(candidateIdx)
    try
        imread(S.ImagePath(candidateIdx(i)));
        idx = candidateIdx(i);
        return;
    catch
    end
end
error("No readable sample image found for feature visualization.");
end

function displayVec = normalize_vector_for_display(featureVector)
v = double(featureVector(:)');
v(~isfinite(v)) = 0;
lo = prctile(v, 1);
hi = prctile(v, 99);
if abs(hi - lo) < eps
    displayVec = zeros(size(v));
else
    v = min(max(v, lo), hi);
    displayVec = (v - lo) ./ (hi - lo);
end
end

function value = feature_value(featureVector, featureNames, featureName)
idx = find(featureNames == string(featureName), 1);
if isempty(idx)
    value = NaN;
else
    value = featureVector(idx);
end
end

function textValue = format_value(value)
if isnan(value)
    textValue = "NaN";
else
    textValue = string(sprintf("%.4f", value));
end
end

function label = label_to_chinese_single(label)
if label == "normal"
    label = "正常样本";
elseif label == "anomaly"
    label = "缺陷样本";
end
end

function make_metrics_horizontal(R, figDir, pptDir, theme)
fig = figure('Color', theme.bg, 'Position', [100 100 1120 680]);
ax = axes(fig);
draw_metrics_horizontal(ax, R, theme, true);
export_to_both(fig, figDir, pptDir, "02_五大指标横向对比.png");
close(fig);
end

function draw_metrics_horizontal(ax, R, theme, showTitle)
metricNames = ["准确率", "精确率", "召回率", "F1值", "AUC"];
baseline = [R.TestAccuracy(1), R.TestPrecision(1), R.TestRecall(1), R.TestF1(1), R.TestAUC(1)];
optimized = [R.TestAccuracy(end), R.TestPrecision(end), R.TestRecall(end), R.TestF1(end), R.TestAUC(end)];
data = [baseline(:), optimized(:)];

b = barh(ax, data, 'grouped', 'BarWidth', 0.72);
b(1).FaceColor = theme.gray;
b(1).EdgeColor = 'none';
b(2).FaceColor = theme.deepBlue;
b(2).EdgeColor = 'none';

style_axes(ax, theme);
grid(ax, 'off');
ax.YTick = 1:numel(metricNames);
ax.YTickLabel = metricNames;
ax.YDir = 'reverse';
xlim(ax, [0 1.18]);
xlabel(ax, "指标得分");
legend(ax, ["基准模型", "优化后"], 'Location', 'southoutside', ...
    'Orientation', 'horizontal', 'Box', 'off', 'FontSize', 12);
if showTitle
    title(ax, "五大指标横向对比：基准模型 vs 优化后", 'FontWeight', 'bold');
else
    title(ax, "核心指标对比", 'FontWeight', 'bold');
end
annotate_barh_values(ax, b, 3);
end

function make_metrics_vertical(R, figDir, pptDir, theme)
fig = figure('Color', theme.bg, 'Position', [100 100 1160 650]);
ax = axes(fig);
draw_metrics_vertical(ax, R, theme, true);
export_to_both(fig, figDir, pptDir, "03_贝叶斯优化迭代趋势.png");
close(fig);
end

function draw_metrics_vertical(ax, R, theme, showTitle)
x = 1:height(R);
labels = "Bayes-" + string(0:height(R)-1);
hold(ax, 'on');

for y = 0.2:0.1:1.0
    yline(ax, y, '-', 'Color', theme.grid, 'LineWidth', 0.7, ...
        'HandleVisibility', 'off');
end

plot(ax, x, R.TestF1, '-o', 'LineWidth', 2.0, 'MarkerSize', 7, ...
    'MarkerFaceColor', theme.darkRed, 'MarkerEdgeColor', 'w', ...
    'Color', theme.darkRed, 'DisplayName', "F1值");
plot(ax, x, R.TestAUC, '--*', 'LineWidth', 2.0, 'MarkerSize', 8, ...
    'Color', theme.deepBlue, 'DisplayName', "AUC");

style_axes(ax, theme);
grid(ax, 'off');
ax.XTick = x;
ax.XTickLabel = labels;
xlabel(ax, "优化迭代阶段");
ylabel(ax, "性能得分");
ylim(ax, [0.25 0.98]);
xlim(ax, [0.75 height(R) + 0.75]);
legend(ax, 'Location', 'northoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
if showTitle
    title(ax, "纵向趋势：贝叶斯模型逐步优化", 'FontWeight', 'bold');
else
    title(ax, "优化趋势", 'FontWeight', 'bold');
end

targetX = x(end);
targetY = R.TestF1(end);
shadowText = sprintf("最终优化结果\nF1=%.3f  AUC=%.3f", R.TestF1(end), R.TestAUC(end));
text(ax, targetX - 0.02, targetY + 0.055, shadowText, ...
    'FontSize', 11, 'FontWeight', 'bold', 'Color', [0.55 0.55 0.55], ...
    'BackgroundColor', [0.74 0.74 0.74], 'Margin', 5, ...
    'HorizontalAlignment', 'right', 'Clipping', 'on');
text(ax, targetX - 0.05, targetY + 0.075, shadowText, ...
    'FontSize', 11, 'FontWeight', 'bold', 'Color', theme.text, ...
    'BackgroundColor', [1 1 1], 'EdgeColor', theme.lightGray, ...
    'LineWidth', 1.0, 'Margin', 5, 'HorizontalAlignment', 'right', ...
    'Clipping', 'on');
end

function make_error_tradeoff(R, figDir, pptDir, theme)
fig = figure('Color', theme.bg, 'Position', [100 100 1160 650]);
ax = axes(fig);
draw_error_tradeoff(ax, R, theme, true);
export_to_both(fig, figDir, pptDir, "04_误报率与漏报率权衡.png");
close(fig);
end

function draw_error_tradeoff(ax, R, theme, showTitle)
x = 1:height(R);
labels = "Bayes-" + string(0:height(R)-1);
fpr = R.TestFPR(:);
fnr = R.TestFNR(:);
balanceX = find_balance_x(x(:), fpr, fnr);

hold(ax, 'on');
yyaxis(ax, 'left');
p1 = plot(ax, x, fpr, '-o', 'Color', theme.deepBlue, ...
    'MarkerFaceColor', theme.deepBlue, 'MarkerEdgeColor', 'w', ...
    'LineWidth', 2.2, 'MarkerSize', 7, 'DisplayName', "误报率 (FPR)");
ylabel(ax, "误报率 (FPR)");
ylim(ax, [0 0.55]);

yyaxis(ax, 'right');
p2 = plot(ax, x, fnr, '-s', 'Color', theme.orangeRed, ...
    'MarkerFaceColor', theme.orangeRed, 'MarkerEdgeColor', 'w', ...
    'LineWidth', 2.2, 'MarkerSize', 7, 'DisplayName', "漏报率 (FNR)");
ylabel(ax, "漏报率 (FNR)");
ylim(ax, [0 0.55]);

eerLine = xline(ax, balanceX, '--', ...
    'Color', [0.18 0.18 0.20], 'LineWidth', 1.5, ...
    'HandleVisibility', 'off');
eerLine.HandleVisibility = 'off';

style_axes(ax, theme);
ax.YAxis(1).Color = theme.deepBlue;
ax.YAxis(2).Color = theme.orangeRed;
ax.XTick = x;
ax.XTickLabel = labels;
xlim(ax, [0.75 height(R) + 0.25]);
xlabel(ax, "优化迭代阶段");
yyaxis(ax, 'left');
xText = min(balanceX + 0.12, height(R) - 0.35);
text(ax, xText, 0.50, "等价错误率 (EER) 平衡点", ...
    'Color', [0.18 0.18 0.20], 'FontSize', 11, 'FontWeight', 'bold', ...
    'BackgroundColor', [1 1 1], 'EdgeColor', theme.lightGray, ...
    'Margin', 4);
legend(ax, [p1 p2], 'Location', 'northoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
if showTitle
    title(ax, "误报率与漏报率权衡", 'FontWeight', 'bold');
else
    title(ax, "错误率权衡", 'FontWeight', 'bold');
end
end

function make_parameter_heatmaps(valRows, figDir, pptDir, theme)
fig = figure('Color', theme.bg, 'Position', [100 100 1040 690]);
ax = axes(fig);
draw_parameter_heatmap(ax, valRows, theme, true);
export_to_both(fig, figDir, pptDir, "05_主成分维度与正则化参数热力图.png");
close(fig);
end

function draw_parameter_heatmap(ax, valRows, theme, showTitle)
R = valRows(string(valRows.ModelName) == "RegularizedGaussianLDA", :);
if isempty(R)
    text(ax, 0.5, 0.5, "没有可用的正则化贝叶斯调参结果", ...
        'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    axis(ax, 'off');
    return;
end

dims = unique(R.PCADim, "stable");
gammas = unique(R.Gamma, "stable");
f1Grid = nan(numel(dims), numel(gammas));
for d = 1:numel(dims)
    for g = 1:numel(gammas)
        idx = R.PCADim == dims(d) & abs(R.Gamma - gammas(g)) < 1e-12;
        subset = R(idx, :);
        if ~isempty(subset)
            [~, bestIdx] = max(subset.f1);
            f1Grid(d, g) = subset.f1(bestIdx);
        end
    end
end

[X, Y] = meshgrid(1:numel(gammas), 1:numel(dims));
[Xi, Yi] = meshgrid(linspace(1, numel(gammas), 240), linspace(1, numel(dims), 240));
Zi = interp2(X, Y, f1Grid, Xi, Yi, 'linear');

contourf(ax, Xi, Yi, Zi, 28, 'LineStyle', 'none');
shading(ax, 'interp');
colormap(ax, blue_colormap());
cb = colorbar(ax);
cb.Box = 'off';
cb.Label.String = "F1得分";
cb.Label.FontName = theme.font;
cb.Label.FontSize = 12;
clim(ax, [max(0, min(f1Grid(:), [], 'omitnan') - 0.03), 1.0]);

[bestValue, bestLinearIdx] = max(f1Grid(:), [], 'omitnan');
[bestDimIdx, bestGammaIdx] = ind2sub(size(f1Grid), bestLinearIdx);
rectangle(ax, 'Position', [bestGammaIdx - 0.5, bestDimIdx - 0.5, 1, 1], ...
    'EdgeColor', theme.gold, 'LineWidth', 3.0);
text(ax, min(bestGammaIdx + 0.18, numel(gammas) - 0.05), ...
    max(bestDimIdx - 0.32, 0.68), sprintf("最优参数\nF1=%.3f", bestValue), ...
    'Color', theme.text, 'FontWeight', 'bold', 'FontSize', 11, ...
    'BackgroundColor', [1.00 0.96 0.84], 'EdgeColor', theme.gold, ...
    'Margin', 4);

style_axes(ax, theme);
ax.XTick = 1:numel(gammas);
ax.XTickLabel = string(gammas);
ax.YTick = 1:numel(dims);
ax.YTickLabel = string(dims);
ax.YDir = 'normal';
xlim(ax, [0.5 numel(gammas) + 0.5]);
ylim(ax, [0.5 numel(dims) + 0.5]);
xlabel(ax, "正则化参数 \gamma", 'Interpreter', 'tex');
ylabel(ax, "PCA 特征维度");
if showTitle
    title(ax, "参数热力图：PCA 维度 × 正则化参数", 'FontWeight', 'bold');
else
    title(ax, "参数热力图", 'FontWeight', 'bold');
end
end

function make_threshold_tradeoff(valRows, bestSpec, figDir, pptDir, theme)
fig = figure('Color', theme.bg, 'Position', [100 100 760 760]);
ax = axes(fig);
draw_threshold_tradeoff(ax, valRows, bestSpec, theme, true);
export_to_both(fig, figDir, pptDir, "06_后验概率阈值决策曲线.png");
close(fig);
end

function draw_threshold_tradeoff(ax, valRows, bestSpec, theme, showTitle)
R = threshold_rows(valRows, bestSpec);
if isempty(R)
    text(ax, 0.5, 0.5, "没有可用的阈值实验结果", ...
        'HorizontalAlignment', 'center', 'FontWeight', 'bold');
    axis(ax, 'off');
    return;
end

x = R.Threshold(:);
precision = R.precision(:);
recall = R.recall(:);
f1 = R.f1(:);
upper = max(precision, recall);
lower = min(precision, recall);

hold(ax, 'on');
fill(ax, [x; flipud(x)], [upper; flipud(lower)], [0.72 0.72 0.74], ...
    'FaceAlpha', 0.22, 'EdgeColor', 'none', 'HandleVisibility', 'off');
plot(ax, x, precision, '-o', 'Color', theme.deepBlue, ...
    'MarkerFaceColor', theme.deepBlue, 'MarkerEdgeColor', 'w', ...
    'LineWidth', 2.0, 'DisplayName', "精确率");
plot(ax, x, recall, '-s', 'Color', theme.orangeRed, ...
    'MarkerFaceColor', theme.orangeRed, 'MarkerEdgeColor', 'w', ...
    'LineWidth', 2.0, 'DisplayName', "召回率");
plot(ax, x, f1, '-^', 'Color', theme.darkRed, ...
    'MarkerFaceColor', theme.darkRed, 'MarkerEdgeColor', 'w', ...
    'LineWidth', 2.2, 'DisplayName', "F1值");

[~, bestIdx] = max(f1);
bestThreshold = x(bestIdx);
bestLine = xline(ax, bestThreshold, '--', ...
    'Color', theme.darkRed, 'LineWidth', 2.0, ...
    'HandleVisibility', 'off');
bestLine.HandleVisibility = 'off';
text(ax, min(bestThreshold + 0.025, 0.82), 0.93, "推荐决策阈值", ...
    'Color', theme.darkRed, 'FontSize', 11, 'FontWeight', 'bold', ...
    'BackgroundColor', [1 1 1], 'Margin', 4);

style_axes(ax, theme);
axis(ax, [0 1 0 1]);
axis(ax, 'square');
xlabel(ax, "后验概率分类阈值");
ylabel(ax, "指标得分");
legend(ax, 'Location', 'southoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
if showTitle
    title(ax, "阈值决策曲线：精确率、召回率与 F1 权衡", 'FontWeight', 'bold');
else
    title(ax, "阈值权衡", 'FontWeight', 'bold');
end
end

function make_posterior_density_risk(S, B, figDir, pptDir, theme)
testMask = string(S.Split) == "test";
X = double(S.X(testMask, :));
Y = categorical(string(S.Y(testMask)), ["normal", "anomaly"]);

XZ = (X - B.prepBase.mu) ./ B.prepBase.sigma;
XZ(~isfinite(XZ)) = 0;
XP = XZ * B.prep.coeff(:, 1:B.prep.pcaDim);
[~, score] = predict(B.bestModel, XP);
scoreAnomaly = positive_score(B.bestModel, score);
scoreAnomaly = max(0, min(1, scoreAnomaly));

normalScores = scoreAnomaly(Y == "normal");
anomalyScores = scoreAnomaly(Y == "anomaly");
x = linspace(0, 1, 500);

pdfNormal = posterior_density(normalScores, x);
pdfAnomaly = posterior_density(anomalyScores, x);
densityNormal = pdfNormal ./ max(pdfNormal);
densityAnomaly = pdfAnomaly ./ max(pdfAnomaly);
densityNormal(~isfinite(densityNormal)) = 0;
densityAnomaly(~isfinite(densityAnomaly)) = 0;
overlapPdf = min(densityNormal, densityAnomaly);

fig = figure('Color', theme.bg, 'Position', [100 100 1160 660]);
ax = axes(fig);
hold(ax, 'on');

fill(ax, [x, fliplr(x)], [densityNormal, zeros(size(densityNormal))], ...
    theme.deepBlue, 'FaceAlpha', 0.18, 'EdgeColor', 'none', ...
    'DisplayName', "正常样本后验密度");
fill(ax, [x, fliplr(x)], [densityAnomaly, zeros(size(densityAnomaly))], ...
    theme.orangeRed, 'FaceAlpha', 0.20, 'EdgeColor', 'none', ...
    'DisplayName', "缺陷样本后验密度");
area(ax, x, overlapPdf, 'FaceColor', [0.42 0.43 0.46], ...
    'FaceAlpha', 0.42, 'EdgeColor', 'none', ...
    'DisplayName', "重叠区域 / 期望误差");

plot(ax, x, densityNormal, 'Color', theme.deepBlue, 'LineWidth', 2.4, ...
    'HandleVisibility', 'off');
plot(ax, x, densityAnomaly, 'Color', theme.orangeRed, 'LineWidth', 2.4, ...
    'HandleVisibility', 'off');

threshold = B.bestSpec.Threshold;
db = xline(ax, threshold, '--', "决策阈值  T = " + string(threshold), ...
    'Color', theme.darkRed, 'LineWidth', 2.0);
db.LabelVerticalAlignment = 'middle';
db.LabelHorizontalAlignment = 'left';
db.FontWeight = 'bold';
db.HandleVisibility = 'off';

[maxOverlap, maxIdx] = max(overlapPdf);
text(ax, x(maxIdx) + 0.02, maxOverlap * 1.12, ...
    "贝叶斯误差风险区", 'Color', theme.text, ...
    'FontSize', 12, 'FontWeight', 'bold');
text(ax, 0.05, 0.92, "判为正常区域", 'Color', theme.deepBlue, ...
    'FontWeight', 'bold', 'FontSize', 12);
text(ax, min(0.78, threshold + 0.07), 0.78, "判为缺陷区域", ...
    'Color', theme.orangeRed, 'FontWeight', 'bold', 'FontSize', 12);

style_axes(ax, theme);
xlabel(ax, "后验概率  P(缺陷 | x)");
ylabel(ax, "归一化密度");
title(ax, "后验概率分布、决策阈值与误判重叠区", 'FontWeight', 'bold');
legend(ax, 'Location', 'northoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
xlim(ax, [0 1]);
ylim(ax, [0 1.18]);
export_to_both(fig, figDir, pptDir, "07_后验概率分布与误判风险.png");
close(fig);
end

function make_summary_dashboard(R, valRows, bestSpec, figDir, pptDir, theme)
fig = figure('Color', theme.bg, 'Position', [100 100 1450 900]);
t = tiledlayout(fig, 2, 2, 'TileSpacing', 'compact', 'Padding', 'compact');

ax1 = nexttile(t, 1);
draw_metrics_vertical(ax1, R, theme, false);

ax2 = nexttile(t, 2);
draw_threshold_tradeoff(ax2, valRows, bestSpec, theme, false);

ax3 = nexttile(t, 3);
draw_parameter_heatmap(ax3, valRows, theme, false);

ax4 = nexttile(t, 4);
draw_metrics_horizontal(ax4, R, theme, false);

sgtitle(fig, "基于贝叶斯优化的 PCB 缺陷检测系统性能评估", ...
    'FontWeight', 'bold', 'FontSize', 21, 'Color', theme.text, ...
    'FontName', theme.font);
export_to_both(fig, figDir, pptDir, "08_贝叶斯优化性能评估仪表盘.png");
close(fig);
end

function R = threshold_rows(valRows, bestSpec)
mask = string(valRows.ModelName) == string(bestSpec.ModelName) & valRows.PCADim == bestSpec.PCADim;
if isnan(bestSpec.Gamma)
    mask = mask & isnan(valRows.Gamma);
else
    mask = mask & abs(valRows.Gamma - bestSpec.Gamma) < 1e-12;
end
R = sortrows(valRows(mask, :), "Threshold");
end

function density = posterior_density(samples, x)
samples = samples(:);
samples = samples(isfinite(samples));
if numel(samples) < 3 || numel(unique(samples)) < 2
    mu = mean(samples, 'omitnan');
    sigma = max(std(samples, 0, 'omitnan'), 0.05);
    density = normpdf(x, mu, sigma);
    return;
end

try
    density = ksdensity(samples, x, 'Support', [0 1], ...
        'BoundaryCorrection', 'reflection');
catch
    density = ksdensity(samples, x);
end
density(~isfinite(density)) = 0;
end

function scoreAnomaly = positive_score(model, score)
classNames = string(model.ClassNames);
posCol = find(classNames == "anomaly", 1);
if isempty(posCol)
    error("The model does not contain an anomaly class.");
end
scoreAnomaly = score(:, posCol);
end

function xBalance = find_balance_x(x, fpr, fnr)
diffValue = fpr - fnr;
crossIdx = find(diffValue(1:end-1) .* diffValue(2:end) <= 0, 1);
if ~isempty(crossIdx)
    x1 = x(crossIdx);
    x2 = x(crossIdx + 1);
    d1 = diffValue(crossIdx);
    d2 = diffValue(crossIdx + 1);
    if abs(d2 - d1) < eps
        xBalance = x1;
    else
        xBalance = x1 + (0 - d1) * (x2 - x1) / (d2 - d1);
    end
else
    [~, idx] = min(abs(diffValue));
    xBalance = x(idx);
end
end

function style_axes(ax, theme)
ax.Color = theme.panel;
ax.FontName = theme.font;
ax.FontSize = 12;
ax.LineWidth = 1.0;
ax.XColor = theme.text;
ax.YColor = theme.text;
ax.GridColor = theme.grid;
ax.GridAlpha = 0.35;
ax.MinorGridAlpha = 0.15;
ax.TickDir = 'out';
ax.Layer = 'top';
grid(ax, 'off');
box(ax, 'off');
set(ax, 'LooseInset', get(ax, 'TightInset'));
end

function annotate_barh_values(~, bars, decimals)
for i = 1:numel(bars)
    xtips = bars(i).YEndPoints;
    ytips = bars(i).XEndPoints;
    values = bars(i).YData;
    for j = 1:numel(values)
        text(xtips(j) + 0.014, ytips(j), sprintf("%.*f", decimals, values(j)), ...
            'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle', ...
            'FontSize', 10.5, 'FontWeight', 'bold', 'Color', [0.14 0.16 0.20]);
    end
end
end

function add_bar_labels(~, bars, decimals)
for i = 1:numel(bars)
    xtips = bars(i).XEndPoints;
    ytips = bars(i).YEndPoints;
    values = bars(i).YData;
    for j = 1:numel(values)
        text(xtips(j), ytips(j), sprintf("%.*f", decimals, values(j)), ...
            'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', ...
            'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.12 0.14 0.18]);
    end
end
end

function cmap = blue_colormap()
anchors = [
    1.00 1.00 1.00
    0.82 0.91 0.97
    0.48 0.70 0.86
    0.16 0.42 0.66
    0.00 0.18 0.36
];
x = linspace(0, 1, size(anchors, 1));
xi = linspace(0, 1, 256);
cmap = interp1(x, anchors, xi);
end

function rgb = hex2rgb(hex)
hex = erase(string(hex), "#");
rgb = sscanf(hex, "%2x%2x%2x", [1 3]) / 255;
end

function export_to_both(fig, figDir, pptDir, fileName)
hide_axes_toolbars(fig);
exportgraphics(fig, fullfile(figDir, fileName), 'Resolution', 300);
exportgraphics(fig, fullfile(pptDir, fileName), 'Resolution', 300);
end

function hide_axes_toolbars(fig)
axesList = findall(fig, 'Type', 'axes');
for i = 1:numel(axesList)
    try
        axesList(i).Toolbar.Visible = 'off';
    catch
    end
    try
        disableDefaultInteractivity(axesList(i));
    catch
    end
end
end
