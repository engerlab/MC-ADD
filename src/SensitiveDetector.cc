// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::       Source file for Sensitive Detector      :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

// Include user-made and needed libraries
#include "SensitiveDetector.hh"


// ::::::::::::::::::::::::::::::::
// :::  Constructor definition  :::
// ::::::::::::::::::::::::::::::::

SensitiveDetector::SensitiveDetector(G4String Name) : G4VSensitiveDetector(Name)
{
    fTotalEnergyDeposited = 0.0;
}

// ::::::::::::::::::::::::::::::::
// :::  Destructor definition   :::
// ::::::::::::::::::::::::::::::::

SensitiveDetector::~SensitiveDetector()
{}


// ::::::::::::::::::::::::::::::::
// :::   Functions definition   :::
// ::::::::::::::::::::::::::::::::

void SensitiveDetector::Initialize(G4HCofThisEvent *)
{
    fTotalEnergyDeposited = 0.0; // We set the energy variable as 0 to start "filling it"
}


// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::   Main part that processes what happens inside the detector   :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

G4bool SensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory *)
{
    G4int eventID = G4RunManager::GetRunManager()->GetCurrentEvent()->GetEventID();    // Variable for the eventID
    G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();

    G4StepPoint *preStepPoint = aStep->GetPreStepPoint();                              // Includes all information of the first interaction in one step
    G4double      fGlobalTime = preStepPoint->GetGlobalTime();
    G4double fEnergyDeposited = aStep->GetTotalEnergyDeposit();                         // For each step, we get the total energy deposited per particle
    G4ThreeVector   posPhoton = preStepPoint->GetPosition();                             // For the photon position
    G4ThreeVector   momPhoton = preStepPoint->GetMomentum();                             // For the photon momentum
    G4double    fMomPhotonMag = momPhoton.mag();                                         // Moment Magnitude
    G4double            fWlen = (1.239841939 *eV / fMomPhotonMag)*1E+03;                 // Wavelength calculation
    const auto* track = aStep->GetTrack();
    G4ParticleDefinition *Particle = track   -> GetDefinition();     // We get the particle definition
    G4String                  Name = Particle -> GetParticleName();   // The particle name

    // ::: Filling up the Ntuples :::
    analysisManager->FillNtupleIColumn(0, 0, eventID);
    analysisManager->FillNtupleDColumn(0, 1, posPhoton[0]);                             // First position of the photon position
    analysisManager->FillNtupleDColumn(0, 2, posPhoton[1]);
    analysisManager->FillNtupleDColumn(0, 3, posPhoton[2]);
    //analysisManager->FillNtupleDColumn(0, 4, fGlobalTime);
    //analysisManager->FillNtupleDColumn(0, 5, fWlen);
    analysisManager->FillNtupleDColumn(0, 4, fEnergyDeposited);
    analysisManager->AddNtupleRow(0);                                                    // First row is compleated, now for every photon interaction we get another row

    if(fEnergyDeposited > 0)                                    // Conditional for the fTotalEnergyDeposited (= 0) to be increased according to fEnergyDeposited... if fEnergyDeposited is > 0 
    {
        fTotalEnergyDeposited += fEnergyDeposited;
    }

    return true;
}

void SensitiveDetector::EndOfEvent(G4HCofThisEvent *)
{
    G4int eventID = G4RunManager::GetRunManager()->GetCurrentEvent()->GetEventID();
    G4AnalysisManager *analysisManager = G4AnalysisManager::Instance();

    // ::: Filling up the Histograms :::
    analysisManager->FillH1(0, fTotalEnergyDeposited);

    // ::: Printing the deposited energy inside the crystal :::

    G4cout << "Event " << eventID << " deposited: " << fTotalEnergyDeposited << " MeV." << G4endl;  // We print in the terminal the total energy deposited per event as soon as it finishes
}