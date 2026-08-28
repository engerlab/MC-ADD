// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::       Header file for Stacking Action         :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

#ifndef STACKINGACTION_HH
#define STACKINGACTION_HH

// Include needed libraries
#include "G4UserStackingAction.hh"        // Main class from which we will inherit
#include "G4ParticleDefinition.hh"
#include "G4Track.hh"


// ::::::::::::::::::::::::::::::::
// :::    Class definition      :::
// ::::::::::::::::::::::::::::::::

class StackingAction : public G4UserStackingAction
{
public: 
    StackingAction();           // Constructor
    virtual ~StackingAction();  // Destructor

    virtual G4ClassificationOfNewTrack ClassifyNewTrack(const G4Track *aTrack);
    
    G4ClassificationOfNewTrack classification;

//private: 

    bool isDaRTSimulation;      // Boolean flag to check if we are running a DaRT simulation

};




#endif