% 中文注释：比较多个贝叶斯优化版本在 PCB 缺陷检测任务上的表现。
% 主要流程：逐步加入 PCA、协方差正则化、阈值优化和风险代价设置，观察指标变化。
% 输出结果：生成 Bayes-0 到 Bayes-4 的对比结果，支撑论文/PPT 中的优化分析。

function optimizationResultsFile = run_visa_bayes_optimization_comparison(featuresFile, bayesResultsFile, cfg)
%RUN_VISA_BAYES_OPTIMIZATION_COMPARISON Compare only Bayesian optimizations.
%
% The comparison is intentionally kept inside the Bayesian decision framework:
%   1. Original Naive Bayes
%   2. Naive Bayes + PCA
%   3. Gaussian Bayes with covariance modeling
%   4. Regularized Gaussian Bayes
%   5. Regularized Gaussian Bayes + tuned posterior threshold

S = load(featuresFile);
B = load(bayesResultsFile);

X = double(S.X);
Y = categorical(string(S.Y), ["normal", "anomaly"]);
Split = string(S.Split);

trainMask = Split == "train";
valMask = Split == "val";
testMask = Split == "test";

XTrain = X(trainMask, :);
YTrain = Y(trainMask);
XVal = X(valMask, :);
YVal = Y(valMask);
XTest = X(testMask, :);
YTest = Y(testMask);

[XTrainZ, prepBase] = standardize_train(XTrain);
XValZ = standardize_apply(XVal, prepBase);
XTestZ = standardize_apply(XTest, prepBase);

[coeff, ~] = pca(XTrainZ);
bestDim = min(B.bestSpec.PCADim, size(coeff, 2));
bestGamma = B.bestSpec.Gamma;
bestThreshold = B.bestSpec.Threshold;

rows = table();

% Stage 0: the original, least engineered Bayesian classifier.
model = fitcnb(XTrainZ, YTrain, ...
    'DistributionNames', 'normal', ...
    'Prior', 'uniform');
rows = [rows; evaluate_stage("Bayes-0", "Original Naive Bayes", ...
    model, XValZ, YVal, XTestZ, YTest, NaN, NaN, 0.50)]; %#ok<AGROW>

% Stage 1: PCA reduces noise and high-dimensional instability.
XTrainP = XTrainZ * coeff(:, 1:bestDim);
XValP = XValZ * coeff(:, 1:bestDim);
XTestP = XTestZ * coeff(:, 1:bestDim);

model = fitcnb(XTrainP, YTrain, ...
    'DistributionNames', 'normal', ...
    'Prior', 'uniform');
rows = [rows; evaluate_stage("Bayes-1", "Naive Bayes + PCA", ...
    model, XValP, YVal, XTestP, YTest, bestDim, NaN, 0.50)]; %#ok<AGROW>

% Stage 2: multivariate Gaussian Bayes weakens the naive independence assumption.
model = fitcdiscr(XTrainP, YTrain, ...
    'DiscrimType', 'pseudoQuadratic', ...
    'Prior', 'uniform');
rows = [rows; evaluate_stage("Bayes-2", "Gaussian Bayes + PCA", ...
    model, XValP, YVal, XTestP, YTest, bestDim, NaN, 0.50)]; %#ok<AGROW>

% Stage 3: regularization improves covariance estimation.
model = fitcdiscr(XTrainP, YTrain, ...
    'DiscrimType', 'linear', ...
    'Gamma', bestGamma, ...
    'Prior', 'uniform');
rows = [rows; evaluate_stage("Bayes-3", "Regularized Gaussian Bayes", ...
    model, XValP, YVal, XTestP, YTest, bestDim, bestGamma, 0.50)]; %#ok<AGROW>

% Stage 4: posterior threshold tuning reflects Bayesian decision/risk control.
model = fitcdiscr(XTrainP, YTrain, ...
    'DiscrimType', 'linear', ...
    'Gamma', bestGamma, ...
    'Prior', 'uniform');
rows = [rows; evaluate_stage("Bayes-4", "Regularized Bayes + threshold", ...
    model, XValP, YVal, XTestP, YTest, bestDim, bestGamma, bestThreshold)]; %#ok<AGROW>

outDir = fullfile(cfg.projectRoot, "results", "visa_pcb");
ensure_dir(outDir);
modelsDir = fullfile(cfg.projectRoot, "results", "models");
ensure_dir(modelsDir);

csvFile = fullfile(outDir, "bayes_optimization_comparison.csv");
optimizationResultsFile = fullfile(modelsDir, "visa_pcb_bayes_optimization_results.mat");

writetable(rows, csvFile);
save(optimizationResultsFile, "rows", "prepBase", "coeff", "bestDim", ...
    "bestGamma", "bestThreshold");

fprintf("Bayes-only optimization comparison saved: %s\n", csvFile);
end

function row = evaluate_stage(stageId, methodName, model, XVal, YVal, XTest, YTest, pcaDim, gamma, threshold)
[~, valScoreRaw] = predict(model, XVal);
valScore = positive_score(model, valScoreRaw);
valPred = threshold_predict(valScore, threshold);
valMetrics = classification_metrics(YVal, valPred, valScore, "anomaly");

[~, testScoreRaw] = predict(model, XTest);
testScore = positive_score(model, testScoreRaw);
testPred = threshold_predict(testScore, threshold);
testMetrics = classification_metrics(YTest, testPred, testScore, "anomaly");

row = table(string(stageId), string(methodName), pcaDim, gamma, threshold, ...
    valMetrics.accuracy, valMetrics.precision, valMetrics.recall, valMetrics.f1, valMetrics.auc, ...
    testMetrics.accuracy, testMetrics.precision, testMetrics.recall, testMetrics.specificity, ...
    testMetrics.fpr, testMetrics.fnr, testMetrics.f1, testMetrics.iou, testMetrics.auc, ...
    testMetrics.tp, testMetrics.fp, testMetrics.tn, testMetrics.fn, ...
    'VariableNames', {'Stage', 'BayesOptimization', 'PCADim', 'Gamma', 'Threshold', ...
    'ValAccuracy', 'ValPrecision', 'ValRecall', 'ValF1', 'ValAUC', ...
    'TestAccuracy', 'TestPrecision', 'TestRecall', 'TestSpecificity', ...
    'TestFPR', 'TestFNR', 'TestF1', 'TestIoU', 'TestAUC', ...
    'TP', 'FP', 'TN', 'FN'});
end

function scoreAnomaly = positive_score(model, score)
classNames = string(model.ClassNames);
posCol = find(classNames == "anomaly", 1);
if isempty(posCol)
    error("The model does not contain an anomaly class.");
end
scoreAnomaly = score(:, posCol);
end

function yPred = threshold_predict(scoreAnomaly, threshold)
labels = repmat("normal", numel(scoreAnomaly), 1);
labels(scoreAnomaly >= threshold) = "anomaly";
yPred = categorical(labels, ["normal", "anomaly"]);
end

function [XZ, prep] = standardize_train(X)
prep.mu = mean(X, 1, 'omitnan');
prep.sigma = std(X, 0, 1, 'omitnan');
prep.sigma(prep.sigma == 0 | ~isfinite(prep.sigma)) = 1;
XZ = (X - prep.mu) ./ prep.sigma;
XZ(~isfinite(XZ)) = 0;
end

function XZ = standardize_apply(X, prep)
XZ = (X - prep.mu) ./ prep.sigma;
XZ(~isfinite(XZ)) = 0;
end
