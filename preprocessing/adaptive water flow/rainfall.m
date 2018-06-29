function G = rainfall(I, BW, SW)

%     edges = edge(I, 'Canny'); %ROIs for pouring water
    edges = edge(BW, 'Canny'); %ROIs for pouring water
    
    rois = find(edges);
    S = zeros(size(I)); %Threshold for stopping rainfall
    C = local_contrast(I, edges, SW);
    G = I;
    while any(any(S < C)) %rainfall while stopping condition is not met for at least one pixel
        for idx = 1:length(rois)
            [y, x] = ind2sub(size(edges),    rois(idx));
            if S(y,x) < C(y,x)%only drop water if stopping condition is not met
                [i, j] = local_minima(I, y, x);
                G(i,j) = G(i,j) + SW(i, j)/2;
                S(y,x) = S(y,x) + 1;
            end
        end
    end
end