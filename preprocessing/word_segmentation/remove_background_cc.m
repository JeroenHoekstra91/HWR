function BW = remove_background_cc(BW)
%   This removes all the background components that are part of the line
%   by checking for presence of a structuring square that is 1/3 the height
%   of the line

    CC = bwconncomp(~BW);
    [row col] = size(BW);
    numPixels = cellfun(@numel,CC.PixelIdxList);

    struc_size = int8(row/3);    
    
    for i=1:CC.NumObjects 
        new_line = zeros(row,col);
        toKeep = CC.PixelIdxList{i};
        new_line(toKeep) = 1;
        struc = ones(struc_size,struc_size);
        if (numPixels(i)>struc_size*struc_size) &  (existence_submatrix(new_line,struc)) 
                BW(CC.PixelIdxList{i}) = 1;
        end
    end
 
end
