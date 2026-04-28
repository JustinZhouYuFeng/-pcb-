% 中文注释：运行 PCB 缺陷检测的基础贝叶斯分类实验。
% 主要流程：加载特征、估计类别先验和类条件分布、计算后验概率并按阈值判别。
% 输出结果：保存准确率、召回率、F1、AUC 等指标，用于评估贝叶斯决策效果。

% 函数说明：训练并评估基础贝叶斯模型，输出不同参数和阈值下的分类指标。
% 行注释：这里开始定义 run_visa_bayes_experiments 函数。
function resultsFile = run_visa_bayes_experiments(featuresFile, cfg)
%RUN_VISA_BAYES_EXPERIMENTS Train Bayes decision models and tune threshold.

% 行注释：这里从磁盘读取前面步骤保存的数据文件。
S = load(featuresFile);

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
[coeff, ~, ~, ~, explained] = pca(XTrainZ);
% 行注释：这里计算或设置 maxDim，供后续步骤使用。
maxDim = size(coeff, 2);

% 行注释：这里计算或设置 valRows，供后续步骤使用。
valRows = table();

% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for p = 1:numel(cfg.pcaDims)
    % 行注释：这里计算或设置 pcaDim，供后续步骤使用。
    pcaDim = min(cfg.pcaDims(p), maxDim);
    % 行注释：这里计算或设置 XTrainP，供后续步骤使用。
    XTrainP = XTrainZ * coeff(:, 1:pcaDim);
    % 行注释：这里计算或设置 XValP，供后续步骤使用。
    XValP = XValZ * coeff(:, 1:pcaDim);

    % 行注释：这里训练朴素贝叶斯分类器。
    model = fitcnb(XTrainP, YTrain, ...
        'DistributionNames', 'normal', ...
        'Prior', 'uniform');
    % 行注释：这里用训练好的模型预测标签或概率分数。
    [~, scoreVal] = predict(model, XValP);
    % 行注释：这里计算或设置 scoreAnomaly，供后续步骤使用。
    scoreAnomaly = positive_score(model, scoreVal);
    % 行注释：这里计算或设置 valRows，供后续步骤使用。
    valRows = [valRows; threshold_rows("NaiveBayes", pcaDim, NaN, ...
        cfg.decisionThresholds, YVal, scoreAnomaly)]; %#ok<AGROW>

    % 行注释：这里训练判别分析形式的贝叶斯分类器。
    model = fitcdiscr(XTrainP, YTrain, ...
        'DiscrimType', 'pseudoQuadratic', ...
        'Prior', 'uniform');
    % 行注释：这里用训练好的模型预测标签或概率分数。
    [~, scoreVal] = predict(model, XValP);
    % 行注释：这里计算或设置 scoreAnomaly，供后续步骤使用。
    scoreAnomaly = positive_score(model, scoreVal);
    % 行注释：这里计算或设置 valRows，供后续步骤使用。
    valRows = [valRows; threshold_rows("GaussianQDA", pcaDim, NaN, ...
        cfg.decisionThresholds, YVal, scoreAnomaly)]; %#ok<AGROW>

    % 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
    for g = 1:numel(cfg.bayesGammas)
        % 行注释：这里计算或设置 gamma，供后续步骤使用。
        gamma = cfg.bayesGammas(g);
        % 行注释：这里训练判别分析形式的贝叶斯分类器。
        model = fitcdiscr(XTrainP, YTrain, ...
            'DiscrimType', 'linear', ...
            'Gamma', gamma, ...
            'Prior', 'uniform');
        % 行注释：这里用训练好的模型预测标签或概率分数。
        [~, scoreVal] = predict(model, XValP);
        % 行注释：这里计算或设置 scoreAnomaly，供后续步骤使用。
        scoreAnomaly = positive_score(model, scoreVal);
        % 行注释：这里计算或设置 valRows，供后续步骤使用。
        valRows = [valRows; threshold_rows("RegularizedGaussianLDA", pcaDim, gamma, ...
            cfg.decisionThresholds, YVal, scoreAnomaly)]; %#ok<AGROW>
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 selectionScore，供后续步骤使用。
selectionScore = valRows.f1 + 1e-3 * valRows.recall + 1e-6 * valRows.specificity;
% 行注释：这里计算或设置 占位输出, bestIdx，供后续步骤使用。
[~, bestIdx] = max(selectionScore);
% 行注释：这里计算或设置 bestSpec，供后续步骤使用。
bestSpec = valRows(bestIdx, :);

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Best Bayes validation setting:\n");
% 行注释：这里把关键表格或变量显示出来，方便检查。
disp(bestSpec(:, ["ModelName", "PCADim", "Gamma", "Threshold", ...
    "accuracy", "precision", "recall", "f1", "auc"]));

