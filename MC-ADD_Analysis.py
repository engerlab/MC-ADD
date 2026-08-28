# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                                                                                                                          :::
# :::                                               MC-ADD Analysis Script                                                     :::
# :::                                                                                                                          :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# This Python script corresponds to the third phase of the MC-ADD: Analysis phase.
# This script is an alternative to aid users not familiar with Root to analyze simulation results.
# This script does the following:
#       - Opens the Geant4-generated output .csv files: MC-ADD_Results_h1_Energy_Deposit.csv and MC-ADD_Results_nt_Photons.csv
#       - Extracts the energy histogram information from MC-ADD_Results_h1_Energy_Deposit.csv and plots the energy spectrum
#       - Extracts the energy deposited information from MC-ADD_Results_nt_Photons.csv for each hit inside the detector generating
#         a 3D-hits map
#       - Generates a 2D image from the radioactive source seen from the detector using the GammaEnergyDep.csv file. This file may 
#         contain energy deposited or absorbed dose (depending on the user's choice)
#            
# Author: Víctor Daniel Díaz Martínez
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::



# :::::: We import the needed libraries ::::::
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D  
from Histograms import Histograms
from GaussianBroadening import GaussianBroadening
from matplotlib.cm import ScalarMappable
from VDDColorMap import VDD_cmap          # Import the custom colormap




# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::                                       FLAGS                                            ::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# The following flags enable the visualization of the hits map inside the
# detector and the reconstructed image, and the broadening of the energy
# spectrum according to experimental measurements (energy resolution)

# 1: enables visualization
# 0: disables visualization
#    The more runs in the macro file, the larger the size of the file --> the longer it will take to generate the maps

visFlag1 = 0   # Hits map
visFlag2 = 0   # Reconstructed image
ResFlag  = 1   # Broadening of the energy spectrum
ShpFlag  = 0   # Box: 0 or Cylinder: 1



# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::                                    WELCOMING MESSAGE                                   ::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

print('::::::::::::::::::::::::::::::::::::::::::::::: MC-ADD :::::::::::::::::::::::::::::::::::::::::::::::')
print()
print('                             Welcome to MC-ADD Analysis phase!')
print()
print('  I am analyzing your output files. Give me a moment...')
print()



# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                                    ENERGY SPECTRUM                                      :::
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

EnergySpectrumHisto, bin_centers, num_bins, x_min, x_max = Histograms()


EnergySpectrumHisto[0] = 0               # Set the first bin count to 0 since it represents events that did not interact inside the crystal
X = np.linspace(x_min, x_max, num_bins)  # Energy array for the energy spectrum
Error = np.sqrt(EnergySpectrumHisto)     # Uncertainty for each count per bin

# ::: E N E R G Y    H I S T O G R A M :::

plt.figure(2)

plt.plot(X,EnergySpectrumHisto, '-b', linewidth=0.5)
# plt.errorbar(X, EnergySpectrumHisto, yerr=Error, fmt='.-b', linewidth=1, markersize=10, capsize=0) # To plot the energy spectrum with error bars instead:
plt.title(r'Energy Spectrum', fontsize=13)
plt.xlabel('Energy (MeV)', fontsize=13)
plt.ylabel('No. of counts', fontsize=13)
plt.tick_params(direction='out')
plt.xlim([0, 1])
plt.gca().set_box_aspect(1)
plt.show()



# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                     E N E R G Y    R E S O L U T I O N                    :::
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

