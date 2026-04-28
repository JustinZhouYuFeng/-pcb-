% 中文注释：确保指定目录存在的小工具函数。
% 主要流程：检查路径是否存在，不存在时自动创建，避免保存结果时报错。
% 注意事项：常用于保存模型、图表和中间结果之前的目录准备。

% 函数说明：检查目录是否存在，不存在就创建，确保后续文件能正常保存。
% 行注释：这里开始定义 ensure_dir 函数。
function ensure_dir(folderPath)
%ENSURE_DIR Create a directory if it does not already exist.

% 行注释：这里判断条件是否成立，再决定走哪一段逻辑。
if ~isfolder(folderPath)
    % 行注释：这里执行当前语句，完成这一小步处理。
    mkdir(folderPath);
% 行注释：这里结束当前的 if、for 或函数代码块。
end
% 行注释：这里结束当前的 if、for 或函数代码块。
end
