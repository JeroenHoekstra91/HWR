%% line segmentation
clear; clc; close all;

load bw_images.mat;
load segmented_parchment.mat;

P = segm{15};

BW = binarization(P, 121, 0.34, 'sauvola');
R = BW;

%% dilation/erosion for improving peak detection

BW2 = remove_cc(BW);

ver = strel('rectangle', [7 1]);
hor = strel('rectangle', [1 15]);
BW2 = imdilate(~BW2, hor);
BW2 = imerode(BW2, ver);
subplot(1,2,1)
imshow(BW2);
H = line_histogram2(~BW2);
subplot(1,2,2);
imshow(histogram_visualization(R, H));

%% rotating image to maximise histogram peak volume
%14, 15, 20
close all;
BWcc = remove_cc(BW);
best_score = 0;
best_orientation = -100;
for a = -10:2:10
    BW2 = imrotate(~BWcc, a, 'nearest', 'crop'); %image is inverted so that background added from rotation is the same
    [H, baselines, ~] = line_histogram2(~BW2); %reinvert the image to get black chars
    
    total_peaks = sum(H(baselines));
    if total_peaks > best_score
        best_score = total_peaks;
        best_orientation = a;
    end
    
    BW2 = histogram_visualization(~BW2, H);
    BW2 = visualize_baselines(BW2, baselines, baselines);
    BW2 = insertText(BW2, [200 200], num2str(total_peaks), 'FontSize', 100);
    figure
    imshow(BW2);
end

figure
subplot(1, 2, 1);
title('Original orientation');
[H, baselines, ~] = line_histogram2(BW);
BW2 = histogram_visualization(BWcc, H);
BW2 = visualize_baselines(BW, baselines, baselines);
imshow(BW2);
subplot(1, 2, 2);
title(strcat('Rotated image by ', num2str(best_orientation)));
BW2 = imrotate(BWcc, best_orientation, 'nearest', 'crop');
[H, baselines, ~] = line_histogram2(BW2);
BW2 = histogram_visualization(BW2, H);
BW2 = visualize_baselines(BW2, baselines, baselines);
imshow(BW2);


%% TODO

% [ ] Improve CC removal to make it work for all images
% [ ] Offset for line segmentation to capture the ascenders
% [X] Look at line segmentation results for all the lines
% [ ] Fine tune sauvola for optimal results