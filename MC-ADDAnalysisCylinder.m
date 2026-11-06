% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% :::                                                                                                                         :::
% :::                                 MC-ADD Analysis Script                                      :::
% :::                                                                                                                         :::
% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% This Python script corresponds to the third phase of the MC-ADD: Analysis phase.
% This script is an alternative to aid users not familiar with Root to analyze simulation results.
% This script does the following:
%       - Opens the Geant4-generated output .csv files: MC-ADD_Results_h1_Energy_Deposit.csv and MC-ADD_Results_nt_Photons.csv
%       - Extracts the energy histogram information from MC-ADD_Results_h1_Energy_Deposit.csv and plots the energy spectrum
%       - Extracts the energy deposited information from MC-ADD_Results_nt_Photons.csv for each hit inside the detector generating
%         a 3D-hits map
%       - Generates a 2D image from the radioactive source seen from the detector using the GammaEnergyDep.csv file. This file may 
%         contain energy deposited or absorbed dose (depending on the user's choice)
%            
% Author: Víctor Daniel Díaz Martínez
% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

clc; close all; clear;                                                                                      % Cleaning commands
addpath('/Users/victor/Documents/MATLAB/Functions')                        % We add the path to the folder containing all the functions. Make sure to add yours!


% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% :::                                 ENERGY SPECTRUM                           :::
% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

[EnergySpectrumNtuple, EnergySpectrumHisto, bin_centers] = Histograms;    % We call the function Histograms to plot the energy spectrum

EnergySpectrumHisto(1) = 0;                                                                                 % Set the first bin count to 0 since it represents radiation that did not interact inside the detector
maxLim = max(EnergySpectrumHisto) + 1000;                                                     % Set the max Y-axis value for better visualization

% ::: Ntuple histogram :::
figure(1)
histogram(EnergySpectrumNtuple, 300, 'FaceColor','r', 'EdgeColor', 'none');
title('Energy Deposited Ntuples', 'Interpreter', 'latex', 'FontSize', 13);
xlabel('Energy (MeV)', 'Interpreter', 'latex', 'FontSize', 13);
ylabel('No. of counts', 'Interpreter', 'latex', 'FontSize', 13);
axis square

% ::: Energy Histogram :::
figure(2)
bar(bin_centers, EnergySpectrumHisto, 'BarWidth', 1, 'FaceColor', 'b', 'EdgeColor', 'none');
title('Energy Spectrum Histogram', 'Interpreter', 'latex', 'FontSize', 13);
xlabel('Energy (MeV)', 'Interpreter', 'latex', 'FontSize', 13);
ylabel('No. of counts', 'Interpreter', 'latex', 'FontSize', 13);
ylim([0 maxLim])
axis square



% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% :::                                 VISUALIZATION                                    :::
% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

% :::::: 3D Energy Deposition Map ::::::
%   The more runs in the macro file, the larger the size of the file, therefore, the longer it will take to generate the 3D map
% 
% Data = readtable('MC-ADD_Results_nt_Photons.csv');  % We import the name of the file containing the photon hits information in Ntuples
% 
% X = Data(:,2);                                                                % Extraction of data
% Y = Data(:,3);
% Z = Data(:,4);
% Energy = Data(:,7);
% 
% X = table2array(X);                                                       % Conversion to arrays
% Y = table2array(Y);
% Z = table2array(Z);
% Energy = table2array(Energy);
% 
% figure(3)                                                                        % 3D Plot
% scatter3(X, Y, Z, 5, Energy, 'filled');
% title('3D Energy Deposition Hits');
% xlabel('X (mm)');
% ylabel('Y (mm)');
% zlabel('Z (mm)'); 
% xlim([-3 3])
% ylim([-10 10])
% zlim([-3 3])
% colormap jet; colorbar;
% view (180,0);



% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% :::                 COMMAND-BASED FILES ANALYSIS                  :::
% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

% ::::::::: Extracting Information from Macro file:::::::::

macroFile     = 'MC-ADD.mac';                                                              % Read the macro file to extract data 
fid                 = fopen(macroFile, 'r');

if fid == -1                                                                                            % If statement if the file cannot be opened
    error('Could not open the .mac file.');
end

lines = textscan(fid, '%s', 'Delimiter', '\n');       
fclose(fid);
lines = lines{1};                                                                                    % Convert cell to array of strings


% ::: Detector size :::
cylinderSizeLine = lines{22};                                                               % Size of the scoring volume located in line 22 of the macrofile
tokens = regexp(cylinderSizeLine, '([\d.]+) ([\d.]+)', 'tokens');            % Extracting the R and Z size values
CylSize = str2double(tokens{1});                                                         % Converting string into doubles


% ::: Voxels :::
nBinLine = lines{23};                                                                            % Number of voxels located in line 23 of the macrofile 
tokens = regexp(nBinLine, '([\d.]+) ([\d.]+) ([\d.]+)', 'tokens');            % Extracting the  R, Z, Phi no. of voxels
nBin = str2double(tokens{1});                                                             % Converting string to doubles

NoVoxR    = nBin(1);
NoVoxZ    = nBin(2);
NoVoxPhi = nBin(3);

DetRad = CylSize(1);
DetLen = 2*CylSize(2);


% ::::::::: Extracting Information from .csv file:::::::::

GammaData = readmatrix('CylinderGammaEnergyDep.csv');         % We read the csv file 

% ::: Voxels Information :::
iZ          = GammaData(:, 1);                                                               % Z (layer)
iPhi       = GammaData(:, 2);                                                               % Phi (angle)
iR          = GammaData(:, 3);                                                               % R (radius)
Energy = GammaData(:, 4);                                                               % Energy deposition

% ::: Getting unique values of each vector  :::
uniqueZ    = unique(iZ);                                                                      % Unique Z values (layers)
uniquePhi = unique(iPhi);                                                                   % Unique Phi values (angles)
uniqueR    = unique(iR);                                                                      % Unique R values (radii)

EnergyMatrices = cell(NoVoxZ, 1);                                                     % Initialize a cell array to store the matrices for each Z layer

% ::: Loop through each Z layer :::
for zIdx = 1:NoVoxZ

    currentZ = uniqueZ(zIdx);  
    layerData = GammaData(iZ == currentZ, :);                    % Filter data for the current Z layer
    EnergyMatrix = zeros(NoVoxR, NoVoxPhi);                     % Initialize energy matrix for this layer (R x Phi)

    % ::: Fill the matrix with energy values :::
    for row = 1:size(layerData, 1)
        rIdx     = find(uniqueR == layerData(row, 3));              % Get R index (row)
        phiIdx = find(uniquePhi == layerData(row, 2));           % Get Phi index (column)
        EnergyMatrix(rIdx, phiIdx) = layerData(row, 4);          % Store Energy
    end

    
    EnergyMatrices{zIdx} = EnergyMatrix;                            % Store the matrices
end


% ::::::::: Plot :::::::::

%intensity_matrix = repmat(linspace(100, 0, NoVoxR)', 1, NoVoxPhi);        % Intensity matrix for testing purposes (100 - 0)
%intensity_matrix(1:20,:) = 0;

% ::: Radial and Angular Dimensions :::
r = linspace(0, DetRad, NoVoxR)';                                                                   % Radii range (0 - scoring volume max radius)
theta = linspace(0, 2*pi, NoVoxPhi);                                                              % Angular dimension (0°- 360°)

[R, Theta] = meshgrid(r, theta);                                                                      % Polar coordinates mesh
[X, Y] = pol2cart(Theta, R);                                                                             % Converting polar coordinates to cartesian 

ArrayEnergyMatrices = cat(3,EnergyMatrices{:});                                         % Converting the cell arrays into a 3D array (R, Phi, Layers)
LayerEnMatrix = ArrayEnergyMatrices(:, :, 50);                                             % 50 is the 50th layer. Choose the layer you would like to visualize
LayerEnMatrix(1:2, :) = 0;                                                                             % Set the inside of the cylindrical scoring volume to 0 to correctly vizualize the detector


% ::: Plot :::
figure(4)
surf(X, Y, LayerEnMatrix');
%surf(X, Y, intensity_matrix');
title('Gráfica Polar con Intensidad desde Matriz (Dimensiones Corregidas)');
xlabel('X (mm)');
ylabel('Y (mm)');
shading flat; 
colormap dosemap; 
colorbar;
axis equal;
view(2)



% :::::::::: MOVING FILES TO A SPECIFIC LOCATION ::::::::::

% SpectraPath = (pwd +"/Results/");     % We 'cd' to the folder in which we want to send the files
% addpath(SpectraPath);                      % We add the path for the Results folder
% movefile *.csv  Results                       % We move all the .csv files to the Results folder

% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: END ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