if ResFlag == 1:
    # ::: E N E R G Y   R E S O L U T I O N :::

    # This section contains an energy spectrum measured experimentally with the Captus 3000 well-type detector.
    # NOT NEEDED FOR THE GENERAL PURPOSE/WORKFLOW OF MC-ADD!!

    # ::: Captus :::
    Captus = pd.read_csv('New2_Cs137_14_25_RawData.csv', skiprows=15)
    CaptusEnergy = Captus.iloc[:, 1].to_numpy(dtype=float)/1000
    CaptusCounts = Captus.iloc[:, 2].to_numpy(dtype=float)
    # ::: End of Captus :::

    # ::: Captus3000 :::
    energyRef = 0.662

    # Use the following lines to obtain the FWHM from a Gaussian fit:
    # c1 = VALUE FROM GAUSSIAN FIT
    # sigma = c1 / np.sqrt(2)
    # FWHM = 2 * np.sqrt(2 * np.log(2)) * sigma
    # resolutionRef = FWHM / energyRef

    resolutionRef = 0.079

    # ::: G A U S S I A N   B R O A D E N I N G   &   E R R O R   P R O P A G A T I O N :::
    BroadEnergySpectrumHisto, BroadError = GaussianBroadening(bin_centers, EnergySpectrumHisto, resolutionRef, energyRef)

    # ::: N O R M A L I Z A T I O N   T O   P H O T O P E A K :::

    # ::: Window around the photopeak :::
    idxPeak = (CaptusEnergy >= 0.64) & (CaptusEnergy <= 0.69)
    MCidxPeak = (X >= 0.64) & (X <= 0.69)

    # ::: Getting Max values in the photopeak :::
    CaptusPeakMax = np.max(CaptusCounts[idxPeak])
    EnergySpectrumHistoMax = np.max(EnergySpectrumHisto[MCidxPeak])
    BroadEnergySpectrumHistoMax = np.max(BroadEnergySpectrumHisto[MCidxPeak])

    # ::: Normalization :::
    CaptusCountsNorm = CaptusCounts / CaptusPeakMax
    EnergySpectrumHistoNorm = EnergySpectrumHisto / EnergySpectrumHistoMax
    BroadEnergySpectrumHistoNorm = BroadEnergySpectrumHisto / BroadEnergySpectrumHistoMax

    BroadErrorNorm = BroadError / BroadEnergySpectrumHistoMax
    EnergySpectrumErrorNorm = Error / EnergySpectrumHistoMax

    # ::: Q U A L I T A T I V E   A S S E S S M E N T:
    #     P E A K   T O   C O M P T O N   R A T I O :::

    PeakROI    = [0.612, 0.711]
    ComptonROI = [0.250, 0.540]

    # ::: Captus indices :::
    idxPeak_Captus = np.where(
        (CaptusEnergy >= PeakROI[0]) &
        (CaptusEnergy <= PeakROI[1])
    )[0]

    idxComp_Captus = np.where(
        (CaptusEnergy >= ComptonROI[0]) &
        (CaptusEnergy <= ComptonROI[1])
    )[0]

    # ::: MC-ADD indices :::
    idxPeak_MC = np.where(
        (bin_centers >= PeakROI[0]) &
        (bin_centers <= PeakROI[1])
    )[0]

    idxComp_MC = np.where(
        (bin_centers >= ComptonROI[0]) &
        (bin_centers <= ComptonROI[1])
    )[0]

    # ::: Integrated counts :::
    P_Captus = np.sum(CaptusCounts[idxPeak_Captus])
    C_Captus = np.sum(CaptusCounts[idxComp_Captus])

    P_MC = np.sum(BroadEnergySpectrumHisto[idxPeak_MC])
    C_MC = np.sum(BroadEnergySpectrumHisto[idxComp_MC])

    # ::: Peak-to-Compton count ratios :::
    PC_Captus = P_Captus / C_Captus
    PC_MC = P_MC / C_MC

    Difference_PC = (abs(PC_MC - PC_Captus) / PC_Captus) * 100

    print('  Peak-to-Compton ratio')
    print()
    print(f'    Captus P/C = {PC_Captus:.4f}')
    print(f'    MC-ADD P/C = {PC_MC:.4f}')
    print(f'    Relative difference = {Difference_PC:.2f} %')

    labels1 = ['MC-ADD Smeared', 'MC-ADD']
    labels2 = ['Captus3000', 'MC-ADD', 'MC-ADD Smeared']
    labels3 = ['Captus3000', 'MC-ADD Smeared']

    # :::::::::::::::::
    # ::: P L O T S :::
    # :::::::::::::::::

    fig, ax = plt.subplots(2, 3, num=3, figsize=(13, 8))

    # ::: Ideal :::
    ax[0,0].plot(X, EnergySpectrumHisto, '-b', linewidth=0.5)
    ax[0,0].set_title('MC-ADD Energy Spectrum', fontsize=13)
    ax[0,0].set_xlabel('Energy (MeV)', fontsize=13)
    ax[0,0].set_ylabel('No. of counts', fontsize=13)
    ax[0,0].tick_params(direction='out')
    ax[0,0].set_xlim([0, 1])
    ax[0,0].set_box_aspect(1)

    # ::: Ideal zoom :::
    ax[0,1].plot(X, EnergySpectrumHisto, '-b', linewidth=0.5)
    ax[0,1].set_title('MC-ADD Energy Spectrum Zoom', fontsize=13)
    ax[0,1].set_xlabel('Energy (MeV)', fontsize=13)
    ax[0,1].set_ylabel('No. of counts', fontsize=13)
    ax[0,1].tick_params(direction='out')
    ax[0,1].set_xlim([0, 0.65])
    ax[0,1].set_ylim([0, 10e4])
    ax[0,1].set_box_aspect(1)

    # ::: Ideal and Smeared :::
    ax[0,2].errorbar(bin_centers, BroadEnergySpectrumHisto, yerr=BroadError, fmt='.r', markersize=2, linewidth=0.5, capsize=0)
    ax[0,2].plot(bin_centers, EnergySpectrumHisto, '-b', linewidth=0.5)
    ax[0,2].set_title('Ideal and Smeared energy spectrum', fontsize=13)
    ax[0,2].set_xlabel('Energy (MeV)', fontsize=13)
    ax[0,2].set_ylabel('No. of counts', fontsize=13)
    ax[0,2].tick_params(direction='out')
    ax[0,2].set_xlim([0, 1])
    ax[0,2].set_ylim([0, 1.1 * np.max(BroadEnergySpectrumHisto)])
    ax[0,2].legend(labels1, loc='upper right')
    ax[0,2].set_box_aspect(1)

    # ::: Experimental :::
    ax[1,0].plot(CaptusEnergy, CaptusCounts, '-', linewidth=1.2)
    ax[1,0].set_title('Captus', fontsize=13)
    ax[1,0].set_xlabel('Energy (MeV)', fontsize=13)
    ax[1,0].set_ylabel('No. of counts', fontsize=13)
    ax[1,0].tick_params(direction='out')
    ax[1,0].set_xlim([0, 1])
    ax[1,0].set_box_aspect(1)

    # ::: Experimental and Smeared :::
    ax[1,1].plot(CaptusEnergy, CaptusCounts, '-', linewidth=1.2)
    ax[1,1].errorbar(bin_centers, BroadEnergySpectrumHisto, yerr=BroadErrorNorm, fmt='.r', markersize=1, linewidth=0.5, capsize=0)
    ax[1,1].set_title('Captus vs MC-ADD', fontsize=13)
    ax[1,1].set_xlabel('Energy (MeV)', fontsize=13)
    ax[1,1].set_ylabel('Normalized Counts', fontsize=13)
    ax[1,1].tick_params(direction='out')
    ax[1,1].set_xlim([0, 1])
    ax[1,1].legend(labels3, loc='upper right')
    ax[1,1].set_box_aspect(1)

    # ::: Normalized Ideal, Smeared, and Experimental :::
    ax[1,2].plot(CaptusEnergy, CaptusCountsNorm, '-', linewidth=1.2)
    ax[1,2].plot(bin_centers, EnergySpectrumHistoNorm, '-b', linewidth=0.8)
    ax[1,2].errorbar(bin_centers, BroadEnergySpectrumHistoNorm, yerr=BroadErrorNorm, fmt='.r', markersize=1, linewidth=0.5, capsize=0)
    ax[1,2].set_title(r'Normalized $^{137}$Cs Energy Spectrum', fontsize=13)
    ax[1,2].set_xlabel('Energy (MeV)', fontsize=13)
    ax[1,2].set_ylabel('Normalized Counts', fontsize=13)
    ax[1,2].tick_params(direction='out')
    ax[1,2].set_xlim([0, 1])
    ax[1,2].set_ylim([0, 2.7])
    ax[1,2].legend(labels2, loc='upper right')
    ax[1,2].set_box_aspect(1)

    plt.tight_layout()
    plt.show()


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::       DETECTOR  EFFICIENCY   AND  VISUALIZATION          :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

