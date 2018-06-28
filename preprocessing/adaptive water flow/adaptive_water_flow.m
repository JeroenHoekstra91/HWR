function BW = adaptive_water_flow(I)
%ADAPTIVE_WATER_FLOW Summary of this function goes here
%   I: image to be binarized
%   BW: binarized image
    
    
    BW = binarization(I, 121, 0.34, 'sauvola');
    %Remove largest component
    CC = bwconncomp(~BW);
    numPixels = cellfun(@numel,CC.PixelIdxList);
    [~,idx] = max(numPixels);
    BW(CC.PixelIdxList{idx}) = 1;

    SW = compute_stroke_width(BW);
    
    G = rainfall(I, BW, SW);
    
    %Extract ponds
    BW = ~(G - I > 0);
    disp('done');
end

