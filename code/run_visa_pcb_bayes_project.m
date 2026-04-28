% 中文注释：整个 VisA PCB 贝叶斯缺陷检测项目的 MATLAB 主入口。
% 主要流程：依次完成元数据准备、特征提取、贝叶斯实验、优化对比和可视化生成。
% 使用目的：一键复现实验流程，方便在汇报或答辩前重新生成全部结果。

%% VisA PCB Bayesian decision project
% Main task:
%   Binary classification for real color PCB images: normal vs anomaly.
%
% Run this file after downloading/extracting the VisA PCB subsets with:
%   code/01_preprocessing/download_visa_pcb.ps1

clear; clc; close all;

codeDir = fileparts(mfilename("fullpath"));
projectRoot = fileparts(codeDir);
addpath(genpath(codeDir));

cfg = struct();
cfg.projectRoot = projectRoot;
cfg.seed = 42;
cfg.pcbSubsets = ["pcb1", "pcb2", "pcb3", "pcb4"];
cfg.imageSize = [256 256];
cfg.valRatio = 0.15;
cfg.testRatio = 0.15;
cfg.forceFeatureExtraction = false;

% Bayes parameter analysis.
cfg.pcaDims = [10 20 40 80 120];
cfg.bayesGammas = [0 0.1 0.3 0.6 0.9];
cfg.decisionThresholds = 0.20:0.05:0.80;

fprintf("Project root: %s\n", projectRoot);
fprintf("Preparing VisA PCB metadata...\n");
metadataFile = prepare_visa_pcb_metadata(cfg);

fprintf("Extracting image features...\n");
featuresFile = extract_visa_pcb_features(metadataFile, cfg);

fprintf("Running Bayesian decision experiments...\n");
bayesResultsFile = run_visa_bayes_experiments(featuresFile, cfg);

fprintf("Running Bayes-only optimization comparison...\n");
optimizationResultsFile = run_visa_bayes_optimization_comparison(featuresFile, bayesResultsFile, cfg);

fprintf("Creating visualization figures...\n");
make_visa_pcb_visuals(featuresFile, bayesResultsFile, optimizationResultsFile, cfg);
make_visa_pcb_polished_visuals(featuresFile, bayesResultsFile, optimizationResultsFile, cfg);
make_bayes_theory_chinese_visuals(featuresFile, bayesResultsFile, cfg);

fprintf("\nDone. Check these folders:\n");
fprintf("  results/visa_pcb\n");
fprintf("  results/figures\n");
fprintf("  ppt_materials/visa_pcb\n");
