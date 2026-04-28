% 中文注释：比较多个贝叶斯优化版本在 PCB 缺陷检测任务上的表现。
% 主要流程：逐步加入 PCA、协方差正则化、阈值优化和风险代价设置，观察指标变化。
% 输出结果：生成 Bayes-0 到 Bayes-4 的对比结果，支撑论文/PPT 中的优化分析。

% 函数说明：按优化阶段比较贝叶斯模型性能，展示从基础模型到最终模型的提升。
% 行注释：这里开始定义 run_visa_bayes_optimization_comparison 函数。
function optimizationResultsFile = run_visa_bayes_optimization_comparison(featuresFile, bayesResultsFile, cfg)
%RUN_VISA_BAYES_OPTIMIZATION_COMPARISON Compare only Bayesian optimizations.
%
% The comparison is intentionally kept inside the Bayesian decision framework:
%   1. Original Naive Bayes
%   2. Naive Bayes + PCA
%   3. Gaussian Bayes with covariance modeling
%   4. Regularized Gaussian Bayes
%   5. Regularized Gaussian Bayes + tuned posterior threshold

% 行注释：这里从磁盘读取前面步骤保存的数据文件。
S = load(featuresFile);
% 行注释：这里从磁盘读取前面步骤保存的数据文件。
B = load(bayesResultsFile);

% 行注释：这里计算或设置 X，供后续步骤使用。
X = double(S.X);
% 行注释：这里计算或设置 Y，供后续步骤使用。
Y = categorical(string(S.Y), ["normal", "anomaly"]);
% 行注释：这里计算或设置 Split，供后续步骤使用。
Split = string(S.Split);

% 行注释：这里计算或设置 trainMask，供后续步骤使用。
trainMask = Split == "train";
% 行注释：这里计算或设置 valMask，供后续步骤使用。
valMask = Split == "val";
% 行注释：这里计算或设置 testMask，供后续步骤使用。
testMask = Split == "test";

% 行注释：这里计算或设置 XTrain，供后续步骤使用。
XTrain = X(trainMask, :);
% 行注释：这里计算或设置 YTrain，供后续步骤使用。
YTrain = Y(trainMask);
% 行注释：这里计算或设置 XVal，供后续步骤使用。
XVal = X(valMask, :);
% 行注释：这里计算或设置 YVal，供后续步骤使用。
YVal = Y(valMask);
% 行注释：这里计算或设置 XTest，供后续步骤使用。
XTest = X(testMask, :);
% 行注释：这里计算或设置 YTest，供后续步骤使用。
YTest = Y(testMask);

% 行注释：这里计算或设置 XTrainZ, prepBase，供后续步骤使用。
[XTrainZ, prepBase] = standardize_train(XTrain);
% 行注释：这里计算或设置 XValZ，供后续步骤使用。
XValZ = standardize_apply(XVal, prepBase);
% 行注释：这里计算或设置 XTestZ，供后续步骤使用。
XTestZ = standardize_apply(XTest, prepBase);

% 行注释：这里做 PCA 降维，减少特征维度并保留主要信息。
[coeff, ~] = pca(XTrainZ);
% 行注释：这里计算或设置 bestDim，供后续步骤使用。
bestDim = min(B.bestSpec.PCADim, size(coeff, 2));
% 行注释：这里计算或设置 bestGamma，供后续步骤使用。
bestGamma = B.bestSpec.Gamma;
% 行注释：这里计算或设置 bestThreshold，供后续步骤使用。
bestThreshold = B.bestSpec.Threshold;

% 行注释：这里计算或设置 rows，供后续步骤使用。
rows = table();

% Stage 0: the original, least engineered Bayesian classifier.
% 行注释：这里训练朴素贝叶斯分类器。
model = fitcnb(XTrainZ, YTrain, ...
    'DistributionNames', 'normal', ...
    'Prior', 'uniform');
% 行注释：这里计算或设置 rows，供后续步骤使用。
rows = [rows; evaluate_stage("Bayes-0", "Original Naive Bayes", ...
    model, XValZ, YVal, XTestZ, YTest, NaN, NaN, 0.50)]; %#ok<AGROW>

% Stage 1: PCA reduces noise and high-dimensional instability.
% 行注释：这里计算或设置 XTrainP，供后续步骤使用。
XTrainP = XTrainZ * coeff(:, 1:bestDim);
% 行注释：这里计算或设置 XValP，供后续步骤使用。
XValP = XValZ * coeff(:, 1:bestDim);
% 行注释：这里计算或设置 XTestP，供后续步骤使用。
XTestP = XTestZ * coeff(:, 1:bestDim);

% 行注释：这里训练朴素贝叶斯分类器。
model = fitcnb(XTrainP, YTrain, ...
    'DistributionNames', 'normal', ...
    'Prior', 'uniform');
% 行注释：这里计算或设置 rows，供后续步骤使用。
rows = [rows; evaluate_stage("Bayes-1", "Naive Bayes + PCA", ...
    model, XValP, YVal, XTestP, YTest, bestDim, NaN, 0.50)]; %#ok<AGROW>

% Stage 2: multivariate Gaussian Bayes weakens the naive independence assumption.
% 行注释：这里训练判别分析形式的贝叶斯分类器。
model = fitcdiscr(XTrainP, YTrain, ...
    'DiscrimType', 'pseudoQuadratic', ...
    'Prior', 'uniform');
% 行注释：这里计算或设置 rows，供后续步骤使用。
rows = [rows; evaluate_stage("Bayes-2", "Gaussian Bayes + PCA", ...
    model, XValP, YVal, XTestP, YTest, bestDim, NaN, 0.50)]; %#ok<AGROW>

