function M = classification_metrics(yTrue, yPred, scorePositive, positiveLabel)
%CLASSIFICATION_METRICS Binary classification metrics for PCB anomaly.

if nargin < 4
    positiveLabel = "anomaly";
end

yTrue = categorical(string(yTrue), ["normal", "anomaly"]);
yPred = categorical(string(yPred), ["normal", "anomaly"]);
positiveLabel = categorical(string(positiveLabel), ["normal", "anomaly"]);
negativeLabel = categorical("normal", ["normal", "anomaly"]);

tp = sum(yTrue == positiveLabel & yPred == positiveLabel);
fp = sum(yTrue == negativeLabel & yPred == positiveLabel);
tn = sum(yTrue == negativeLabel & yPred == negativeLabel);
fn = sum(yTrue == positiveLabel & yPred == negativeLabel);

accuracy = safe_div(tp + tn, tp + fp + tn + fn);
precision = safe_div(tp, tp + fp);
recall = safe_div(tp, tp + fn);
specificity = safe_div(tn, tn + fp);
fpr = safe_div(fp, fp + tn);
fnr = safe_div(fn, fn + tp);
f1 = safe_div(2 * precision * recall, precision + recall);
iou = safe_div(tp, tp + fp + fn);
balancedAccuracy = 0.5 * (recall + specificity);

auc = NaN;
if nargin >= 3 && ~isempty(scorePositive)
    try
        [~, ~, ~, auc] = perfcurve(yTrue, double(scorePositive), positiveLabel);
    catch
        auc = NaN;
    end
end

M = table(accuracy, precision, recall, specificity, fpr, fnr, f1, iou, ...
    balancedAccuracy, auc, tp, fp, tn, fn);
end

function value = safe_div(num, den)
if den == 0
    value = 0;
else
    value = double(num) / double(den);
end
end
