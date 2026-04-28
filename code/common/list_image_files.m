% 中文注释：列出指定目录下的图像文件。
% 主要流程：按常见图片后缀递归或非递归扫描文件，返回统一格式的路径列表。
% 注意事项：供元数据准备和图像读取流程复用。

function files = list_image_files(rootDir)
%LIST_IMAGE_FILES Recursively list common image files under rootDir.

if ~isfolder(rootDir)
    files = strings(0, 1);
    return;
end

patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif", "*.tiff"];
files = strings(0, 1);
for p = 1:numel(patterns)
    matches = dir(fullfile(rootDir, "**", patterns(p)));
    paths = string(fullfile({matches.folder}', {matches.name}'));
    files = [files; paths]; %#ok<AGROW>
end

files = unique(files);
end
