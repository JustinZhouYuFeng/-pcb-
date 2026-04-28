% 中文注释：生成 PCB 贝叶斯实验的基础可视化图表。
% 主要流程：展示数据分布、特征降维、模型指标和阈值变化趋势。
% 输出结果：用于快速检查实验是否合理，也可作为报告素材。

% 函数说明：生成基础版实验图表，方便快速检查和汇报。
% 行注释：这里开始定义 make_visa_pcb_visuals 函数。
function make_visa_pcb_visuals(featuresFile, bayesResultsFile, optimizationResultsFile, cfg)
%MAKE_VISA_PCB_VISUALS Generate Chinese supporting figures for the VisA PCB project.

% 行注释：这里从磁盘读取前面步骤保存的数据文件。
S = load(featuresFile);
% 行注释：这里从磁盘读取前面步骤保存的数据文件。
B = load(bayesResultsFile);
% 行注释：这里从磁盘读取前面步骤保存的数据文件。
O = load(optimizationResultsFile);

% 行注释：这里计算或设置 figDir，供后续步骤使用。
figDir = fullfile(cfg.projectRoot, "results", "figures");
% 行注释：这里计算或设置 pptDir，供后续步骤使用。
pptDir = fullfile(cfg.projectRoot, "ppt_materials", "visa_pcb");
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(figDir);
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(pptDir);

% 行注释：这里计算或设置 theme，供后续步骤使用。
theme = pcb_theme_basic();
% 行注释：这里执行当前语句，完成这一小步处理。
setup_chinese_style(theme);