macroFile = 'MC-ADD.mac'

with open(macroFile, 'r') as file:
    lines = file.readlines()

# ::: N U M B E R    O F    R U N S :::

targetLine = ''

for line in lines:
    if '/run/beamOn' in line:
        targetLine = line
        break

if targetLine:
    tokens = re.findall(r'[\d.]+', targetLine)

    if tokens:
        N_simulated = float(tokens[0])
    else:
        print('No number was found with /run/beamOn.')
else:
    print('No line was found with /run/beamOn in the macro file.')


# ::::::  D E T E C T O R    E F F I C I E N C Y ::::::

# This section computes the absolute detection efficiency considering only the ideal spectrum.
# If you wish to obtain full-energy peak detection efficiency (if applicable) ...
# get N_photopeak directly from the energy spectrum and add it to N_detected
# This section must be done manually for the scenarios where the
# radionuclide emits more than one photon (e.g. Na22)

# The following lines were adapted to the Cs-137 example

Prob_emission = 0.8501
N_emitted = N_simulated * Prob_emission

# N_detected = np.sum(EnergySpectrumHisto)
N_detected = np.max(EnergySpectrumHisto)

Det_e = N_detected / N_emitted
DetEff = Det_e * 100


# ::: E F F I C I E N C Y    U N C E R T A I N T Y :::

