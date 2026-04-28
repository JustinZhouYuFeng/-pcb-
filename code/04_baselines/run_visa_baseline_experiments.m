% 中文注释：运行 KNN、SVM 等非贝叶斯基线实验，用来对照贝叶斯方法的效果。
% 主要流程：读取同一份特征数据，训练基线分类器，统一计算测试集评价指标。
% 注意事项：该模块用于横向比较，不改变项目主线中的贝叶斯模型结果。

% 函数说明：运行非贝叶斯基线模型，用来和贝叶斯方法做横向对比。
% 行注释：这里开始定义 run_visa_baseline_experiments 函数。
function resultsFile = run_visa_baseline_experiments(featuresFile, cfg)
%RUN_VISA_BASELINE_EXPERIMENTS Compare Bayes with KNN and SVM baselines.

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
% 行注释：这里计算或设置 testMask，供后续步骤使用。
testMask = Split == "test";

% 行注释：这里计算或设置 XTrain，供后续步骤使用。
XTrain = X(trainMask, :);
% 行注释：这里计算或设置 YTrain，供后续步骤使用。
YTrain = Y(trainMask);
% 行注释：这里计算或设置 XTest，供后续步骤使用。
XTest = X(testMask, :);
% 行注释：这里计算或设置 YTest，供后续步骤使用。
YTest = Y(testMask);

% 行注释：这里计算或设置 XTrainZ, prepBase，供后续步骤使用。
[XTrainZ, prepBase] = standardize_train(XTrain);
% 行注释：这里计算或设置 XTestZ，供后续步骤使用。
XTestZ = standardize_apply(XTest, prepBase);

% 行注释：这里做 PCA 降维，减少特征维度并保留主要信息。
[coeff, ~] = pca(XTrainZ);
% 行注释：这里计算或设置 pcaDim，供后续步骤使用。
pcaDim = min(cfg.baselinePCADim, size(coeff, 2));
% 行注释：这里计算或设置 XTrainP，供后续步骤使用。
XTrainP = XTrainZ * coeff(:, 1:pcaDim);
% 行注释：这里计算或设置 XTestP，供后续步骤使用。
XTestP = XTestZ * coeff(:, 1:pcaDim);

% 行注释：这里计算或设置 rows，供后续步骤使用。
rows = table();
% 行注释：这里计算或设置 models，供后续步骤使用。
models = struct();

% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(cfg.knnNeighbors)
    % 行注释：这里计算或设置 k，供后续步骤使用。
    k = cfg.knnNeighbors(i);
    % 行注释：这里训练 KNN 基线模型。
    model = fitcknn(XTrainP, YTrain, ...
        'NumNeighbors', k, ...
        'Distance', 'euclidean', ...
        'Prior', 'uniform', ...
        'Standardize', false);
    % 行注释：这里用训练好的模型预测标签或概率分数。
    [yPred, score] = predict(model, XTestP);
    % 行注释：这里计算或设置 scoreAnomaly，供后续步骤使用。
    scoreAnomaly = positive_score(model, score);
    % 行注释：这里统一计算准确率、召回率、F1 等分类指标。
    metrics = classification_metrics(YTest, yPred, scoreAnomaly, "anomaly");
    % 行注释：这里计算或设置 prefix，供后续步骤使用。
    prefix = table("KNN", pcaDim, k, "euclidean", ...
        'VariableNames', {'ModelName', 'PCADim', 'MainParam', 'Kernel'});
    % 行注释：这里计算或设置 rows，供后续步骤使用。
    rows = [rows; [prefix, metrics]]; %#ok<AGROW>
    % 行注释：这里执行当前语句，完成这一小步处理。
    models.(sprintf("KNN_%d", k)) = model;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里训练 SVM 基线模型。
svmLinear = fitcsvm(XTrainP, YTrain, ...
    'KernelFunction', 'linear', ...
    'Standardize', false, ...
    'Prior', 'uniform', ...
    'ClassNames', categorical(["normal", "anomaly"]));
% 行注释：这里计算或设置 svmLinear，供后续步骤使用。
svmLinear = fitPosterior(svmLinear, XTrainP, YTrain);
% 行注释：这里用训练好的模型预测标签或概率分数。
[yPred, score] = predict(svmLinear, XTestP);
% 行注释：这里计算或设置 scoreAnomaly，供后续步骤使用。
scoreAnomaly = positive_score(svmLinear, score);
% 行注释：这里统一计算准确率、召回率、F1 等分类指标。
metrics = classification_metrics(YTest, yPred, scoreAnomaly, "anomaly");
% 行注释：这里计算或设置 rows，供后续步骤使用。
rows = [rows; [table("SVM", pcaDim, 1, "linear", ...
    'VariableNames', {'ModelName', 'PCADim', 'MainParam', 'Kernel'}), metrics]]; %#ok<AGROW>
% 行注释：这里执行当前语句，完成这一小步处理。
models.SVM_linear = svmLinear;

% 行注释：这里训练 SVM 基线模型。
svmRbf = fitcsvm(XTrainP, YTrain, ...
    'KernelFunction', 'rbf', ...
    'KernelScale', 'auto', ...
    'BoxConstraint', 1, ...
    'Standardize', false, ...
    'Prior', 'uniform', ...
    'ClassNames', categorical(["normal", "anomaly"]));
% 行注释：这里计算或设置 svmRbf，供后续步骤使用。
svmRbf = fitPosterior(svmRbf, XTrainP, YTrain);
% 行注释：这里用训练好的模型预测标签或概率分数。
[yPred, score] = predict(svmRbf, XTestP);
% 行注释：这里计算或设置 scoreAnomaly，供后续步骤使用。
scoreAnomaly = positive_score(svmRbf, score);
% 行注释：这里统一计算准确率、召回率、F1 等分类指标。
metrics = classification_metrics(YTest, yPred, scoreAnomaly, "anomaly");
% 行注释：这里计算或设置 rows，供后续步骤使用。
rows = [rows; [table("SVM", pcaDim, 1, "rbf", ...
    'VariableNames', {'ModelName', 'PCADim', 'MainParam', 'Kernel'}), metrics]]; %#ok<AGROW>
% 行注释：这里执行当前语句，完成这一小步处理。
models.SVM_rbf = svmRbf;

% 行注释：这里计算或设置 outDir，供后续步骤使用。
outDir = fullfile(cfg.projectRoot, "results", "visa_pcb");
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(outDir);
% 行注释：这里计算或设置 modelsDir，供后续步骤使用。
modelsDir = fullfile(cfg.projectRoot, "results", "models");
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(modelsDir);

% 行注释：这里计算或设置 csvFile，供后续步骤使用。
csvFile = fullfile(outDir, "baseline_test_metrics.csv");
% 行注释：这里计算或设置 resultsFile，供后续步骤使用。
resultsFile = fullfile(modelsDir, "visa_pcb_baseline_results.mat");

% 行注释：这里执行当前语句，完成这一小步处理。
writetable(rows, csvFile);
% 行注释：这里把计算结果保存到文件，便于后续脚本继续使用。
save(resultsFile, "models", "rows", "prepBase", "coeff", "pcaDim");

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Baseline metrics saved: %s\n", csvFile);
% 行注释：这里在命令行输出进度或结果提示。
fprintf("Baseline models saved: %s\n", resultsFile);
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
