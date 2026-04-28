% 中文注释：生成贝叶斯理论部分的中文示意图。
% 主要流程：绘制先验、后验、阈值和最小风险等概念图，帮助解释模型原理。
% 输出结果：保存可直接放入 PPT 或报告中的中文可视化素材。

% 函数说明：生成贝叶斯理论讲解需要的中文示意图。
% 行注释：这里开始定义 make_bayes_theory_chinese_visuals 函数。
function make_bayes_theory_chinese_visuals(featuresFile, bayesResultsFile, cfg)
%MAKE_BAYES_THEORY_CHINESE_VISUALS Create Chinese annotated Bayes theory plots.
%
% Figures:
%   1. 1D Gaussian class distributions and Bayes error overlap.
%   2. 2D posterior probability decision regions in PCA feature space.
%   3. Conditional risk curves for minimum-risk Bayesian decision.

% 行注释：这里从磁盘读取前面步骤保存的数据文件。
S = load(featuresFile);
% 行注释：这里从磁盘读取前面步骤保存的数据文件。
B = load(bayesResultsFile);

% 行注释：这里计算或设置 figDir，供后续步骤使用。
figDir = fullfile(cfg.projectRoot, "results", "figures");
% 行注释：这里计算或设置 pptDir，供后续步骤使用。
pptDir = fullfile(cfg.projectRoot, "ppt_materials", "visa_pcb", "polished");
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(figDir);
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(pptDir);

% 行注释：这里执行当前语句，完成这一小步处理。
colors.blue = hex2rgb("#2E5A88");
% 行注释：这里执行当前语句，完成这一小步处理。
colors.orange = hex2rgb("#D95319");
% 行注释：这里执行当前语句，完成这一小步处理。
colors.gray = [0.40 0.40 0.42];
% 行注释：这里执行当前语句，完成这一小步处理。
colors.black = [0.10 0.11 0.13];
% 行注释：这里执行当前语句，完成这一小步处理。
colors.bg = [1 1 1];
% 行注释：这里执行当前语句，完成这一小步处理。
colors.font = 'Microsoft YaHei';

% 行注释：这里执行当前语句，完成这一小步处理。
set(groot, 'DefaultAxesFontName', colors.font);
% 行注释：这里执行当前语句，完成这一小步处理。
set(groot, 'DefaultTextFontName', colors.font);
% 行注释：这里执行当前语句，完成这一小步处理。
set(groot, 'DefaultLegendFontName', colors.font);
% 行注释：这里执行当前语句，完成这一小步处理。
set(groot, 'DefaultColorbarFontName', colors.font);

% 行注释：这里执行当前语句，完成这一小步处理。
make_1d_gaussian_overlap(figDir, pptDir, colors);
% 行注释：这里执行当前语句，完成这一小步处理。
make_2d_posterior_decision(S, B, figDir, pptDir, colors);
% 行注释：这里执行当前语句，完成这一小步处理。
make_bayesian_risk_curves(figDir, pptDir, colors);

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Chinese Bayes theory figures saved to: %s\n", pptDir);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：画一维正态/缺陷分布重叠图，解释误判区域为什么存在。
% 行注释：这里开始定义 make_1d_gaussian_overlap 函数。
function make_1d_gaussian_overlap(figDir, pptDir, colors)
% 行注释：这里计算或设置 mu1，供后续步骤使用。
mu1 = 0.0;
% 行注释：这里计算或设置 sigma1，供后续步骤使用。
sigma1 = 1.05;
% 行注释：这里计算或设置 mu2，供后续步骤使用。
mu2 = 2.25;
% 行注释：这里计算或设置 sigma2，供后续步骤使用。
sigma2 = 1.15;
% 行注释：这里计算或设置 prior1，供后续步骤使用。
prior1 = 0.58;
% 行注释：这里计算或设置 prior2，供后续步骤使用。
prior2 = 0.42;