sigma_eff = np.sqrt(Det_e * (1 - Det_e) / N_emitted) * 100

# ::: C A P T U S   E F F I C I E N C Y   V S   M C - A D D :::

captus_DetEff = 15.08

Diff = (abs(captus_DetEff - DetEff) / captus_DetEff) * 100



# :::::: 3D   E N E R G Y    D E P O S I T I O N    H I T    M A P ::::::

if visFlag1 == 1:

    # ::: V I S U A L I Z A T I O N :::
    DataTable = pd.read_csv('MC-ADD_Results_nt_Photons.csv', header=None, sep=',', skiprows=9, usecols=[0, 1, 2, 3, 4])
    Data = DataTable.to_numpy()

    Events = Data[:, 0]
    X = Data[:, 1]
    Y = Data[:, 2]
    Z = Data[:, 3]
    Energy = Data[:, 4]

    # :::::: E R R O R    C A L C U L A T I O N ::::::
    Unique_Events = np.unique(Events)
    AllEvents = len(Unique_Events)
    TotEnergyperEvent = np.zeros(AllEvents)

    for i in range(AllEvents):
        EventID = Unique_Events[i]
        TotEnergyperEvent[i] = np.sum(Energy[Events == EventID])

    E_mean = np.mean(TotEnergyperEvent)

    # ::: H I S T O R Y  -  B Y  -  H I S T O R Y :::
    sum_x2 = np.sum(TotEnergyperEvent**2) / N_detected
    sum_x = (np.sum(TotEnergyperEvent) / N_detected)**2
    sigma_Edep = np.sqrt((sum_x2 - sum_x) / (N_detected - 1))

    # ::: 3 D   P L O T :::
    fig = plt.figure(3)
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(X, Y, Z, s=2, c=Energy, cmap='jet')

    ax.set_title('3D Hits Map', fontsize=13)
    ax.set_xlabel('X (mm)', fontsize=13)
    ax.set_ylabel('Y (mm)', fontsize=13)
    ax.set_zlabel('Z (mm)', fontsize=13)
    #ax.view_init(elev=0, azim=180)  # Optional 2D visualization
    plt.colorbar(scatter, ax=ax)
    plt.show()



# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                 COMMAND-BASED FILES ANALYSIS                  :::
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# ::::::::: BOX :::::::::
if ((ShpFlag == 0) and (visFlag2 == 1)):
    GammaData = np.loadtxt('GammaEnergyDep.csv', delimiter=',', skiprows=1)  # Read the CSV file
    mac_file = 'MC-ADD.mac'                                                   # Read the MC-ADD.mac file

    with open(mac_file, 'r') as f:
        lines = f.readlines()
        
    # ::: Detector size :::
    box_size_line = lines[21]                                                # Size of the scoring volume. It says 21 because Python starts counting from 0
    tokens = re.findall(r'([\d.]+) ([\d.]+) ([\d.]+)', box_size_line)[0]     # Extract x, y, z sizes
    box_size = np.array([float(val) for val in tokens])                      # Convert strings to floats

    X = 2 * box_size[0]
    Y = 2 * box_size[1]

    # ::: Voxels :::
    n_bin_line = lines[22]                                                   # Number of voxels
    tokens = re.findall(r'([\d.]+) ([\d.]+) ([\d.]+)', n_bin_line)[0]        # Extract nBin values
    n_bin = np.array([int(float(val)) for val in tokens])                    # Convert to integers

    NumVoxX, NumVoxY, NoVoxZ = n_bin


    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # :::                 2D Map Generation                 :::
    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    SlicesTot = np.zeros((NumVoxX, NumVoxY, NoVoxZ))

    # ::: Extraction and storage of the voxels information :::
    for z in range(NoVoxZ):                                                  # Iterate over Z slices
        for y in range(NumVoxY):                                             # Iterate over Y rows
            Idx = (y * NoVoxZ) + z                                           # Calculate index for data extraction
            vectorTot = GammaData[Idx::(NumVoxY * NoVoxZ), 3]                # Extract 4th column (index 3 in Python)
            SlicesTot[NumVoxY - y - 1, :, z] = vectorTot                     # Invert for reconstruction

    # ::: 3D Visualization :::
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    z_spacing = 0.1                                                          # Define spacing between Z slices

    # ::: Normalzation :::
    vmin = np.min(SlicesTot)
    vmax = np.max(SlicesTot)

    # Create a ScalarMappable object for the colorbar
    sm = ScalarMappable(cmap=VDD_cmap)
    sm.set_clim(vmin, vmax)                                                  # Set the range of the colormap

    for z in range(NoVoxZ):                                                  # Iterate through each slice
        sliceTot = SlicesTot[:, :, z]                                        # Extract XY slice
        face_colors = VDD_cmap((sliceTot - vmin) / (vmax - vmin))            # Scale within the dataset range

        # Create a transformed image in 3D space
        x = np.arange(NumVoxX)
        y = np.arange(NumVoxY)
        X_grid, Y_grid = np.meshgrid(x, y)

        ax.plot_surface(X_grid, Y_grid, np.full_like(X_grid, z * z_spacing), 
                        facecolors=face_colors, 
                        rstride=1, cstride=1, antialiased=True, shade=False)

    cbar = fig.colorbar(sm, ax=ax, shrink=0.7, aspect=20, pad=0.1)
    ax.set_title('Reconstructed Image')
    cbar.set_label('Energy (MeV)')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.view_init(elev=90, azim=270)  
    plt.show()

