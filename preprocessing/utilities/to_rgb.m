function O = to_rgb(I)
%TO_RGB converts matrix I into a 3d matrix (rgb channels)
%   Detailed explanation goes here
%cast to uint8 and make sure the color range is from 0 to 255
    if isa(I, 'logical')
        I = uint8(I)*255
    elseif ~isa(I, 'uint8')
        I = uint8(I)
    end
    
    %make sure the matrix is rgb
    if size(I, 3) == 3
        O = I;
    else
        O(:,:,1) = I;
        O(:,:,2) = I;
        O(:,:,3) = I;
    end
end

