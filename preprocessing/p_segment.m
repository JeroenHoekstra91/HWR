function r = p_segment( I_cur )
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
    e_1 = imerode(d_1, strel('rectangle', [5,220]));
    e_2 = imerode(e_1, strel('rectangle', [220,5]));

    %removing the boundary
    [r c] = size(e_2);
    e_2 = e_2(2:r-1,2:c-1);

    % Step - 3 : Reconstruct parment area
    e_2_grey = uint8(e_2*255);
%     r = imreconstruct(e_2_grey, I_cur);  % use to reconstruct greyscale image
    r =  imreconstruct(e_2, I_bin);    % use to reconstrct binary image    
end

