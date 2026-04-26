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
