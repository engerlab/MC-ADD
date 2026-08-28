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

# ::: Energy Spectrum Plot :::
bin_edges = np.linspace(x_min, x_max, no_bins + 1)              # Bin edges
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2              # Bin center

plt.bar(bin_centers, entries, width=(x_max - x_min) / no_bins, edgecolor='none', alpha=0.7, color='red') 
plt.title("Energy Spectrum Histogram") 
plt.xlabel("Energy Deposition (MeV)") 
plt.ylabel("Number of Counts")
plt.ylim(0, max(entries) + 1000)  
                                   


# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                                  VISUALIZATION                               :::
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# :::::: 3D Energy Deposition Map ::::::
#    The more runs in the macro file, the larger the size of the file, therefore, the longer it will take to generate the 3D map

#file_name = "MC-ADD_Results_nt_Photons.csv"                                              # Load the CSV file
#data = pd.read_csv(file_name, header=None, sep=',', skiprows=11, usecols=[1, 2, 3, 6])  # Read the csv file skipping the first 11 header lines (metadata)

# ::: Extract columns for X, Y, Z, and Energy :::
#x = data[1]  
#y = data[2]  
#z = data[3]  
#energy = data[6]

# ::: 3D Scatter Plot :::
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#scatter = ax.scatter(x, y, z, c=energy, cmap=VDD_cmap, s=0.5)         # Scatter plot with energy hits in colormap
#colorbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=10)
#colorbar.set_label('Energy (MeV)')
#ax.set_xlabel('X (mm)', labelpad=15) 
#ax.set_ylabel('Y (mm)', labelpad=15)
#ax.set_zlabel('Z (mm)', labelpad=15)
#ax.set_title('3D Energy Distribution', pad=20)
#ax.view_init(elev=0, azim=90)                                       # View point
#plt.tight_layout()                                                  # Adjust the layout to make better use of space


# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# :::                 COMMAND-BASED FILES ANALYSIS                  :::
# :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

mac_file = 'MC-ADD.mac'                                                           # Read the MC-ADD.mac file

with open(mac_file, 'r') as f:
    lines = f.readlines()

# ::: Detector size :::
cylinder_size_line = lines[21]                                                # Size of the scoring volume. It says 21 because Python starts counting from 0
tokens = re.findall(r'([\d.]+) ([\d.]+)', cylinder_size_line)[0]              # Extract x, y, z sizes
Cyl_size = np.array([float(val) for val in tokens])                           # Convert strings to floats


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
iZ     = GammaData[:, 0]    # Z (layer)
iPhi   = GammaData[:, 1]    # Phi (angle)
iR     = GammaData[:, 2]    # R (radius)
Energy = GammaData[:, 3]    # Energy deposition

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
    layerData = GammaData[iZ == currentZ]        # Filter data for the current Z layer
    EnergyMatrix = np.zeros((NoVoxR, NoVoxPhi))  # Initialize energy matrix for this layer (R x Phi)
    
    # ::: Fill the matrix with energy values :::
    for row in layerData:
        rIdx = np.where(uniqueR == row[2])[0][0]      # Get R index (row)
        phiIdx = np.where(uniquePhi == row[1])[0][0]  # Get Phi index (column)
        EnergyMatrix[rIdx, phiIdx] = row[3]           # Store Energy
    
    EnergyMatrices.append(EnergyMatrix)               # Store the matrix

# ::::::::: Plot :::::::::
DetRad = max(uniqueR)                        # Define detector radius
r = np.linspace(0, DetRad, NoVoxR)           # Radii range (0 - scoring volume max radius)
theta = np.linspace(0, 2 * np.pi, NoVoxPhi)  # Angular dimension (0°- 360°)

R, Theta = np.meshgrid(r, theta)             # Polar coordinates mesh
X, Y = R * np.cos(Theta), R * np.sin(Theta)  # Convert polar to Cartesian

# Convert list of matrices into 3D NumPy array
ArrayEnergyMatrices = np.stack(EnergyMatrices, axis=2)

# Select a specific layer to visualize (e.g., 50th layer)
LayerEnMatrix = ArrayEnergyMatrices[:, :, 49]  # Indexing starts at 0 in Python
LayerEnMatrix[:2, :] = 0                      # Set inside of cylindrical scoring volume to 0

# ::: Plot :::
plt.figure(figsize=(8, 8))
plt.pcolormesh(X, Y, LayerEnMatrix.T, shading='auto', cmap=VDD_cmap) 
plt.colorbar(label='Energy Deposition')
plt.title('Reconstructed Image')
plt.xlabel('X (mm)')
plt.ylabel('Y (mm)')
plt.axis('equal')
plt.show()