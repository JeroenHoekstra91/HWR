function [SW, BRIs] = compute_stroke_width(BW)
    %Computes stroke width (SW) based on Black Run Images according to paper

    D = [-1,1; 0, 1; 1, 1; 1, 0]; %scannig directions (row, colum offset)
    BRIs = ones([size(BW), length(D)])*Inf; %Black Run Image for each of the directions
%     BRI = ones(size(I))*inf;
    [black_i, black_j] = find(BW(2:end-1, 1:end-1) == 0); %no left padding because directions are towards the right always
    black_pixels_idx = [black_i+1, black_j];% +1 on i since we start at 2
    %Find min BRI for each black pixel
    for p = 1:length(black_pixels_idx)
        p_idx = black_pixels_idx(p,:);
        for i = 1:length(D)
            line = p_idx;
            next_idx = p_idx+D(i,:); %subindices of the next pixel in direction i
            bri = 0; %Number of black pixels in direction i
            %If p_idx has already been computed skip it
            if BRIs(p_idx(1), p_idx(2), i) ~= Inf
                disp('skipping');
                continue;
            end
            %Traverse in direction i
            while BW(next_idx(1), next_idx(2)) == 0
                line(end+1,:) = next_idx;
                bri = bri + 1;
                next_idx = next_idx + D(i,:);
                if any( next_idx < [1,2]) || any( next_idx > size(BW)-1 )
                    break;
                end
            end
            BRIs(sub2ind(size(BRIs), [line ones(size(line,1),1)*i])) = bri;
        end
    end
    SW = min(BRIs,[], 3);
    SW(find(SW == Inf)) = 0;%Set white pixels stroke to 0
    SW = movmean(SW, 30); %Smooth stroke width
end