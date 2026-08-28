% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% :::                                                                                             :::
% :::                                 MC-ADD Analysis Script                                      :::
% :::                                                                                             :::
% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% This MATLAB script corresponds to the third phase of the MC-ADD: Analysis phase.
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

clc; close all; clear;                                                      % Cleaning commands
%addpath('/Users/victor/Documents/MATLAB/Functions')                        % We add the path to the folder containing all the functions. Make sure to add yours!


% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% ::::::                                       FLAGS                                     ::::::
% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

% The following flags enable the visualization of the hits map inside the
% detector and the reconstructed image, and the broadening of the energy
% spectrum according to experimental measurements (energy resolution)

% 1: enables visualization
% 0: disbales visualization
%    The more runs in the macro file, the larger the size of the file --> the longer it will take to generate the maps

visFlag1 = 0;  % Hits map
visFlag2 = 0;  % Reconstructed image
ResFlag = 1;   % Broadening of the energy spectrum
ShpFlag = 0;   % Box: 0 or Cylinder: 1



% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% ::::::                        WELCOMING MESSAGE                         ::::::
% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

disp('::::::::::::::::::::::::::::::::::::::::::::::: MC-ADD :::::::::::::::::::::::::::::::::::::::::::::::');
fprintf('\n');
fprintf('                             Welcome to MC-ADD Analysis phase!\n');
fprintf('\n');
fprintf('  I am analyzing your output files. Give me a moment...\n'); 
fprintf('\n');


% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% :::                                 ENERGY SPECTRUM                           :::
% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

[EnergySpectrumHisto, bin_centers, num_bins, x_min, x_max] = Histograms; % We call the function Histograms to plot the energy spectrum
%[EnergySpectrumNtuple, EnergySpectrumHisto, bin_centers, num_bins, x_min, x_max] = Histograms; % We call the function Histograms to plot the energy spectrum


EnergySpectrumHisto(1) = 0;                                                                    % Set the first bin count to 0 since it represents events that did not interact isnide the crystal
X = linspace(x_min, x_max, num_bins);                                                          % Energy array for the energy spectrum
Error = sqrt(EnergySpectrumHisto);                                                             % Uncertainty for each cpunt per bin


% % ::: N T U P L E    H I S T O G R A M :::
% figure(1)
% histogram(EnergySpectrumNtuple, 300, 'FaceColor','r', 'EdgeColor', 'none');
% title('Energy Deposited Ntuples', 'Interpreter', 'latex', 'FontSize', 13);
% xlabel('Energy (MeV)', 'Interpreter', 'latex', 'FontSize', 13);
% ylabel('No. of counts', 'Interpreter', 'latex', 'FontSize', 13);
% axis square


% ::: E N E R G Y    H I S T O G R A M :::
figure(2)
plot(X,EnergySpectrumHisto, '-b', 'LineWidth',1);
%errorbar(X, EnergySpectrumHisto, Error, '.-b', 'LineWidth', 1, 'CapSize', 0, 'MarkerSize', 10);
title('Energy Spectrum', 'Interpreter', 'latex', 'FontSize', 13);
xlabel('Energy (MeV)', 'Interpreter', 'latex', 'FontSize', 13);
ylabel('No. of counts', 'Interpreter', 'latex', 'FontSize', 13);
set(gca,'TickDir','out');
%xlim([0.001 0.511])
%xlim([ 0 0.7])
%ylim([ 0 2.2e+06])
axis square


% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% :::                     E N E R G Y    R E S O L U T I O N                    :::
% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