% 行注释：这里执行当前语句，完成这一小步处理。
make_dataset_count_chart(S, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_sample_grid(S, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_pca_scatter(S, B, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_bayes_confusion(S, B, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_bayes_optimization_comparison(O, figDir, pptDir, theme);
% 行注释：这里执行当前语句，完成这一小步处理。
make_threshold_curve(B, figDir, pptDir, theme);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：定义基础版图表的颜色和字体风格。
% 行注释：这里开始定义 pcb_theme_basic 函数。
function theme = pcb_theme_basic()
% 行注释：这里执行当前语句，完成这一小步处理。
theme.font = 'Microsoft YaHei';
% 行注释：这里执行当前语句，完成这一小步处理。
theme.bg = [1 1 1];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.text = [0.10 0.12 0.16];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.grid = [0.90 0.91 0.93];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.deepBlue = hex2rgb("#004488");
% 行注释：这里执行当前语句，完成这一小步处理。
theme.blue = hex2rgb("#2E5A88");
% 行注释：这里执行当前语句，完成这一小步处理。
theme.gray = hex2rgb("#CCCCCC");
% 行注释：这里执行当前语句，完成这一小步处理。
theme.orangeRed = hex2rgb("#E4572E");
% 行注释：这里执行当前语句，完成这一小步处理。
theme.darkRed = hex2rgb("#B22222");
% 行注释：这里执行当前语句，完成这一小步处理。
theme.green = [0.20 0.56 0.36];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.gold = [0.96 0.68 0.16];
% 行注释：这里执行当前语句，完成这一小步处理。
theme.palette = [
    % 行注释：这里执行当前语句，完成这一小步处理。
    theme.deepBlue
    % 行注释：这里执行当前语句，完成这一小步处理。
    theme.gray
    % 行注释：这里执行当前语句，完成这一小步处理。
    theme.orangeRed
    % 行注释：这里执行当前语句，完成这一小步处理。
    theme.darkRed
    % 行注释：这里执行当前语句，完成这一小步处理。
    theme.green
% 行注释：这里结束当前多行参数、列表或结构。
];
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
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：绘制各 PCB 子集的样本数量统计图。
% 行注释：这里开始定义 make_dataset_count_chart 函数。
function make_dataset_count_chart(S, figDir, pptDir, theme)
% 行注释：这里计算或设置 labelCn，供后续步骤使用。
labelCn = label_to_chinese(string(S.Y));
% 行注释：这里计算或设置 T，供后续步骤使用。
T = table(string(S.PCBSubset), categorical(labelCn, ["正常", "缺陷"]), string(S.Split), ...
    'VariableNames', {'PCBSubset', 'Label', 'Split'});
% 行注释：这里计算或设置 G，供后续步骤使用。
G = groupsummary(T, ["PCBSubset", "Label"]);

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 1080 560]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里计算或设置 b，供后续步骤使用。
b = bar(ax, categorical(strcat(string(G.PCBSubset), "_", string(G.Label))), G.GroupCount, 0.62);
% 行注释：这里执行当前语句，完成这一小步处理。
b.FaceColor = theme.deepBlue;
% 行注释：这里执行当前语句，完成这一小步处理。
b.EdgeColor = 'none';
% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax, theme);
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "图像数量");
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax, "VisA PCB 数据集：子集与类别样本数", 'FontWeight', 'bold');
% 行注释：这里执行当前语句，完成这一小步处理。
xtickangle(ax, 25);
% 行注释：这里执行当前语句，完成这一小步处理。
add_vertical_bar_labels(b, 0);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "基础图_数据集样本统计.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：拼出正常和缺陷样本示例图。
% 行注释：这里开始定义 make_sample_grid 函数。
function make_sample_grid(S, figDir, pptDir, theme)
% 行注释：这里执行当前语句，完成这一小步处理。
rng(42);
% 行注释：这里计算或设置 subsets，供后续步骤使用。
subsets = ["pcb1", "pcb2", "pcb3", "pcb4"];
% 行注释：这里计算或设置 subsetNames，供后续步骤使用。
subsetNames = ["电路板子集 1", "电路板子集 2", "电路板子集 3", "电路板子集 4"];
% 行注释：这里计算或设置 columnNames，供后续步骤使用。
columnNames = ["正常样本", "缺陷样本 1", "缺陷样本 2"];

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 1280 960]);
% 行注释：这里执行当前语句，完成这一小步处理。
tiledlayout(numel(subsets), 3, 'TileSpacing', 'compact', 'Padding', 'compact');
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for s = 1:numel(subsets)
    % 行注释：这里计算或设置 subsetMask，供后续步骤使用。
    subsetMask = string(S.PCBSubset) == subsets(s);
    % 行注释：这里计算或设置 normalIdx，供后续步骤使用。
    normalIdx = find(subsetMask & string(S.Y) == "normal");
    % 行注释：这里计算或设置 anomalyIdx，供后续步骤使用。
    anomalyIdx = find(subsetMask & string(S.Y) == "anomaly");

    % 行注释：这里计算或设置 normalPick，供后续步骤使用。
    normalPick = deterministic_pick(normalIdx, 1);
    % 行注释：这里计算或设置 anomalyPick，供后续步骤使用。
    anomalyPick = deterministic_pick(anomalyIdx, 2);
    % 行注释：这里计算或设置 picks，供后续步骤使用。
    picks = [normalPick(:); anomalyPick(:)];

    % 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
    for c = 1:3
        % 行注释：这里计算或设置 ax，供后续步骤使用。
        ax = nexttile;
        % 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
        if c <= numel(picks) && ~isnan(picks(c))
            % 行注释：这里执行当前语句，完成这一小步处理。
            imshow(imread(S.ImagePath(picks(c))), 'Parent', ax);
            % 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
            if c == 1
                % 行注释：这里计算或设置 titleText，供后续步骤使用。
                titleText = subsetNames(s) + "  |  " + columnNames(c);
                % 行注释：这里计算或设置 titleColor，供后续步骤使用。
                titleColor = theme.deepBlue;
            % 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
            else
                % 行注释：这里计算或设置 titleText，供后续步骤使用。
                titleText = subsetNames(s) + "  |  " + columnNames(c);
                % 行注释：这里计算或设置 titleColor，供后续步骤使用。
                titleColor = theme.orangeRed;
            % 行注释：这里结束当前的 if、for 或函数代码块。
            end
            % 行注释：这里给图表添加标题、标签或说明文字。
            title(ax, titleText, 'Interpreter', 'none', 'FontName', theme.font, ...
                'FontSize', 11, 'FontWeight', 'bold', 'Color', titleColor);
        % 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
        else
            % 行注释：这里调整坐标轴、网格或绘图状态。
            axis(ax, 'off');
            % 行注释：这里给图表添加标题、标签或说明文字。
            text(ax, 0.5, 0.5, "样本不足", 'HorizontalAlignment', 'center', ...
                'FontName', theme.font, 'FontWeight', 'bold', 'Color', theme.text);
        % 行注释：这里结束当前的 if、for 或函数代码块。
        end
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里执行当前语句，完成这一小步处理。
sgtitle(fig, "VisA 电路板真实图像样本预览：每类 1 张正常 + 2 张缺陷", 'FontName', theme.font, ...
    'FontWeight', 'bold', 'FontSize', 18, 'Color', theme.text);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "基础图_真实电路板样本预览.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：用固定规则选样本，保证每次生成的示例图一致。
