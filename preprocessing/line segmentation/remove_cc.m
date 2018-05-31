function BW = remove_cc(BW)
%REMOVE_CC Summary of this function goes here
%   Detailed explanation goes here
    CC = bwconncomp(~BW);

    numPixels = cellfun(@numel,CC.PixelIdxList);
    [biggest,idx] = max(numPixels);
    BW(CC.PixelIdxList{idx}) = 1;

    numPixels(idx) = []; %Remove background component
    background = CC.PixelIdxList{idx};
    CC.PixelIdxList(idx) = [];
    CC.NumObjects = CC.NumObjects - 1;
    S = std(numPixels);
    mu = mean(numPixels);
    
    % Remove components that are further than 2stds from the mean
    toRemove = abs(mu-numPixels) > S*2;
    for i=1:length(toRemove) %for some reason we have to run the loop manually, cant pass the whole list to PixelIdxList
        if toRemove(i)
            toRemoveImg = CC.PixelIdxList{i};
            BW(toRemoveImg) = 1;
        end
    end
end

