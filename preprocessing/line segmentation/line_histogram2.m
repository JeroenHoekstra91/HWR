function [ H ] = line_histogram2( BW )
% LINE_HISTOGRAM2 Compute the number of black pixels per row
%
%       H = line_segmentation(BW)
%
%       INPUT
%       BW: Binary image (logical class).
%
%       OUTPUT
%       H: counts per row

    H = size(BW,2) - sum(BW, 2);

end

