function r_final = p_segment( I_cur )

    % Step - 1 - remove all the characters
    level = graythresh(I_cur);
    I_bin = imbinarize(I_cur,level);
    d_1 = imdilate(I_bin, strel('square', 30));    
    
    % a boundary to help in erosion
    [r c] = size(d_1);
    I_new = zeros(r+2,c+2);
    I_new(2:1+r,2:1+c) = d_1;
    d_1 = im2bw(I_new);

    % Step - 2 : Horizontal/vertical struct erode !
    e_1 = imerode(d_1, strel('rectangle', [5,230]));
    e_2 = imerode(e_1, strel('rectangle', [230,5]));

    %removing the boundary
    [r c] = size(e_2);
    e_2 = e_2(2:r-1,2:c-1);

    % Step - 3 : Reconstruct parment area
    e_2_grey = uint8(e_2*255);
    r = imreconstruct(e_2_grey, I_cur);  % use to reconstruct greyscale image
    % r =  imreconstruct(e_2, I_bin);    % use to reconstrct binary image    
    r(r < 16) = 0; %Threshold dark values.
    
    
    % Step - 4 : To remove the connected palettes
    % Get grey level images. These won't have the palettes !
    level = graythresh(r);
    r_bin = imbinarize(r,level);  
    
    % find the row thresholds
    [row col] = size(r_bin);
    sum_r = zeros(row);
    for i = 1:row
        for j = 1:col
          sum_r(i) = sum_r(i) + r_bin(i,j);
        end
    end
    pos_nonzero = find(sum_r);
    max_r = max(pos_nonzero);
    min_r = min(pos_nonzero);
    
    % find the col thresholds
    sum_c = zeros(col);
    for i = 1:col
        for j = 1:row
          sum_c(i) = sum_c(i) + r_bin(j,i);
        end
    end
    pos_nonzero = find(sum_c);
    max_c = max(pos_nonzero);
    min_c = min(pos_nonzero);
    
    % binarized image sometime is problematic and removes small portions,
    % so add a small extension to the thresholds (might not be necessary)
    if(min_r - 5 > 0)
        min_r = min_r - 5;
    end
    if(min_c - 5 > 0)
        min_c = min_c - 5;
    end
    if(max_r + 5 < row)
        max_r = max_r + 5;
    end 
    if(max_c + 5 < col)
        max_c = max_c + 5;
    end 
    
    % final masking to remove the connected palettes
    r_final = uint8(zeros(row,col));
    r_final(min_r:max_r,min_c:max_c) = 1;
    r_final = r.*r_final;
    
end