% 行注释：这里计算或设置 bestModel, prep，供后续步骤使用。
[bestModel, prep] = train_selected_bayes_model(XTrainZ, YTrain, coeff, bestSpec);

% 行注释：这里计算或设置 testScore，供后续步骤使用。
testScore = predict_anomaly_score(bestModel, XTestZ, prep);
% 行注释：这里用训练好的模型预测标签或概率分数。
testPred = threshold_predict(testScore, bestSpec.Threshold);
% 行注释：这里统一计算准确率、召回率、F1 等分类指标。
testMetrics = classification_metrics(YTest, testPred, testScore, "anomaly");
% 行注释：这里计算或设置 testResults，供后续步骤使用。
testResults = [bestSpec(:, ["ModelName", "PCADim", "Gamma", "Threshold"]), testMetrics];

% 行注释：这里计算或设置 valScore，供后续步骤使用。
valScore = predict_anomaly_score(bestModel, XValZ, prep);
% 行注释：这里用训练好的模型预测标签或概率分数。
valPred = threshold_predict(valScore, bestSpec.Threshold);
% 行注释：这里统一计算准确率、召回率、F1 等分类指标。
valMetricsBest = classification_metrics(YVal, valPred, valScore, "anomaly");
% 行注释：这里计算或设置 valBestResults，供后续步骤使用。
valBestResults = [bestSpec(:, ["ModelName", "PCADim", "Gamma", "Threshold"]), valMetricsBest];

% 行注释：这里计算或设置 outDir，供后续步骤使用。
outDir = fullfile(cfg.projectRoot, "results", "visa_pcb");
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(outDir);
% 行注释：这里计算或设置 modelsDir，供后续步骤使用。
modelsDir = fullfile(cfg.projectRoot, "results", "models");
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(modelsDir);

% 行注释：这里计算或设置 validationCsv，供后续步骤使用。
validationCsv = fullfile(outDir, "bayes_validation_grid.csv");
% 行注释：这里计算或设置 testCsv，供后续步骤使用。
testCsv = fullfile(outDir, "bayes_test_best.csv");
% 行注释：这里计算或设置 valBestCsv，供后续步骤使用。
valBestCsv = fullfile(outDir, "bayes_validation_best.csv");
% 行注释：这里计算或设置 resultsFile，供后续步骤使用。
resultsFile = fullfile(modelsDir, "visa_pcb_bayes_results.mat");

% 行注释：这里执行当前语句，完成这一小步处理。
writetable(valRows, validationCsv);
% 行注释：这里执行当前语句，完成这一小步处理。
writetable(testResults, testCsv);
% 行注释：这里执行当前语句，完成这一小步处理。
writetable(valBestResults, valBestCsv);

