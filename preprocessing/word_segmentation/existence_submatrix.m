function [found] = existence_submatrix(total,sub)
% finds if the submatrix is present withing the total matrix
	found = false;
    for x = 1:size(total,1)-size(sub,1)+1
         for y = 1:size(total,2)-size(sub,2)+1
             for z = 1:size(total,3)-size(sub,3)+1
                 block = total(x:x+size(sub,1)-1,y:y+size(sub,2)-1,z:z+size(sub,3)-1);
                 if isequal(sub,block)
                     found = true;
                 end
             end
         end
    end  
end

