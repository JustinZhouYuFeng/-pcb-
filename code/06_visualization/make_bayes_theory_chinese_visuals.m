% 中文注释：生成贝叶斯理论部分的中文示意图。
% 主要流程：绘制先验、后验、阈值和最小风险等概念图，帮助解释模型原理。
% 输出结果：保存可直接放入 PPT 或报告中的中文可视化素材。

function make_bayes_theory_chinese_visuals(featuresFile, bayesResultsFile, cfg)
%MAKE_BAYES_THEORY_CHINESE_VISUALS Create Chinese annotated Bayes theory plots.
%
% Figures:
%   1. 1D Gaussian class distributions and Bayes error overlap.
%   2. 2D posterior probability decision regions in PCA feature space.
%   3. Conditional risk curves for minimum-risk Bayesian decision.

S = load(featuresFile);
B = load(bayesResultsFile);

figDir = fullfile(cfg.projectRoot, "results", "figures");
pptDir = fullfile(cfg.projectRoot, "ppt_materials", "visa_pcb", "polished");
ensure_dir(figDir);
ensure_dir(pptDir);

colors.blue = hex2rgb("#2E5A88");
colors.orange = hex2rgb("#D95319");
colors.gray = [0.40 0.40 0.42];
colors.black = [0.10 0.11 0.13];
colors.bg = [1 1 1];
colors.font = 'Microsoft YaHei';

set(groot, 'DefaultAxesFontName', colors.font);
set(groot, 'DefaultTextFontName', colors.font);
set(groot, 'DefaultLegendFontName', colors.font);
set(groot, 'DefaultColorbarFontName', colors.font);

make_1d_gaussian_overlap(figDir, pptDir, colors);
make_2d_posterior_decision(S, B, figDir, pptDir, colors);
make_bayesian_risk_curves(figDir, pptDir, colors);

fprintf("Chinese Bayes theory figures saved to: %s\n", pptDir);
end

function make_1d_gaussian_overlap(figDir, pptDir, colors)
mu1 = 0.0;
sigma1 = 1.05;
mu2 = 2.25;
sigma2 = 1.15;
prior1 = 0.58;
prior2 = 0.42;

x = linspace(-4, 6, 900);
pdf1 = normpdf(x, mu1, sigma1);
pdf2 = normpdf(x, mu2, sigma2);
w1 = prior1 * pdf1;
w2 = prior2 * pdf2;
boundary = find_gaussian_boundary(mu1, sigma1, prior1, mu2, sigma2, prior2);
overlap = min(w1, w2);

fig = figure('Color', colors.bg, 'Position', [100 100 1120 650]);
ax = axes(fig);
hold(ax, 'on');

fill(ax, [x, fliplr(x)], [pdf1, zeros(size(pdf1))], colors.blue, ...
    'FaceAlpha', 0.15, 'EdgeColor', 'none', 'HandleVisibility', 'off');
fill(ax, [x, fliplr(x)], [pdf2, zeros(size(pdf2))], colors.orange, ...
    'FaceAlpha', 0.15, 'EdgeColor', 'none', 'HandleVisibility', 'off');
area(ax, x, overlap, 'FaceColor', colors.gray, 'FaceAlpha', 0.38, ...
    'EdgeColor', 'none', 'DisplayName', "误判重叠区");

plot(ax, x, pdf1, 'LineWidth', 2.5, 'Color', colors.blue, ...
    'DisplayName', "P(x|\omega_1) 正常类");
plot(ax, x, pdf2, 'LineWidth', 2.5, 'Color', colors.orange, ...
    'DisplayName', "P(x|\omega_2) 异常类");

db = xline(ax, boundary, '--', "决策边界", ...
    'Color', [0.80 0.10 0.10], 'LineWidth', 1.8);
db.LabelVerticalAlignment = 'middle';
db.LabelHorizontalAlignment = 'left';
db.FontWeight = 'bold';
db.HandleVisibility = 'off';

[maxOverlap, idx] = max(overlap);
text(ax, x(idx) + 0.18, maxOverlap + 0.018, ...
    "\leftarrow 贝叶斯误差 Bayes Error", ...
    'Color', colors.black, 'FontSize', 13, 'FontWeight', 'bold');

