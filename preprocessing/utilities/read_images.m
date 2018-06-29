function [imgs, file_names] = read_images(data_dir)
    warning('off', 'backtrace')
    % List all files
    dir_list = dir(data_dir); % All files with its metadata
    dir_list = dir_list(~[dir_list.isdir]);
    imgs = {};
    file_names = {};
    for i = 1:length(dir_list)
        file_name = dir_list(i).name;
        try
            I = imread(fullfile(data_dir, file_name));
        catch ex
            warning(['File ', file_name, ' could not be read as an image. Skipping...'])
            continue;
        end
        file_names{end+1} = file_name;
        if length(size(I)) > 2
            warning(['Our pipeline only works for gray images, converting ', file_name, ' to gray values']);
            I = rgb2gray(I);
        end
        imgs{end+1} = I;
    end
end