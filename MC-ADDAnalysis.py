# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                                                                                                                          :::
# :::                                               MC-ADD Analysis Script                                                :::
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
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
from mpl_toolkits.mplot3d import Axes3D  
from matplotlib.cm import ScalarMappable
from VDDColorMap import VDD_cmap          # Import the custom colormap


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::                                       FLAGS                                     ::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# The following flags enable the visualization of the hits map inside the
# detector and the reconstructed image, and the broadening of the energy
# spectrum according to experimental measurements (energy resolution)

# 1: enables visualization
# 0: disbales visualization
#    The more runs in the macro file, the larger the size of the file --> the longer it will take to generate the maps

visFlag1 = 0  # Hits map
visFlag2 = 1  # Reconstructed image
ResFlag  = 1  # Broadening of the energy spectrum
ShpFlag  = 0  # Box: 0 or Cylinder: 1



# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::                                    WELCOMING MESSAGE                                   ::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

print('\n')
print('::::::::::::::::::::::::::::::::::::::::::::::: MC-ADD :::::::::::::::::::::::::::::::::::::::::::::::\n')
print('                                  Welcome to MC-ADD Analysis phase!\n')
print('  I am analyzing your output files. Give me a moment...\n')


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                               ENERGY SPECTRUM                                :::
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 

fileName = "MC-ADD_Results_h1_Energy_Deposit.csv"                # Name of the csv 

with open(fileName, "r") as file:                               # Open and read the file
    lines = file.readlines()

# ::: No. of bins, Min and Max Energy :::
no_bins = None                                                  # Empty variable for the number of bins used later
x_min = None                                                    # Empty variables for energy ranges used later
x_max = None 

for line in lines:                                              # Finding the line containing the No. of bins, and energy range information
    if line.startswith("#axis fixed"):                          # Line where the information is located
        parts    = line.split()
        no_bins = int(parts[2])                                 # Getting the Number of bins
        x_min    = float(parts[3])                              # Getting the Minimum energy value
        x_max    = float(parts[4])                              # Getting the Maximum energy value
        break                                                   # Stop after finding the relevant line

if no_bins is None or x_min is None or x_max is None:           # Check if the values were extracted correctly
    raise ValueError("Could not extract axis information.")

data_lines = lines[7:]                                          # Extract histogram data skipping metadata information

# ::: Extracting the numerical data :::
entries = []                                                    # Empty variable for th enumber of entries 
for line in data_lines:
    values = line.strip().split(",")
    if len(values) >= 1:
        entries.append(int(values[0]))                          # First column is the event count per bin


entries = entries[1:-1]                                         # Remove underflow and overflow bins. Keep only the bins within the defined range

if len(entries) > 0:                                            # Set the first bin count to 0 since it represents radiation that did not interact inside the detector
    entries[0] = 0

# ::: E N E R G Y    H I S T O G R A M :::
X = np.linspace(x_min, x_max, no_bins)
bin_edges = np.linspace(x_min, x_max, no_bins + 1)              # Bin edges
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2              # Bin center
Error = np.sqrt(entries)                                        # Error calculation

plt.figure(1)
#plt.bar(bin_centers, entries, width=(x_max - x_min) / no_bins, edgecolor='none', alpha=0.7, color='red')  # To plot the energy spectrum in bar format
plt.plot(X, entries, color = 'b', linestyle = '-', markersize = 4, linewidth = 1)
plt.title("Energy Spectrum Histogram") 
plt.xlabel("Energy Deposition (MeV)") 
plt.ylabel("Number of Counts")
plt.xlim(0, 1)
plt.show()

                                   
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                              ENERGY RESOLUTION                               :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

if ResFlag == 1:
    # :: E N E R G Y    R E S O L U T I O N :::
    FWHM = 0.13                                   # FWHM = 0.13 MeV
    sigmaRes = FWHM / 2.355                       # Convert FWHM to standard deviation

    # ::: S M E A R I N G   U S I N G   G A U S S I A N    S U M M A T I O N :::
    def spectrum(E, osc, sigma, x):
        BroadEnergySpectrumHisto = []             # Initialize list for broadened spectrum
        
        for Ei in x:
            total = 0
            for Ej, os in zip(E, osc):
                total += os * np.exp(-(((Ej - Ei) / sigma) ** 2))    
            BroadEnergySpectrumHisto.append(total)
        return BroadEnergySpectrumHisto
        
    BroadEnergySpectrumHisto = spectrum(X, entries, sigmaRes, X)

    # ::: P L O T :::
    plt.figure(2)
    plt.plot(X, BroadEnergySpectrumHisto, 'r',linewidth=1, label='Broadened Spectrum')
    plt.plot(X, entries, 'b', linewidth=1, label='Discrete Spectrum')
    plt.title('Broadened Energy Spectrum')
    plt.xlabel('Energy (MeV)')
    plt.ylabel('Counts')
    plt.xlim([0, 1])
    plt.legend()
    plt.gca().tick_params(direction='out')  
    plt.show()



# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                          DETECTOR  EFFICIENCY   AND  VISUALIZATION                            :::
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

file_name = "MC-ADD_Results_nt_Photons.csv"                                                   # Load the CSV file
data = pd.read_csv(file_name, header=None, sep=',', skiprows=9, usecols=[0, 1, 2, 3, 4])     # Read the csv file skipping the first 11 header lines (metadata)

# ::: Extract columns for X, Y, Z, and Energy :::
event_numbers = data[0]
x = data[1]  
y = data[2]  
z = data[3]  
energy = data[4]


# :::::: E R R O R   C A L C U L A T I O N ::::::

unique_events = np.unique(event_numbers)                                                                      # Fnd unique events (events that actually deposited energy)
total_energy_per_event = np.array([np.sum(energy[event_numbers == event_id]) for event_id in unique_events])  # Total energy deposited per event

mac_file = 'MC-ADD.mac'                                                                                        # Read the MC-ADD.mac file
with open(mac_file, 'r') as f:                                                                                # Open and read all lines from the file
    lines = f.readlines()

# ::: NUMBER OF RUNS :::
target_line = None                                                                                            # Variable to store the line containing /run/beamOn

for line in lines:
    if "/run/beamOn" in line:                                                                                 # Search for the line containing "/run/beamOn"
        target_line = line.strip()                                                                            # Store the line and remove any trailing spaces
        break 


if target_line:
    match = re.search(r'\b\d+\b', target_line)                                                                # Extract the numeric value from the line number
    if match:
        N_simulated = int(match.group())                                                                      # Convert the value to an integer
    else:
        print("No number was found with /run/beamOn.")
else:
    print("No line was found with /run/beamOn in the macro file.")

N_detected = total_energy_per_event[total_energy_per_event > 0]                                               # Number of detected events
N_detected = len(N_detected)
E_mean = np.mean(total_energy_per_event)                                                                      # Calculate mean energy deposited per event



# ::: H I S T O R Y - B Y -  H I S T O R Y    M E T H O D :::
sum_x2 = np.sum(total_energy_per_event**2)/N_detected
sum_x  = (np.sum(total_energy_per_event)/N_detected)**2
sigma_Edep = np.sqrt((sum_x2 - sum_x)/(N_detected - 1))    


# ::::::  D E T E C T O R    E F F I C I E N C Y ::::::
Det_e = N_detected/N_simulated
DetEff = Det_e*100


# ::: E F F I C I E N C Y    U N C E R T A I N T Y :::
sigma_eff = np.sqrt( (1/N_detected) + (1/N_simulated) ) * 100 * Det_e


# :::::: 3D   E N E R G Y    D E P O S I T I O N    M A P ::::::
if visFlag1 == 1:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(x, y, z, c=energy, cmap=VDD_cmap, s=0.5)         # Scatter plot with energy hits in colormap
    colorbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=10)
    colorbar.set_label('Energy (MeV)')
    ax.set_xlabel('X (mm)', labelpad=15) 
    ax.set_ylabel('Y (mm)', labelpad=15)
    ax.set_zlabel('Z (mm)', labelpad=15)
    ax.set_title('3D Energy Distribution', pad=20)
    ax.view_init(elev=0, azim=90)                                         # View point
    plt.tight_layout()                                                    # Adjust the layout to make better use of space


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
elif ((ShpFlag == 1) and (visFlag1 == 1)):
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



# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# ::::::                           DISPLAYING RESULTS                         ::::::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
print('  I finished! Your results are listed below.\n')
print(':::::::::::::::::::::::::::::::::::::::::::::::   RESULTS   :::::::::::::::::::::::::::::::::::::::::::::::\n')
print(f"  Events simulated:        {N_simulated}")
print(f"  Events in the detector:  {N_detected}")
print(f"  Mean energy deposited:   {E_mean:.4f} Mev")
print(f"  Statistical uncertainty: {sigma_Edep:.4f} MeV \n")
print(f"  Detector efficiency:     {DetEff:.4f} %  ±  {sigma_eff:.4f} % \n")
print(':::::::::::::::::::::::::::::::::::::::::::::::     END     :::::::::::::::::::::::::::::::::::::::::::::::\n')