if ResFlag == 1
    % ::: E N E R G Y   R E S O L U T I O N :::

    % This section contains an energy spectrum measured experimentally with the Captus 3000 well-type detector.
    % NOT NEEDED FOR THE GENERAL PURPOSE/WORKFLOW OF MC-ADD!!

    % ::: Captus :::
    Captus = readtable('New2_Cs137_14_25_RawData.csv', 'PreserveVariableNames', true);   % Opening the blood measurements from Captus
    CaptusEnergy = Captus{15:end, 2};                                                    % Column 2: Energy (keV)
    CaptusCounts = Captus{15:end, 3};                                                    % Column 3: Counts
    CaptusEnergy = CaptusEnergy / 1000;                                                  % Convert to MeV
    % ::: End of Captus :::

    % ::: Captus3000 :::
    
    energyRef = 0.662;                                                                   % Reference Energy [MeV]

    % ::: Use the following lines to obtain the FWHM from a Gaussian fit :::
    %c1 = VALUE;                                                                         % Value obtained form the Gaussian fit using Captus's ROI of 612 to 711
    %sigma = c1/sqrt(2);                                                                  % sigma from the Gaussian fit
    %FWHM = 2*sqrt(2*log(2))*sigma;                                                       % FWHM [MeV]
    %resolutionRef = FWHM/energyRef;                                                      % Energy resolution [%]
    resolutionRef = 0.079;                                                               % Experimentally measured

    % ::: G A U S S I A N   B R O A D E N I N G   &   E R R O R   P R O P A G A T I O N :::
    [BroadEnergySpectrumHisto, BroadError] = GaussianBroadening(bin_centers, EnergySpectrumHisto, resolutionRef, energyRef);


    % ::: N O R M A L I Z A T I O N   T O   P H O T O P E A K :::

    % ::: Window around the photopeak :::
    idxPeak = CaptusEnergy >= 0.64 & CaptusEnergy <= 0.69;     % CAPTUS 3000
    MCidxPeak = X >= 0.64 & X <= 0.69;                         % MC-ADD
    
    % ::: Getting Max values in the photopeak :::
    CaptusPeakMax               = max(CaptusCounts(idxPeak));
    EnergySpectrumHistoMax      = max(EnergySpectrumHisto(MCidxPeak));
    BroadEnergySpectrumHistoMax = max(BroadEnergySpectrumHisto(MCidxPeak));
    
    % ::: Normalization :::
    CaptusCountsNorm             = CaptusCounts/CaptusPeakMax;
    EnergySpectrumHistoNorm      = EnergySpectrumHisto/EnergySpectrumHistoMax;
    BroadEnergySpectrumHistoNorm = BroadEnergySpectrumHisto/BroadEnergySpectrumHistoMax;
    
    BroadErrorNorm = BroadError / BroadEnergySpectrumHistoMax;
    EnergySpectrumErrorNorm = Error / EnergySpectrumHistoMax;

    % ::: Q U A L I T A T I V E   A S S E S S M E N T:   P E A K   T O   C O M P T O N   R A T I O :::

    % ::: ROIs :::
    PeakROI    = [0.612 0.711]; % Based on Captus photopeak ROI
    ComptonROI = [0.250 0.540]; % Chosen in the mostly 'uniform' compton continious

    % ::: Captus index :::
    
    idxPeak_Captus = find(CaptusEnergy >= PeakROI(1) & CaptusEnergy <= PeakROI(2));
    idxComp_Captus = find(CaptusEnergy >= ComptonROI(1) & CaptusEnergy <= ComptonROI(2));

    % ::: MC-ADD indices :::
    idxPeak_MC = find(bin_centers >= PeakROI(1) & bin_centers <= PeakROI(2));
    idxComp_MC = find(bin_centers >= ComptonROI(1) & bin_centers <= ComptonROI(2));

    % ::: Integrated counts :::
    P_Captus = sum(CaptusCounts(idxPeak_Captus));
    C_Captus = sum(CaptusCounts(idxComp_Captus));
    
    P_MC = sum(BroadEnergySpectrumHisto(idxPeak_MC));
    C_MC = sum(BroadEnergySpectrumHisto(idxComp_MC));
    
    % ::: Peak-to-Compton Count ratios :::
    PC_Captus = P_Captus / C_Captus;
    PC_MC     = P_MC / C_MC;
    
    Difference_PC = (abs(PC_MC - PC_Captus) / PC_Captus) * 100;

    fprintf('  Peak-to-Compton ratio');
    fprintf('\n');
    fprintf('    Captus P/C = %.4f\n', PC_Captus);
    fprintf('    MC-ADD P/C = %.4f\n', PC_MC);
    fprintf('    Relative difference = %.2f %%\n', Difference_PC);
    

    % :::::::::::::::::
    % ::: P L O T S :::
    % :::::::::::::::::

    % ::: For qualitative visual assessment :::
    labels1 = {'MC-ADD Smeared', 'MC-ADD'};
    labels2 = {'Captus3000', 'MC-ADD', 'MC-ADD Smeared'};
    labels3 = {'Captus3000', 'MC-ADD Smeared'};

    figure(3)
    % ::: Ideal :::
    subplot(2,3,1)
    plot(X,EnergySpectrumHisto, '-b', 'LineWidth',1);              
    title('MC-ADD Energy Spectrum', 'Interpreter', 'latex', 'FontSize', 13);
    xlabel('Energy (MeV)', 'Interpreter', 'latex', 'FontSize', 13);
    ylabel('No. of counts', 'Interpreter', 'latex', 'FontSize', 13);
    set(gca,'TickDir','out');
    xlim([0 1])
    axis square

    % ::: Ideal zoom :::
    subplot(2,3,2)
    plot(X,EnergySpectrumHisto, '-b', 'LineWidth',1);
    title('MC-ADD Energy Spectrum Zoom', 'Interpreter', 'latex', 'FontSize', 13);
    xlabel('Energy (MeV)', 'Interpreter', 'latex', 'FontSize', 13);
    ylabel('No. of counts', 'Interpreter', 'latex', 'FontSize', 13);
    set(gca,'TickDir','out');
    xlim([0 0.65])
    ylim([0 10E+04])
    axis square

    % ::: Ideal and Smeared :::
    subplot(2,3,3)
    errorbar(bin_centers, BroadEnergySpectrumHisto, BroadError, '.r', 'MarkerSize', 2, 'LineWidth', 1, 'CapSize', 0);
    hold on
    plot(bin_centers, EnergySpectrumHisto, '-b', 'LineWidth', 0.1); % Ideal spectrum
    title('Ideal and Smeared energy spectrum', 'Interpreter', 'latex', 'FontSize', 13);
    xlabel('Energy (MeV)', 'Interpreter', 'latex', 'FontSize', 13);
    ylabel('No. of counts', 'Interpreter', 'latex', 'FontSize', 13);
    set(gca,'TickDir','out')
    xlim([0 1]);
    ylim([0 1.1*max(BroadEnergySpectrumHisto)]);
    legend(labels1, 'Interpreter', 'latex', 'Location', 'northeast');
    axis square
        
    % ::: Experimental :::
    subplot(2,3,4)
    plot(CaptusEnergy, CaptusCounts, '-', 'LineWidth', 1.2);
    title('Captus', 'Interpreter', 'latex', 'FontSize', 13);
    xlabel('Energy (MeV)', 'Interpreter', 'latex', 'FontSize', 13);
    ylabel('No. of counts', 'Interpreter', 'latex', 'FontSize', 13);
    set(gca,'TickDir','out');
    xlim([0 1]);
    axis square
    
    % ::: Experimental and Smeared :::
    subplot(2,3,5)
    plot(CaptusEnergy, CaptusCounts, '-', 'LineWidth', 1.2);  % Experimental
    hold on
    errorbar(bin_centers, BroadEnergySpectrumHisto, BroadErrorNorm, '.r', 'MarkerSize', 2, 'LineWidth', 0.8, 'CapSize', 0); % Blur with errors
    title('Captus vs MC-ADD', 'Interpreter', 'latex', 'FontSize', 13);
    xlabel('Energy (MeV)', 'Interpreter', 'latex', 'FontSize', 13);
    ylabel('Normalized Counts', 'Interpreter', 'latex', 'FontSize', 13);
    set(gca, 'TickDir', 'out');
    xlim([0 1]);
    legend(labels3, 'Interpreter', 'latex', 'Location', 'northeast');
    axis square
    
    % ::: Normalized Ideal, Smeared, and Experimental :::
    
    subplot(2,3,6)
    plot(CaptusEnergy, CaptusCountsNorm, '-', 'LineWidth', 1.2);  % Experimental
    hold on
    plot(bin_centers, EnergySpectrumHistoNorm, '-b', 'LineWidth', 0.8);  % Ideal
    errorbar(bin_centers, BroadEnergySpectrumHistoNorm, BroadErrorNorm, '.r', 'MarkerSize', 2, 'LineWidth', 0.8, 'CapSize', 0); % Blur with errors
    title('Normalized Cs-137 Energy Spectrum', 'Interpreter', 'latex', 'FontSize', 13);
    xlabel('Energy (MeV)', 'Interpreter', 'latex', 'FontSize', 13);
    ylabel('Normalized Counts', 'Interpreter', 'latex', 'FontSize', 13);
    set(gca, 'TickDir', 'out');
    xlim([0 1]);
    ylim([0 2.7]);
    legend(labels2, 'Interpreter', 'latex', 'Location', 'northeast');
    axis square