% Stage 3: regularization improves covariance estimation.
% 行注释：这里训练判别分析形式的贝叶斯分类器。
model = fitcdiscr(XTrainP, YTrain, ...
    'DiscrimType', 'linear', ...
    'Gamma', bestGamma, ...
    'Prior', 'uniform');
% 行注释：这里计算或设置 rows，供后续步骤使用。
rows = [rows; evaluate_stage("Bayes-3", "Regularized Gaussian Bayes", ...
    model, XValP, YVal, XTestP, YTest, bestDim, bestGamma, 0.50)]; %#ok<AGROW>

% Stage 4: posterior threshold tuning reflects Bayesian decision/risk control.
% 行注释：这里训练判别分析形式的贝叶斯分类器。
model = fitcdiscr(XTrainP, YTrain, ...
    'DiscrimType', 'linear', ...
    'Gamma', bestGamma, ...
    'Prior', 'uniform');
% 行注释：这里计算或设置 rows，供后续步骤使用。
rows = [rows; evaluate_stage("Bayes-4", "Regularized Bayes + threshold", ...
    model, XValP, YVal, XTestP, YTest, bestDim, bestGamma, bestThreshold)]; %#ok<AGROW>

% 行注释：这里计算或设置 outDir，供后续步骤使用。
outDir = fullfile(cfg.projectRoot, "results", "visa_pcb");
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(outDir);
% 行注释：这里计算或设置 modelsDir，供后续步骤使用。
modelsDir = fullfile(cfg.projectRoot, "results", "models");
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(modelsDir);

% 行注释：这里计算或设置 csvFile，供后续步骤使用。
csvFile = fullfile(outDir, "bayes_optimization_comparison.csv");
% 行注释：这里计算或设置 optimizationResultsFile，供后续步骤使用。
optimizationResultsFile = fullfile(modelsDir, "visa_pcb_bayes_optimization_results.mat");

% 行注释：这里执行当前语句，完成这一小步处理。
writetable(rows, csvFile);
% 行注释：这里把计算结果保存到文件，便于后续脚本继续使用。
save(optimizationResultsFile, "rows", "prepBase", "coeff", "bestDim", ...
    "bestGamma", "bestThreshold");

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Bayes-only optimization comparison saved: %s\n", csvFile);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：评估某个优化阶段在验证集和测试集上的表现。
% 行注释：这里开始定义 evaluate_stage 函数。
function row = evaluate_stage(stageId, methodName, model, XVal, YVal, XTest, YTest, pcaDim, gamma, threshold)
% 行注释：这里用训练好的模型预测标签或概率分数。
[~, valScoreRaw] = predict(model, XVal);
% 行注释：这里计算或设置 valScore，供后续步骤使用。
valScore = positive_score(model, valScoreRaw);
% 行注释：这里用训练好的模型预测标签或概率分数。
valPred = threshold_predict(valScore, threshold);
% 行注释：这里统一计算准确率、召回率、F1 等分类指标。
valMetrics = classification_metrics(YVal, valPred, valScore, "anomaly");

% 行注释：这里用训练好的模型预测标签或概率分数。
[~, testScoreRaw] = predict(model, XTest);
% 行注释：这里计算或设置 testScore，供后续步骤使用。
testScore = positive_score(model, testScoreRaw);
% 行注释：这里用训练好的模型预测标签或概率分数。
testPred = threshold_predict(testScore, threshold);
% 行注释：这里统一计算准确率、召回率、F1 等分类指标。
testMetrics = classification_metrics(YTest, testPred, testScore, "anomaly");

% 行注释：这里计算或设置 row，供后续步骤使用。
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

% 函数说明：把缺陷概率和阈值比较，转成最终的正常/缺陷标签。
% 行注释：这里开始定义 threshold_predict 函数。
function yPred = threshold_predict(scoreAnomaly, threshold)
% 行注释：这里计算或设置 labels，供后续步骤使用。
labels = repmat("normal", numel(scoreAnomaly), 1);
% 行注释：这里执行当前语句，完成这一小步处理。
labels(scoreAnomaly >= threshold) = "anomaly";
% 行注释：这里计算或设置 yPred，供后续步骤使用。
yPred = categorical(labels, ["normal", "anomaly"]);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：用训练集计算均值和标准差，并完成特征标准化。
% 行注释：这里开始定义 standardize_train 函数。
function [XZ, prep] = standardize_train(X)
% 行注释：这里执行当前语句，完成这一小步处理。
prep.mu = mean(X, 1, 'omitnan');
% 行注释：这里执行当前语句，完成这一小步处理。
prep.sigma = std(X, 0, 1, 'omitnan');
% 行注释：这里执行当前语句，完成这一小步处理。
prep.sigma(prep.sigma == 0 | ~isfinite(prep.sigma)) = 1;
% 行注释：这里计算或设置 XZ，供后续步骤使用。
XZ = (X - prep.mu) ./ prep.sigma;
% 行注释：这里执行当前语句，完成这一小步处理。
XZ(~isfinite(XZ)) = 0;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：把训练阶段得到的标准化参数应用到验证集或测试集。
% 行注释：这里开始定义 standardize_apply 函数。
function XZ = standardize_apply(X, prep)
% 行注释：这里计算或设置 XZ，供后续步骤使用。
XZ = (X - prep.mu) ./ prep.sigma;
% 行注释：这里执行当前语句，完成这一小步处理。
XZ(~isfinite(XZ)) = 0;
% 行注释：这里结束当前的 if、for 或函数代码块。
end
