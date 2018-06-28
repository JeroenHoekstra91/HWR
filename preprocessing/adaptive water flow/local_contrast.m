function C = local_contrast(I, edges, SW)
%LOCAL_CONTRAST computes local contrast for edges pixel in the image
% based on a window controlled by SW.
%   I: image to binarize.
%   edges: image edges.
%   SW: stroke width
%   C: output contrast values for the pixels in edges
    [is, js] = find(edges);
    C = zeros(size(I));
    for idx = 1:length(is)
        y = is(idx);
        x = js(idx);
        R = max(1, SW(y,x));
        p  = [y, x-R; y-R, x-R; y-R, x; y-R x+R];
        p_ = [y, x+R; y+R, x+R; y+R, x; y+R, x-R];
        for i = 1:4
            if ~(out_of_bounds(size(I), p(i, :)) || out_of_bounds(size(I), p_(i,:)))
                C(y,x) = max(abs(I(p(i,1), p(i,2)) - I(p_(i,1), p_(i,2))), C(y,x)); 
            end
        end
    end
end

