%% To save all the words
    
    % Directory where the the given images are stored
    data_dir = '/Users/mario/Developer/HWR-data/data/image-data/';
    
    % where to save the extracted words
    folder_save = '/Users/mario/Developer/HWR-data/results/word-seg';

    % get the images and the segmented parchments
    [imgs, ~] = read_images(data_dir);
    parchment_only = [];
    for i = 1:length(imgs)
        parchment_only{i} = p_segment(imgs{i});
    end
    

    for i = 1:size(parchment_only,2)
        % get all the lines from parchment i
        cur_parchment = parchment_only{i};
        parchment_bin = binarization(cur_parchment, 121, 0.34, 'sauvola');
        bin_lines = line_segmentation_bin_line(parchment_bin, imgs{i});
        for j = 1:size(lines)
            % get all word positions from line j in parchment i 
            % line_cur needs to be a binarized line
            line_cur = bin_lines{j};
            rm_background = remove_background_cc(line_cur);
            rm_boundary_noise = remove_boundary_noise(rm_background);
            [r c] = size(rm_boundary_noise);
            add_padding = logical(ones(r,c+250));
            add_padding(:,125:c+124) = rm_boundary_noise; 
            word_positions = word_histogram(add_padding);
            word_start = word_positions(:,1);
            word_indx = word_start > 0;
            word_count = 1;
            for k = 1:length(word_indx)
                % save all the words 
                if word_indx(k)
                    baseFileName = sprintf('Parchment#%d_Line#%d_Word#%d.png', i,j,word_count);
                    fullFileName = fullfile(folder_save, baseFileName);
                    word_cur = add_padding(:, word_positions(k,1):word_positions(k,2));
                    imwrite(word_cur, fullFileName);
                    word_count = word_count + 1;
                end
            end
        end
    end

%%


