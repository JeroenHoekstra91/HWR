function O = tests(I)
    segm = line_segmentation2(I, I);
    S = segm{7};
    [H, baseline, gap] = line_histogram2(S);
    
    O = visualize_baselines(histogram_visualization(S, H), baseline, gap);
    
end