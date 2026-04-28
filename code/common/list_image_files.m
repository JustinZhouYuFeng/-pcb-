% 中文注释：列出指定目录下的图像文件。
% 主要流程：按常见图片后缀递归或非递归扫描文件，返回统一格式的路径列表。
% 注意事项：供元数据准备和图像读取流程复用。

% 函数说明：列出目录下常见格式的图片文件，供数据整理阶段使用。
% 行注释：这里开始定义 list_image_files 函数。
function files = list_image_files(rootDir)
%LIST_IMAGE_FILES Recursively list common image files under rootDir.

% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if ~isfolder(rootDir)
    % 行注释：这里计算或设置 files，供后续步骤使用。
    files = strings(0, 1);
    % 行注释：这里提前返回，结束当前函数的后续执行。
    return;
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 patterns，供后续步骤使用。
patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.tif", "*.tiff"];
% 行注释：这里计算或设置 files，供后续步骤使用。
files = strings(0, 1);
% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for p = 1:numel(patterns)
    % 行注释：这里计算或设置 matches，供后续步骤使用。
    matches = dir(fullfile(rootDir, "**", patterns(p)));
    % 行注释：这里计算或设置 paths，供后续步骤使用。
    paths = string(fullfile({matches.folder}', {matches.name}'));
    % 行注释：这里计算或设置 files，供后续步骤使用。
    files = [files; paths]; %#ok<AGROW>
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里计算或设置 files，供后续步骤使用。
files = unique(files);
% 行注释：这里结束当前的 if、for 或函数代码块。
end
