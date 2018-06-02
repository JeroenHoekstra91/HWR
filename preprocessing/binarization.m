function bw = binarization(I, sz, k, method)

    I_ = double(I);
    
    assert(mod(sz,2) ~= 0, 'sz must be odd');
    assert(sz > 2, 'sz must be 3 or greater');
    assert(strcmp('niblack', method) | strcmp('sauvola', method), '''method'' must be either ''niblack'' or ''sauvola'''); 
    
    dist = floor(sz/2);

    m = movmean(I_, dist);
    s = movstd(I_, dist);
    
    if strcmp('niblack', method)
        T = m + k*s;
    else
        R = max(s(:)) - min(s(:));
        T = m.*(1+k*(s/R-1));
    end
    
    T = cast(T, class(I));
    
    bw = I > T;    
    bw = medfilt2(bw, [7 7]);

end