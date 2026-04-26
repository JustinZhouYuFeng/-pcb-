function make_visa_pcb_visuals(featuresFile, bayesResultsFile, optimizationResultsFile, cfg)
%MAKE_VISA_PCB_VISUALS Generate Chinese supporting figures for the VisA PCB project.

S = load(featuresFile);
B = load(bayesResultsFile);
O = load(optimizationResultsFile);

figDir = fullfile(cfg.projectRoot, "results", "figures");
pptDir = fullfile(cfg.projectRoot, "ppt_materials", "visa_pcb");
ensure_dir(figDir);
ensure_dir(pptDir);

theme = pcb_theme_basic();
setup_chinese_style(theme);

make_dataset_count_chart(S, figDir, pptDir, theme);
make_sample_grid(S, figDir, pptDir, theme);
make_pca_scatter(S, B, figDir, pptDir, theme);
make_bayes_confusion(S, B, figDir, pptDir, theme);
make_bayes_optimization_comparison(O, figDir, pptDir, theme);
make_threshold_curve(B, figDir, pptDir, theme);
end

function theme = pcb_theme_basic()
theme.font = 'Microsoft YaHei';
theme.bg = [1 1 1];
theme.text = [0.10 0.12 0.16];
theme.grid = [0.90 0.91 0.93];
theme.deepBlue = hex2rgb("#004488");
theme.blue = hex2rgb("#2E5A88");
theme.gray = hex2rgb("#CCCCCC");
theme.orangeRed = hex2rgb("#E4572E");
theme.darkRed = hex2rgb("#B22222");
theme.green = [0.20 0.56 0.36];
theme.gold = [0.96 0.68 0.16];
theme.palette = [
    theme.deepBlue
    theme.gray
    theme.orangeRed
    theme.darkRed
    theme.green
];
end

function setup_chinese_style(theme)
set(groot, 'DefaultAxesFontName', theme.font);
set(groot, 'DefaultTextFontName', theme.font);
set(groot, 'DefaultLegendFontName', theme.font);
set(groot, 'DefaultColorbarFontName', theme.font);
set(groot, 'DefaultAxesTickDir', 'out');
end

function make_dataset_count_chart(S, figDir, pptDir, theme)
labelCn = label_to_chinese(string(S.Y));
T = table(string(S.PCBSubset), categorical(labelCn, ["正常", "缺陷"]), string(S.Split), ...
    'VariableNames', {'PCBSubset', 'Label', 'Split'});
G = groupsummary(T, ["PCBSubset", "Label"]);

fig = figure('Color', theme.bg, 'Position', [100 100 1080 560]);
ax = axes(fig);
b = bar(ax, categorical(strcat(string(G.PCBSubset), "_", string(G.Label))), G.GroupCount, 0.62);
b.FaceColor = theme.deepBlue;
b.EdgeColor = 'none';
style_axes(ax, theme);
ylabel(ax, "图像数量");
title(ax, "VisA PCB 数据集：子集与类别样本数", 'FontWeight', 'bold');
xtickangle(ax, 25);
add_vertical_bar_labels(b, 0);
export_to_both(fig, figDir, pptDir, "基础图_数据集样本统计.png");
close(fig);
end

function make_sample_grid(S, figDir, pptDir, theme)
rng(42);
subsets = ["pcb1", "pcb2", "pcb3", "pcb4"];
subsetNames = ["电路板子集 1", "电路板子集 2", "电路板子集 3", "电路板子集 4"];
columnNames = ["正常样本", "缺陷样本 1", "缺陷样本 2"];

fig = figure('Color', theme.bg, 'Position', [100 100 1280 960]);
tiledlayout(numel(subsets), 3, 'TileSpacing', 'compact', 'Padding', 'compact');
for s = 1:numel(subsets)
    subsetMask = string(S.PCBSubset) == subsets(s);
    normalIdx = find(subsetMask & string(S.Y) == "normal");
    anomalyIdx = find(subsetMask & string(S.Y) == "anomaly");

    normalPick = deterministic_pick(normalIdx, 1);
    anomalyPick = deterministic_pick(anomalyIdx, 2);
    picks = [normalPick(:); anomalyPick(:)];

    for c = 1:3
        ax = nexttile;
        if c <= numel(picks) && ~isnan(picks(c))
            imshow(imread(S.ImagePath(picks(c))), 'Parent', ax);
            if c == 1
                titleText = subsetNames(s) + "  |  " + columnNames(c);
                titleColor = theme.deepBlue;
            else
                titleText = subsetNames(s) + "  |  " + columnNames(c);
                titleColor = theme.orangeRed;
            end
            title(ax, titleText, 'Interpreter', 'none', 'FontName', theme.font, ...
                'FontSize', 11, 'FontWeight', 'bold', 'Color', titleColor);
        else
            axis(ax, 'off');
            text(ax, 0.5, 0.5, "样本不足", 'HorizontalAlignment', 'center', ...
                'FontName', theme.font, 'FontWeight', 'bold', 'Color', theme.text);
        end
    end
