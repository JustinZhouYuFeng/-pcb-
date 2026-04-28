% 中文注释：扫描 VisA PCB 原始图像目录，并整理训练、验证、测试元数据。
% 主要流程：读取正常/缺陷样本路径、生成标签、按比例划分数据集并保存表格。
% 输出结果：供特征提取脚本读取的 metadata 文件，保证后续实验使用同一份划分。

% 函数说明：整理 PCB 数据集清单，把每张图的路径、标签和所属划分保存下来。
% 行注释：这里开始定义 prepare_visa_pcb_metadata 函数。
function metadataFile = prepare_visa_pcb_metadata(cfg)
%PREPARE_VISA_PCB_METADATA Build a train/val/test table for VisA PCB.

% 行注释：这里执行当前语句，完成这一小步处理。
rng(cfg.seed);

% 行注释：这里计算或设置 outDir，供后续步骤使用。
outDir = fullfile(cfg.projectRoot, "data", "processed", "visa_pcb_binary");
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(outDir);
% 行注释：这里计算或设置 metadataFile，供后续步骤使用。
metadataFile = fullfile(outDir, "visa_pcb_metadata.csv");

% 行注释：这里计算或设置 visaRoot，供后续步骤使用。
visaRoot = find_visa_root(cfg.projectRoot);
% 行注释：这里在命令行输出进度或结果提示。
fprintf("VisA root: %s\n", visaRoot);

% 行注释：这里计算或设置 imagePaths，供后续步骤使用。
imagePaths = strings(0, 1);
% 行注释：这里计算或设置 labels，供后续步骤使用。
labels = strings(0, 1);
% 行注释：这里计算或设置 subsets，供后续步骤使用。
subsets = strings(0, 1);
% 行注释：这里计算或设置 maskPaths，供后续步骤使用。
maskPaths = strings(0, 1);

% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for s = 1:numel(cfg.pcbSubsets)
    % 行注释：这里计算或设置 subsetName，供后续步骤使用。
    subsetName = cfg.pcbSubsets(s);
    % 行注释：这里计算或设置 subsetRoot，供后续步骤使用。
    subsetRoot = fullfile(visaRoot, subsetName);
    % 行注释：这里计算或设置 imageRoot，供后续步骤使用。
    imageRoot = fullfile(subsetRoot, "Data", "Images");
    % 行注释：这里计算或设置 normalRoot，供后续步骤使用。
    normalRoot = fullfile(imageRoot, "Normal");
    % 行注释：这里计算或设置 anomalyRoot，供后续步骤使用。
    anomalyRoot = fullfile(imageRoot, "Anomaly");
    % 行注释：这里计算或设置 maskRoot，供后续步骤使用。
    maskRoot = fullfile(subsetRoot, "Data", "Masks", "Anomaly");

    % 行注释：这里计算或设置 normalFiles，供后续步骤使用。
    normalFiles = list_image_files(normalRoot);
    % 行注释：这里计算或设置 anomalyFiles，供后续步骤使用。
    anomalyFiles = list_image_files(anomalyRoot);

    % 行注释：这里计算或设置 imagePaths，供后续步骤使用。
    imagePaths = [imagePaths; normalFiles; anomalyFiles]; %#ok<AGROW>
    % 行注释：这里计算或设置 labels，供后续步骤使用。
    labels = [labels; repmat("normal", numel(normalFiles), 1); ...
        repmat("anomaly", numel(anomalyFiles), 1)]; %#ok<AGROW>
    % 行注释：这里计算或设置 subsets，供后续步骤使用。
    subsets = [subsets; repmat(subsetName, numel(normalFiles) + numel(anomalyFiles), 1)]; %#ok<AGROW>
    % 行注释：这里计算或设置 maskPaths，供后续步骤使用。
    maskPaths = [maskPaths; repmat("", numel(normalFiles), 1); ...
        estimate_mask_paths(anomalyFiles, anomalyRoot, maskRoot)]; %#ok<AGROW>

    % 行注释：这里在命令行输出进度或结果提示。
    fprintf("%s: normal=%d, anomaly=%d\n", subsetName, numel(normalFiles), numel(anomalyFiles));
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if isempty(imagePaths)
    % 行注释：这里执行当前语句，完成这一小步处理。
    error("No VisA PCB images were found under %s.", visaRoot);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 T，供后续步骤使用。
