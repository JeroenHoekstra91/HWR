function [line_bin] = remove_boundary_noise(line_bin)
%   Removes all the compoenents whose mean y is close to the boundary of
%   the line

    CC = bwconncomp(~line_bin);
    [row col] = size(line_bin);    
    
    for i=1:CC.NumObjects 
        new_line = zeros(row,col);
        toKeep = CC.PixelIdxList{i};
        new_line(toKeep) = 1;
        mean = mean_y(new_line);
        if (mean > row*0.8) | (mean < row*0.2)
                line_bin(CC.PixelIdxList{i}) = 1;
        end
    end
end

