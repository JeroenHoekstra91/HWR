%%
% find the right threshold for word length 
     gaps = zeros(3000,1);
     count = 1;
     for i = 1:size(parchment_only,2)
        % get all the lines from parchment i
        cur_parchment = parchment_only{i};
        parchment_bin = binarization(cur_parchment, 121, 0.34, 'sauvola');
        lines = line_segmentation_bin_line(parchment_bin, imgs{i});
        for j = 1:size(lines)
            % get all word positions from line j in parchment i 
            line_cur = lines{j};
            rm_background = remove_background_cc(line_cur);
            line_bin = remove_boundary_noise(rm_background);  
            
            % find the gaps
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
           % H_sm at this point contains the spaces
            CC = bwconncomp(H_sm);
            numPixels = cellfun(@numel,CC.PixelIdxList);
            
            % remove the flanking spaces from consideration
            for i = 2:length(numPixels)-1
               gaps(count) = numPixels(i);
               count = count + 1;
            end
        end
     end
     
    % these are all the gaps found in all the parchments
    actual_gaps = gaps(gaps>0);   
    
    mean_gaps = mean(actual_gaps);
    st_gaps = std(actual_gaps);
    
    
    % consider only the small gaps   
    final_small_gaps = actual_gaps(actual_gaps < mean_gaps);
    % the final mean is calculated after removing those
    final_mean = mean(final_small_gaps);

 % the final mean is 9.34
 
 %%