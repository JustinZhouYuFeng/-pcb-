% 中文注释：自动定位 VisA 数据集根目录。
% 主要流程：根据项目配置和常见目录结构查找 PCB 原始数据所在位置。
% 注意事项：集中处理路径差异，减少主流程脚本中的硬编码路径。

% 函数说明：在常见位置中寻找 VisA 数据集根目录，减少手动改路径。
% 行注释：这里开始定义 find_visa_root 函数。
function visaRoot = find_visa_root(projectRoot)
%FIND_VISA_ROOT Locate the extracted VisA folder that contains pcb1..pcb4.

% 行注释：这里计算或设置 rawRoot，供后续步骤使用。
rawRoot = fullfile(projectRoot, "data", "raw", "visa");
% 行注释：这里计算或设置 candidates，供后续步骤使用。
candidates = [
    % 行注释：这里执行当前语句，完成这一小步处理。
    fullfile(rawRoot, "VisA")
    % 行注释：这里执行当前语句，完成这一小步处理。
    rawRoot
    % 行注释：这里执行当前语句，完成这一小步处理。
    fullfile(rawRoot, "VisA_20220922", "VisA")
    % 行注释：这里执行当前语句，完成这一小步处理。
    fullfile(rawRoot, "VisA_20220922")
% 行注释：这里结束当前多行参数、列表或结构。
];

% 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
for i = 1:numel(candidates)
    % 行注释：这里计算或设置 candidate，供后续步骤使用。
    candidate = candidates(i);
    % 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
    if isfolder(fullfile(candidate, "pcb1")) && isfolder(fullfile(candidate, "pcb4"))
        % 行注释：这里计算或设置 visaRoot，供后续步骤使用。
        visaRoot = char(candidate);
        % 行注释：这里提前返回，结束当前函数的后续执行。
        return;
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if isfolder(rawRoot)
    % 行注释：这里计算或设置 listing，供后续步骤使用。
    listing = dir(fullfile(rawRoot, "**", "pcb1"));
    % 行注释：这里开始循环，逐个处理一组参数、样本或图形元素。
    for i = 1:numel(listing)
        % 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
        if listing(i).isdir
            % 行注释：这里计算或设置 candidate，供后续步骤使用。
            candidate = string(listing(i).folder);
            % 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
            if isfolder(fullfile(candidate, "pcb4"))
                % 行注释：这里计算或设置 visaRoot，供后续步骤使用。
                visaRoot = char(candidate);
                % 行注释：这里提前返回，结束当前函数的后续执行。
                return;
            % 行注释：这里结束当前的 if、for 或函数代码块。
            end
        % 行注释：这里结束当前的 if、for 或函数代码块。
        end
    % 行注释：这里结束当前的 if、for 或函数代码块。
    end
% 行注释：这里结束当前的 if、for 或函数代码块。
end

% 行注释：这里执行当前语句，完成这一小步处理。
error(["VisA PCB data was not found. Run this PowerShell script first:" newline ...
    "  code/01_preprocessing/download_visa_pcb.ps1"]);
% 行注释：这里结束当前的 if、for 或函数代码块。
end