% 行注释：这里计算或设置 x，供后续步骤使用。
x = linspace(-4, 6, 900);
% 行注释：这里计算或设置 pdf1，供后续步骤使用。
pdf1 = normpdf(x, mu1, sigma1);
% 行注释：这里计算或设置 pdf2，供后续步骤使用。
pdf2 = normpdf(x, mu2, sigma2);
% 行注释：这里计算或设置 w1，供后续步骤使用。
w1 = prior1 * pdf1;
% 行注释：这里计算或设置 w2，供后续步骤使用。
w2 = prior2 * pdf2;
% 行注释：这里计算或设置 boundary，供后续步骤使用。
boundary = find_gaussian_boundary(mu1, sigma1, prior1, mu2, sigma2, prior2);
% 行注释：这里计算或设置 overlap，供后续步骤使用。
overlap = min(w1, w2);

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', colors.bg, 'Position', [100 100 1120 650]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里调整坐标轴、网格或绘图状态。
hold(ax, 'on');

% 行注释：这里执行当前语句，完成这一小步处理。
fill(ax, [x, fliplr(x)], [pdf1, zeros(size(pdf1))], colors.blue, ...
    'FaceAlpha', 0.15, 'EdgeColor', 'none', 'HandleVisibility', 'off');
% 行注释：这里执行当前语句，完成这一小步处理。
fill(ax, [x, fliplr(x)], [pdf2, zeros(size(pdf2))], colors.orange, ...
    'FaceAlpha', 0.15, 'EdgeColor', 'none', 'HandleVisibility', 'off');
% 行注释：这里执行当前语句，完成这一小步处理。
area(ax, x, overlap, 'FaceColor', colors.gray, 'FaceAlpha', 0.38, ...
    'EdgeColor', 'none', 'DisplayName', "误判重叠区");

% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, pdf1, 'LineWidth', 2.5, 'Color', colors.blue, ...
    'DisplayName', "P(x|\omega_1) 正常类");
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, pdf2, 'LineWidth', 2.5, 'Color', colors.orange, ...
    'DisplayName', "P(x|\omega_2) 异常类");

% 行注释：这里计算或设置 db，供后续步骤使用。
db = xline(ax, boundary, '--', "决策边界", ...
    'Color', [0.80 0.10 0.10], 'LineWidth', 1.8);
% 行注释：这里执行当前语句，完成这一小步处理。
db.LabelVerticalAlignment = 'middle';
% 行注释：这里执行当前语句，完成这一小步处理。
db.LabelHorizontalAlignment = 'left';
% 行注释：这里执行当前语句，完成这一小步处理。
db.FontWeight = 'bold';
% 行注释：这里执行当前语句，完成这一小步处理。
db.HandleVisibility = 'off';

% 行注释：这里计算或设置 maxOverlap, idx，供后续步骤使用。
[maxOverlap, idx] = max(overlap);
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax, x(idx) + 0.18, maxOverlap + 0.018, ...
    "\leftarrow 贝叶斯误差 Bayes Error", ...
    'Color', colors.black, 'FontSize', 13, 'FontWeight', 'bold');

% 行注释：这里给图表添加标题、标签或说明文字。
title(ax, "一维类条件概率分布与贝叶斯误判区域", 'FontWeight', 'bold');
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "特征空间 x");
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "概率密度");
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, 'Location', 'northoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'Interpreter', 'tex');
% 行注释：这里执行当前语句，完成这一小步处理。
style_chinese_axes(ax);
% 行注释：这里调整坐标轴、网格或绘图状态。
ylim(ax, [0 max([pdf1 pdf2]) * 1.22]);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "09_一维概率分布与贝叶斯误差.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：画二维后验概率和决策边界，让贝叶斯分类过程更直观。
% 行注释：这里开始定义 make_2d_posterior_decision 函数。
function make_2d_posterior_decision(S, B, figDir, pptDir, colors)
% 行注释：这里计算或设置 X，供后续步骤使用。
X = double(S.X);
% 行注释：这里计算或设置 Y，供后续步骤使用。
Y = categorical(string(S.Y), ["normal", "anomaly"]);
% 行注释：这里计算或设置 Split，供后续步骤使用。
Split = string(S.Split);
% 行注释：这里计算或设置 trainMask，供后续步骤使用。
trainMask = Split == "train";

