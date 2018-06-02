%% line segmentation
clear; clc; close all;

load bw_images.mat;
load segmented_parchment.mat;

P = segm{6};

BW = medfilt2(binarization(P, 121, 0.34, 'sauvola'), [7 7]);


%REMOVE_CC Summary of this function goes here
%   Detailed explanation goes here
    CC = bwconncomp(~BW);

    numPixels = cellfun(@numel,CC.PixelIdxList);
    [~,idx] = max(numPixels);
    BW(CC.PixelIdxList{idx}) = 1;

    numPixels(idx) = []; %Remove background component
    CC.PixelIdxList(idx) = [];
    CC.NumObjects = CC.NumObjects - 1;
    S = std(numPixels);
    mu = mean(numPixels);

    % Remove components that are further than 2stds from the mean
    toRemove = abs(mu-numPixels) > S*2;
    for i=1:length(toRemove) %for some reason we have to run the loop manually, cant pass the whole list to PixelIdxList
        if toRemove(i)
            toRemoveImg = CC.PixelIdxList{i};
            BW(toRemoveImg) = 1;
        end
    end

% VISUALIZE ---------------------------------------------
imshow(BW);



%% TODO

% [ ] Improve CC removal to make it work for all images
% [ ] Offset for line segmentation to capture the ascenders
% [X] Look at line segmentation results for all the lines
% [ ] Fine tune sauvola for optimal results