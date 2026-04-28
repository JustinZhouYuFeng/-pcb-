% 中文注释：统一计算二分类任务的常用评价指标。
% 主要流程：根据真实标签、预测标签和预测分数，统计准确率、精确率、召回率、F1 和 AUC。
% 注意事项：该函数被多个实验脚本复用，保证指标口径一致。

% 函数说明：根据真实标签、预测标签和分数统一计算二分类指标。
% 行注释：这里开始定义 classification_metrics 函数。
function M = classification_metrics(yTrue, yPred, scorePositive, positiveLabel)
%CLASSIFICATION_METRICS Binary classification metrics for PCB anomaly.

% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if nargin < 4
    % 行注释：这里计算或设置 positiveLabel，供后续步骤使用。
    positiveLabel = "anomaly";
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 yTrue，供后续步骤使用。
yTrue = categorical(string(yTrue), ["normal", "anomaly"]);
% 行注释：这里计算或设置 yPred，供后续步骤使用。
yPred = categorical(string(yPred), ["normal", "anomaly"]);
% 行注释：这里计算或设置 positiveLabel，供后续步骤使用。
positiveLabel = categorical(string(positiveLabel), ["normal", "anomaly"]);
% 行注释：这里计算或设置 negativeLabel，供后续步骤使用。
negativeLabel = categorical("normal", ["normal", "anomaly"]);

% 行注释：这里计算或设置 tp，供后续步骤使用。
tp = sum(yTrue == positiveLabel & yPred == positiveLabel);
% 行注释：这里计算或设置 fp，供后续步骤使用。
fp = sum(yTrue == negativeLabel & yPred == positiveLabel);
% 行注释：这里计算或设置 tn，供后续步骤使用。
tn = sum(yTrue == negativeLabel & yPred == negativeLabel);
% 行注释：这里计算或设置 fn，供后续步骤使用。
fn = sum(yTrue == positiveLabel & yPred == negativeLabel);

% 行注释：这里计算或设置 accuracy，供后续步骤使用。
accuracy = safe_div(tp + tn, tp + fp + tn + fn);
% 行注释：这里计算或设置 precision，供后续步骤使用。
precision = safe_div(tp, tp + fp);
% 行注释：这里计算或设置 recall，供后续步骤使用。
recall = safe_div(tp, tp + fn);
% 行注释：这里计算或设置 specificity，供后续步骤使用。
specificity = safe_div(tn, tn + fp);
% 行注释：这里计算或设置 fpr，供后续步骤使用。
fpr = safe_div(fp, fp + tn);
% 行注释：这里计算或设置 fnr，供后续步骤使用。
fnr = safe_div(fn, fn + tp);
% 行注释：这里计算或设置 f1，供后续步骤使用。
f1 = safe_div(2 * precision * recall, precision + recall);
% 行注释：这里计算或设置 iou，供后续步骤使用。
iou = safe_div(tp, tp + fp + fn);
% 行注释：这里计算或设置 balancedAccuracy，供后续步骤使用。
balancedAccuracy = 0.5 * (recall + specificity);

% 行注释：这里计算或设置 auc，供后续步骤使用。
auc = NaN;
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if nargin >= 3 && ~isempty(scorePositive)
    % 行注释：这里开始尝试执行可能出错的代码。
    try
        % 行注释：这里计算或设置 占位输出, 占位输出, 占位输出, auc，供后续步骤使用。
        [~, ~, ~, auc] = perfcurve(yTrue, double(scorePositive), positiveLabel);
    % 行注释：如果 try 中出错，这里负责兜底处理。
    catch
        % 行注释：这里计算或设置 auc，供后续步骤使用。
        auc = NaN;
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 M，供后续步骤使用。
M = table(accuracy, precision, recall, specificity, fpr, fnr, f1, iou, ...
    balancedAccuracy, auc, tp, fp, tn, fn);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：做除法时处理分母为零的情况，避免指标计算报错。
% 行注释：这里开始定义 safe_div 函数。
function value = safe_div(num, den)
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if den == 0
    % 行注释：这里计算或设置 value，供后续步骤使用。
    value = 0;
% 行注释：当前面的条件都不满足时，执行这里的备用逻辑。
else
    % 行注释：这里计算或设置 value，供后续步骤使用。
    value = double(num) / double(den);
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end