% 行注释：这里计算或设置 XZ，供后续步骤使用。
XZ = (X - B.prepBase.mu) ./ B.prepBase.sigma;
% 行注释：这里执行当前语句，完成这一小步处理。
XZ(~isfinite(XZ)) = 0;
% 行注释：这里计算或设置 scores，供后续步骤使用。
scores = XZ * B.coeff(:, 1:2);

% 行注释：这里计算或设置 trainScores，供后续步骤使用。
trainScores = scores(trainMask, :);
% 行注释：这里计算或设置 trainY，供后续步骤使用。
trainY = Y(trainMask);

% 行注释：这里计算或设置 normalTrain，供后续步骤使用。
normalTrain = trainScores(trainY == "normal", :);
% 行注释：这里计算或设置 anomalyTrain，供后续步骤使用。
anomalyTrain = trainScores(trainY == "anomaly", :);

% 行注释：这里计算或设置 muNormal，供后续步骤使用。
muNormal = mean(normalTrain, 1);
% 行注释：这里计算或设置 muAnomaly，供后续步骤使用。
muAnomaly = mean(anomalyTrain, 1);
% 行注释：这里计算或设置 covNormal，供后续步骤使用。
covNormal = cov(normalTrain) + 0.08 * eye(2);
% 行注释：这里计算或设置 covAnomaly，供后续步骤使用。
covAnomaly = cov(anomalyTrain) + 0.08 * eye(2);
% Use equal priors for this visualization so the posterior decision surface
% is visible. The experiment tables still use the tuned model metrics.
% 行注释：这里计算或设置 priorNormal，供后续步骤使用。
priorNormal = 0.5;
% 行注释：这里计算或设置 priorAnomaly，供后续步骤使用。
priorAnomaly = 0.5;

% 行注释：这里计算或设置 allScores，供后续步骤使用。
allScores = scores;
% 行注释：这里计算或设置 lo，供后续步骤使用。
lo = prctile(allScores, 1, 1);
% 行注释：这里计算或设置 hi，供后续步骤使用。
hi = prctile(allScores, 99, 1);
% 行注释：这里计算或设置 pad，供后续步骤使用。
pad = 0.15 * (hi - lo);
% 行注释：这里计算或设置 x1，供后续步骤使用。
x1 = linspace(lo(1) - pad(1), hi(1) + pad(1), 220);
% 行注释：这里计算或设置 x2，供后续步骤使用。
x2 = linspace(lo(2) - pad(2), hi(2) + pad(2), 220);
% 行注释：这里计算或设置 X1, X2，供后续步骤使用。
[X1, X2] = meshgrid(x1, x2);
% 行注释：这里计算或设置 gridPoints，供后续步骤使用。
gridPoints = [X1(:), X2(:)];

% 行注释：这里计算或设置 pNormal，供后续步骤使用。
pNormal = priorNormal * mvnpdf(gridPoints, muNormal, covNormal);
% 行注释：这里计算或设置 pAnomaly，供后续步骤使用。
pAnomaly = priorAnomaly * mvnpdf(gridPoints, muAnomaly, covAnomaly);
% 行注释：这里计算或设置 posteriorAnomaly，供后续步骤使用。
posteriorAnomaly = pAnomaly ./ (pNormal + pAnomaly + eps);
% 行注释：这里计算或设置 Z，供后续步骤使用。
Z = reshape(posteriorAnomaly, size(X1));

% 行注释：这里计算或设置 sampleN，供后续步骤使用。
sampleN = min(1800, size(scores, 1));
% 行注释：这里执行当前语句，完成这一小步处理。
rng(42);
% 行注释：这里计算或设置 idx，供后续步骤使用。
idx = randperm(size(scores, 1), sampleN);

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', colors.bg, 'Position', [100 100 950 800]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里调整坐标轴、网格或绘图状态。
hold(ax, 'on');

