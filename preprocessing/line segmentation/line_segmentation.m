function seg = line_segmentation(BW, R)
% LINE_SEGMENTATION Identify handwritten lines from a binary image.
%
%       [baseline, line_width, I] = line_segmentation(BW, R)
%
%       INPUT
%       BW: Binary image (logical class)
%       R: Reference image
%
%       OUTPUT
%       L: cell array of segmented lines in R

    %Fuse background with parchment
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
    
    H = line_histogram2(BW);

    H = double(H);

    %smooth Histogram and find maxima
    H = smooth_signal(H, 30);
    [pks, baselines] = findpeaks(H,'MinPeakProminence',40);

    x = [1:length(H)];

    %minima
    Hinv = H*-1;
    [~, gaps] = findpeaks(Hinv,'MinPeakProminence',60);
    
    % Segment based on maxima,minima
    dists = pdist2(baselines, gaps);
    seg = {}
    for bs = 1:length(baselines) %iterate through all lines
        [min_dist, loc] = sort(dists(bs, :)); %sort gaps by distance to baseline
        above = gaps < baselines(bs); %find all gaps above current baseline
        above_idx = loc(find(above(loc), 1)); %select closest gap that is above
        below = gaps > baselines(bs);
        below_idx = loc(find(below(loc), 1));
        %segment based on which gaps have been found
        if above_idx & below_idx
            seg{bs} = R(gaps(above_idx):gaps(below_idx), :);
        elseif above
            seg{bs} = R(gaps(above_idx):min(size(R,1),baselines(bs)+dists(above_idx)), :); %equidistant above and below
        else
            seg{bs} = R(max(1, baselines(bs) - dists(below_idx)):gaps(below_idx), :); %equidistant above and below
        end
    end
end