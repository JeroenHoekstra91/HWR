function H = line_histogram( BW )
% LINE_HISTOGRAM Compute the black pixels within parchment histogram on the
% y axis
%
%       H = line_segmentation(BW)
%
%       INPUT
%       BW: Binary image (logical class).
%
%       OUTPUT
%       H: counts per row

    % Horizontal gravity histogram
    for i=1:size(BW,1)
        % Scan horizontally to find where the parchment begins and ends
        b = 1; e = size(BW,2); %Initialize begin,end to image size.
        for j=1:size(BW,2)
            if BW(i,j) > 0
                b = j;
                break;
            end
        end
        if b~=1 %if parchment was found in this line
            for j=size(BW,2):b
                if BW(i,j) > 0
                    e = j;
                    break;
                end
            end
        end
        if b~=1
            H(i) = uint32((e - b - sum(BW(i,b:e)))/(e-b) * 600); % percentage of black pixels normalised to 100
        else
            H(i) = 0;
        end
    end   
end

