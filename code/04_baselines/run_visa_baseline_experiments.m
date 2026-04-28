% 中文注释：运行 KNN、SVM 等非贝叶斯基线实验，用来对照贝叶斯方法的效果。
% 主要流程：读取同一份特征数据，训练基线分类器，统一计算测试集评价指标。
% 注意事项：该模块用于横向比较，不改变项目主线中的贝叶斯模型结果。

% 函数说明：运行非贝叶斯基线模型，用来和贝叶斯方法做横向对比。
function resultsFile = run_visa_baseline_experiments(featuresFile, cfg)
%RUN_VISA_BASELINE_EXPERIMENTS Compare Bayes with KNN and SVM baselines.

S = load(featuresFile);

X = double(S.X);
Y = categorical(string(S.Y), ["normal", "anomaly"]);
Split = string(S.Split);

trainMask = Split == "train";
testMask = Split == "test";

XTrain = X(trainMask, :);
YTrain = Y(trainMask);
XTest = X(testMask, :);
YTest = Y(testMask);

[XTrainZ, prepBase] = standardize_train(XTrain);
XTestZ = standardize_apply(XTest, prepBase);

[coeff, ~] = pca(XTrainZ);
pcaDim = min(cfg.baselinePCADim, size(coeff, 2));
XTrainP = XTrainZ * coeff(:, 1:pcaDim);
XTestP = XTestZ * coeff(:, 1:pcaDim);

rows = table();
models = struct();

for i = 1:numel(cfg.knnNeighbors)
    k = cfg.knnNeighbors(i);
    model = fitcknn(XTrainP, YTrain, ...
        'NumNeighbors', k, ...
        'Distance', 'euclidean', ...
        'Prior', 'uniform', ...
        'Standardize', false);
    [yPred, score] = predict(model, XTestP);
    scoreAnomaly = positive_score(model, score);
    metrics = classification_metrics(YTest, yPred, scoreAnomaly, "anomaly");
    prefix = table("KNN", pcaDim, k, "euclidean", ...
        'VariableNames', {'ModelName', 'PCADim', 'MainParam', 'Kernel'});
    rows = [rows; [prefix, metrics]]; %#ok<AGROW>
    models.(sprintf("KNN_%d", k)) = model;
end

svmLinear = fitcsvm(XTrainP, YTrain, ...
    'KernelFunction', 'linear', ...
    'Standardize', false, ...
    'Prior', 'uniform', ...
    'ClassNames', categorical(["normal", "anomaly"]));
svmLinear = fitPosterior(svmLinear, XTrainP, YTrain);
[yPred, score] = predict(svmLinear, XTestP);
scoreAnomaly = positive_score(svmLinear, score);
metrics = classification_metrics(YTest, yPred, scoreAnomaly, "anomaly");
rows = [rows; [table("SVM", pcaDim, 1, "linear", ...
    'VariableNames', {'ModelName', 'PCADim', 'MainParam', 'Kernel'}), metrics]]; %#ok<AGROW>
models.SVM_linear = svmLinear;

svmRbf = fitcsvm(XTrainP, YTrain, ...
    'KernelFunction', 'rbf', ...
    'KernelScale', 'auto', ...
    'BoxConstraint', 1, ...
    'Standardize', false, ...
    'Prior', 'uniform', ...
    'ClassNames', categorical(["normal", "anomaly"]));
svmRbf = fitPosterior(svmRbf, XTrainP, YTrain);
[yPred, score] = predict(svmRbf, XTestP);
scoreAnomaly = positive_score(svmRbf, score);
metrics = classification_metrics(YTest, yPred, scoreAnomaly, "anomaly");
rows = [rows; [table("SVM", pcaDim, 1, "rbf", ...
    'VariableNames', {'ModelName', 'PCADim', 'MainParam', 'Kernel'}), metrics]]; %#ok<AGROW>
models.SVM_rbf = svmRbf;

outDir = fullfile(cfg.projectRoot, "results", "visa_pcb");
ensure_dir(outDir);
modelsDir = fullfile(cfg.projectRoot, "results", "models");
ensure_dir(modelsDir);

csvFile = fullfile(outDir, "baseline_test_metrics.csv");
resultsFile = fullfile(modelsDir, "visa_pcb_baseline_results.mat");

writetable(rows, csvFile);
save(resultsFile, "models", "rows", "prepBase", "coeff", "pcaDim");

fprintf("Baseline metrics saved: %s\n", csvFile);
fprintf("Baseline models saved: %s\n", resultsFile);
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