% 行注释：这里把计算结果保存到文件，便于后续脚本继续使用。
save(resultsFile, "bestModel", "prep", "prepBase", "coeff", "explained", ...
    "bestSpec", "valRows", "testResults", "valBestResults");

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Bayes validation grid saved: %s\n", validationCsv);
% 行注释：这里在命令行输出进度或结果提示。
fprintf("Bayes best test metrics saved: %s\n", testCsv);
% 行注释：这里在命令行输出进度或结果提示。
fprintf("Bayes model saved: %s\n", resultsFile);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：把一组阈值逐个试一遍，记录每个阈值对应的评价结果。
% 行注释：这里开始定义 threshold_rows 函数。
function rows = threshold_rows(modelName, pcaDim, gamma, thresholds, yTrue, scoreAnomaly)
% 行注释：这里计算或设置 rows，供后续步骤使用。
rows = table();
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for t = 1:numel(thresholds)
    % 行注释：这里计算或设置 threshold，供后续步骤使用。
    threshold = thresholds(t);
    % 行注释：这里用训练好的模型预测标签或概率分数。
    yPred = threshold_predict(scoreAnomaly, threshold);
    % 行注释：这里统一计算准确率、召回率、F1 等分类指标。
    metrics = classification_metrics(yTrue, yPred, scoreAnomaly, "anomaly");
    % 行注释：这里计算或设置 prefix，供后续步骤使用。
    prefix = table(string(modelName), pcaDim, gamma, threshold, ...
        'VariableNames', {'ModelName', 'PCADim', 'Gamma', 'Threshold'});
    % 行注释：这里计算或设置 rows，供后续步骤使用。
    rows = [rows; [prefix, metrics]]; %#ok<AGROW>
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：按指定 PCA 维数和正则化参数训练贝叶斯分类器。
% 行注释：这里开始定义 train_selected_bayes_model 函数。
function [model, prep] = train_selected_bayes_model(XTrainZ, YTrain, coeff, spec)
% 行注释：这里计算或设置 pcaDim，供后续步骤使用。
pcaDim = spec.PCADim;
% 行注释：这里计算或设置 XTrainP，供后续步骤使用。
XTrainP = XTrainZ * coeff(:, 1:pcaDim);
% 行注释：这里计算或设置 prep，供后续步骤使用。
prep = struct();
% 行注释：这里执行当前语句，完成这一小步处理。
prep.coeff = coeff;
% 行注释：这里执行当前语句，完成这一小步处理。
prep.pcaDim = pcaDim;

% 行注释：这里根据变量取值选择不同处理分支。
switch string(spec.ModelName)
    % 行注释：这里处理 switch 中的一个具体取值情况。
    case "NaiveBayes"
        % 行注释：这里训练朴素贝叶斯分类器。
        model = fitcnb(XTrainP, YTrain, ...
            'DistributionNames', 'normal', ...
            'Prior', 'uniform');
    % 行注释：这里处理 switch 中的一个具体取值情况。
    case "GaussianQDA"
        % 行注释：这里训练判别分析形式的贝叶斯分类器。
        model = fitcdiscr(XTrainP, YTrain, ...
            'DiscrimType', 'pseudoQuadratic', ...
            'Prior', 'uniform');
    % 行注释：这里处理 switch 中的一个具体取值情况。
    case "RegularizedGaussianLDA"
        % 行注释：这里训练判别分析形式的贝叶斯分类器。
        model = fitcdiscr(XTrainP, YTrain, ...
            'DiscrimType', 'linear', ...
            'Gamma', spec.Gamma, ...
            'Prior', 'uniform');
    % 行注释：这里执行当前语句，完成这一小步处理。
    otherwise
        % 行注释：这里执行当前语句，完成这一小步处理。
        error("Unknown Bayes model: %s", string(spec.ModelName));
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：用训练好的模型预测样本为缺陷的概率分数。
% 行注释：这里开始定义 predict_anomaly_score 函数。
function scoreAnomaly = predict_anomaly_score(model, XZ, prep)
% 行注释：这里计算或设置 XP，供后续步骤使用。
XP = XZ * prep.coeff(:, 1:prep.pcaDim);
% 行注释：这里用训练好的模型预测标签或概率分数。
[~, score] = predict(model, XP);
% 行注释：这里计算或设置 scoreAnomaly，供后续步骤使用。
scoreAnomaly = positive_score(model, score);
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