% 行注释：这里开始定义 deterministic_pick 函数。
function picked = deterministic_pick(indices, count)
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if isempty(indices)
    % 行注释：这里计算或设置 picked，供后续步骤使用。
    picked = NaN(count, 1);
    % 行注释：这里提前返回，结束当前函数的后续执行。
    return;
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里计算或设置 order，供后续步骤使用。
order = randperm(numel(indices), min(count, numel(indices)));
% 行注释：这里计算或设置 picked，供后续步骤使用。
picked = indices(order);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if numel(picked) < count
    % 行注释：这里计算或设置 picked，供后续步骤使用。
    picked = [picked(:); nan(count - numel(picked), 1)];
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：绘制 PCA 降维散点图，观察正常和缺陷样本是否可分。
% 行注释：这里开始定义 make_pca_scatter 函数。
function make_pca_scatter(S, B, figDir, pptDir, theme)
% 行注释：这里计算或设置 X，供后续步骤使用。
X = double(S.X);
% 行注释：这里计算或设置 XZ，供后续步骤使用。
XZ = (X - B.prepBase.mu) ./ B.prepBase.sigma;
% 行注释：这里执行当前语句，完成这一小步处理。
XZ(~isfinite(XZ)) = 0;
% 行注释：这里计算或设置 scores，供后续步骤使用。
scores = XZ * B.coeff(:, 1:2);

% 行注释：这里计算或设置 labels，供后续步骤使用。
labels = categorical(label_to_chinese(string(S.Y)), ["正常", "缺陷"]);
% 行注释：这里计算或设置 sampleN，供后续步骤使用。
sampleN = min(2500, size(scores, 1));
% 行注释：这里执行当前语句，完成这一小步处理。
rng(42);
% 行注释：这里计算或设置 idx，供后续步骤使用。
idx = randperm(size(scores, 1), sampleN);

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 880 680]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里执行当前语句，完成这一小步处理。
gscatter(scores(idx, 1), scores(idx, 2), labels(idx), ...
    [theme.deepBlue; theme.orangeRed], 'oo', 7, 'off');
% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax, theme);
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "主成分特征 PC1");
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "主成分特征 PC2");
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax, "手工特征 PCA 二维投影", 'FontWeight', 'bold');
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, ["正常样本", "缺陷样本"], 'Location', 'northoutside', ...
    'Orientation', 'horizontal', 'Box', 'off', 'FontSize', 12);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "基础图_主成分二维散点图.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：绘制贝叶斯模型的混淆矩阵。
% 行注释：这里开始定义 make_bayes_confusion 函数。
function make_bayes_confusion(S, B, figDir, pptDir, theme)
% 行注释：这里计算或设置 testMask，供后续步骤使用。
testMask = string(S.Split) == "test";
% 行注释：这里计算或设置 X，供后续步骤使用。
X = double(S.X(testMask, :));
% 行注释：这里计算或设置 Y，供后续步骤使用。
Y = categorical(label_to_chinese(string(S.Y(testMask))), ["正常", "缺陷"]);

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

