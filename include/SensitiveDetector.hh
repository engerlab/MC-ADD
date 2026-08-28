// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::       Header file for Sensitive Detector      :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

#ifndef SENSITIVEDETECTOR_HH
#define SENSITIVEDETECTOR_HH

// Include needed libraries
#include "G4VSensitiveDetector.hh"        // Main class from which we will inherit
#include "G4AnalysisManager.hh"           
#include "G4RunManager.hh"                // Library to get the event number
#include "G4SystemOfUnits.hh"             // Library to use units like m, ev, etc.
#include "G4UnitsTable.hh"


// ::::::::::::::::::::::::::::::::
// :::    Class definition      :::
// ::::::::::::::::::::::::::::::::

class SensitiveDetector : public G4VSensitiveDetector
{
public:
    SensitiveDetector(G4String);  // Constructor  G4String = Detector Name
    ~SensitiveDetector();         // Destructor

private:
    G4double fTotalEnergyDeposited; // Tot energy deposited epr event
    
    virtual void Initialize(G4HCofThisEvent *) override;           // Called by Geant4 when a new event starts. HC = Hits Collection
    virtual void EndOfEvent(G4HCofThisEvent *) override;           // Called when the event is compelated

    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory *);    // Main function that handles what ever happens during the time a particle is inside the detector. We can get some information of the particle


};

#endif