% 中文注释：运行 PCB 缺陷检测的基础贝叶斯分类实验。
% 主要流程：加载特征、估计类别先验和类条件分布、计算后验概率并按阈值判别。
% 输出结果：保存准确率、召回率、F1、AUC 等指标，用于评估贝叶斯决策效果。

% 函数说明：训练并评估基础贝叶斯模型，输出不同参数和阈值下的分类指标。
function resultsFile = run_visa_bayes_experiments(featuresFile, cfg)
%RUN_VISA_BAYES_EXPERIMENTS Train Bayes decision models and tune threshold.

S = load(featuresFile);

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

[coeff, ~, ~, ~, explained] = pca(XTrainZ);
maxDim = size(coeff, 2);

valRows = table();

for p = 1:numel(cfg.pcaDims)
    pcaDim = min(cfg.pcaDims(p), maxDim);
    XTrainP = XTrainZ * coeff(:, 1:pcaDim);
    XValP = XValZ * coeff(:, 1:pcaDim);

    model = fitcnb(XTrainP, YTrain, ...
        'DistributionNames', 'normal', ...
        'Prior', 'uniform');
    [~, scoreVal] = predict(model, XValP);
    scoreAnomaly = positive_score(model, scoreVal);
    valRows = [valRows; threshold_rows("NaiveBayes", pcaDim, NaN, ...
        cfg.decisionThresholds, YVal, scoreAnomaly)]; %#ok<AGROW>

    model = fitcdiscr(XTrainP, YTrain, ...
        'DiscrimType', 'pseudoQuadratic', ...
        'Prior', 'uniform');
    [~, scoreVal] = predict(model, XValP);
    scoreAnomaly = positive_score(model, scoreVal);
    valRows = [valRows; threshold_rows("GaussianQDA", pcaDim, NaN, ...
        cfg.decisionThresholds, YVal, scoreAnomaly)]; %#ok<AGROW>

    for g = 1:numel(cfg.bayesGammas)
        gamma = cfg.bayesGammas(g);
        model = fitcdiscr(XTrainP, YTrain, ...
            'DiscrimType', 'linear', ...
            'Gamma', gamma, ...
            'Prior', 'uniform');
        [~, scoreVal] = predict(model, XValP);
        scoreAnomaly = positive_score(model, scoreVal);
        valRows = [valRows; threshold_rows("RegularizedGaussianLDA", pcaDim, gamma, ...
            cfg.decisionThresholds, YVal, scoreAnomaly)]; %#ok<AGROW>
    end
end

selectionScore = valRows.f1 + 1e-3 * valRows.recall + 1e-6 * valRows.specificity;
[~, bestIdx] = max(selectionScore);
bestSpec = valRows(bestIdx, :);

fprintf("Best Bayes validation setting:\n");
disp(bestSpec(:, ["ModelName", "PCADim", "Gamma", "Threshold", ...
    "accuracy", "precision", "recall", "f1", "auc"]));

[bestModel, prep] = train_selected_bayes_model(XTrainZ, YTrain, coeff, bestSpec);

testScore = predict_anomaly_score(bestModel, XTestZ, prep);
testPred = threshold_predict(testScore, bestSpec.Threshold);
testMetrics = classification_metrics(YTest, testPred, testScore, "anomaly");
testResults = [bestSpec(:, ["ModelName", "PCADim", "Gamma", "Threshold"]), testMetrics];

valScore = predict_anomaly_score(bestModel, XValZ, prep);
valPred = threshold_predict(valScore, bestSpec.Threshold);
valMetricsBest = classification_metrics(YVal, valPred, valScore, "anomaly");
valBestResults = [bestSpec(:, ["ModelName", "PCADim", "Gamma", "Threshold"]), valMetricsBest];

outDir = fullfile(cfg.projectRoot, "results", "visa_pcb");
ensure_dir(outDir);
modelsDir = fullfile(cfg.projectRoot, "results", "models");
ensure_dir(modelsDir);

validationCsv = fullfile(outDir, "bayes_validation_grid.csv");
testCsv = fullfile(outDir, "bayes_test_best.csv");
valBestCsv = fullfile(outDir, "bayes_validation_best.csv");
resultsFile = fullfile(modelsDir, "visa_pcb_bayes_results.mat");

