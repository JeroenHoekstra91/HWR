function O = histogram_visualization( I, H )
% HISTOGRAM_VISUALIZATION Compute the black pixels within parchment histogram on the
% y axis
%
%       O = histogram_visualization( I, H )
%
%       INPUT
%       I: 2d reference image where histogram is embedded.
%       H: Histogram (vector)
%
%       OUTPUT
%       O: Embedded histogram (3d image)

    if strcmp(class(I), 'logical')
        I = uint8(I)*255;
    end
    O = uint8(ones([size(I), 3]));
    O(1:size(I,1),1:size(I,2),1) = I;
    O(1:size(I,1),1:size(I,2),2) = I;
    O(1:size(I,1),1:size(I,2),3) = I;
    H = int32(H);
    for i=1:size(O,1)
        O(i,size(O,2)-(H(i)-1):size(O,2),1) = 255;
        O(i,size(O,2)-(H(i)-1):size(O,2),2) = 0;
        O(i,size(O,2)-(H(i)-1):size(O,2),3) = 255;
    end
end