% 行注释：这里计算或设置 yPred，供后续步骤使用。
yPred = repmat("正常", numel(scoreAnomaly), 1);
% 行注释：这里执行当前语句，完成这一小步处理。
yPred(scoreAnomaly >= B.bestSpec.Threshold) = "缺陷";
% 行注释：这里计算或设置 yPred，供后续步骤使用。
yPred = categorical(yPred, ["正常", "缺陷"]);

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 760 640]);
% 行注释：这里执行当前语句，完成这一小步处理。
confusionchart(Y, yPred, ...
    'Title', "贝叶斯决策测试集混淆矩阵", ...
    'RowSummary', 'row-normalized', ...
    'ColumnSummary', 'column-normalized');
% 行注释：这里执行当前语句，完成这一小步处理。
set(findall(fig, '-property', 'FontName'), 'FontName', theme.font);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "基础图_贝叶斯混淆矩阵.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：绘制贝叶斯不同优化阶段的指标对比图。
% 行注释：这里开始定义 make_bayes_optimization_comparison 函数。
function make_bayes_optimization_comparison(O, figDir, pptDir, theme)
% 行注释：这里计算或设置 R，供后续步骤使用。
R = O.rows;
% 行注释：这里计算或设置 labels，供后续步骤使用。
labels = "Bayes-" + string(0:height(R)-1);
% 行注释：这里计算或设置 values，供后续步骤使用。
values = [R.TestAccuracy, R.TestPrecision, R.TestRecall, R.TestF1, R.TestAUC];

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 1160 720]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里计算或设置 b，供后续步骤使用。
b = barh(ax, values, 'grouped', 'BarWidth', 0.76);
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(b)
    % 行注释：这里执行当前语句，完成这一小步处理。
    b(i).FaceColor = theme.palette(i, :);
    % 行注释：这里执行当前语句，完成这一小步处理。
    b(i).EdgeColor = 'none';
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax, theme);
% 行注释：这里调整坐标轴、网格或绘图状态。
xlim(ax, [0 1.05]);
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YTick = 1:numel(labels);
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YTickLabel = labels;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YDir = 'reverse';
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "指标得分");
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax, "贝叶斯优化阶段性能对比", 'FontWeight', 'bold');
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, ["准确率", "精确率", "召回率", "F1值", "AUC"], ...
    'Location', 'southoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "基础图_贝叶斯优化阶段对比.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：绘制阈值变化带来的性能曲线。
% 行注释：这里开始定义 make_threshold_curve 函数。
function make_threshold_curve(B, figDir, pptDir, theme)
% 行注释：这里计算或设置 rows，供后续步骤使用。
rows = B.valRows;
% 行注释：这里计算或设置 spec，供后续步骤使用。
spec = B.bestSpec;
% 行注释：这里计算或设置 mask，供后续步骤使用。
mask = string(rows.ModelName) == string(spec.ModelName) & rows.PCADim == spec.PCADim;
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if isnan(spec.Gamma)
    % 行注释：这里计算或设置 mask，供后续步骤使用。
    mask = mask & isnan(rows.Gamma);
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里计算或设置 mask，供后续步骤使用。
    mask = mask & abs(rows.Gamma - spec.Gamma) < 1e-12;
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里计算或设置 R，供后续步骤使用。
R = sortrows(rows(mask, :), "Threshold");

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', theme.bg, 'Position', [100 100 900 600]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里调整坐标轴、网格或绘图状态。
hold(ax, 'on');
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, R.Threshold, R.f1, '-o', 'LineWidth', 2.0, ...
    'Color', theme.darkRed, 'MarkerFaceColor', theme.darkRed, ...
    'MarkerEdgeColor', 'w', 'DisplayName', "F1值");
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, R.Threshold, R.recall, '-s', 'LineWidth', 2.0, ...
    'Color', theme.orangeRed, 'MarkerFaceColor', theme.orangeRed, ...
    'MarkerEdgeColor', 'w', 'DisplayName', "召回率");
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, R.Threshold, R.precision, '-^', 'LineWidth', 2.0, ...
    'Color', theme.deepBlue, 'MarkerFaceColor', theme.deepBlue, ...
    'MarkerEdgeColor', 'w', 'DisplayName', "精确率");
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, R.Threshold, R.fpr, ':', 'LineWidth', 2.0, ...
    'Color', [0.42 0.42 0.46], 'DisplayName', "误报率");
