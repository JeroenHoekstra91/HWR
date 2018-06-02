function seg = line_segmentation2(BW, R)
% LINE_SEGMENTATION segment hw lines based on baselines only (not gaps)
%
%       seg = line_segmentation2(BW, R)
%
%       INPUT
%       BW: Binary image (logical class)
%       R: Reference image
%
%       OUTPUT
%       seg: cell array of segmented lines in R

    %Fuse background with parchment
    BW = remove_cc(BW);
    
    [~, baselines, ~] = line_histogram2(BW);    
    assert(length(baselines) >= 2);
    
    seg = cell(length(baselines), 1);
    
    % Segment based on baseline
    for i = 1:length(baselines)
        l = baselines(i);
        if i == 1 %first baseline -> above and below threshold are equidistant
            d = floor((baselines(i+1) - l)/2); %Threshold distance
            upper_bound = max(1, l-d); %higher bound, as you look at the image (not by index)
            lower_bound = min(size(BW, 1), l+d);
        elseif i == length(baselines) %last baseline -> above and below threshold are equidistant
            d = floor((l - baselines(i-1))/2);
            upper_bound = max(1, l-d);
            lower_bound = min(size(BW, 1), l+d);
        else %mid baseline
            d = floor((l - baselines(i-1))/2); % Upper threshold distance
            upper_bound = max(1, l-d);
            d = floor((baselines(i+1) - l)/2); % Lower threshold distance
            lower_bound = min(size(BW, 1), l+d);
        end
        seg{i} = R(upper_bound:lower_bound, :);
    end
end