# ::::::::: CYLINDER :::::::::
elif ((ShpFlag == 1) and (visFlag2 == 1)):
    mac_file = 'MC-ADD.mac'                                                   # Read the MC-ADD.mac file
    
    with open(mac_file, 'r') as f:
        lines = f.readlines()
    
    # ::: Detector size :::
    cylinder_size_line = lines[21]                                           # Size of the scoring volume. It says 21 because Python starts counting from 0
    tokens = re.findall(r'([\d.]+) ([\d.]+)', cylinder_size_line)[0]         # Extract x, y, z sizes
    Cyl_size = np.array([float(val) for val in tokens])                      # Convert strings to floats

    DetRad = Cyl_size[0]
    DetLen = 2 * Cyl_size[1]


    # ::: Voxels :::
    n_bin_line = lines[22]                                                   # Number of voxels
    tokens = re.findall(r'([\d.]+) ([\d.]+) ([\d.]+)', n_bin_line)[0]        # Extract nBin values
    n_bin = np.array([int(float(val)) for val in tokens])                    # Convert to integers

    NumVoxR  = n_bin[0]
    NoVoxZ   = n_bin[1]
    NoVoxPhi = n_bin[2]

    # ::::::::: Extracting Information from .csv file :::::::::

    GammaData = np.loadtxt('CylinderGammaEnergyDep.csv', delimiter=',', skiprows=1)  # Read the CSV file

    # ::: Voxels Information :::
    iZ     = GammaData[:, 0]     # Z (layer)
    iPhi   = GammaData[:, 1]     # Phi (angle)
    iR     = GammaData[:, 2]     # R (radius)
    Energy = GammaData[:, 3]     # Energy deposition

    # ::: Getting unique values of each vector :::
    uniqueZ   = np.unique(iZ)    # Unique Z values (layers)
    uniquePhi = np.unique(iPhi)  # Unique Phi values (angles)
    uniqueR   = np.unique(iR)    # Unique R values (radii)

    NoVoxZ = len(uniqueZ)
    NoVoxPhi = len(uniquePhi)
    NoVoxR = len(uniqueR)

    EnergyMatrices = []          # List to store energy matrices for each Z layer

    # ::: Loop through each Z layer :::
    for currentZ in uniqueZ:
        layerData = GammaData[iZ == currentZ]              # Filter data for the current Z layer
        EnergyMatrix = np.zeros((NoVoxR, NoVoxPhi))        # Initialize energy matrix for this layer (R x Phi)
    
        # ::: Fill the matrix with energy values :::
        for row in layerData:
            rIdx = np.where(uniqueR == row[2])[0][0]       # Get R index (row)
            phiIdx = np.where(uniquePhi == row[1])[0][0]   # Get Phi index (column)
            EnergyMatrix[rIdx, phiIdx] = row[3]            # Store Energy
    
        EnergyMatrices.append(EnergyMatrix)                # Store the matrix

    # ::::::::: Plot :::::::::
    DetRad = max(uniqueR)                                  # Define detector radius
    r = np.linspace(0, DetRad, NoVoxR)                     # Radii range (0 - scoring volume max radius)
    theta = np.linspace(0, 2 * np.pi, NoVoxPhi)            # Angular dimension (0°- 360°)

    R, Theta = np.meshgrid(r, theta)                       # Polar coordinates mesh
    X, Y = R * np.cos(Theta), R * np.sin(Theta)            # Convert polar to Cartesian

    # Convert list of matrices into 3D NumPy array
    ArrayEnergyMatrices = np.stack(EnergyMatrices, axis=2)

    # Select a specific layer to visualize (e.g., 50th layer)
    LayerEnMatrix = ArrayEnergyMatrices[:, :, 49]          # Indexing starts at 0 in Python
    LayerEnMatrix[:2, :] = 0                               # Set inside of cylindrical scoring volume to 0

    # ::: Plot :::
    plt.figure(figsize=(8, 8))
    plt.pcolormesh(X, Y, LayerEnMatrix.T, shading='auto', cmap=VDD_cmap) 
    plt.colorbar(label='Energy Deposition')
    plt.title('Reconstructed Image')
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.axis('equal')
    plt.show()



# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::                           DISPLAYING RESULTS                         ::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

print('  I finished! Your results are listed below.')
print()

print(':::::::::::::::::::::::::::::::::::::::::::::::      RESULTS      ::::::::::::::::::::::::::::::::::::::::::::::')
print()

print(f'  Events simulated:          {int(N_simulated)}')
print(f'  Events in the detector:    {int(N_detected)}')
print()

print(f'  Detector efficiency: {DetEff:.5f} ± {sigma_eff:.5f} %')
print(f'  Captus efficiency: {captus_DetEff:.5f} %')
print(f'  Percentage difference with Captus: {Diff:.5f} %')
print()
print()

print(':::::::::::::::::::::::::::::::::::::::::::::::          END          :::::::::::::::::::::::::::::::::::::::::::::')