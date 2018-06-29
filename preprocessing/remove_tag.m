function [ O ] = remove_tag( I, sz )
%     imshow(I);
    E = imerode(I, strel('square', sz));
%     figure; imshow(E);
    R = imreconstruct(E, I);
    O = I;
    %Remove everything from original image that is close to black in the
    %reconstructed image
    to_remove = R < 10;
    O(to_remove) = 0;
%     figure; imshow(O);
end

