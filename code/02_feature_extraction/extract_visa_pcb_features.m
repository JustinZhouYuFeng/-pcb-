% 中文注释：把 PCB 图像转换为可供贝叶斯模型使用的手工特征矩阵。
% 主要流程：读取图像、统一尺寸、提取颜色/纹理/边缘/梯度等特征，并做标准化。
% 输出结果：保存特征、标签和数据划分信息，作为分类实验的直接输入。

% 函数说明：读取元数据中的图像，逐张提取手工特征并保存成模型可用的矩阵。
% 行注释：这里开始定义 extract_visa_pcb_features 函数。
function featuresFile = extract_visa_pcb_features(metadataFile, cfg)
%EXTRACT_VISA_PCB_FEATURES Extract color, texture, edge, LBP and HOG features.

% 行注释：这里计算或设置 outDir，供后续步骤使用。
outDir = fullfile(cfg.projectRoot, "data", "processed", "visa_pcb_binary");
% 行注释：这里执行当前语句，完成这一小步处理。
ensure_dir(outDir);
% 行注释：这里计算或设置 featuresFile，供后续步骤使用。
featuresFile = fullfile(outDir, "visa_pcb_features.mat");

% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if isfile(featuresFile) && ~cfg.forceFeatureExtraction
    % 行注释：这里在命令行输出进度或结果提示。
    fprintf("Feature file already exists: %s\n", featuresFile);
    % 行注释：这里在命令行输出进度或结果提示。
    fprintf("Set cfg.forceFeatureExtraction = true to rebuild it.\n");
    % 行注释：这里提前返回，结束当前函数的后续执行。
    return;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 T，供后续步骤使用。
T = readtable(metadataFile, 'TextType', 'string');
% 行注释：这里计算或设置 numImages，供后续步骤使用。
numImages = height(T);

% 行注释：这里计算或设置 X，供后续步骤使用。
X = [];
% 行注释：这里计算或设置 featureNames，供后续步骤使用。
featureNames = strings(0, 1);

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Extracting features from %d images...\n", numImages);
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numImages
    % 行注释：这里计算或设置 feat, names，供后续步骤使用。
    [feat, names] = compute_single_image_features(T.ImagePath(i), cfg.imageSize);

    % 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
    if i == 1
        % 行注释：这里计算或设置 X，供后续步骤使用。
        X = zeros(numImages, numel(feat), 'single');
        % 行注释：这里计算或设置 featureNames，供后续步骤使用。
        featureNames = names;
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end

    % 行注释：这里执行当前语句，完成这一小步处理。
    X(i, :) = single(feat);

    % 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
    if mod(i, 100) == 0 || i == numImages
        % 行注释：这里在命令行输出进度或结果提示。
        fprintf("  %d/%d images processed\n", i, numImages);
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 Y，供后续步骤使用。
Y = categorical(T.Label);
% 行注释：这里计算或设置 Split，供后续步骤使用。
Split = string(T.Split);
% 行注释：这里计算或设置 PCBSubset，供后续步骤使用。
PCBSubset = string(T.PCBSubset);
% 行注释：这里计算或设置 ImagePath，供后续步骤使用。
ImagePath = string(T.ImagePath);
% 行注释：这里计算或设置 MaskPath，供后续步骤使用。
MaskPath = string(T.MaskPath);

% 行注释：这里把计算结果保存到文件，便于后续脚本继续使用。
save(featuresFile, "X", "Y", "Split", "PCBSubset", "ImagePath", ...
    "MaskPath", "featureNames", "-v7.3");

% 行注释：这里在命令行输出进度或结果提示。
fprintf("Features saved: %s\n", featuresFile);
% 行注释：这里在命令行输出进度或结果提示。
fprintf("Feature dimension: %d\n", size(X, 2));
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：对单张 PCB 图像提取颜色、纹理、边缘和梯度等特征。
% 行注释：这里开始定义 compute_single_image_features 函数。
function [features, names] = compute_single_image_features(imagePath, imageSize)
% 行注释：这里计算或设置 img，供后续步骤使用。
img = imread(imagePath);
% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if size(img, 3) == 1
    % 行注释：这里计算或设置 img，供后续步骤使用。
    img = repmat(img, 1, 1, 3);
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 img，供后续步骤使用。
img = im2double(imresize(img, imageSize));
% 行注释：这里计算或设置 gray，供后续步骤使用。
gray = rgb2gray(img);
% 行注释：这里计算或设置 grayEq，供后续步骤使用。
grayEq = adapthisteq(gray);

% 行注释：这里计算或设置 rgb，供后续步骤使用。
rgb = img;
% 行注释：这里计算或设置 hsvImg，供后续步骤使用。
hsvImg = rgb2hsv(img);
% 行注释：这里计算或设置 labImg，供后续步骤使用。
labImg = rgb2lab(img);

% 行注释：这里计算或设置 colorStats, colorNames，供后续步骤使用。
[colorStats, colorNames] = channel_stats(cat(3, rgb, hsvImg, labImg), ...
    ["rgb_r", "rgb_g", "rgb_b", "hsv_h", "hsv_s", "hsv_v", ...
     "lab_l", "lab_a", "lab_b"]);

