function O = visualize_words(I, baselines, gaps)
%  Helps visualise the word boundaries within a line 
    O = to_rgb(I);
    
        for j = 1: length(baselines)
        i = baselines(j);
        if i-2 < 0 | i+2 > size(I,2)
            continue;
        end
        O(:,i-2:i+2, 1) = 255;
        O(:,i-2:i+2, 2) = 0;
        O(:,i-2:i+2, 3) = 0;
    end    
    
     for j = 1: length(gaps)
         i = gaps(j);
         if i-2 < 0 | i+2 > size(I,2)
            continue;
         end
         O(:,i-2:i+2, 1) = 0;
         O(:,i-2:i+2, 2) = 0;
         O(:,i-2:i+2, 3) = 00255;
     end
end
