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