writetable(valRows, validationCsv);
writetable(testResults, testCsv);
writetable(valBestResults, valBestCsv);

save(resultsFile, "bestModel", "prep", "prepBase", "coeff", "explained", ...
    "bestSpec", "valRows", "testResults", "valBestResults");

fprintf("Bayes validation grid saved: %s\n", validationCsv);
fprintf("Bayes best test metrics saved: %s\n", testCsv);
fprintf("Bayes model saved: %s\n", resultsFile);
end

% 函数说明：把一组阈值逐个试一遍，记录每个阈值对应的评价结果。
function rows = threshold_rows(modelName, pcaDim, gamma, thresholds, yTrue, scoreAnomaly)
rows = table();
for t = 1:numel(thresholds)
    threshold = thresholds(t);
    yPred = threshold_predict(scoreAnomaly, threshold);
    metrics = classification_metrics(yTrue, yPred, scoreAnomaly, "anomaly");
    prefix = table(string(modelName), pcaDim, gamma, threshold, ...
        'VariableNames', {'ModelName', 'PCADim', 'Gamma', 'Threshold'});
    rows = [rows; [prefix, metrics]]; %#ok<AGROW>
end
end

% 函数说明：按指定 PCA 维数和正则化参数训练贝叶斯分类器。
function [model, prep] = train_selected_bayes_model(XTrainZ, YTrain, coeff, spec)
pcaDim = spec.PCADim;
XTrainP = XTrainZ * coeff(:, 1:pcaDim);
prep = struct();
prep.coeff = coeff;
prep.pcaDim = pcaDim;

switch string(spec.ModelName)
    case "NaiveBayes"
        model = fitcnb(XTrainP, YTrain, ...
            'DistributionNames', 'normal', ...
            'Prior', 'uniform');
    case "GaussianQDA"
        model = fitcdiscr(XTrainP, YTrain, ...
            'DiscrimType', 'pseudoQuadratic', ...
            'Prior', 'uniform');
    case "RegularizedGaussianLDA"
        model = fitcdiscr(XTrainP, YTrain, ...
            'DiscrimType', 'linear', ...
            'Gamma', spec.Gamma, ...
            'Prior', 'uniform');
    otherwise
        error("Unknown Bayes model: %s", string(spec.ModelName));
end
end

% 函数说明：用训练好的模型预测样本为缺陷的概率分数。
function scoreAnomaly = predict_anomaly_score(model, XZ, prep)
XP = XZ * prep.coeff(:, 1:prep.pcaDim);
[~, score] = predict(model, XP);
scoreAnomaly = positive_score(model, score);
end

% 函数说明：从模型输出的多列概率中取出“缺陷”这一类的概率。
function scoreAnomaly = positive_score(model, score)
classNames = string(model.ClassNames);
posCol = find(classNames == "anomaly", 1);
if isempty(posCol)
    error("The model does not contain an anomaly class.");
end
scoreAnomaly = score(:, posCol);
end

% 函数说明：把缺陷概率和阈值比较，转成最终的正常/缺陷标签。
function yPred = threshold_predict(scoreAnomaly, threshold)
labels = repmat("normal", numel(scoreAnomaly), 1);
labels(scoreAnomaly >= threshold) = "anomaly";
yPred = categorical(labels, ["normal", "anomaly"]);
end

% 函数说明：用训练集计算均值和标准差，并完成特征标准化。
function [XZ, prep] = standardize_train(X)
prep.mu = mean(X, 1, 'omitnan');
prep.sigma = std(X, 0, 1, 'omitnan');
prep.sigma(prep.sigma == 0 | ~isfinite(prep.sigma)) = 1;
XZ = (X - prep.mu) ./ prep.sigma;
XZ(~isfinite(XZ)) = 0;
end

% 函数说明：把训练阶段得到的标准化参数应用到验证集或测试集。
function XZ = standardize_apply(X, prep)
XZ = (X - prep.mu) ./ prep.sigma;
XZ(~isfinite(XZ)) = 0;
end
