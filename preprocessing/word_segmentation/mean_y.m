function [mean] = mean_y(mat)
% gives the mean y of all the ones in the matrix. This is used 
% to get the mean y position of a component

    [row col] = size(mat);
    mean = 0;
    freq = 0;
    for i = 1: row
        for j = 1:col
            if mat(i,j) == 1
                mean = mean + i;
                freq = freq + 1;
            end
        end
    end
    mean = mean/freq;
end

