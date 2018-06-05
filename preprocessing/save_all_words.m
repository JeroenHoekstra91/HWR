%% To save all the words
    
    % Directory where the the given images are stored
    data_dir = 'X:\My Desktop\image-data\';
    
    % where to save the extracted words
    folder_save = 'X:\My Desktop\extracted_words\';

    % get the images and the segmented parchments
    [imgs, ~] = read_images(data_dir);
    parchment_only = dataset_parchment_segmentation(imgs);
    

    for i = 1:size(parchment_only,2)
        % get all the lines from parchment i
        cur_parchment = parchment_only{i};
        parchment_bin = binarization(cur_parchment, 121, 0.34, 'sauvola');
        lines = line_segmentation_bin_line(parchment_bin, imgs{i});
        for j = 1:size(lines)
            % get all word positions from line j in parchment i 
            line_cur = lines{j};
            rm_background = remove_background_cc(line_cur);
            rm_boundary_noise = remove_boundary_noise(rm_background);
            word_positions = word_histogram(rm_boundary_noise);
            word_start = word_positions(:,1);
            word_indx = word_start > 0;
            word_count = 0;
            for k = 1:length(word_indx)
                % save all the words 
                if word_indx(k)
                    baseFileName = sprintf('Word#%d_Line#%d_Parchment#%d.png', word_count,j,i);
                    fullFileName = fullfile(folder_save, baseFileName);
                    word_cur = rm_boundary_noise(:, word_positions(k,1):word_positions(k,2));
                    imwrite(word_cur, fullFileName);
                    word_count = word_count + 1;
                end
            end
        end
    end

%%

