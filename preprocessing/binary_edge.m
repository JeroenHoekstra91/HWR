function [ E ] = binary_edge( I )
    % Enlarge image
    E = zeros(size(I));
    im = zeros(size(I)+2);
    im(2:end-1, 2:end-1) = I;
    
    for i = 2:size(im,1)-1
        for j = 2:size(im,2)-1
            kernel = im(i-1:i+1, j-1:j+1);
            if max(kernel(:)) ~= min(kernel(:))
                E(i-1, j-1) = 1;
            end
        end
    end
end