end



% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% :::       DETECTOR  EFFICIENCY   AND  VISUALIZATION          :::
% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


macroFile     = 'MC-ADD.mac';                                                                                                                       % Read the macro file to extract data for the efficiency 
fid                 = fopen(macroFile, 'r');

lines = textscan(fid, '%s', 'Delimiter', '\n');       
fclose(fid);
lines = lines{1};     
    

% ::: N U M B E R    O F    R U N S :::
targetLine = '';                                                                                                                                             % Empty variable to store the lline 
for i = 1:length(lines)
    if contains(lines{i}, '/run/beamOn')                                                                                                        % Finding: /run/beamOn 
        targetLine = lines{i};                                                                                                                           % Save the line number with /run/beamOn
        break;  
    end
end

if ~isempty(targetLine)
    tokens = regexp(targetLine, '([\d.]+)', 'tokens');                                                                                     % Extract the line number
    if ~isempty(tokens)
        N_simulated = str2double(tokens{1});                                                                                               % Convert the variable to double
    else
        fprintf('No number was found with /run/beamOn.\n');
    end
else
    fprintf('No line was found with /run/beamOn in the macro file.\n');
end


% ::::::  D E T E C T O R    E F F I C I E N C Y ::::::

% This section computes the absolute detection efficiency considering only the ideal spectrum. 
% If you wish to obtain full-energy peak detection efficiency (if applicable) ...
% get N_photopeak directly from the energy spectrum (figure 2) and add it to N_detected (line 179)
% This section must be done manually for the scenarios where the
% radionuclide emitts more than one photon (e.g. Na22)

