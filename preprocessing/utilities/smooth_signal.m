function sm = smooth_signal(S,w)
%SMOOTH_SIGNAL Applies smoothing to signal S based on smoothing factor w
%   INPUTS
%   S: signal to be smoothed
%   w: smoothing factor (higher -> smoothier)
%
%   OUTPUTS
%   sm: smoothed signal

    coeff = ones(1, w)/w;
    sm = filter(coeff, 1, S);
end

