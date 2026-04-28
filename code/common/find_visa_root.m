% 中文注释：自动定位 VisA 数据集根目录。
% 主要流程：根据项目配置和常见目录结构查找 PCB 原始数据所在位置。
% 注意事项：集中处理路径差异，减少主流程脚本中的硬编码路径。

% 函数说明：在常见位置中寻找 VisA 数据集根目录，减少手动改路径。
function visaRoot = find_visa_root(projectRoot)
%FIND_VISA_ROOT Locate the extracted VisA folder that contains pcb1..pcb4.

rawRoot = fullfile(projectRoot, "data", "raw", "visa");
candidates = [
    fullfile(rawRoot, "VisA")
    rawRoot
    fullfile(rawRoot, "VisA_20220922", "VisA")
    fullfile(rawRoot, "VisA_20220922")
];

for i = 1:numel(candidates)
    candidate = candidates(i);
    if isfolder(fullfile(candidate, "pcb1")) && isfolder(fullfile(candidate, "pcb4"))
        visaRoot = char(candidate);
        return;
    end
end

if isfolder(rawRoot)
    listing = dir(fullfile(rawRoot, "**", "pcb1"));
    for i = 1:numel(listing)
        if listing(i).isdir
            candidate = string(listing(i).folder);
            if isfolder(fullfile(candidate, "pcb4"))
                visaRoot = char(candidate);
                return;
            end
        end
    end
end

error(["VisA PCB data was not found. Run this PowerShell script first:" newline ...
    "  code/01_preprocessing/download_visa_pcb.ps1"]);
end
