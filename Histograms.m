%% Energy Histogram

function [EnergySpectrumNtuple, EnergySpectrumHisto, num_bins, x_min, x_max] = Histograms
%function [EnergySpectrumHisto, bin_centers, num_bins, x_min, x_max] = Histograms

% Define file names
fileNameNtuple = 'MC-ADD_Results_nt_Photons.csv';                                                                                  % Ntuple file
fileNameHisto  = 'MC-ADD_Results_h1_Energy_Deposit.csv';                                                                      % Histogram file

% Initialize empty arrays
EnergyNtuple = [];   
EnergyHisto  = [];  

try

    % ::: Read Ntuple File :::
    if exist(fileNameNtuple, 'file') == 2
        DataNtuple     = readtable(fileNameNtuple);                                                                                     % Read entire Ntuple file
        EnergyNtuple = table2array(DataNtuple(:,5));                                                                                  % Extract column 7 (energy values)
    else
        warning("Ntuple file not found: %s", fileNameNtuple);
    end
    
    % ::: Read Histogram File :::
    if exist(fileNameHisto, 'file') == 2
        DataHisto     = readtable(fileNameHisto);                                                                                          % Read entire histogram file
        EnergyHisto = table2array(DataHisto(:,2));                                                                                       % Extract histogram bin counts
        
        % Ensure correct bin count (remove underflow/overflow bins if present)
        if length(EnergyHisto) > 1000
            EnergyHisto = EnergyHisto(2:end-1);                                                                                            % Remove first and last bins
        end
    else
        warning("Histogram file not found: %s", fileNameHisto);
    end
    
catch ME
    warning(ME.identifier, '%s', ME.message);
end


EnergySpectrumNtuple = EnergyNtuple(EnergyNtuple > 0);                                                                   % Remove zeros from Ntuple spectrum
EnergySpectrumHisto = EnergyHisto;  

% :::::: Define histogram bins ::::::
RunActionFile     = 'src/RunAction.cc';                                                                                                        % Read the file to extract data 
fid                        = fopen(RunActionFile, 'r');

if fid == -1
    error('Error opening the file. Check the path.');
end

lines = textscan(fid, '%s', 'Delimiter', '\n');       
fclose(fid);
lines = lines{1};     
    
HistogramInfo = lines{20};                                                                                                                          % Number of runs located in line 83 of the macrofile
tokens = regexp(HistogramInfo, '(\d+),\s*([\d.]+),\s*(\d+)', 'tokens');                                                       % Extracting the number of bins, min, and max energy

if isempty(tokens)
    error('Could not extract histogram information. Check the format.');
end

HistInfo = str2double(tokens{1});                                                                                                               % Converting string to doubles

num_bins = HistInfo(1); 
x_min = HistInfo(2);
x_max = HistInfo(3);

% bin_edges = linspace(x_min, x_max, num_bins + 1);
% bin_centers = (bin_edges(1:end-1) + bin_edges(2:end)) / 2;                                                                    % Midpoints
% 
% % ::: Debugging: Check if lengths match :::
% if length(EnergySpectrumHisto) ~= length(bin_centers)
%     error("Mismatch: bin_centers has %d elements but EnergySpectrumHisto has %d elements.", ...
%           length(bin_centers), length(EnergySpectrumHisto));
% end

end
