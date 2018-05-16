function P = dataset_parchment_segmentation(src)

%     save_dir = '/Users/mario/Developer/HWR-data/results/parchment_segmentation';
    for i = 1:length(src)
        I =src{i};

        Is = p_segment(I);
%         imwrite(Is, strcat(save_dir, num2str(i), 'slides-sw.png'));
        Isr = imclose(Is, strel('square',60));
%         imwrite(Isr, strcat(save_dir, num2str(i), 'close-to-remove-char.png'));
        Isr2 = imreconstruct(~Isr, ~Is);
%         imwrite(Isr2, strcat(save_dir, num2str(i), 'reconstruct-on-inverted-images.png'));
        Isegmented = I;
        Isegmented(Isr2) = 0;
%         imwrite(Isegmented, strcat(save_dir, num2str(i), 'applying-segmentation.png'));
        P{i} = Isegmented;
%         Is = cast(Is, 'uint8');
%         Is(Is == 1) = 255;
%         P{i} = Is;
%         O = uint8(ones(size(I,1),(2*size(I,2)+20))*255);
%         O(1:size(I,1),1:size(I,2)) = Is*255;
%         O(1:size(I,1),size(I,2)+21:size(O,2)) = Isegmented*255;
%         imwrite(O, strcat(save_dir, 'ps',num2str(i), '.png'));
    end
end