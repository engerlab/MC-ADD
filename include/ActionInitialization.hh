// :::::::::::::::::::::::::::::::::::::::::::::::::::::
// :::                                               :::
// :::     Header file for Action Initialization     :::
// :::                                               :::
// :::::::::::::::::::::::::::::::::::::::::::::::::::::

#ifndef ACTIONINITIALIZATION_HH
#define ACTIONINITIALIZATION_HH

// Include needed libraries
#include "G4VUserActionInitialization.hh" // Main class from which we will inherit
#include "PrimaryGenerator.hh"            // We need to call the Primary Generator class here because we cannot directly hand Primary Generator to the main file
#include "StackingAction.hh"
#include "RunAction.hh"



// ::::::::::::::::::::::::::::::::
// :::    Class definition      :::
// ::::::::::::::::::::::::::::::::

class ActionInitialization : public G4VUserActionInitialization  // We name our own class "ActionInitialization" inherited from G4VUserActionInitialization
{
public:
    ActionInitialization();    // Constructor
    ~ActionInitialization();   // Destructor           

    virtual void BuildForMaster() const;     // Virtual functions to overwrite the functions already implemented in the G4VUserActionInitialization class. This includes everything handled by the "MasterThread". For multithreathed mode.
    virtual void Build()const;               // Function for the single threads

};

#endif