T = table(imagePaths, categorical(labels), subsets, maskPaths, ...
    'VariableNames', {'ImagePath', 'Label', 'PCBSubset', 'MaskPath'});

% 行注释：这里执行当前语句，完成这一小步处理。
T.Split = stratified_split(T, cfg.valRatio, cfg.testRatio);
% 行注释：这里计算或设置 T，供后续步骤使用。
T = T(randperm(height(T)), :);

% 行注释：这里执行当前语句，完成这一小步处理。
writetable(T, metadataFile);

% 行注释：这里计算或设置 summaryTable，供后续步骤使用。
summaryTable = groupsummary(T, ["PCBSubset", "Label", "Split"]);
% 行注释：这里把关键表格或变量显示出来，方便检查。
disp(summaryTable);
% 行注释：这里在命令行输出进度或结果提示。
fprintf("Metadata saved: %s\n", metadataFile);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：按正常和缺陷两类分别划分数据，保证训练、验证、测试集中类别比例更稳定。
% 行注释：这里开始定义 stratified_split 函数。
function split = stratified_split(T, valRatio, testRatio)
% 行注释：这里计算或设置 split，供后续步骤使用。
split = strings(height(T), 1);
% 行注释：这里计算或设置 groupId，供后续步骤使用。
groupId = findgroups(T.PCBSubset, T.Label);

% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for g = 1:max(groupId)
    % 行注释：这里计算或设置 idx，供后续步骤使用。
    idx = find(groupId == g);
    % 行注释：这里计算或设置 idx，供后续步骤使用。
    idx = idx(randperm(numel(idx)));
    % 行注释：这里计算或设置 n，供后续步骤使用。
    n = numel(idx);

    % 行注释：这里计算或设置 nTest，供后续步骤使用。
    nTest = max(1, round(n * testRatio));
    % 行注释：这里计算或设置 nVal，供后续步骤使用。
    nVal = max(1, round(n * valRatio));
    % 行注释：这里计算或设置 nTrain，供后续步骤使用。
    nTrain = n - nVal - nTest;

    % 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
    if nTrain < 1
        % 行注释：这里计算或设置 nTrain，供后续步骤使用。
        nTrain = max(1, n - 2);
        % 行注释：这里计算或设置 nVal，供后续步骤使用。
        nVal = 1;
        % 行注释：这里计算或设置 nTest，供后续步骤使用。
        nTest = n - nTrain - nVal;
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end

    % 行注释：这里执行当前语句，完成这一小步处理。
    split(idx(1:nTrain)) = "train";
    % 行注释：这里执行当前语句，完成这一小步处理。
    split(idx(nTrain + 1:nTrain + nVal)) = "val";
    % 行注释：这里执行当前语句，完成这一小步处理。
    split(idx(nTrain + nVal + 1:end)) = "test";
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：根据缺陷图像路径推断对应的掩膜路径，方便后续查看缺陷区域。
% 行注释：这里开始定义 estimate_mask_paths 函数。
function maskPaths = estimate_mask_paths(anomalyFiles, anomalyRoot, maskRoot)
% 行注释：这里计算或设置 maskPaths，供后续步骤使用。
maskPaths = strings(numel(anomalyFiles), 1);

% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if ~isfolder(maskRoot)
    % 行注释：这里提前返回，结束当前函数的后续执行。
    return;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(anomalyFiles)
    % 行注释：这里计算或设置 rel，供后续步骤使用。
    rel = erase(anomalyFiles(i), string(anomalyRoot) + filesep);
    % 行注释：这里计算或设置 relFolder, baseName, 占位输出，供后续步骤使用。
    [relFolder, baseName, ~] = fileparts(rel);
    % 行注释：这里计算或设置 candidates，供后续步骤使用。
    candidates = dir(fullfile(maskRoot, relFolder, baseName + ".*"));
    % 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
    if ~isempty(candidates)
        % 行注释：这里执行当前语句，完成这一小步处理。
        maskPaths(i) = string(fullfile(candidates(1).folder, candidates(1).name));
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end
