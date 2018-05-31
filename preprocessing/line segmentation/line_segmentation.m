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
    BW = remove_CC(BW);
    
    [H baselines gaps] = line_histogram2(BW);    
    
    % Segment based on maxima,minima
    dists = pdist2(baselines, gaps);
    seg = {length(baselines)};
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