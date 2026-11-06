// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::          Header file for Run Action           :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

#ifndef RUNACTION_HH
#define RUNACTION_HH

// Include needed libraries
#include "G4UserRunAction.hh"   // Main class from which we will inherit
#include "G4Run.hh"              
#include "G4AnalysisManager.hh"  // Libray to handle the histograms and Ntuples
#include "G4SystemOfUnits.hh"
#include "G4UnitsTable.hh"

// ::::::::::::::::::::::::::::::::
// :::    Class definition      :::
// ::::::::::::::::::::::::::::::::

class RunAction : public G4UserRunAction
{
public:
    RunAction();  // Constructor
    ~RunAction(); // Destructor

    virtual void BeginOfRunAction(const G4Run *);
    virtual void EndOfRunAction(const G4Run *);
};

#endif
