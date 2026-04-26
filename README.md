# 基于贝叶斯决策的 PCB 缺陷检测

本项目是模式识别课程研讨实验，面向电子信息方向的 PCB 真实图像缺陷检测任务。项目使用 VisA PCB 真实彩色图像，将 normal / anomaly 设置为二分类问题，并在贝叶斯分类框架内进行逐步优化。

## 项目主线

```text
PCB 图像
→ 1318 维手工特征
→ 贝叶斯后验概率 P(缺陷|x)
→ PCA / Gamma / 阈值 T 优化
→ 多指标性能评估与可视化汇报
```

## 方法设计

- **Bayes-0**：原始朴素贝叶斯
- **Bayes-1**：朴素贝叶斯 + PCA 特征空间优化
- **Bayes-2**：高斯贝叶斯建模优化
- **Bayes-3**：Gamma 正则化优化
- **Bayes-4**：正则化贝叶斯 + 后验阈值优化

## 特征构成

每张 PCB 图像提取为 1318 维特征向量，包含：

- 颜色统计特征：RGB / HSV / Lab
- 灰度统计特征：均值、方差、熵、分位数等
- 边缘密度特征：Canny / Sobel
- GLCM 纹理特征：Contrast、Correlation、Energy、Homogeneity
- LBP 局部纹理特征
- HOG 梯度结构特征

## 关键结果

最终优化模型 Bayes-4 在测试集上的核心结果：

| 指标 | 数值 |
| --- | ---: |
| Accuracy | 0.918 |
| F1-score | 0.542 |
| AUC | 0.899 |
| IoU | 0.372 |

## 目录说明

- `code/`：MATLAB 实验代码
- `results/`：实验结果表格和可视化图
- `ppt_materials/`：PPT 可用图表素材
- `image2_report_pages/`：用 image 模型生成的整套汇报图片页
- `image_report_pages/`：本地脚本生成的整套汇报图片页
- `references/`：参考资料
- `notes/`：项目笔记

## 数据说明

由于原始数据集和 `.mat` 特征文件较大，仓库默认不上传：

- `data/raw/`
- `data/processed/**/*.mat`
- `results/models/`

如需复现实验，请先准备 VisA PCB 数据集，并运行：

```matlab
code/run_visa_pcb_bayes_project.m
```

## 汇报亮点

本项目强调：

- 与电子信息方向相关的真实 PCB 缺陷检测场景
- 贝叶斯后验概率的可解释决策过程
- PCA、Gamma、后验阈值三类参数优化
- Accuracy、Precision、Recall、F1、IoU、AUC、FPR、FNR 等多指标评价
- 高质量中文图表和汇报图片页