% 行注释：这里计算或设置 levels，供后续步骤使用。
levels = linspace(0, 1, 24);
% 行注释：这里执行当前语句，完成这一小步处理。
contourf(ax, X1, X2, Z, levels, 'LineStyle', 'none');
% 行注释：这里执行当前语句，完成这一小步处理。
shading(ax, 'interp');
% 行注释：这里执行当前语句，完成这一小步处理。
colormap(ax, skyline_colormap());

% 行注释：这里执行当前语句，完成这一小步处理。
contour(ax, X1, X2, Z, [0.5 0.5], 'k-', 'LineWidth', 1.2, ...
    'DisplayName', "后验概率相等边界");

% 行注释：这里计算或设置 g，供后续步骤使用。
g = gscatter(scores(idx, 1), scores(idx, 2), Y(idx), ...
    [colors.blue; colors.orange], 'oo', 6, 'off');
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(g)
    % 行注释：这里执行当前语句，完成这一小步处理。
    g(i).MarkerFaceColor = g(i).Color;
    % 行注释：这里执行当前语句，完成这一小步处理。
    g(i).MarkerEdgeColor = 'w';
    % 行注释：这里执行当前语句，完成这一小步处理。
    g(i).LineWidth = 0.4;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 cb，供后续步骤使用。
cb = colorbar(ax);
% 行注释：这里执行当前语句，完成这一小步处理。
cb.Label.String = "后验概率 P(异常|x)";
% 行注释：这里执行当前语句，完成这一小步处理。
cb.Label.FontSize = 12;
% 行注释：这里执行当前语句，完成这一小步处理。
clim(ax, [0 1]);

% 行注释：这里调整坐标轴、网格或绘图状态。
axis(ax, 'equal');
% 行注释：这里调整坐标轴、网格或绘图状态。
xlim(ax, [min(x1) max(x1)]);
% 行注释：这里调整坐标轴、网格或绘图状态。
ylim(ax, [min(x2) max(x2)]);
% 行注释：这里给图表添加标题、标签或说明文字。
title(ax, "二维特征空间中的贝叶斯后验概率决策面（等先验可视化）", 'FontWeight', 'bold');
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "主成分特征 PC1");
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "主成分特征 PC2");
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, ["决策边界 P=0.5", "正常样本", "异常样本"], ...
    'Location', 'northoutside', 'Orientation', 'horizontal', 'Box', 'off');
% 行注释：这里执行当前语句，完成这一小步处理。
style_chinese_axes(ax);
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "10_二维后验概率决策面.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：画不同动作的条件风险曲线，说明最小风险决策怎么选。
% 行注释：这里开始定义 make_bayesian_risk_curves 函数。
function make_bayesian_risk_curves(figDir, pptDir, colors)
% 行注释：这里计算或设置 mu1，供后续步骤使用。
mu1 = 0.0;
% 行注释：这里计算或设置 sigma1，供后续步骤使用。
sigma1 = 1.05;
% 行注释：这里计算或设置 mu2，供后续步骤使用。
mu2 = 2.25;
% 行注释：这里计算或设置 sigma2，供后续步骤使用。
sigma2 = 1.15;
% 行注释：这里计算或设置 priorNormal，供后续步骤使用。
priorNormal = 0.58;
% 行注释：这里计算或设置 priorAnomaly，供后续步骤使用。
priorAnomaly = 0.42;
% 行注释：这里计算或设置 costFP，供后续步骤使用。
costFP = 1.0;
% 行注释：这里计算或设置 costFN，供后续步骤使用。
costFN = 4.0;

% 行注释：这里计算或设置 x，供后续步骤使用。
x = linspace(-4, 6, 900);
% 行注释：这里计算或设置 pNormal，供后续步骤使用。
pNormal = priorNormal * normpdf(x, mu1, sigma1);
% 行注释：这里计算或设置 pAnomaly，供后续步骤使用。
pAnomaly = priorAnomaly * normpdf(x, mu2, sigma2);
% 行注释：这里计算或设置 postNormal，供后续步骤使用。
postNormal = pNormal ./ (pNormal + pAnomaly + eps);
% 行注释：这里计算或设置 postAnomaly，供后续步骤使用。
postAnomaly = pAnomaly ./ (pNormal + pAnomaly + eps);

