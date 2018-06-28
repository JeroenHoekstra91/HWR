clear;
% I = [10,10,10,10,10,10,10,10,10,10;10,10,10,10,10,10,10,10,10,10;10,10,10,10,10,10,10,10,10,10;10,10,10,10,10,10,10,10,10,10;10,10,10,10,4,10,10,10,10,10;10,10,10,10,10,10,10,10,10,10;10,10,10,10,2,10,0,10,10,10;10,10,10,10,10,10,10,10,10,10;10,10,10,10,10,10,10,10,10,10;10,10,10,10,10,10,10,10,10,10];
% i = 5; j = 5;
% [i, j] = local_minima(I, i, j);


I = [true,true,true,true,true,true,true,true,true,true;true,true,false,false,false,true,true,true,true,true;true,true,false,false,false,true,true,true,true,true;true,true,false,false,false,true,true,true,true,true;true,true,false,false,false,true,true,true,true,true;true,true,false,false,false,true,true,true,true,true;true,true,false,false,false,true,true,true,true,true;true,true,false,true,true,true,true,true,true,true;true,true,false,true,true,true,true,true,true,true;true,true,false,true,true,true,true,true,true,true];
[SW, BRIs] = compute_stroke_width(I);

BRI1 = BRIs(:,:,1);
BRI2 = BRIs(:,:,2);
BRI3 = BRIs(:,:,3);
BRI4 = BRIs(:,:,4);

% [i_next, j_next] = i-W-1