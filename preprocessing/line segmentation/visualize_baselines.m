function O = visualize_baselines(I, baselines, gaps)
%VISUALIZE_BASELINES draws the detected baselines and gaps from the
%histogram
%
%       O = visualize_baselines(I, baselines, gaps)
%
%       INPUT
%       I: background image to draw on
%       baselines: y coordinate of each baseline
%       gaps: y coordinate of each gap line
%
%       OUTPUT
%       O: 
    O = to_rgb(I);
    
%     % All baselines are painted red
%     O(baselines, :, 1) = 255;
%     O(baselines, :, 2) = 0;
%     O(baselines, :, 3) = 0;
%     
%     % All gap lines are painted blue
%     O(gaps, :, 1) = 0;
%     O(gaps, :, 2) = 0;
%     O(gaps, :, 3) = 255;
    
    % i know it's not efficient but i'm lazy
    for j = 1: length(baselines)
        i = baselines(j);
        O(i-2:i+2, :, 1) = 255;
        O(i-2:i+2, :, 2) = 0;
        O(i-2:i+2, :, 3) = 0;
    end    
    
%     for j = 1: length(gaps)
%         i = gaps(j);
%         O(i-2:i+2, :, 1) = 0;
%         O(i-2:i+2, :, 2) = 0;
%         O(i-2:i+2, :, 3) = 255;
%     end
end

