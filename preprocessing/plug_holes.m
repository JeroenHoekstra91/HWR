function [holes_plugged] = plug_holes(reconstructed,original)
% This function plus holes in the reconstructed image.
    [row col] = size(reconstructed);
    holes_plugged = uint8(zeros(row,col));
    for i = 1:row
        line = reconstructed(i,:);
        indx_pos = find(line>0);
        max_indx = max(indx_pos);
        min_indx = min(indx_pos);
        holes_plugged(i,min_indx:max_indx) = original(i,min_indx:max_indx);
    end
end

