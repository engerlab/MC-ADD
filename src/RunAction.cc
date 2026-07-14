// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::           Source file for Run Action          :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

// Include user-made and needed libraries
#include "RunAction.hh"


// ::::::::::::::::::::::::::::::::
// :::  Constructor definition  :::
// ::::::::::::::::::::::::::::::::

RunAction::RunAction()
{
    G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();

    // ::: 1D Histograms :::
    analysisManager->CreateH1("Energy_Deposit", "Energy Deposit", 10000, 0., 10*MeV); // Energy deposited histogram with 100 bins from 0-1.1 MeV

    // ::: Ntuples :::
    analysisManager->CreateNtuple("Photons", "Photons");  // Name
    analysisManager->CreateNtupleIColumn("iEvent");       // I = integers
    analysisManager->CreateNtupleDColumn("PosX");         // D = doubles        
    analysisManager->CreateNtupleDColumn("PosY");
    analysisManager->CreateNtupleDColumn("PosZ");
    //analysisManager->CreateNtupleDColumn("fGlobalTime");  // Refers only to the time when the particle was created
    //analysisManager->CreateNtupleDColumn("fWlen");
    analysisManager->CreateNtupleDColumn("fEnergyDeposited");
    analysisManager->FinishNtuple(0);                     // Definitions of Ntuples is compleated
}


// ::::::::::::::::::::::::::::::::
// :::   Destructor definition  :::
// ::::::::::::::::::::::::::::::::

RunAction::~RunAction()
{}


// ::::::::::::::::::::::::::::::::::::::::::::::
// :::   Function before Run Action operates  :::
// ::::::::::::::::::::::::::::::::::::::::::::::

void RunAction::BeginOfRunAction(const G4Run *run)
{
    G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();

    //G4String OutputFileName = "MC-ADD_Results.root";
    G4String OutputFileName = "MC-ADD_Results.csv";
    //G4String OutputFileName = "MC-ADD_Results.hdf5";
    //G4String OutputFileName = "MC-ADD_Results.xml";
    
    analysisManager->OpenFile(OutputFileName);
    
    //G4int runID = run->GetRunID();
    //std::stringstream strRunID;  // We include the runID into the root file name 
    //strRunID << runID;
    //analysisManager->OpenFile("MC-ADD_Output" + strRunID.str() + ".root"); 
}


// :::::::::::::::::::::::::::::::::::::::::::::
// :::   Function after Run Action operates  :::
// :::::::::::::::::::::::::::::::::::::::::::::
void RunAction::EndOfRunAction(const G4Run *run)
{
    G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();

    analysisManager->Write();      // At the end of each run, it writes the file and fills up the histograms and Ntuples. Important to store information
    analysisManager->CloseFile();  // We close the files

    G4int runID = run->GetRunID();

    G4cout << "\n" << G4endl;
    G4cout << ":::::::::::::::::::::::::::::::::::::::::" << G4endl;
    G4cout << ":::         Simulation Finished       :::" << G4endl; 
    G4cout << ":::::::::::::::::::::::::::::::::::::::::" << G4endl;
    G4cout << "\n" << G4endl;
}