% 行注释：这里计算或设置 grayVec，供后续步骤使用。
grayVec = grayEq(:);
% 行注释：这里计算或设置 grayStats，供后续步骤使用。
grayStats = [
    % 行注释：这里执行当前语句，完成这一小步处理。
    mean(grayVec), std(grayVec), skewness(grayVec), kurtosis(grayVec), ...
    entropy(grayEq), prctile(grayVec, 10), prctile(grayVec, 50), prctile(grayVec, 90)
% 行注释：这里结束当前多行参数、列表或结构。
];
% 行注释：这里计算或设置 grayNames，供后续步骤使用。
grayNames = [
    % 行注释：这里执行当前语句，完成这一小步处理。
    "gray_mean", "gray_std", "gray_skewness", "gray_kurtosis", ...
    "gray_entropy", "gray_p10", "gray_p50", "gray_p90"
% 行注释：这里结束当前多行参数、列表或结构。
];

% 行注释：这里计算或设置 edgeCanny，供后续步骤使用。
edgeCanny = edge(grayEq, "Canny");
% 行注释：这里计算或设置 edgeSobel，供后续步骤使用。
edgeSobel = edge(grayEq, "Sobel");
% 行注释：这里计算或设置 edgeStats，供后续步骤使用。
edgeStats = [
    % 行注释：这里执行当前语句，完成这一小步处理。
    nnz(edgeCanny) / numel(edgeCanny), ...
    nnz(edgeSobel) / numel(edgeSobel)
% 行注释：这里结束当前多行参数、列表或结构。
];
% 行注释：这里计算或设置 edgeNames，供后续步骤使用。
edgeNames = ["edge_density_canny", "edge_density_sobel"];

% 行注释：这里计算或设置 glcm，供后续步骤使用。
glcm = graycomatrix(im2uint8(grayEq), ...
    'Offset', [0 1; -1 1; -1 0; -1 -1], ...
    'NumLevels', 16, 'Symmetric', true);
% 行注释：这里计算或设置 props，供后续步骤使用。
props = graycoprops(glcm, {'Contrast', 'Correlation', 'Energy', 'Homogeneity'});
% 行注释：这里计算或设置 textureStats，供后续步骤使用。
textureStats = [
    % 行注释：这里执行当前语句，完成这一小步处理。
    mean(props.Contrast), mean(props.Correlation), ...
    mean(props.Energy), mean(props.Homogeneity)
% 行注释：这里结束当前多行参数、列表或结构。
];
% 行注释：这里计算或设置 textureNames，供后续步骤使用。
textureNames = ["glcm_contrast", "glcm_correlation", "glcm_energy", "glcm_homogeneity"];

% 行注释：这里计算或设置 lbp，供后续步骤使用。
lbp = extractLBPFeatures(grayEq, 'CellSize', [64 64], 'Normalization', 'L2');
% 行注释：这里计算或设置 hog，供后续步骤使用。
hog = extractHOGFeatures(grayEq, 'CellSize', [64 64]);

% 行注释：这里计算或设置 lbpNames，供后续步骤使用。
lbpNames = "lbp_" + string(1:numel(lbp));
% 行注释：这里计算或设置 hogNames，供后续步骤使用。
hogNames = "hog_" + string(1:numel(hog));

% 行注释：这里计算或设置 features，供后续步骤使用。
features = double([colorStats, grayStats, edgeStats, textureStats, lbp, hog]);
% 行注释：这里计算或设置 names，供后续步骤使用。
names = [colorNames, grayNames, edgeNames, textureNames, lbpNames, hogNames]';

% 行注释：这里执行当前语句，完成这一小步处理。
features(~isfinite(features)) = 0;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 函数说明：计算一个通道的均值、方差、分位数等统计量，作为图像特征的一部分。
% 行注释：这里开始定义 channel_stats 函数。
function [stats, names] = channel_stats(stack, channelNames)
% 行注释：这里计算或设置 stats，供后续步骤使用。
stats = [];
% 行注释：这里计算或设置 names，供后续步骤使用。
names = strings(1, 0);

% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for c = 1:size(stack, 3)
    % 行注释：这里计算或设置 values，供后续步骤使用。
    values = stack(:, :, c);
    % 行注释：这里计算或设置 values，供后续步骤使用。
    values = values(:);
    % 行注释：这里计算或设置 one，供后续步骤使用。
    one = [mean(values), std(values), skewness(values), kurtosis(values)];
    % 行注释：这里计算或设置 stats，供后续步骤使用。
    stats = [stats, one]; %#ok<AGROW>
    % 行注释：这里计算或设置 names，供后续步骤使用。
    names = [names, ...
        channelNames(c) + "_mean", channelNames(c) + "_std", ...
        channelNames(c) + "_skewness", channelNames(c) + "_kurtosis"]; %#ok<AGROW>
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end