% 行注释：这里计算或设置 riskNormal，供后续步骤使用。
riskNormal = costFN * postAnomaly;
% 行注释：这里计算或设置 riskAnomaly，供后续步骤使用。
riskAnomaly = costFP * postNormal;
% 行注释：这里计算或设置 chosenRisk，供后续步骤使用。
chosenRisk = min(riskNormal, riskAnomaly);
% 行注释：这里计算或设置 alternativeRisk，供后续步骤使用。
alternativeRisk = max(riskNormal, riskAnomaly);
% 行注释：这里计算或设置 savedRisk，供后续步骤使用。
savedRisk = alternativeRisk - chosenRisk;
% 行注释：这里计算或设置 decisionIdx，供后续步骤使用。
decisionIdx = find(abs(riskNormal - riskAnomaly) == min(abs(riskNormal - riskAnomaly)), 1);
% 行注释：这里计算或设置 boundary，供后续步骤使用。
boundary = x(decisionIdx);

% 行注释：这里计算或设置 fig，供后续步骤使用。
fig = figure('Color', colors.bg, 'Position', [100 100 1120 650]);
% 行注释：这里计算或设置 ax，供后续步骤使用。
ax = axes(fig);
% 行注释：这里调整坐标轴、网格或绘图状态。
hold(ax, 'on');

% 行注释：这里执行当前语句，完成这一小步处理。
fill(ax, [x, fliplr(x)], [alternativeRisk, fliplr(chosenRisk)], ...
    [0.30 0.62 0.48], 'FaceAlpha', 0.20, 'EdgeColor', 'none', ...
    'DisplayName', "节省风险区域");
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, riskNormal, ':', 'LineWidth', 2.2, 'Color', colors.blue, ...
    'DisplayName', "R(\alpha_{normal}|x) 判为正常的风险");
% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, riskAnomaly, ':', 'LineWidth', 2.2, 'Color', colors.orange, ...
    'DisplayName', "R(\alpha_{anomaly}|x) 判为异常的风险");

% 行注释：这里把数据画成图形，便于直观看出趋势或对比。
plot(ax, x, chosenRisk, '-', 'LineWidth', 3.0, 'Color', colors.black, ...
    'DisplayName', "最小条件风险");

% 行注释：这里计算或设置 db，供后续步骤使用。
db = xline(ax, boundary, '--', "最小风险决策边界", ...
    'Color', [0.80 0.10 0.10], 'LineWidth', 1.7);
% 行注释：这里执行当前语句，完成这一小步处理。
db.LabelVerticalAlignment = 'middle';
% 行注释：这里执行当前语句，完成这一小步处理。
db.LabelHorizontalAlignment = 'left';
% 行注释：这里执行当前语句，完成这一小步处理。
db.FontWeight = 'bold';
% 行注释：这里执行当前语句，完成这一小步处理。
db.HandleVisibility = 'off';

% 行注释：这里计算或设置 占位输出, maxIdx，供后续步骤使用。
[~, maxIdx] = max(savedRisk);
% 行注释：这里给图表添加标题、标签或说明文字。
text(ax, x(maxIdx) - 1.4, chosenRisk(maxIdx) + savedRisk(maxIdx) * 0.48, ...
    "代价敏感决策降低的风险", 'Color', [0.18 0.35 0.28], ...
    'FontSize', 13, 'FontWeight', 'bold');

