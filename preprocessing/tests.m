%% line segmentation
clear; clc; close all;

load('bw_images');

save_data_dir = '/Users/mario/Developer/HWR-data/results/line_segmentation/';

I = bw{12};

BW = binarization(p_segment(I), 121, 0.34, 'sauvola');

%Fuse background with parchment
CC = bwconncomp(~BW);

numPixels = cellfun(@numel,CC.PixelIdxList);
[biggest,idx] = max(numPixels);
BW(CC.PixelIdxList{idx}) = 1;

numPixels(idx) = []; %Remove background component
background = CC.PixelIdxList{idx};
CC.PixelIdxList(idx) = [];
CC.NumObjects = CC.NumObjects - 1;
S = std(numPixels);
mu = mean(numPixels);

%% Remove components that are further than 2stds from the mean
toRemove = abs(mu-numPixels) > S*2;
for i=1:length(toRemove)
    if toRemove(i)
        toRemoveImg = CC.PixelIdxList{i};
        BW(toRemoveImg) = 1;
    end
end



%% Compute histogram

%Get background back -> Neccesary because it modulates the histogram (row
%count is % of pixels of that parchment line that are black
BW(background) = 1;
H = line_histogram2(BW);

H = double(H);
[pks, baseline] = findpeaks(H,'MinPeakProminence',40);

x = [1:length(H)];

plot(x, H);
hold on;
scatter(baseline, H(baseline), 'filled');

%minima
Hinv = H*-1;
figure,
plot(x, Hinv);
[~, gaps] = findpeaks(Hinv,'MinPeakProminence',60);
hold on;
scatter(gaps, Hinv(gaps), 'filled');

%% visualize baseline and gaps
figure;
O = histogram_visualization(BW*255, H);
imshow(O);
hold on;
x = repmat([1,size(I, 2)]', [1, length(baseline)]);
y = [baseline,baseline]';
plot(x, y, 'Color', 'b', 'LineWidth', 2);

% x2 = repmat([1,size(I, 2)]', [1, length(gaps)]);
% y2 = [gaps,gaps]';
% plot(x2, y2, 'Color', 'r', 'LineWidth', 2);