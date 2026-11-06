import numpy as np

def GaussianBroadening(Energy, counts, resolutionRef, energyRef):

    BroadEnergySpectrumHisto = np.zeros_like(Energy, dtype=float)
    BroadVariance = np.zeros_like(Energy, dtype=float)

    for j in range(len(Energy)):

        if counts[j] <= 0 or Energy[j] <= 0:
            continue

        FWHM = resolutionRef * np.sqrt(energyRef * Energy[j])
        sigma = FWHM / 2.355

        lowerIndex = np.where(Energy >= Energy[j] - 5*sigma)[0][0]
        upperIndex = np.where(Energy <= Energy[j] + 5*sigma)[0][-1]

        gaussian = np.exp(-0.5*((Energy[lowerIndex:upperIndex+1] - Energy[j])/sigma)**2)
        gaussian = gaussian / np.sum(gaussian)

        BroadEnergySpectrumHisto[lowerIndex:upperIndex+1] = BroadEnergySpectrumHisto[lowerIndex:upperIndex+1] + counts[j]*gaussian
        BroadVariance[lowerIndex:upperIndex+1] = BroadVariance[lowerIndex:upperIndex+1] + counts[j]*(gaussian**2)

    BroadError = np.sqrt(BroadVariance)

    return BroadEnergySpectrumHisto, BroadError