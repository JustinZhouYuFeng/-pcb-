# VisA PCB Experiment Summary

## Task

Main task:

```text
Real-color PCB normal/anomaly binary classification
```

Dataset:

```text
VisA pcb1-pcb4
normal images: 4013
anomaly images: 400
total images used: 4413
```

Data split:

```text
train: 70%
validation: 15%
test: 15%
stratified by PCB subset and label
```

## Feature Design

Each image is resized to 256 x 256 and represented by 1318 handcrafted
features:

```text
RGB/HSV/Lab color statistics
gray-level statistics
Canny and Sobel edge density
GLCM texture features
LBP local texture features
HOG shape/orientation features
```

## Bayesian Decision Models

Compared Bayesian variants:

```text
Naive Bayes
Gaussian QDA
Regularized Gaussian LDA
```

Parameter analysis:

```text
PCA dimensions: 10, 20, 40, 80, 120
regularization gamma: 0, 0.1, 0.3, 0.6, 0.9
posterior threshold: 0.20 to 0.80
```

Best validation setting:

```text
model: Regularized Gaussian LDA
PCA dimension: 80
gamma: 0.1
posterior threshold: 0.75
```

Test metrics:

```text
Accuracy: 0.9184
Precision: 0.5517
Recall: 0.5333
Specificity: 0.9568
FPR: 0.0432
FNR: 0.4667
F1-score: 0.5424
IoU: 0.3721
AUC: 0.8986
```

Confusion matrix on test set:

```text
TP = 32
FP = 26
TN = 576
FN = 28
```

## Bayes-Only Optimization Comparison

This seminar no longer uses KNN, SVM, BP or CNN as the main comparison.
All comparisons are kept inside the Bayesian decision framework.

Optimization stages:

```text
Bayes-0: Original Naive Bayes
Bayes-1: Naive Bayes + PCA
Bayes-2: Gaussian Bayes + PCA
Bayes-3: Regularized Gaussian Bayes
Bayes-4: Regularized Bayes + posterior threshold
```

Test comparison:

```text
Bayes-0  Accuracy=0.7160  F1=0.2879  AUC=0.8000
Bayes-1  Accuracy=0.8761  F1=0.4533  AUC=0.8304
Bayes-2  Accuracy=0.8731  F1=0.4940  AUC=0.9062
Bayes-3  Accuracy=0.8701  F1=0.5000  AUC=0.8986
Bayes-4  Accuracy=0.9184  F1=0.5424  AUC=0.8986
```

## Report Interpretation

The original Naive Bayes classifier has high false-positive pressure because
PCB color, texture and edge features are strongly correlated. PCA reduces
feature redundancy and raises accuracy from 0.7160 to 0.8761. Gaussian Bayes
with covariance modeling improves AUC, showing that weakening the naive
independence assumption is useful. Regularization stabilizes the covariance
estimation and improves recall. Finally, posterior probability threshold tuning
controls the trade-off between false alarms and missed detections.

This supports a strong seminar conclusion:

```text
The project is not a comparison between unrelated classifiers. It studies how
Bayesian decision performance changes after PCA dimensionality reduction,
Gaussian probability modeling, covariance regularization and posterior-risk
threshold optimization.
```

## PPT Figures

Generated figures:

```text
ppt_materials/visa_pcb/基础图_真实电路板样本预览.png
ppt_materials/visa_pcb/基础图_数据集样本统计.png
ppt_materials/visa_pcb/基础图_主成分二维散点图.png
ppt_materials/visa_pcb/基础图_贝叶斯混淆矩阵.png
ppt_materials/visa_pcb/基础图_贝叶斯优化阶段对比.png
ppt_materials/visa_pcb/基础图_后验阈值分析曲线.png
```
