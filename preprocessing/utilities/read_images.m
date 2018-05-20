function [bw, rgb] = read_images(data_dir)
    % List all files
    dir_list = dir(data_dir); % All files with its metadata
    
    % Keep only jpg images and separate color from grayscale
    idx = 0;
    bw = {};
    rgb = {};
    for i = 1:length(dir_list)
        file_name = dir_list(i).name;
        if file_name(1) == '.' | ~contains(file_name, '.jpg') %not an image we are interested in
            continue;
        end
        if contains(file_name, 'fused') %BW
            bw{end+1} = imread(strcat(data_dir, file_name));
        else %RGB
            rgb{end+1} = imread(strcat(data_dir, file_name));
        end
    end
    
%     files = [dir_list.name]; % All file names in a single string
%     files = files(4:length(files)); % Skip '.' and '..'
%     files = split(files, '.jpg'); % Split one row per file name without extension
%     bw = {};
%     % Separate BW from RGB images
%     for i = 1:length(files)
%         if contains(files(i), 'fused')
%             bw_paths = string(data_dir) + string('/') + files(i) + string('.jpg'); 
%             bw{end+1} = imread(char(bw_paths));
%         end
% %         else
% %             rgb_paths = string(data_dir) + string('/') + files(i) + string('.jpg'); 
% %             rgb{i} = imread(char(rgb_paths));
% %         end
%     end
end