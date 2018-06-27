function [word_positions] = word_histogram(line_bin)

% the function takes a line from the original image.
% it returns a array, each row of which has the start and end 
% indices of the words 
     
    d_1 = imerode(line_bin, strel('rectangle', [3, 1]));
    
    H = size(line_bin,1) - sum(line_bin, 1);
    
    H = double(H);
    
    % make all the cols having words, a negative threshold
    H (H > 0.5) = -5;
    
    % all the gaps now have a positive peaks
    H = H + 5;
    
    % smoothen the peaks
    H_sm =  smooth_signal(H, 3);
    
    % make the spaces clearer 
    H_sm (H_sm < 5) = 0;
    
    H_last = H_sm;
        
    % H_sm at this point contains the spaces
    CC = bwconncomp(H_sm);
    numPixels = cellfun(@numel,CC.PixelIdxList);
    %S = std(numPixels);
    %mu = mean(numPixels);
    %rm_large_gaps = numPixels(numPixels < mu);
    %S = std(rm_large_gaps);
    %mu = mean(rm_large_gaps);
    
    toRemove = (numPixels < 9);
    for i=1:length(toRemove) 
        if toRemove(i)
            toRemoveImg = CC.PixelIdxList{i};
            H_sm(toRemoveImg) = 0;
        end
    end
    
    % now we have the words
    H_sm = H_sm*-1;
    H_sm = H_sm + 5;
    
    CC = bwconncomp(H_sm);
    numPixels = cellfun(@numel,CC.PixelIdxList);
    
    % find the word positions and store them
    word_positions = zeros(length(numPixels),2);
    
    for i=2:length(numPixels)
        if numPixels(i) > 30
            word_positions(i-1,1) = min(CC.PixelIdxList{i});
            word_positions(i-1,2) = max(CC.PixelIdxList{i});
        end
    end
   
end