% 行注释：这里给图表添加标题、标签或说明文字。
title(ax, "贝叶斯最小风险决策与损失函数可视化", 'FontWeight', 'bold');
% 行注释：这里给图表添加标题、标签或说明文字。
xlabel(ax, "特征空间 x", 'FontSize', 13);
% 行注释：这里给图表添加标题、标签或说明文字。
ylabel(ax, "条件风险", 'FontSize', 13);
% 行注释：这里给图表添加标题、标签或说明文字。
legend(ax, 'Location', 'northoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'Interpreter', 'tex');
% 行注释：这里执行当前语句，完成这一小步处理。
style_chinese_axes(ax);
% 行注释：这里执行当前语句，完成这一小步处理。
set(ax, 'LooseInset', get(ax, 'TightInset'));
% 行注释：这里执行当前语句，完成这一小步处理。
export_to_both(fig, figDir, pptDir, "11_贝叶斯风险与损失函数.png");
% 行注释：这里执行当前语句，完成这一小步处理。
close(fig);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：求两条高斯曲线加权后相交的位置，用作理论决策边界。
% 行注释：这里开始定义 find_gaussian_boundary 函数。
function boundary = find_gaussian_boundary(mu1, s1, p1, mu2, s2, p2)
% Solve p1*N(mu1,s1) = p2*N(mu2,s2).
% 行注释：这里计算或设置 a，供后续步骤使用。
a = 1 / (2 * s2^2) - 1 / (2 * s1^2);
% 行注释：这里计算或设置 b，供后续步骤使用。
b = mu1 / s1^2 - mu2 / s2^2;
% 行注释：这里计算或设置 c，供后续步骤使用。
c = mu2^2 / (2 * s2^2) - mu1^2 / (2 * s1^2) + log((p2 * s1) / (p1 * s2));

% 行注释：这里计算或设置 rootsCandidate，供后续步骤使用。
rootsCandidate = roots([a b c]);
% 行注释：这里计算或设置 rootsCandidate，供后续步骤使用。
rootsCandidate = real(rootsCandidate(abs(imag(rootsCandidate)) < 1e-8));
% 行注释：这里计算或设置 between，供后续步骤使用。
between = rootsCandidate(rootsCandidate > min(mu1, mu2) & rootsCandidate < max(mu1, mu2));
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if ~isempty(between)
    % 行注释：这里计算或设置 boundary，供后续步骤使用。
    boundary = between(1);
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里计算或设置 占位输出, idx，供后续步骤使用。
    [~, idx] = min(abs(rootsCandidate - mean([mu1 mu2])));
    % 行注释：这里计算或设置 boundary，供后续步骤使用。
    boundary = rootsCandidate(idx);
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

% 函数说明：生成蓝色系渐变色，用于后验概率等热力图。
% 行注释：这里开始定义 skyline_colormap 函数。
function cmap = skyline_colormap()
% 行注释：这里计算或设置 anchors，供后续步骤使用。
anchors = [
    % 行注释：这里执行当前语句，完成这一小步处理。
    0.18 0.32 0.55
    % 行注释：这里执行当前语句，完成这一小步处理。
    0.55 0.74 0.86
    % 行注释：这里执行当前语句，完成这一小步处理。
    0.98 0.98 0.95
    % 行注释：这里执行当前语句，完成这一小步处理。
    0.94 0.64 0.42
    % 行注释：这里执行当前语句，完成这一小步处理。
    0.76 0.25 0.16
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

% 函数说明：统一设置中文图表坐标轴字体、线宽和网格样式。
% 行注释：这里开始定义 style_chinese_axes 函数。
function style_chinese_axes(ax)
% 行注释：这里执行当前语句，完成这一小步处理。
set(ax, 'FontName', 'Microsoft YaHei', 'FontSize', 12, ...
    'LineWidth', 1.1, 'TickDir', 'out', 'Box', 'off');
% 行注释：这里调整坐标轴、网格或绘图状态。
grid(ax, 'on');
% 行注释：这里执行当前语句，完成这一小步处理。
ax.GridAlpha = 0.18;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.MinorGridAlpha = 0.08;
% 行注释：这里执行当前语句，完成这一小步处理。
ax.XColor = [0.10 0.11 0.13];
% 行注释：这里执行当前语句，完成这一小步处理。
ax.YColor = [0.10 0.11 0.13];
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：把同一张图同时保存到结果目录和 PPT 素材目录。
% 行注释：这里开始定义 export_to_both 函数。
function export_to_both(fig, figDir, pptDir, fileName)
% 行注释：这里执行当前语句，完成这一小步处理。
set(findall(fig, '-property', 'FontName'), 'FontName', 'Microsoft YaHei');
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