end
sgtitle(fig, "VisA 电路板真实图像样本预览：每类 1 张正常 + 2 张缺陷", 'FontName', theme.font, ...
    'FontWeight', 'bold', 'FontSize', 18, 'Color', theme.text);
export_to_both(fig, figDir, pptDir, "基础图_真实电路板样本预览.png");
close(fig);
end

function picked = deterministic_pick(indices, count)
if isempty(indices)
    picked = NaN(count, 1);
    return;
end
order = randperm(numel(indices), min(count, numel(indices)));
picked = indices(order);
if numel(picked) < count
    picked = [picked(:); nan(count - numel(picked), 1)];
end
end

function make_pca_scatter(S, B, figDir, pptDir, theme)
X = double(S.X);
XZ = (X - B.prepBase.mu) ./ B.prepBase.sigma;
XZ(~isfinite(XZ)) = 0;
scores = XZ * B.coeff(:, 1:2);

labels = categorical(label_to_chinese(string(S.Y)), ["正常", "缺陷"]);
sampleN = min(2500, size(scores, 1));
rng(42);
idx = randperm(size(scores, 1), sampleN);

fig = figure('Color', theme.bg, 'Position', [100 100 880 680]);
ax = axes(fig);
gscatter(scores(idx, 1), scores(idx, 2), labels(idx), ...
    [theme.deepBlue; theme.orangeRed], 'oo', 7, 'off');
style_axes(ax, theme);
xlabel(ax, "主成分特征 PC1");
ylabel(ax, "主成分特征 PC2");
title(ax, "手工特征 PCA 二维投影", 'FontWeight', 'bold');
legend(ax, ["正常样本", "缺陷样本"], 'Location', 'northoutside', ...
    'Orientation', 'horizontal', 'Box', 'off', 'FontSize', 12);
export_to_both(fig, figDir, pptDir, "基础图_主成分二维散点图.png");
close(fig);
end

function make_bayes_confusion(S, B, figDir, pptDir, theme)
testMask = string(S.Split) == "test";
X = double(S.X(testMask, :));
Y = categorical(label_to_chinese(string(S.Y(testMask))), ["正常", "缺陷"]);

XZ = (X - B.prepBase.mu) ./ B.prepBase.sigma;
XZ(~isfinite(XZ)) = 0;
XP = XZ * B.prep.coeff(:, 1:B.prep.pcaDim);
[~, score] = predict(B.bestModel, XP);
scoreAnomaly = positive_score(B.bestModel, score);

yPred = repmat("正常", numel(scoreAnomaly), 1);
yPred(scoreAnomaly >= B.bestSpec.Threshold) = "缺陷";
yPred = categorical(yPred, ["正常", "缺陷"]);

fig = figure('Color', theme.bg, 'Position', [100 100 760 640]);
confusionchart(Y, yPred, ...
    'Title', "贝叶斯决策测试集混淆矩阵", ...
    'RowSummary', 'row-normalized', ...
    'ColumnSummary', 'column-normalized');
set(findall(fig, '-property', 'FontName'), 'FontName', theme.font);
export_to_both(fig, figDir, pptDir, "基础图_贝叶斯混淆矩阵.png");
close(fig);
end

function make_bayes_optimization_comparison(O, figDir, pptDir, theme)
R = O.rows;
labels = "Bayes-" + string(0:height(R)-1);
values = [R.TestAccuracy, R.TestPrecision, R.TestRecall, R.TestF1, R.TestAUC];

fig = figure('Color', theme.bg, 'Position', [100 100 1160 720]);
ax = axes(fig);
b = barh(ax, values, 'grouped', 'BarWidth', 0.76);
for i = 1:numel(b)
    b(i).FaceColor = theme.palette(i, :);
    b(i).EdgeColor = 'none';
