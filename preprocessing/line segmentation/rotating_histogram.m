function [BW, best_orientation] = rotating_histogram(BW)
% ROTATING_HISTOGRAM finds the angle that maximises histogram peaks
%
%       BW = rotating_histogram(BW)
%
%       INPUT
%       BW: Binary image (logical class)
%
%       OUTPUT
%       BW: the original image rotated to the optimal angle
%       best_orientation: the angle (degrees) by which BW is rotated
    
    
    % Select orientation that will maximise the histogram peak height
    best_score = 0;
    best_orientation = Inf;
    for a = -10:2:10
        BW2 = imrotate(~BW, a, 'nearest', 'crop'); %image is inverted so that background added from rotation is the same
        [H, baselines, ~] = line_histogram2(~BW2); %reinvert the image to get black chars

        total_peaks = sum(H(baselines));
        if total_peaks > best_score
            best_score = total_peaks;
            best_orientation = a;
        end
    end
    BW = imrotate(~BW, best_orientation, 'nearest', 'crop');
    BW = ~BW;
end

