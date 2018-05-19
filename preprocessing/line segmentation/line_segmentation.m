function L = line_segmentation(BW, R)
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

    H = line_histogram(BW);

    H = double(H);
    [pks, baseline] = findpeaks(H,'MinPeakProminence',40);

    % Compute mean distance between baseline candidates
    lines_width = baseline(2:length(baseline))-baseline(1:length(baseline)-1);

    %Use histogram to identify the common line width
    [width_hist, edges] = histcounts(lines_width);
    [~,idx] = max(width_hist);

    line_width = (edges(idx+1)-edges(idx))/2;
    
    L = {};
end