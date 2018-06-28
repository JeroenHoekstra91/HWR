function O = tests(I, P, BW)
%     lines = line_segmentation2(BW, P);
%     O = adaptive_water_flow(lines{4});
    segm = line_segmentation2(BW, P);
    im = segm{3};
    O = adaptive_water_flow(im);
%     O(end, end+size(segm{3}
end