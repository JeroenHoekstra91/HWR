function binarization_gui
    clear; clc; close all;
    
    %Change paths to your own machine
    data_dir = '/Users/mario/Developer/HWR-data/data/image-data/';
    save_dir = '/Users/mario/Developer/HWR-data/results/';
    
    disp('Reading images...');
%     [imgs, ~] = read_images(data_dir);
    load 'bw_images' 'bw';
    imgs = bw;
    disp('Done');
    disp('Segmenting parchment...');
%     segm = dataset_parchment_segmentation(imgs);
    load 'segmented_parchment';
    disp('Done');
    
    idx = 1;
    I = imgs{idx};
    P = segm{idx};
%     P = imgs{idx};
    O1 = I;
    O2 = P;
    BW = imbinarize(P, graythresh(P));
    src1 = 'original';
    src2 = 'parchment only';
    sz = 121;
    k = 0.34;
    left_hoverlay = false;
    right_hoverlay = false;
    
    save_path = strcat(save_dir, 'gui/');
    
    % Create a figure and axes
    f = figure('Visible','off','units','normalized','outerposition',[0 0 1 1]);
    ax = axes('Units','pixels');
	update
    
    source_list = {'original','parchment only','sauvola', 'median filter', 'otsu', 'adaptive', 'after CC', 'line segmentation'};
    
    % Create pop-up menu
    popup = uicontrol('Style', 'popup',...
       'String', source_list,...
       'Position', [20 550 100 50],...
       'Callback', @setsource, 'Tag', 'source1');    
   
    popup2 = uicontrol('Style', 'popup',...
       'String', source_list,...
       'Position', [900 550 100 50],...
       'Callback', @setsource, 'Tag', 'source2', 'val', 2);    
   
    % Next image button
    btn_next = uicontrol('Style', 'pushbutton', 'String', 'next image',...
    'Position', [120 20 60 20],...
    'Callback', @next);       
    
    fig_txt = uicontrol('Style','text',...
        'Position',[200 20 60 20],...
        'String',strcat('figure id: ',num2str(idx)));

    % Previous image button
    btn_prev = uicontrol('Style', 'pushbutton', 'String', 'previous image',...
    'Position', [20 20 80 20],...
    'Callback', @prev);       
    
    % Histogram overlay for left image
    chk_hist_left = uicontrol('Style', 'checkbox', 'String', 'histogram overlay',...
    'Position', [20 530 120 50],...
    'Callback', @hist_overlay, 'Tag', 'hleft');       
    
    % Histogram overlay for right image
    chk_hist_right = uicontrol('Style', 'checkbox', 'String', 'histogram overlay',...
    'Position', [900 530 120 50],...
    'Callback', @hist_overlay, 'Tag', 'hright');       
    
    % Save figures button
    btn_save = uicontrol('Style', 'pushbutton', 'String', 'save figures',...
    'Position', [950 20 60 20],...
    'Callback', @save);       

    % k slider label  
    k_txt = uicontrol('Style','text',...
    'Position',[300 20 120 20],...
    'String',strcat('k parameter: ',num2str(k)));

    % k slider
    sld_k = uicontrol('Style', 'slider',...
    'Min',0,'Max',1,'Value',0.21,...
    'Position', [400 20 120 20],...
    'Callback', @setk); 
    
    % sz slider label
    sz_txt = uicontrol('Style','text',...
    'Position',[600 20 200 20],...
    'String',strcat('Binarization window size: ', num2str(sz)));
    
    % sz slider
    sld_sz = uicontrol('Style', 'slider',...
    'Min',10,'Max',300,'Value',121,...
    'Position', [790 20 130 20],...
    'Callback', @setsz); 

    % Make figure visble after adding all components
    f.Visible = 'on';
    % This code uses dot notation to set properties. 
    % Dot notation runs in R2014b and later.
    % For R2014a and earlier: set(f,'Visible','on');

    function setsource(source,event)
        val = source.Value;
        maps = source.String;
        if source.Tag == 'source1'
            src1 = maps{val};
        else
            src2 = maps{val};
        end
        update;
    end

    function hist_overlay(source, event)
        val = source.Value;
        if strcmp(source.Tag, 'hleft')
            left_hoverlay = val;
        else
            right_hoverlay = val;
        end
        update;
    end

    function next(source, event)
        if idx < length(imgs)
            idx = idx + 1;
            I = imgs{idx};
            P = segm{idx};
            update;
        end
        fig_txt.String = strcat('figure id: ', num2str(idx));
    end

    function prev(source, event)
        if idx > 1
            idx = idx - 1;
            I = imgs{idx};
            P = segm{idx};
            update;
        end
        fig_txt.String = strcat('figure id: ', num2str(idx));
    end

    function save(source, event)
        if length(size(O1)) > 2 | length(size(O2)) > 2
            OW = uint8(ones(size(I,1),(2*size(I,2)+20),3)*255);
            if length(size(O1)) > 2
                OW(1:size(I,1),1:size(I,2),:) = O1;
            else
                OW(1:size(I,1),1:size(I,2),1) = O1;
                OW(1:size(I,1),1:size(I,2),2) = O1;
                OW(1:size(I,1),1:size(I,2),3) = O1;
            end
            if length(size(O2)) > 2
                OW(1:size(I,1),size(I,2)+21:size(OW,2),:) = O2;
            else
                OW(1:size(I,1),size(I,2)+21:size(OW,2),1) = O2;
                OW(1:size(I,1),size(I,2)+21:size(OW,2),2) = O2;
                OW(1:size(I,1),size(I,2)+21:size(OW,2),3) = O2;
            end
        else
            OW = uint8(ones(size(I,1),(2*size(I,2)+20))*255);
            OW(1:size(I,1),1:size(I,2),1) = O1;
            OW(1:size(I,1),size(I,2)+21:size(OW,2)) = O2;
        end
        imwrite(OW, strcat(save_path, num2str(idx), '_', src1, '_', src2, '.png'));
    end

    function setk(source, event)
        k = source.Value;
        k_txt.String = strcat('k parameter: ', num2str(k));
