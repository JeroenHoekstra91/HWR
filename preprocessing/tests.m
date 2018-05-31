%% line segmentation
clear; clc; close all;

load bw_images.mat;
load segmented_parchment.mat;

P = segm{6};

BW = binarization(P, 121, 0.34, 'sauvola');


imshow(remove_cc(BW));



%% TODO

% [ ] Improve CC removal to make it work for all images
% [ ] Offset for line segmentation to capture the ascenders
% [X] Look at line segmentation results for all the lines
% [ ] Fine tune sauvola for optimal results