% The following lines were MC-ADDed to the Cs-137 example

Prob_emission = 0.8501;                     % Define the radiation quality probability of emission of your radioniclude in 
N_emitted = N_simulated*Prob_emission;      % Number of photons emitted
%N_detected = sum(EnergySpectrumHisto);      % Events that deposited energy. Comment when the full-energy peak detection efficiency is required
N_detected = max(EnergySpectrumHisto);      % For the full-energy peak detection efficiency only. Modify Accordingly
Det_e = N_detected/N_emitted;               % Fraction of photons detected to the emitted ones
DetEff = Det_e*100;                         % Detection efficiency [%]


% ::: E F F I C I E N C Y    U N C E R T A I N T Y :::
sigma_eff = sqrt( Det_e*(1 - Det_e)/N_emitted )*100;


% ::: C A P T U S   E F F I C I E N C Y   V S   M C - A D D  :::
captus_DetEff = 15.08;         % Captus Efficiency

Diff = (abs(captus_DetEff - DetEff)/captus_DetEff)*100;


% :::::: 3D   E N E R G Y    D E P O S I T I O N    H I T    M A P ::::::
if visFlag1 == 1
    % ::: V I Z U A L I Z A T I O N :::
    DataTable = readtable('MC-ADD_Results_nt_Photons.csv', 'PreserveVariableNames', true );                    % We import the name of the file containing the photon information in Ntuples
    Data = table2array(DataTable);                                                                                                                 % Conversion to arrays
    
    Events  = Data(:,1);                                                                                                                                     % Extraction of data
    X           = Data(:,2);                                                                
    Y           = Data(:,3);
    Z           = Data(:,4);
    Energy = Data(:,5);
    
    
    % :::::: E R R O R    C A L C U L A T I O N ::::::
    Unique_Events = unique(Events);                                                                                                              % Events that had an interaction in the detector
    AllEvents = length(Unique_Events);                                                                                                           % All events scored in the detector
    TotEnergyperEvent = zeros(AllEvents,1);                                                                                                  % Empty array for the Total Energy Deposited per Event
    
    for i = 1:AllEvents
        EventID = Unique_Events(i);
        TotEnergyperEvent(i) = sum(Energy(Events == EventID));                                                                   % Iteration over each event to get the total energy deposited per event
    end
    
    E_mean = mean(TotEnergyperEvent);                                                                                                       % Mean energy deposited
    
    
    % ::: H I S T O R Y  -  B Y  -  H I S T O R Y :::
    sum_x2 = sum(TotEnergyperEvent.^2)/N_detected;                                                                                % First term 
    sum_x   = (sum(TotEnergyperEvent)/N_detected)^2;                                                                               % Second term
    sigma_Edep = sqrt((sum_x2 - sum_x) / (N_detected - 1));                                                                        % Uncertainty

    figure(3)                                                                        % 3D Plot
    scatter3(X, Y, Z, 5, Energy, 'filled');
    title('3D Hits Map', 'Interpreter', 'latex', 'FontSize', 13);
    xlabel('X (mm)', 'Interpreter', 'latex', 'FontSize', 13);
    ylabel('Y (mm)', 'Interpreter', 'latex', 'FontSize', 13);
    zlabel('Z (mm)', 'Interpreter', 'latex', 'FontSize', 13);
    colormap jet; colorbar;
    %view (180,0);  % 2D visualization
