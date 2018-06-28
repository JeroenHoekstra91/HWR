
function [i, j] = local_minima(I, i, j)
%LOCAL_MINIMA Summary of this function goes here
%   Detailed explanation goes here
    W = 2;
    I = double(padarray(I, [W, W], Inf)); %Padding to avoid out of bounds
    i = i + W; %To compensate for padding
    j = j + W;
    
    mask = ones(2*W+1)*Inf;
    mask(W+1,:) = 0;
    mask(:,W+1) = 0;
    
    masked = I(i-W:i+W, j-W:j+W)+mask;
    [minima, minima_idx] = min(masked(:));
    
    while minima < I(i, j)
        [i_offset, j_offset] = ind2sub(size(masked), minima_idx);
        i = i_offset + i-W-1;
        j = j_offset + j-W-1;
        masked = I(i-W:i+W, j-W:j+W)+mask;
        [minima, minima_idx] = min(masked(:));
    end 
    i = i - W;
    j = j - W;
end

