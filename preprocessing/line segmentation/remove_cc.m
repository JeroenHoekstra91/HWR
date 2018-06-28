function BW = remove_cc(BW)
%REMOVE_CC Summary of this function goes here
%   Detailed explanation goes here
    CC = bwconncomp(~BW);

    %Dilate vertically to try to disconnect some components
    imerode(BW, strel('rectangle', [21 3]));
    
    numPixels = cellfun(@numel,CC.PixelIdxList);
    [~,idx] = max(numPixels);
    BW(CC.PixelIdxList{idx}) = 1;

    numPixels(idx) = []; %Remove background component
%     background = CC.PixelIdxList{idx};
    CC.PixelIdxList(idx) = [];
    CC.NumObjects = CC.NumObjects - 1;
    S = std(numPixels);
    mu = mean(numPixels);
    
    % Remove components that are further than 1std for small components and
    % 2stds for large ones from the mean
    toRemove = or(mu-numPixels > S, numPixels-mu > 3*S);
%     toRemove = abs(mu-numPixels) > 2.5*S;
    for i=1:length(toRemove) %for some reason we have to run the loop manually, cant pass the whole list to PixelIdxList
        if toRemove(i)
            toRemoveImg = CC.PixelIdxList{i};
            BW(toRemoveImg) = 1;
        end
    end
end

