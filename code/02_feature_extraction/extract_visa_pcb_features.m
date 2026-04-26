function featuresFile = extract_visa_pcb_features(metadataFile, cfg)
%EXTRACT_VISA_PCB_FEATURES Extract color, texture, edge, LBP and HOG features.

outDir = fullfile(cfg.projectRoot, "data", "processed", "visa_pcb_binary");
ensure_dir(outDir);
featuresFile = fullfile(outDir, "visa_pcb_features.mat");

if isfile(featuresFile) && ~cfg.forceFeatureExtraction
    fprintf("Feature file already exists: %s\n", featuresFile);
    fprintf("Set cfg.forceFeatureExtraction = true to rebuild it.\n");
    return;
end

T = readtable(metadataFile, 'TextType', 'string');
numImages = height(T);

X = [];
featureNames = strings(0, 1);

fprintf("Extracting features from %d images...\n", numImages);
for i = 1:numImages
    [feat, names] = compute_single_image_features(T.ImagePath(i), cfg.imageSize);

    if i == 1
        X = zeros(numImages, numel(feat), 'single');
        featureNames = names;
    end

    X(i, :) = single(feat);

    if mod(i, 100) == 0 || i == numImages
        fprintf("  %d/%d images processed\n", i, numImages);
    end
end

Y = categorical(T.Label);
Split = string(T.Split);
PCBSubset = string(T.PCBSubset);
ImagePath = string(T.ImagePath);
MaskPath = string(T.MaskPath);

save(featuresFile, "X", "Y", "Split", "PCBSubset", "ImagePath", ...
    "MaskPath", "featureNames", "-v7.3");

fprintf("Features saved: %s\n", featuresFile);
fprintf("Feature dimension: %d\n", size(X, 2));
end

function [features, names] = compute_single_image_features(imagePath, imageSize)
img = imread(imagePath);
if size(img, 3) == 1
    img = repmat(img, 1, 1, 3);
end

img = im2double(imresize(img, imageSize));
gray = rgb2gray(img);
grayEq = adapthisteq(gray);

rgb = img;
hsvImg = rgb2hsv(img);
labImg = rgb2lab(img);

[colorStats, colorNames] = channel_stats(cat(3, rgb, hsvImg, labImg), ...
    ["rgb_r", "rgb_g", "rgb_b", "hsv_h", "hsv_s", "hsv_v", ...
     "lab_l", "lab_a", "lab_b"]);

grayVec = grayEq(:);
grayStats = [
    mean(grayVec), std(grayVec), skewness(grayVec), kurtosis(grayVec), ...
    entropy(grayEq), prctile(grayVec, 10), prctile(grayVec, 50), prctile(grayVec, 90)
];
grayNames = [
    "gray_mean", "gray_std", "gray_skewness", "gray_kurtosis", ...
    "gray_entropy", "gray_p10", "gray_p50", "gray_p90"
];

edgeCanny = edge(grayEq, "Canny");
edgeSobel = edge(grayEq, "Sobel");
edgeStats = [
    nnz(edgeCanny) / numel(edgeCanny), ...
    nnz(edgeSobel) / numel(edgeSobel)
];
edgeNames = ["edge_density_canny", "edge_density_sobel"];

glcm = graycomatrix(im2uint8(grayEq), ...
    'Offset', [0 1; -1 1; -1 0; -1 -1], ...
    'NumLevels', 16, 'Symmetric', true);
props = graycoprops(glcm, {'Contrast', 'Correlation', 'Energy', 'Homogeneity'});
textureStats = [
    mean(props.Contrast), mean(props.Correlation), ...
    mean(props.Energy), mean(props.Homogeneity)
];
textureNames = ["glcm_contrast", "glcm_correlation", "glcm_energy", "glcm_homogeneity"];

lbp = extractLBPFeatures(grayEq, 'CellSize', [64 64], 'Normalization', 'L2');
hog = extractHOGFeatures(grayEq, 'CellSize', [64 64]);

lbpNames = "lbp_" + string(1:numel(lbp));
hogNames = "hog_" + string(1:numel(hog));

features = double([colorStats, grayStats, edgeStats, textureStats, lbp, hog]);
names = [colorNames, grayNames, edgeNames, textureNames, lbpNames, hogNames]';

features(~isfinite(features)) = 0;
end

function [stats, names] = channel_stats(stack, channelNames)
stats = [];
names = strings(1, 0);

for c = 1:size(stack, 3)
    values = stack(:, :, c);
    values = values(:);
    one = [mean(values), std(values), skewness(values), kurtosis(values)];
    stats = [stats, one]; %#ok<AGROW>
    names = [names, ...
        channelNames(c) + "_mean", channelNames(c) + "_std", ...
        channelNames(c) + "_skewness", channelNames(c) + "_kurtosis"]; %#ok<AGROW>
end
end
