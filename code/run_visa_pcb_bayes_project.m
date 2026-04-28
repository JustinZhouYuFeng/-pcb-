% 中文注释：整个 VisA PCB 贝叶斯缺陷检测项目的 MATLAB 主入口。
% 主要流程：依次完成元数据准备、特征提取、贝叶斯实验、优化对比和可视化生成。
% 使用目的：一键复现实验流程，方便在汇报或答辩前重新生成全部结果。

%% VisA PCB Bayesian decision project
% Main task:
%   Binary classification for real color PCB images: normal vs anomaly.
%
% Run this file after downloading/extracting the VisA PCB subsets with:
%   code/01_preprocessing/download_visa_pcb.ps1

% 行注释：这里执行当前语句，完成这一小步处理。
clear; clc; close all;

% 行注释：这里计算或设置 codeDir，供后续步骤使用。
codeDir = fileparts(mfilename("fullpath"));
% 行注释：这里计算或设置 projectRoot，供后续步骤使用。
projectRoot = fileparts(codeDir);
% 行注释：这里执行当前语句，完成这一小步处理。
addpath(genpath(codeDir));

% 模块说明：集中配置项目路径、随机种子、图像尺寸和数据划分比例。
% 行注释：这里计算或设置 cfg，供后续步骤使用。
cfg = struct();
% 行注释：这里执行当前语句，完成这一小步处理。
cfg.projectRoot = projectRoot;
% 行注释：这里执行当前语句，完成这一小步处理。
cfg.seed = 42;
% 行注释：这里执行当前语句，完成这一小步处理。
cfg.pcbSubsets = ["pcb1", "pcb2", "pcb3", "pcb4"];
% 行注释：这里执行当前语句，完成这一小步处理。
cfg.imageSize = [256 256];
% 行注释：这里执行当前语句，完成这一小步处理。
cfg.valRatio = 0.15;
% 行注释：这里执行当前语句，完成这一小步处理。
cfg.testRatio = 0.15;
% 行注释：这里执行当前语句，完成这一小步处理。
cfg.forceFeatureExtraction = false;

% Bayes parameter analysis.
% 模块说明：配置要比较的 PCA 维数、贝叶斯正则化参数和判别阈值。
% 行注释：这里执行当前语句，完成这一小步处理。
cfg.pcaDims = [10 20 40 80 120];
% 行注释：这里执行当前语句，完成这一小步处理。
cfg.bayesGammas = [0 0.1 0.3 0.6 0.9];
% 行注释：这里执行当前语句，完成这一小步处理。
cfg.decisionThresholds = 0.20:0.05:0.80;

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Project root: %s\n", projectRoot);
% 行注释：这里在命令行输出进度或结果提示。
fprintf("Preparing VisA PCB metadata...\n");
% 模块说明：第一步整理数据清单，为后续步骤提供统一输入。
% 行注释：这里计算或设置 metadataFile，供后续步骤使用。
metadataFile = prepare_visa_pcb_metadata(cfg);

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Extracting image features...\n");
% 模块说明：第二步把图像转成数值特征，模型不能直接处理原始图片。
% 行注释：这里计算或设置 featuresFile，供后续步骤使用。
featuresFile = extract_visa_pcb_features(metadataFile, cfg);

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Running Bayesian decision experiments...\n");
% 模块说明：第三步训练和评估贝叶斯模型，得到核心实验结果。
% 行注释：这里计算或设置 bayesResultsFile，供后续步骤使用。
bayesResultsFile = run_visa_bayes_experiments(featuresFile, cfg);

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Running Bayes-only optimization comparison...\n");
% 模块说明：第四步比较不同优化策略，说明最终方案为什么更好。
% 行注释：这里计算或设置 optimizationResultsFile，供后续步骤使用。
optimizationResultsFile = run_visa_bayes_optimization_comparison(featuresFile, bayesResultsFile, cfg);

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Creating visualization figures...\n");
% 模块说明：第五步把结果画成图，方便写报告和制作 PPT。
% 行注释：这里执行当前语句，完成这一小步处理。
make_visa_pcb_visuals(featuresFile, bayesResultsFile, optimizationResultsFile, cfg);
% 行注释：这里执行当前语句，完成这一小步处理。
make_visa_pcb_polished_visuals(featuresFile, bayesResultsFile, optimizationResultsFile, cfg);
% 行注释：这里执行当前语句，完成这一小步处理。
make_bayes_theory_chinese_visuals(featuresFile, bayesResultsFile, cfg);

% 行注释：这里在命令行输出进度或结果提示。
fprintf("\nDone. Check these folders:\n");
% 行注释：这里在命令行输出进度或结果提示。
fprintf("  results/visa_pcb\n");
% 行注释：这里在命令行输出进度或结果提示。
fprintf("  results/figures\n");
% 行注释：这里在命令行输出进度或结果提示。
fprintf("  ppt_materials/visa_pcb\n");
