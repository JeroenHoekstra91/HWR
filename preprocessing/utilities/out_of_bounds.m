function ob = out_of_bounds(sz,sb)
%OUT_OF_BOUNDS checks if subindex sb is out of bounds of size sz
%   only works for 2D matrices
    ob = any(sb < 1) || any(sb > sz);
end

