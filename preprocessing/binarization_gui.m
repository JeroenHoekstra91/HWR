function binarization_gui
    clear; clc; close all;
    
    %Change paths to your own machine
    data_dir = '/Users/mario/Developer/HWR-data/data/image-data/';
    save_dir = '/Users/mario/Developer/HWR-data/results/';
    
    disp('Reading images...');
    [imgs, ~] = read_images(data_dir);
    disp('Done');
    disp('Segmenting parchment...');
    segm = dataset_parchment_segmentation(imgs);
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
    k = 0.21;
    
    save_path = strcat(save_dir, 'gui/');
    
    % Create a figure and axes
    f = figure('Visible','off','units','normalized','outerposition',[0 0 1 1]);
    ax = axes('Units','pixels');
	update

    % Create pop-up menu
    popup = uicontrol('Style', 'popup',...
       'String', {'original','parchment only','sauvola', 'otsu'},...
       'Position', [20 550 100 50],...
       'Callback', @setsource, 'Tag', 'source1');    
   
    popup2 = uicontrol('Style', 'popup',...
       'String', {'original','parchment only','sauvola', 'otsu'},...
       'Position', [900 550 100 50],...
       'Callback', @setsource, 'Tag', 'source2', 'val', 2);    
   
    % Next image button
    btn_next = uicontrol('Style', 'pushbutton', 'String', 'next image',...
    'Position', [120 20 60 20],...
    'Callback', @next);       
    
    % Previous image button
    btn_prev = uicontrol('Style', 'pushbutton', 'String', 'previous image',...
    'Position', [20 20 80 20],...
    'Callback', @prev);       
    
    % Save figures button
    btn_save = uicontrol('Style', 'pushbutton', 'String', 'save figures',...
    'Position', [850 20 60 20],...
    'Callback', @save);       

    % k slider label  
    txt = uicontrol('Style','text',...
    'Position',[300 20 120 20],...
    'String','k parameter');

    % k slider
    sld_k = uicontrol('Style', 'slider',...
    'Min',0,'Max',1,'Value',0.21,...
    'Position', [400 20 120 20],...
    'Callback', @setk); 
    
    % sz slider label
    txt = uicontrol('Style','text',...
    'Position',[600 20 120 20],...
    'String','Binarization window size');
    
    % sz slider
    sld_sz = uicontrol('Style', 'slider',...
    'Min',10,'Max',300,'Value',121,...
    'Position', [720 20 120 20],...
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

    function next(source, event)
        if idx < length(imgs)
            idx = idx + 1;
            I = imgs{idx};
            P = segm{idx};
            update;
        end
    end

    function prev(source, event)
        if idx > 1
            idx = idx - 1;
            I = imgs{idx};
            P = segm{idx};
            update;
        end
    end

    function save(source, event)
        OW = uint8(ones(size(I,1),(2*size(I,2)+20))*255);
        OW(1:size(I,1),1:size(I,2),1) = O1;
        OW(1:size(I,1),size(I,2)+21:size(OW,2)) = O2;
        imwrite(OW, strcat(save_path, num2str(idx), '_', src1, '_', src2, '.png'));
    end

    function setk(source, event)
        k = source.Value
        update;
    end

    function setsz(source, event)
        sz = 2*floor(source.Value/2)+1;
        update;
    end

    function update
        switch src1
            case 'original'
                O1 = I;
            case 'parchment only'
                O1 = P;
            case 'sauvola'
                O1 = binarization(P, sz, k, 'sauvola')*255;
            case 'otsu'
                O1 = imbinarize(P, graythresh(P))*255;
        end
        switch src2
            case 'original'
                O2 = I;
            case 'parchment only'
                O2 = P;
            case 'sauvola'
                O2 = binarization(P, sz, k, 'sauvola')*255;
            case 'otsu'
                O2 = imbinarize(P, graythresh(P))*255;
        end
        subplot(1,2,1);
        imshow(O1);
        subplot(1,2,2);
        imshow(O2);        
    end
end