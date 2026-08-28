import numpy as np
import pandas as pd
import re


def Histograms():

    # Define file names
    fileNameHisto = 'MC-ADD_Results_h1_Energy_Deposit_FINAL.csv'

    # Initialize empty array
    EnergyHisto = np.array([])

    try:

        # The first 6 lines are Geant4 metadata and line 7
        # contains the CSV column names.
        # Numerical data therefore begin on line 8.
        DataHisto = pd.read_csv(fileNameHisto, skiprows=7, header=None)

        # Column 1 contains histogram entries
        EnergyHisto = DataHisto.iloc[:, 0].to_numpy(dtype=float)

        # Remove Geant4 underflow and overflow bins
        EnergyHisto = EnergyHisto[1:-1]

    except FileNotFoundError:
        raise FileNotFoundError(
            f'Histogram file not found: {fileNameHisto}'
        )

    except Exception as e:
        raise RuntimeError(
            f'Error reading histogram file: {e}'
        )


    EnergySpectrumHisto = EnergyHisto


    # :::::: Define histogram bins ::::::

    RunActionFile = 'src/RunAction.cc'

    try:
        with open(RunActionFile, 'r') as file:
            lines = file.readlines()

    except FileNotFoundError:
        raise FileNotFoundError(
            f'Error opening the file: {RunActionFile}'
        )


    # Histogram information is located in line 20 of RunAction.cc
    # Python indexing starts at 0
    HistogramInfo = lines[19]

    tokens = re.search(
        r'(\d+),\s*([\d.]+),\s*([\d.]+)',
        HistogramInfo
    )

    if tokens is None:
        raise ValueError(
            'Could not extract histogram information. Check the format.'
        )


    num_bins = int(tokens.group(1))
    x_min    = float(tokens.group(2))
    x_max    = float(tokens.group(3))


    # ::: Bin centers :::

    bin_edges = np.linspace(
        x_min,
        x_max,
        num_bins + 1
    )

    bin_centers = (
        bin_edges[:-1] + bin_edges[1:]
    ) / 2


    # ::: Debugging: Check if lengths match :::

    if len(EnergySpectrumHisto) != len(bin_centers):
        raise ValueError(
            f'Mismatch: bin_centers has {len(bin_centers)} elements '
            f'but EnergySpectrumHisto has {len(EnergySpectrumHisto)} elements.'
        )


    return (
        EnergySpectrumHisto,
        bin_centers,
        num_bins,
        x_min,
        x_max
    )