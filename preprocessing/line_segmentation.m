clear; close all; clc;

%Update this your path to the images folder
data_dir = '/Users/mario/Developer/HWR/data/image-data'; 
% List all files
dir_list = dir(data_dir); % All files with its metadata
files = [dir_list.name]; % All file names in a single string
files = files(4:length(files)); % Skip '.' and '..'
files = split(files, '.jpg'); % Split one row per file name without extension

% Separate BW from RGB images
bw_paths = [];
rgb_paths = [];
for im = 1:length(files)
    if contains(files(im), 'fused')
        bw_paths = [bw_paths; string(data_dir) + string('/') + files(im) + string('.jpg')]; 
    else
        rgb_paths = [rgb_paths; string(data_dir) + string('/') + files(im) + string('.jpg')]; 
    end
end

%% segment parchment and compute horizontal gravity histogram

save_data_dir = '/Users/mario/Developer/HWR/results/line_histograms/';
for im = 1:length(bw_paths)
    I =imread(char(bw_paths(im)));
    P = p_segment(I);
    
    % Horizontal gravity histogram
    for i=1:size(P,1)
        % Scan horizontally to find where the parchment begins and ends
        b = 1; e = size(P,2); %Initialize begin,end to image size.
        for j=1:size(P,2)
            if P(i,j) > 0
                b = j;
                break;
            end
        end
        if b~=1 %if parchment was found in this line
            for j=size(P,2):b
                if P(i,j) > 0
                    e = j;
                    break;
                end
            end
        end
        if b~=1
            H(i) = uint32((e - b - sum(P(i,b:e)))/(e-b) * 600); % percentage of black pixels normalised to 100
        else
            H(i) = 0;
        end
    end   
    %Visualize
    O = uint8(ones(size(I,1),(2*size(I,2)+20), 3)*255);
    O(1:size(I,1),1:size(I,2),1) = I;
    O(1:size(I,1),1:size(I,2),2) = I;
    O(1:size(I,1),1:size(I,2),3) = I;
    O(1:size(I,1),size(I,2)+21:size(O,2),1) = P*255;
    O(1:size(I,1),size(I,2)+21:size(O,2),2) = P*255;
    O(1:size(I,1),size(I,2)+21:size(O,2),3) = P*255;
    for i=1:size(O,1)
        O(i,size(O,2)-(H(i)-1):size(O,2),1) = 255;
        O(i,size(O,2)-(H(i)-1):size(O,2),2) = 0;
        O(i,size(O,2)-(H(i)-1):size(O,2),3) = 255;
    end
    imwrite(O, strcat(save_data_dir, 'ps',num2str(im), '.png'));
end








