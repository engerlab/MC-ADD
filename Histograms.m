%% Energy Histogram

%function [EnergySpectrumNtuple, EnergySpectrumHisto, bin_centers, num_bins, x_min, x_max] = Histograms
function [EnergySpectrumHisto, bin_centers, num_bins, x_min, x_max] = Histograms

% Define file names
%fileNameNtuple = 'MC-ADD_Results_nt_Photons.csv';
fileNameHisto  = 'MC-ADD_Results_h1_Energy_Deposit.csv';

% Initialize empty arrays
%EnergyNtuple = [];
EnergyHisto  = [];

try

    % % ::: Read Ntuple File :::
    % if exist(fileNameNtuple, 'file') == 2
    % 
    %     DataNtuple = readtable(fileNameNtuple);
    %     EnergyNtuple = table2array(DataNtuple(:,5));
    % 
    % else
    %     warning("Ntuple file not found: %s", fileNameNtuple);
    % end


    % ::: Read Histogram File :::
    if exist(fileNameHisto, 'file') == 2

        % The first 6 lines are Geant4 metadata and line 7
        % contains the CSV column names.
        % Numerical data therefore begin on line 8.
        DataHisto = readmatrix(fileNameHisto, 'NumHeaderLines', 7);

        % Column 1 contains histogram entries
        EnergyHisto = DataHisto(:,1);

        % Remove Geant4 underflow and overflow bins
        EnergyHisto = EnergyHisto(2:end-1);

    else
        warning("Histogram file not found: %s", fileNameHisto);
    end


catch ME
    rethrow(ME);
end


% ::: Clean spectra :::
%EnergySpectrumNtuple = EnergyNtuple(EnergyNtuple > 0);
EnergySpectrumHisto  = EnergyHisto;


% :::::: Define histogram bins ::::::

RunActionFile = 'src/RunAction.cc';

fid = fopen(RunActionFile, 'r');

if fid == -1
    error('Error opening the file. Check the path.');
end

lines = textscan(fid, '%s', 'Delimiter', '\n');
fclose(fid);

lines = lines{1};

HistogramInfo = lines{20};

tokens = regexp(HistogramInfo, '(\d+),\s*([\d.]+),\s*(\d+)', 'tokens');

if isempty(tokens)
    error('Could not extract histogram information. Check the format.');
end

HistInfo = str2double(tokens{1});

num_bins = HistInfo(1);
x_min    = HistInfo(2);
x_max    = HistInfo(3);


% ::: Define bin centers :::

bin_edges = linspace(x_min, x_max, num_bins + 1);

bin_centers = (bin_edges(1:end-1) + bin_edges(2:end)) / 2;


% Force both arrays to columns
EnergySpectrumHisto = EnergySpectrumHisto(:);
bin_centers = bin_centers(:);


% ::: Debugging output :::

% fprintf('\nHistogram diagnostic:\n');
% fprintf('  Raw Geant4 rows after readmatrix = %d\n', size(DataHisto,1));
% fprintf('  Physical histogram bins         = %d\n', length(EnergySpectrumHisto));
% fprintf('  Expected bins from RunAction.cc = %d\n', num_bins);
% fprintf('  Bin centers                     = %d\n\n', length(bin_centers));


% ::: Consistency check :::

if length(EnergySpectrumHisto) ~= length(bin_centers)

    error("Mismatch: bin_centers has %d elements but EnergySpectrumHisto has %d elements.", length(bin_centers), length(EnergySpectrumHisto));

end

end