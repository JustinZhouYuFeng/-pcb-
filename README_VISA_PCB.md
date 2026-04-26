# VisA PCB Bayesian Decision Project

## Goal

This project uses the real-color PCB subsets from the Visual Anomaly dataset
to build and optimize a PCB normal/anomaly binary classifier with Bayesian
decision theory.

Main experiment:

```text
normal PCB image vs anomalous PCB image
```

The project compares only Bayesian decision variants. KNN, SVM, BP and CNN are
not used as the main comparison methods.

## Data Source

Official dataset:

```text
Visual Anomaly (VisA)
AWS Open Data: https://registry.opendata.aws/visa/
Project page: https://github.com/amazon-science/spot-diff
```

The VisA dataset contains 10,821 high-resolution color images:

```text
9,621 normal samples
1,200 anomalous samples
```

PCB subsets:

```text
pcb1, pcb2, pcb3, pcb4
```

## Download

Open PowerShell from the project root and run:

```powershell
.\code\01_preprocessing\download_visa_pcb.ps1
```

The script downloads the official VisA tar file from AWS Open Data and extracts
only the four PCB subsets.

## Run MATLAB Pipeline

In MATLAB, open:

```text
code/run_visa_pcb_bayes_project.m
```

Then run the script. It will:

```text
1. Build metadata for pcb1-pcb4
2. Split data into train/val/test
3. Extract color, gray, edge, GLCM, LBP and HOG features
4. Train Naive Bayes, Gaussian QDA and regularized Gaussian LDA
5. Tune PCA dimension, covariance regularization and posterior threshold
6. Compare the original Bayes classifier with optimized Bayes variants
7. Generate PPT-ready figures
```

## Outputs

```text
data/processed/visa_pcb_binary/visa_pcb_metadata.csv
data/processed/visa_pcb_binary/visa_pcb_features.mat
results/visa_pcb/bayes_validation_grid.csv
results/visa_pcb/bayes_test_best.csv
results/visa_pcb/bayes_optimization_comparison.csv
results/figures/*.png
ppt_materials/visa_pcb/*.png
```

## Suggested Report Title

```text
Bayesian Decision Based Anomaly Detection for Real-Color PCB Images
```

Chinese report title:

```text
基于贝叶斯决策的彩色 PCB 图像异常检测研究
```

## Talking Points

Use Bayesian decision as an interpretable and lightweight pattern recognition
method, not as the strongest industrial model. The experiment should emphasize:

```text
feature engineering
posterior probability
false positive rate
false negative rate
PCA dimensionality reduction
Gaussian probability modeling
covariance regularization
posterior threshold optimization
minimum-risk decision
```
