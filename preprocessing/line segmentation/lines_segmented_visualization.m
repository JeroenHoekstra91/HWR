function O = lines_segmented_visualization(lines)
%LINES_SEGMENTED_VISUALIZATION Puts together the segmented lines into a
%single image
%       O = lines_segmented_visualization(lines)
%
%       INPUT
%       lines: a cell array with the images of each of the segmented lines.
%
%       OUTPUT
%       O: a single image with all the lines put together with a
%       sepparation gap.
    gap_height = 20;
    background = 100;
    O = [];
    for l=1:length(lines)
        line = lines{l};
        if isempty(O)
            O = uint8(line);
        else
            O(end+1:end+gap_height, 1:size(line, 2)) = uint8(ones(gap_height, size(line,2))*background);
            O(end+1:end+size(line,1), 1:size(line, 2)) = uint8(line);
        end  
    end
end