% 行注释：这里执行当前语句，完成这一小步处理。
style_axes(ax, theme);
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "后验概率分类阈值");
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "指标得分");
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax, "验证集后验阈值分析", 'FontWeight', 'bold');
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, 'Location', 'southoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'FontSize', 12);
% 行注释：这里调整坐标轴、网格或绘图状态。
ylim(ax, [0 1]);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "基础图_后验阈值分析曲线.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：从模型输出的多列概率中取出“缺陷”这一类的概率。
% 行注释：这里开始定义 positive_score 函数。
function scoreAnomaly = positive_score(model, score)
% 行注释：这里计算或设置 classNames，供后续步骤使用。
classNames = string(model.ClassNames);
% 行注释：这里计算或设置 posCol，供后续步骤使用。
posCol = find(classNames == "anomaly", 1);
% 行注释：这里计算或设置 scoreAnomaly，供后续步骤使用。
scoreAnomaly = score(:, posCol);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：把模型标签转换成中文显示。
% 行注释：这里开始定义 label_to_chinese 函数。
function labelCn = label_to_chinese(label)
% 行注释：这里计算或设置 label，供后续步骤使用。
label = string(label);
% 行注释：这里计算或设置 labelCn，供后续步骤使用。
labelCn = strings(size(label));
% 行注释：这里执行当前语句，完成这一小步处理。
labelCn(label == "normal") = "正常";
% 行注释：这里执行当前语句，完成这一小步处理。
labelCn(label == "anomaly") = "缺陷";
% 行注释：这里执行当前语句，完成这一小步处理。
labelCn(labelCn == "") = label(labelCn == "");
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：统一设置图表坐标轴的视觉样式。
% 行注释：这里开始定义 style_axes 函数。
function style_axes(ax, theme)
% 行注释：这里执行当前语句，完成这一小步处理。
ax.Color = theme.bg;
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
ax.GridAlpha = 0.30;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.TickDir = 'out';
% 行注释：这里执行当前语句，完成这一小步处理。
box(ax, 'off');
% 行注释：这里调整坐标轴、网格或绘图状态。
grid(ax, 'off');
% 行注释：这里执行当前语句，完成这一小步处理。
set(ax, 'LooseInset', get(ax, 'TightInset'));
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：给竖向柱状图添加数值标签。
% 行注释：这里开始定义 add_vertical_bar_labels 函数。
function add_vertical_bar_labels(bars, decimals)
% 行注释：这里计算或设置 xtips，供后续步骤使用。
xtips = bars.XEndPoints;
% 行注释：这里计算或设置 ytips，供后续步骤使用。
ytips = bars.YEndPoints;
% 行注释：这里计算或设置 values，供后续步骤使用。
values = bars.YData;
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(values)
    % 行注释：这里给图表添加标题、标签或说明文字。
    text(xtips(i), ytips(i), sprintf("%.*f", decimals, values(i)), ...
        'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom', ...
        'FontSize', 10, 'FontWeight', 'bold', 'Color', [0.12 0.14 0.18]);
% 行注释：这里结束当前的 if、for 或函数代码块。
end
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
exportgraphics(fig, fullfile(figDir, fileName), 'Resolution', 260);
% 行注释：这里执行当前语句，完成这一小步处理。
exportgraphics(fig, fullfile(pptDir, fileName), 'Resolution', 260);
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