end


% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% :::                 COMMAND-BASED FILES ANALYSIS                  :::
% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

% :::::: M A C R O    F I L E ::::::

% ::::::::: BOX :::::::::
if (ShpFlag == 0 && visFlag2 == 1)

    macroFile     = 'MC-ADD.mac';                                                              % Read the macro file to extract data 
    fid                 = fopen(macroFile, 'r');

    if fid == -1                                                                                            % If statement if the file cannot be opened
        error('Could not open the .mac file.');
    end

    lines = textscan(fid, '%s', 'Delimiter', '\n');       
    fclose(fid);
    lines = lines{1};                                                                                    % Convert cell to array of strings
    
    
    % ::: D E T E C T O R    S I Z E :::
    boxSizeLine = lines{22};                                                                     % Size of the scoring volume located in line 21 of the macrofile
    tokens = regexp(boxSizeLine, '([\d.]+) ([\d.]+) ([\d.]+)', 'tokens');      % Extracting the x y z size values
    boxSize = str2double(tokens{1});                                                       % Converting string into doubles
    
    
    % ::: V O X E L S :::
    nBinLine = lines{23};                                                                           % Number of voxels located in line 22 of the macrofile
    tokens = regexp(nBinLine, '([\d.]+) ([\d.]+) ([\d.]+)', 'tokens');           % Extracting the x y z no. of voxels
    nBin = str2double(tokens{1});                                                            % Converting string to doubles
    
    NumVoxX = nBin(1);
    NumVoxY = nBin(2);
    NoVoxZ    = nBin(3);
    
    
    % ::::::::: C S V    F I L E :::::::::
    
    GammaData = readmatrix('GammaEnergyDep.csv');         % We read the csv file 
    
    SlicesTot = zeros(NumVoxX, NumVoxY, NoVoxZ);

    
    % ::: Generation of a matrix :::
    for z = 1:NoVoxZ                                                                         % Runs over each Z (slide)
        for y = 1:NumVoxY                                                                  % For each row in Y (rows) 
            Idx = (y - 1) * NoVoxZ + z;                                                   % Start index to run over the data file getting all the correct values for each Z and each Y row to generate the plane XY
            vectorTot = GammaData(Idx:NumVoxY*NoVoxZ:end, 4);  % Extraction of the dose/energy data from the output file
            SlicesTot(NumVoxY - y + 1, :, z) = vectorTot';                     % Inversion of the vector for reconstruction purposes in a 3D matrix: all the XY planes
        end
    end
    
    % :::::: P L O T ::::::
    figure (4);
    hold on;
    z_spacing = 0.1;                                                                                                                                           % Define the spacing between each slice in the Z axis
    for z = 1:NoVoxZ                                                                                                                                          % Iterate through each slice in the 3D array
        sliceTot = SlicesTot(:, :, z);                                                                                                                        % Get the current slice (XY plane) SlicesTot ORIGINAL
        hTransform = hgtransform;                                                                                                                     % Create a transformation group
        hImage = imagesc(sliceTot, 'XData', [1 NumVoxX], 'YData', [1 NumVoxY], 'CDataMapping', 'scaled'); % Display the slice using imagesc and set its parent to the transformation group
        set(hImage, 'Parent', hTransform);
        transformationMatrix = makehgtform('translate', [0, 0, z * z_spacing]);                                              % Set the transformation matrix for the transformation group to position the slice at the correct Z level
        set(hTransform, 'Matrix', transformationMatrix);
    end
    
    xlabel('X');
    ylabel('Y');
    zlabel('Z');
    title('Reconstructed Image');
    colormap dosemap; colorbar;
    set(gca,'TickDir','out')
    view(2);
    axis square

