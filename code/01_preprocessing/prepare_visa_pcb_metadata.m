% 中文注释：扫描 VisA PCB 原始图像目录，并整理训练、验证、测试元数据。
% 主要流程：读取正常/缺陷样本路径、生成标签、按比例划分数据集并保存表格。
% 输出结果：供特征提取脚本读取的 metadata 文件，保证后续实验使用同一份划分。

function metadataFile = prepare_visa_pcb_metadata(cfg)
%PREPARE_VISA_PCB_METADATA Build a train/val/test table for VisA PCB.

rng(cfg.seed);

outDir = fullfile(cfg.projectRoot, "data", "processed", "visa_pcb_binary");
ensure_dir(outDir);
metadataFile = fullfile(outDir, "visa_pcb_metadata.csv");

visaRoot = find_visa_root(cfg.projectRoot);
fprintf("VisA root: %s\n", visaRoot);

imagePaths = strings(0, 1);
labels = strings(0, 1);
subsets = strings(0, 1);
maskPaths = strings(0, 1);

for s = 1:numel(cfg.pcbSubsets)
    subsetName = cfg.pcbSubsets(s);
    subsetRoot = fullfile(visaRoot, subsetName);
    imageRoot = fullfile(subsetRoot, "Data", "Images");
    normalRoot = fullfile(imageRoot, "Normal");
    anomalyRoot = fullfile(imageRoot, "Anomaly");
    maskRoot = fullfile(subsetRoot, "Data", "Masks", "Anomaly");

    normalFiles = list_image_files(normalRoot);
    anomalyFiles = list_image_files(anomalyRoot);

    imagePaths = [imagePaths; normalFiles; anomalyFiles]; %#ok<AGROW>
    labels = [labels; repmat("normal", numel(normalFiles), 1); ...
        repmat("anomaly", numel(anomalyFiles), 1)]; %#ok<AGROW>
    subsets = [subsets; repmat(subsetName, numel(normalFiles) + numel(anomalyFiles), 1)]; %#ok<AGROW>
    maskPaths = [maskPaths; repmat("", numel(normalFiles), 1); ...
        estimate_mask_paths(anomalyFiles, anomalyRoot, maskRoot)]; %#ok<AGROW>

    fprintf("%s: normal=%d, anomaly=%d\n", subsetName, numel(normalFiles), numel(anomalyFiles));
end

if isempty(imagePaths)
    error("No VisA PCB images were found under %s.", visaRoot);
end

T = table(imagePaths, categorical(labels), subsets, maskPaths, ...
    'VariableNames', {'ImagePath', 'Label', 'PCBSubset', 'MaskPath'});

T.Split = stratified_split(T, cfg.valRatio, cfg.testRatio);
T = T(randperm(height(T)), :);

writetable(T, metadataFile);

summaryTable = groupsummary(T, ["PCBSubset", "Label", "Split"]);
disp(summaryTable);
fprintf("Metadata saved: %s\n", metadataFile);
end

function split = stratified_split(T, valRatio, testRatio)
split = strings(height(T), 1);
groupId = findgroups(T.PCBSubset, T.Label);

for g = 1:max(groupId)
    idx = find(groupId == g);
    idx = idx(randperm(numel(idx)));
    n = numel(idx);

    nTest = max(1, round(n * testRatio));
    nVal = max(1, round(n * valRatio));
    nTrain = n - nVal - nTest;

    if nTrain < 1
        nTrain = max(1, n - 2);
        nVal = 1;
        nTest = n - nTrain - nVal;
    end

    split(idx(1:nTrain)) = "train";
    split(idx(nTrain + 1:nTrain + nVal)) = "val";
    split(idx(nTrain + nVal + 1:end)) = "test";
end
end

function maskPaths = estimate_mask_paths(anomalyFiles, anomalyRoot, maskRoot)
maskPaths = strings(numel(anomalyFiles), 1);

if ~isfolder(maskRoot)
    return;
end

for i = 1:numel(anomalyFiles)
    rel = erase(anomalyFiles(i), string(anomalyRoot) + filesep);
    [relFolder, baseName, ~] = fileparts(rel);
    candidates = dir(fullfile(maskRoot, relFolder, baseName + ".*"));
    if ~isempty(candidates)
        maskPaths(i) = string(fullfile(candidates(1).folder, candidates(1).name));
    end
end
end