%         set(k_txt.statictext, 'String', strcat('Binarization window size: ', num2str(sz)));
        update;
    end

    function setsz(source, event)
        sz = 2*floor(source.Value/2)+1;
        sz_txt.String = strcat('Binarization window size: ', num2str(sz));
        update;
    end

    function update
        switch src1
            case 'original'
                O1 = I;
            case 'parchment only'
                O1 = P;
            case 'sauvola'
                O1 = binarization(P, sz, k, 'niblack')*255;
            case 'median filter'
                med = medfilt2(P, [7 7]);
                O1 = binarization(med, sz, k, 'sauvola')*255;
            case 'otsu'
                O1 = imbinarize(P, graythresh(P))*255;
            case 'adaptive'
                O1 = imbinarize(P, 'adaptive')*255;
            case 'after CC'
                BW = binarization(P, sz, k, 'sauvola');
                O1 = remove_cc(BW);
            case 'line histogram'
                BW = binarization(P, sz, k, 'sauvola');
                BW = remove_cc(BW);
                H = line_histogram2(BW);
                O1 = histogram_visualization(I, H);
            case 'line segmentation'
                BW = binarization(P, sz, k, 'sauvola');
                lines = line_segmentation2  (BW, I);
                O1 = lines_segmented_visualization(lines);
        end
        switch src2
            case 'original'
                O2 = I;
            case 'parchment only'
                O2 = P;
            case 'sauvola'
                O2 = binarization(P, sz, k, 'sauvola')*255;
            case 'median filter'
                med = medfilt2(P, [7 7]);
                O2 = binarization(med, sz, k, 'sauvola')*255;
            case 'otsu'
                O2 = imbinarize(P, graythresh(P))*255;
            case 'after CC'
                BW = binarization(P, sz, k, 'sauvola');
                O2 = remove_cc(BW);
            case 'line histogram'
                BW = binarization(P, sz, k, 'sauvola');
                BW = remove_cc(BW);
                H = line_histogram2(BW);
                O2 = histogram_visualization(I, H);
            case 'line segmentation'
                BW = binarization(P, sz, k, 'sauvola');
                lines = line_segmentation2(BW, I);
                O2 = lines_segmented_visualization(lines);
        end
        if left_hoverlay && ~ strcmp('line segmentation', src1)
            BW = binarization(P, sz, k, 'sauvola');
            BW = remove_cc(BW);
            [H, baselines, gaps] = line_histogram2(BW);
%             [H, baselines, gaps] = line_histogram2(O1);
            O1 = visualize_baselines(O1, baselines, gaps);
            O1 = histogram_visualization(O1, H);
        end
        if right_hoverlay && ~ strcmp('line segmentation', src2)
            BW = binarization(P, sz, k, 'sauvola');
            BW = remove_cc(BW);
            
            ver = strel('rectangle', [7 1]);
            hor = strel('rectangle', [1 15]);
            BW = imdilate(~BW, hor);
            BW = imerode(BW, ver);
            BW = ~BW;
            [H, baselines, gaps] = line_histogram2(BW);
            O2 = visualize_baselines(O2, baselines, gaps);
            O2 = histogram_visualization(O2, H);
        end
        subplot(1,2,1);
        imshow(O1);
        subplot(1,2,2);
        imshow(O2);        
    end
end