title(ax, "一维类条件概率分布与贝叶斯误判区域", 'FontWeight', 'bold');
xlabel(ax, "特征空间 x");
ylabel(ax, "概率密度");
legend(ax, 'Location', 'northoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'Interpreter', 'tex');
style_chinese_axes(ax);
ylim(ax, [0 max([pdf1 pdf2]) * 1.22]);
export_to_both(fig, figDir, pptDir, "09_一维概率分布与贝叶斯误差.png");
close(fig);
end

function make_2d_posterior_decision(S, B, figDir, pptDir, colors)
X = double(S.X);
Y = categorical(string(S.Y), ["normal", "anomaly"]);
Split = string(S.Split);
trainMask = Split == "train";

XZ = (X - B.prepBase.mu) ./ B.prepBase.sigma;
XZ(~isfinite(XZ)) = 0;
scores = XZ * B.coeff(:, 1:2);

trainScores = scores(trainMask, :);
trainY = Y(trainMask);

normalTrain = trainScores(trainY == "normal", :);
anomalyTrain = trainScores(trainY == "anomaly", :);

muNormal = mean(normalTrain, 1);
muAnomaly = mean(anomalyTrain, 1);
covNormal = cov(normalTrain) + 0.08 * eye(2);
covAnomaly = cov(anomalyTrain) + 0.08 * eye(2);
% Use equal priors for this visualization so the posterior decision surface
% is visible. The experiment tables still use the tuned model metrics.
priorNormal = 0.5;
priorAnomaly = 0.5;

allScores = scores;
lo = prctile(allScores, 1, 1);
hi = prctile(allScores, 99, 1);
pad = 0.15 * (hi - lo);
x1 = linspace(lo(1) - pad(1), hi(1) + pad(1), 220);
x2 = linspace(lo(2) - pad(2), hi(2) + pad(2), 220);
[X1, X2] = meshgrid(x1, x2);
gridPoints = [X1(:), X2(:)];

pNormal = priorNormal * mvnpdf(gridPoints, muNormal, covNormal);
pAnomaly = priorAnomaly * mvnpdf(gridPoints, muAnomaly, covAnomaly);
posteriorAnomaly = pAnomaly ./ (pNormal + pAnomaly + eps);
Z = reshape(posteriorAnomaly, size(X1));

sampleN = min(1800, size(scores, 1));
rng(42);
idx = randperm(size(scores, 1), sampleN);

fig = figure('Color', colors.bg, 'Position', [100 100 950 800]);
ax = axes(fig);
hold(ax, 'on');

levels = linspace(0, 1, 24);
contourf(ax, X1, X2, Z, levels, 'LineStyle', 'none');
shading(ax, 'interp');
colormap(ax, skyline_colormap());

contour(ax, X1, X2, Z, [0.5 0.5], 'k-', 'LineWidth', 1.2, ...
    'DisplayName', "后验概率相等边界");

g = gscatter(scores(idx, 1), scores(idx, 2), Y(idx), ...
    [colors.blue; colors.orange], 'oo', 6, 'off');
for i = 1:numel(g)
    g(i).MarkerFaceColor = g(i).Color;
    g(i).MarkerEdgeColor = 'w';
    g(i).LineWidth = 0.4;
end

cb = colorbar(ax);
cb.Label.String = "后验概率 P(异常|x)";
cb.Label.FontSize = 12;
clim(ax, [0 1]);

axis(ax, 'equal');
xlim(ax, [min(x1) max(x1)]);
ylim(ax, [min(x2) max(x2)]);
title(ax, "二维特征空间中的贝叶斯后验概率决策面（等先验可视化）", 'FontWeight', 'bold');
xlabel(ax, "主成分特征 PC1");
ylabel(ax, "主成分特征 PC2");
legend(ax, ["决策边界 P=0.5", "正常样本", "异常样本"], ...
    'Location', 'northoutside', 'Orientation', 'horizontal', 'Box', 'off');
style_chinese_axes(ax);
export_to_both(fig, figDir, pptDir, "10_二维后验概率决策面.png");
close(fig);
end

function make_bayesian_risk_curves(figDir, pptDir, colors)
mu1 = 0.0;
sigma1 = 1.05;
mu2 = 2.25;
sigma2 = 1.15;
priorNormal = 0.58;
priorAnomaly = 0.42;
costFP = 1.0;
costFN = 4.0;

x = linspace(-4, 6, 900);
pNormal = priorNormal * normpdf(x, mu1, sigma1);
pAnomaly = priorAnomaly * normpdf(x, mu2, sigma2);
postNormal = pNormal ./ (pNormal + pAnomaly + eps);
postAnomaly = pAnomaly ./ (pNormal + pAnomaly + eps);

riskNormal = costFN * postAnomaly;
riskAnomaly = costFP * postNormal;
chosenRisk = min(riskNormal, riskAnomaly);
alternativeRisk = max(riskNormal, riskAnomaly);
savedRisk = alternativeRisk - chosenRisk;
decisionIdx = find(abs(riskNormal - riskAnomaly) == min(abs(riskNormal - riskAnomaly)), 1);
boundary = x(decisionIdx);

fig = figure('Color', colors.bg, 'Position', [100 100 1120 650]);
ax = axes(fig);
hold(ax, 'on');

fill(ax, [x, fliplr(x)], [alternativeRisk, fliplr(chosenRisk)], ...
    [0.30 0.62 0.48], 'FaceAlpha', 0.20, 'EdgeColor', 'none', ...
    'DisplayName', "节省风险区域");
plot(ax, x, riskNormal, ':', 'LineWidth', 2.2, 'Color', colors.blue, ...
    'DisplayName', "R(\alpha_{normal}|x) 判为正常的风险");
plot(ax, x, riskAnomaly, ':', 'LineWidth', 2.2, 'Color', colors.orange, ...
    'DisplayName', "R(\alpha_{anomaly}|x) 判为异常的风险");

plot(ax, x, chosenRisk, '-', 'LineWidth', 3.0, 'Color', colors.black, ...
    'DisplayName', "最小条件风险");

db = xline(ax, boundary, '--', "最小风险决策边界", ...
    'Color', [0.80 0.10 0.10], 'LineWidth', 1.7);
db.LabelVerticalAlignment = 'middle';
db.LabelHorizontalAlignment = 'left';
db.FontWeight = 'bold';
db.HandleVisibility = 'off';

[~, maxIdx] = max(savedRisk);
text(ax, x(maxIdx) - 1.4, chosenRisk(maxIdx) + savedRisk(maxIdx) * 0.48, ...
    "代价敏感决策降低的风险", 'Color', [0.18 0.35 0.28], ...
    'FontSize', 13, 'FontWeight', 'bold');

title(ax, "贝叶斯最小风险决策与损失函数可视化", 'FontWeight', 'bold');
xlabel(ax, "特征空间 x", 'FontSize', 13);
ylabel(ax, "条件风险", 'FontSize', 13);
legend(ax, 'Location', 'northoutside', 'Orientation', 'horizontal', ...
    'Box', 'off', 'Interpreter', 'tex');
style_chinese_axes(ax);
set(ax, 'LooseInset', get(ax, 'TightInset'));
export_to_both(fig, figDir, pptDir, "11_贝叶斯风险与损失函数.png");
close(fig);
end

function boundary = find_gaussian_boundary(mu1, s1, p1, mu2, s2, p2)
% Solve p1*N(mu1,s1) = p2*N(mu2,s2).
a = 1 / (2 * s2^2) - 1 / (2 * s1^2);
b = mu1 / s1^2 - mu2 / s2^2;
c = mu2^2 / (2 * s2^2) - mu1^2 / (2 * s1^2) + log((p2 * s1) / (p1 * s2));

rootsCandidate = roots([a b c]);
rootsCandidate = real(rootsCandidate(abs(imag(rootsCandidate)) < 1e-8));
between = rootsCandidate(rootsCandidate > min(mu1, mu2) & rootsCandidate < max(mu1, mu2));
if ~isempty(between)
    boundary = between(1);
else
    [~, idx] = min(abs(rootsCandidate - mean([mu1 mu2])));
    boundary = rootsCandidate(idx);
end
end

function rgb = hex2rgb(hex)
hex = erase(string(hex), "#");
rgb = sscanf(hex, "%2x%2x%2x", [1 3]) / 255;
end

function cmap = skyline_colormap()
anchors = [
    0.18 0.32 0.55
    0.55 0.74 0.86
    0.98 0.98 0.95
    0.94 0.64 0.42
    0.76 0.25 0.16
];
x = linspace(0, 1, size(anchors, 1));
xi = linspace(0, 1, 256);
cmap = interp1(x, anchors, xi);
end

function style_chinese_axes(ax)
set(ax, 'FontName', 'Microsoft YaHei', 'FontSize', 12, ...
    'LineWidth', 1.1, 'TickDir', 'out', 'Box', 'off');
grid(ax, 'on');
ax.GridAlpha = 0.18;
ax.MinorGridAlpha = 0.08;
ax.XColor = [0.10 0.11 0.13];
ax.YColor = [0.10 0.11 0.13];
end

function export_to_both(fig, figDir, pptDir, fileName)
set(findall(fig, '-property', 'FontName'), 'FontName', 'Microsoft YaHei');
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
