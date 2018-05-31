%% line segmentation
clear; clc; close all;

load('bw_images');

save_data_dir = '/Users/mario/Developer/HWR-data/results/line_segmentation/';

I = bw{12};
R = p_segment(I);

BW = binarization(p_segment(I), 121, 0.34, 'sauvola');

    % FUNCTION BEGINS HERE____________________________________
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
    
    % Remove components that are further than 2stds from the mean
    toRemove = abs(mu-numPixels) > S*2;
    for i=1:length(toRemove) %for some reason we have to run the loop manually, cant pass the whole list to PixelIdxList
        if toRemove(i)
            toRemoveImg = CC.PixelIdxList{i};
            BW(toRemoveImg) = 1;
        end
    end
    
    H = line_histogram2(BW);

    H = double(H);

    %smooth Histogram and find maxima
    H = smooth_signal(H, 30);
    [pks, baselines] = findpeaks(H,'MinPeakProminence',40);

    x = [1:length(H)];

    %minima
    Hinv = H*-1;
    [~, gaps] = findpeaks(Hinv,'MinPeakProminence',60);
    
    % Segment based on maxima,minima
    dists = pdist2(baselines, gaps);
    seg = {}
    for bs = 1:length(baselines) %iterate through all lines
        [min_dist, loc] = sort(dists(bs, :)); %sort gaps by distance to baseline
        above = gaps < baselines(bs); %find all gaps above current baseline
        above_idx = loc(find(above(loc), 1)); %select closest gap that is above
        below = gaps > baselines(bs);
        below_idx = loc(find(below(loc), 1));
        %segment based on which gaps have been found
        if above_idx & below_idx
            seg{bs} = R(gaps(above_idx):gaps(below_idx), :);
        elseif above
            seg{bs} = R(gaps(above_idx):min(size(R,1),baselines(bs)+dists(above_idx)), :); %equidistant above and below
        else
            seg{bs} = R(max(1, baselines(bs) - dists(below_idx)):gaps(below_idx), :); %equidistant above and below
        end
    end
    
  %% visualize segmented lines
  figure;
  O = [];
  for i= 1:length(seg)
%       subplot(length(seg), 1, i)
      bin = binarization(seg{i},  2*floor(size(seg{i}, 1)/2)+1, 0.34, 'sauvola');
      O = uint8(double([O; ones(20, length(bin))*128; bin*255]));
%       imshow(bin);
  end
  imshow(O)
 
%% visualize baseline and gaps
figure;
O = histogram_visualization(BW*255, H);
imshow(I);
hold on;
x = repmat([1,size(I, 2)]', [1, length(baselines)]);
y = [baselines,baselines]';
plot(x, y, 'Color', 'b', 'LineWidth', 2);

x2 = repmat([1,size(I, 2)]', [1, length(gaps)]);
y2 = [gaps,gaps]';
plot(x2, y2, 'Color', 'r', 'LineWidth', 2);

%% FFT
% clc; close all;
figure;
Y = fft(H);
Fs = 1;
N = length(H);
freqHz = (0:length(H)-1)*Fs/N;
plot(freqHz, abs(Y), 'Color', 'b');
hold on;
Y2 = Y;
Y2(length(Y2)/2:length(Y2)) = 0;
plot(freqHz, abs(Y2), 'Color', 'r');

Hclean = ifft(Y2);
figure;
plot(Hclean)
figure, plot(H);


%% Histogram smoothing

% plot(H, 'Color', 'b');
hold on;
plot(smoothedH, 'Color', 'r');



%% TODO

% [ ] Offset for line segmentation to capture the ascenders
% [ ] Look at line segmentation results for all the lines
% [ ] Fine tune sauvola for optimal results