end
style_axes(ax, theme);
xlim(ax, [0 1.05]);
ax.YTick = 1:numel(labels);
ax.YTickLabel = labels;
ax.YDir = 'reverse';
xlabel(ax, "指标得分");
title(ax, "贝叶斯优化阶段性能对比", 'FontWeight', 'bold');
legend(ax, ["准确率", "精确率", "召回率", "F1值", "AUC"], ...
    'Location', 'southoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
export_to_both(fig, figDir, pptDir, "基础图_贝叶斯优化阶段对比.png");
close(fig);
end

function make_threshold_curve(B, figDir, pptDir, theme)
rows = B.valRows;
spec = B.bestSpec;
mask = string(rows.ModelName) == string(spec.ModelName) & rows.PCADim == spec.PCADim;
if isnan(spec.Gamma)
    mask = mask & isnan(rows.Gamma);
else
    mask = mask & abs(rows.Gamma - spec.Gamma) < 1e-12;
end
R = sortrows(rows(mask, :), "Threshold");

fig = figure('Color', theme.bg, 'Position', [100 100 900 600]);
ax = axes(fig);
hold(ax, 'on');
plot(ax, R.Threshold, R.f1, '-o', 'LineWidth', 2.0, ...
    'Color', theme.darkRed, 'MarkerFaceColor', theme.darkRed, ...
    'MarkerEdgeColor', 'w', 'DisplayName', "F1值");
plot(ax, R.Threshold, R.recall, '-s', 'LineWidth', 2.0, ...
    'Color', theme.orangeRed, 'MarkerFaceColor', theme.orangeRed, ...
    'MarkerEdgeColor', 'w', 'DisplayName', "召回率");
plot(ax, R.Threshold, R.precision, '-^', 'LineWidth', 2.0, ...
    'Color', theme.deepBlue, 'MarkerFaceColor', theme.deepBlue, ...
    'MarkerEdgeColor', 'w', 'DisplayName', "精确率");
plot(ax, R.Threshold, R.fpr, ':', 'LineWidth', 2.0, ...
    'Color', [0.42 0.42 0.46], 'DisplayName', "误报率");
style_axes(ax, theme);
xlabel(ax, "后验概率分类阈值");
ylabel(ax, "指标得分");
title(ax, "验证集后验阈值分析", 'FontWeight', 'bold');
legend(ax, 'Location', 'southoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
ylim(ax, [0 1]);
export_to_both(fig, figDir, pptDir, "基础图_后验阈值分析曲线.png");
close(fig);
end

function scoreAnomaly = positive_score(model, score)
classNames = string(model.ClassNames);
posCol = find(classNames == "anomaly", 1);
scoreAnomaly = score(:, posCol);
end

function labelCn = label_to_chinese(label)
label = string(label);
labelCn = strings(size(label));
labelCn(label == "normal") = "正常";
labelCn(label == "anomaly") = "缺陷";
labelCn(labelCn == "") = label(labelCn == "");
end

function style_axes(ax, theme)
ax.Color = theme.bg;
ax.FontName = theme.font;
ax.FontSize = 12;
ax.LineWidth = 1.0;
ax.XColor = theme.text;
ax.YColor = theme.text;
ax.GridColor = theme.grid;
ax.GridAlpha = 0.30;
ax.TickDir = 'out';
box(ax, 'off');
grid(ax, 'off');
set(ax, 'LooseInset', get(ax, 'TightInset'));
end

function add_vertical_bar_labels(bars, decimals)
xtips = bars.XEndPoints;
ytips = bars.YEndPoints;
values = bars.YData;
for i = 1:numel(values)
    text(xtips(i), ytips(i), sprintf("%.*f", decimals, values(i)), ...
        'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', ...
        'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.12 0.14 0.18]);
end
end

function rgb = hex2rgb(hex)
hex = erase(string(hex), "#");
rgb = sscanf(hex, "%2x%2x%2x", [1 3]) / 255;
end

function export_to_both(fig, figDir, pptDir, fileName)
hide_axes_toolbars(fig);
exportgraphics(fig, fullfile(figDir, fileName), 'Resolution', 260);
exportgraphics(fig, fullfile(pptDir, fileName), 'Resolution', 260);
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
