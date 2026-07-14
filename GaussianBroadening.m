%% Gaussian broadening function

function BroadEenrgySpectrumHisto = GaussianBroadening(Energy, counts, sigma, x)
    % Energy: Array of original energy levels
    % counts: counts in the detector per bin
    % sigma: Standard deviation for Gaussian broadening
    % x: Array of energies at which to evaluate the broadened spectrum


    BroadEenrgySpectrumHisto = zeros(size(x)); % Initialize the output array

    for i = 1:length(x)
        Ei = x(i);
        total = 0;
        for j = 1:length(Energy)
            Ej = Energy(j);
            os = counts(j);
            total = total + os * exp(-((Ej - Ei) / sigma)^2) ;
        end
        BroadEenrgySpectrumHisto(i) = total;
    end
end