%% Gaussian broadening with uncertainty propagation

function [BroadEnergySpectrumHisto, BroadError] = GaussianBroadening(Energy, counts, resolutionRef, energyRef)

    BroadEnergySpectrumHisto = zeros(size(Energy));
    BroadVariance = zeros(size(Energy)); 

    for j = 1:length(Energy)

        if counts(j) <= 0 || Energy(j) <= 0
            continue
        end

        FWHM = resolutionRef * sqrt(energyRef * Energy(j));
        sigma = FWHM / 2.355;

        lowerIndex = find(Energy >= Energy(j) - 5*sigma, 1, 'first');
        upperIndex = find(Energy <= Energy(j) + 5*sigma, 1, 'last');

        gaussian = exp(-0.5*((Energy(lowerIndex:upperIndex) - Energy(j))/sigma).^2);
        gaussian = gaussian/sum(gaussian); 

       
        BroadEnergySpectrumHisto(lowerIndex:upperIndex) = BroadEnergySpectrumHisto(lowerIndex:upperIndex) + counts(j)*gaussian;
        BroadVariance(lowerIndex:upperIndex) = BroadVariance(lowerIndex:upperIndex) + counts(j)*(gaussian.^2);
    end
    
    BroadError = sqrt(BroadVariance);

end