% ::::::::: CYLINDER :::::::::
elseif (ShpFlag == 1 && visFlag2 == 1)
    macroFile     = 'MC-ADD.mac';                                                              % Read the macro file to extract data 
    fid                 = fopen(macroFile, 'r');

    if fid == -1                                                                                            % If statement if the file cannot be opened
        error('Could not open the .mac file.');
    end

    lines = textscan(fid, '%s', 'Delimiter', '\n');       
    fclose(fid);
    lines = lines{1};                                                                                    % Convert cell to array of strings


    % ::: D E T E C T O R    S I Z E :::
    cylinderSizeLine = lines{22};                                                               % Size of the scoring volume located in line 22 of the macrofile
    tokens = regexp(cylinderSizeLine, '([\d.]+) ([\d.]+)', 'tokens');            % Extracting the R and Z size values
    CylSize = str2double(tokens{1});                                                         % Converting string into doubles


    % ::: V O X E L S :::
    nBinLine = lines{23};                                                                            % Number of voxels located in line 23 of the macrofile 
    tokens = regexp(nBinLine, '([\d.]+) ([\d.]+) ([\d.]+)', 'tokens');            % Extracting the  R, Z, Phi no. of voxels
    nBin = str2double(tokens{1});                                                             % Converting string to doubles

    NoVoxR    = nBin(1);
    NoVoxZ    = nBin(2);
    NoVoxPhi = nBin(3);

    DetRad = CylSize(1);
    DetLen = 2*CylSize(2);


    % ::::::::: C S V    F I L E :::::::::

    GammaData = readmatrix('CylinderGammaEnergyDep.csv');         % We read the csv file 

    % ::: V O X E L S    I N F O R M A T I O N :::
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


    % ::::::::: P L O T :::::::::

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

end



% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
% ::::::                           DISPLAYING RESULTS                         ::::::
% ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

disp('  I finished! Your results are listed below.');
fprintf('\n');
disp(':::::::::::::::::::::::::::::::::::::::::::::::      RESULTS      ::::::::::::::::::::::::::::::::::::::::::::::');
fprintf('\n');
fprintf('  Events simulated:           %d\n', N_simulated);
fprintf('  Events in the detector:    %d\n', N_detected);
fprintf('\n');
fprintf('  Detector efficiency: %.5f %%', DetEff);
fprintf(' ± %.5f  %%\n', sigma_eff);
fprintf('  Captus efficiency: %.5f %%', captus_DetEff);
fprintf('\n');
fprintf('  Percentage difference with Captus: %.5f %%', Diff);
fprintf('\n');
disp(':::::::::::::::::::::::::::::::::::::::::::::::          END          :::::::::::::::::::::::::::::::::::::::::::::');


% :::::::::: MOVING FILES TO A SPECIFIC LOCATION ::::::::::

% SpectraPath = (pwd +"/Results/");     % We 'cd' to the folder in which we want to send the files
% addpath(SpectraPath);                 % We add the path for the Results folder
% movefile *.csv  Results               % We move all the .csv files to the Results folder

% :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: END ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

