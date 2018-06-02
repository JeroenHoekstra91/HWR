%% line segmentation
clear; clc; close all;

load bw_images.mat;
load segmented_parchment.mat;

P = segm{12};

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



%% TODO

% [ ] Improve CC removal to make it work for all images
% [ ] Offset for line segmentation to capture the ascenders
% [X] Look at line segmentation results for all the lines
% [ ] Fine tune sauvola for optimal results