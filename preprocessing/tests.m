% clear; clc; close all;

%Update this your path to the images folder
data_dir = '/Users/mario/Developer/HWR/data/image-data'; 
clean_data_dir = '/Users/mario/Developer/HWR/data/image-data/clean';

% List all files
dir_list = dir(data_dir); % All files with its metadata
files = [dir_list.name]; % All file names in a single string
files = files(4:length(files)); % Skip '.' and '..'
files = split(files, '.jpg'); % Split one row per file name without extension

% Separate BW from RGB images
bw_paths = [];
rgb_paths = [];
for i = 1:length(files)
    if contains(files(i), 'fused')
        bw_paths = [bw_paths; string(data_dir) + string('/') + files(i) + string('.jpg')]; 
    else
        rgb_paths = [rgb_paths; string(data_dir) + string('/') + files(i) + string('.jpg')]; 
    end
end

% Same but for clean images
dir_list = dir(clean_data_dir); % All files with its metadata
files = [dir_list.name]; % All file names in a single string
files = files(4:length(files)); % Skip '.' and '..'
files = split(files, '.jpg'); % Split one row per file name without extension

% Separate BW from RGB images
clean_paths = [];
for i = 1:length(files)
    clean_paths = [clean_paths; string(clean_data_dir) + string('/') + files(i) + string('.jpg')]; 
end

   
%% Remove characters from all images
% close all;
% for i = 1:length(bw_paths)
%     I =imread(char(bw_paths(i)));
%     cleanI = remove_tag(I, 100);
% %     subplot(1,2,1);
% %     imshow(cleanI);
% %     subplot(1,2,2);
% %     imshow(I-cleanI);
% %     waitforbuttonpress;
% end
% 
% %% Remove squared shapes
% close all;
% for i = 1:length(bw_paths)
%     I =imread(char(bw_paths(i)));
%     cleanI = remove_tag(I, 100);
% 
%     % Remove values brighter than 80 and normalize result (to have better
%     % resolution on darker colors)
%     to_remove = cleanI > 70;
%     cleanI(to_remove) = 0;
%     cleanI = mat2gray(cleanI);
%     
%     % Binarize and closing to isolate parchment and calibration palletes.
%     th = graythresh(cleanI);
%     cleanI = imbinarize(cleanI,th);
%     cleanI = imclose(cleanI, strel('square',80));
%     figure;
%     disp('figg');
%     imshow(cleanI);
%     waitforbuttonpress;
%     % Obtain edges and straight lines from edges
%     E = edge(cleanI);
%     [H, theta, rho] = hough(E);
%     peaks = houghpeaks(H, 10);
%     
%     imshow(E);
%     for peak = peaks' % iterate over rows
%         r = peak(1); t = peak(2);
%         hold on;
%         draw_line(I, rho(r), theta(t));
%     end
% 
%     waitforbuttonpress
% end
% % figure;

%% Morphological parchment segmentation and binarization
close all;
save_data_dir = '/Users/mario/Developer/HWR/results/parchment_segmentation/';
for i = 1:length(bw_paths)
    I =imread(char(bw_paths(i)));
%     fig = figure;
%     subplot(1,2,1)
%     imshow(I);
    
    Is = p_segment(I);
    Isr = imclose(Is, strel('square',60));
    Isr2 = imreconstruct(~Isr, ~Is);
    Isegmented = I;
    Isegmented(Isr2) = 0;
    
    BW = binarization(Isegmented, 121, 0.21, 'sauvola');
%     subplot(1,2,2)
%     imshow(Isegmented);
%     imshow(BW);
%     waitforbuttonpress;
    
    O = uint8(ones(size(I,1),(2*size(I,2)+20)));
    O(1:size(I,1),1:size(I,2)) = I;
    O(1:size(I,1),size(I,2)+21:size(O,2)) = Isegmented;
    imwrite(O, strcat(save_data_dir, 'ps',num2str(i), '.png'));
%     saveas(fig, strcat(save_data_dir, 'ps',num2str(i), '.png'));
%     close
end